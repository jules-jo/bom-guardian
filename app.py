"""BOM Guardian — Streamlit UI.

Run: streamlit run app.py
"""

import asyncio
from pathlib import Path

import streamlit as st

from bom_guardian import config
from bom_guardian.bom_parser import BomParseError, parse_bom_csv
from bom_guardian.agents.orchestrator import analyze_bom
from bom_guardian.models import RiskLevel
from bom_guardian.report import RISK_ICONS, render_component_markdown
from bom_guardian.youcom_client import YouComClient

DEMO_BOM_PATH = Path(__file__).parent / "data" / "demo_bom.csv"

st.set_page_config(page_title="BOM Guardian", page_icon="🛡️", layout="wide")
st.title("🛡️ BOM Guardian")
st.caption(
    "Paste a bill of materials, get a live, citation-backed risk report: "
    "lifecycle/EOL status, published errata, and supply signals — powered by "
    "You.com Search, Contents, and Research APIs."
)

uploaded = st.file_uploader("Upload BOM CSV (columns: mpn[,manufacturer,description,qty])", type="csv")
use_demo = st.toggle("Use demo BOM", value=uploaded is None)

csv_text = ""
if uploaded is not None and not use_demo:
    csv_text = uploaded.read().decode("utf-8", errors="replace")
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
        use_container_width=True,
    )

    if st.button(f"Analyze {len(components)} components", type="primary"):
        progress_bar = st.progress(0.0, text="Fanning out agents...")
        completed_count = 0

        def on_progress(component, component_report):
            nonlocal completed_count
            completed_count += 1
            progress_bar.progress(
                completed_count / len(components),
                text=f"{component.mpn}: {component_report.risk.value} "
                f"({completed_count}/{len(components)})",
            )

        async def run_analysis():
            client = YouComClient(api_key=config.get_api_key())
            try:
                return await analyze_bom(client, components, on_progress=on_progress)
            finally:
                await client.aclose()

        reports = asyncio.run(run_analysis())
        progress_bar.empty()

        high = [r for r in reports if r.risk == RiskLevel.HIGH]
        medium = [r for r in reports if r.risk == RiskLevel.MEDIUM]
        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 High risk", len(high))
        col2.metric("🟡 Medium risk", len(medium))
        col3.metric("🟢 Low risk", len(reports) - len(high) - len(medium))

        order = {RiskLevel.HIGH: 0, RiskLevel.MEDIUM: 1, RiskLevel.LOW: 2}
        for report in sorted(reports, key=lambda r: order[r.risk]):
            icon = RISK_ICONS[report.risk]
            with st.expander(f"{icon} {report.component.mpn} — {report.risk.value}", expanded=report.risk == RiskLevel.HIGH):
                st.markdown(render_component_markdown(report))
