"""BOM Guardian — Streamlit UI.

Run: streamlit run app.py
"""

import asyncio
import hashlib
import itertools
import logging
from collections.abc import Awaitable, Callable
from pathlib import Path

import streamlit as st

from bom_guardian import config
from bom_guardian.bom_parser import BomParseError, parse_bom_csv
from bom_guardian.agents.orchestrator import analyze_bom
from bom_guardian.models import Component, ComponentReport, RiskLevel
from bom_guardian.report import RISK_ICONS, render_bom_markdown, render_component_markdown
from bom_guardian.sentinel.analyzer import analyze as sentinel_analyze
from bom_guardian.sentinel.analyzer import render_markdown as sentinel_render
from bom_guardian.youcom_client import YouComClient

logger = logging.getLogger(__name__)

DEMO_BOM_PATH = Path(__file__).parent / "data" / "demo_bom.csv"
SAMPLE_FIRMWARE_PATH = Path(__file__).parent / "data" / "sample_firmware.c"
THEME_CSS_PATH = Path(__file__).parent / "assets" / "apple_theme.css"
DEFAULT_SENTINEL_MPN = "STM32H743ZIT6"
ANALYSIS_FAILED_MESSAGE = (
    "Analysis failed — likely a network or API hiccup. Please try again in a moment."
)

st.set_page_config(page_title="BOM Guardian", page_icon="🛡️", layout="wide")
st.markdown(f"<style>{THEME_CSS_PATH.read_text()}</style>", unsafe_allow_html=True)
st.title("BOM Guardian")
st.caption(
    "Know what's going to bite your bill of materials — before it ships. "
    "Live, citation-backed lifecycle, errata, and supply intelligence, "
    "powered by You.com."
)


def _input_key(*parts: str) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8", errors="replace"))
    return digest.hexdigest()


def _parse_domains(raw: str) -> tuple[str, ...]:
    domains = []
    for token in raw.replace(",", " ").split():
        domain = token.strip().removeprefix("https://").removeprefix("http://").strip("/")
        if "." in domain:
            domains.append(domain)
    return tuple(domains)


def _run_analysis(coro_factory: Callable[[YouComClient], Awaitable]):
    """Run an analysis coroutine with a fresh client; return result or None on failure."""

    async def scoped():
        client = YouComClient(
            api_key=config.get_api_key(),
            boost_domains=st.session_state.get("boost_domains", config.VENDOR_BOOST_DOMAINS),
        )
        try:
            return await coro_factory(client)
        finally:
            await client.aclose()

    try:
        return asyncio.run(scoped())
    except config.ConfigError as exc:
        st.error(str(exc))
    except Exception:
        logger.exception("Analysis failed")
        st.error(ANALYSIS_FAILED_MESSAGE)
    return None


with st.expander("Advanced — trusted vendor domains", expanded=False):
    st.caption(
        "Official documents from these domains are ranked higher in errata "
        "searches (soft preference via You.com domain boosting — nothing is excluded). "
        "Match this to your approved-vendor list."
    )
    raw_domains = st.text_input(
        "Boosted domains",
        value=", ".join(config.VENDOR_BOOST_DOMAINS),
        label_visibility="collapsed",
    )
    st.session_state["boost_domains"] = _parse_domains(raw_domains) or config.VENDOR_BOOST_DOMAINS

bom_tab, sentinel_tab = st.tabs(["📋 BOM Risk Radar", "🔬 Silicon Sentinel"])

with bom_tab:
    uploaded = st.file_uploader(
        "Upload BOM CSV (columns: mpn[,manufacturer,description,qty])", type="csv"
    )
    use_demo = st.toggle("Use demo BOM", value=uploaded is None)

    csv_text = ""
    if uploaded is not None and not use_demo:
        csv_text = uploaded.read().decode("utf-8-sig", errors="replace")
    elif use_demo:
        csv_text = DEMO_BOM_PATH.read_text()

    if csv_text:
        try:
            components = parse_bom_csv(csv_text)
        except BomParseError as exc:
            st.error(str(exc))
            st.stop()
        st.dataframe(
            [
                {"MPN": c.mpn, "Manufacturer": c.manufacturer, "Description": c.description, "Qty": c.qty}
                for c in components
            ],
            width="stretch",
        )

        bom_key = _input_key(csv_text)
        if st.button(f"Analyze {len(components)} components", type="primary"):
            progress_bar = st.progress(0.0, text="Fanning out agents...")
            completed_counter = itertools.count(1)

            def on_progress(component: Component, component_report: ComponentReport) -> None:
                completed_count = next(completed_counter)
                progress_bar.progress(
                    completed_count / len(components),
                    text=f"{component.mpn}: {component_report.risk.value} "
                    f"({completed_count}/{len(components)})",
                )

            reports = _run_analysis(
                lambda client: analyze_bom(client, components, on_progress=on_progress)
            )
            progress_bar.empty()
            if reports is not None:
                st.session_state["reports"] = reports
                st.session_state["reports_key"] = bom_key

        # Only show results that belong to the BOM currently on screen.
        reports = (
            st.session_state.get("reports")
            if st.session_state.get("reports_key") == bom_key
            else None
        )
        if reports:
            high = [r for r in reports if r.risk == RiskLevel.HIGH]
            medium = [r for r in reports if r.risk == RiskLevel.MEDIUM]
            col1, col2, col3 = st.columns(3)
            col1.metric("🔴 High risk", len(high))
            col2.metric("🟡 Medium risk", len(medium))
            col3.metric("🟢 Low risk", len(reports) - len(high) - len(medium))

            st.download_button(
                "Download report (Markdown)",
                data=render_bom_markdown(reports),
                file_name="bom-guardian-report.md",
                mime="text/markdown",
            )

            order = {RiskLevel.HIGH: 0, RiskLevel.MEDIUM: 1, RiskLevel.LOW: 2}
            for report in sorted(reports, key=lambda r: order[r.risk]):
                icon = RISK_ICONS[report.risk]
                with st.expander(
                    f"{icon} {report.component.mpn} — {report.risk.value}",
                    expanded=report.risk == RiskLevel.HIGH,
                ):
                    st.markdown(render_component_markdown(report))

with sentinel_tab:
    st.markdown(
        "Cross-check your **firmware** against the part's **live errata sheet**: "
        "which silicon bugs affect the peripherals your code actually uses?"
    )
    mpn = st.text_input("Part number", value=DEFAULT_SENTINEL_MPN)
    code_file = st.file_uploader("Upload firmware source (.c/.h)", type=["c", "h", "cpp", "txt"])
    use_sample = st.toggle("Use sample firmware", value=code_file is None)

    code_text = ""
    if code_file is not None and not use_sample:
        code_text = code_file.read().decode("utf-8-sig", errors="replace")
    elif use_sample:
        code_text = SAMPLE_FIRMWARE_PATH.read_text()

    if code_text:
        with st.expander("Firmware under analysis", expanded=False):
            st.code(code_text, language="c")

    sentinel_key = _input_key(mpn, code_text)
    if st.button("Cross-check errata", type="primary", disabled=not (mpn and code_text)):
        with st.spinner("Finding errata document and cross-checking peripherals..."):
            sentinel_report = _run_analysis(
                lambda client: sentinel_analyze(client, mpn.strip(), code_text)
            )
        if sentinel_report is not None:
            st.session_state["sentinel_report"] = sentinel_report
            st.session_state["sentinel_key"] = sentinel_key

    sentinel_report = (
        st.session_state.get("sentinel_report")
        if st.session_state.get("sentinel_key") == sentinel_key
        else None
    )
    if sentinel_report:
        st.markdown(sentinel_render(sentinel_report))
