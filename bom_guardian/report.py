"""Risk scoring and markdown rendering for component reports."""

from .models import ComponentReport, Finding, LifecycleStatus, RiskLevel, Source

RISK_ICONS = {RiskLevel.HIGH: "🔴", RiskLevel.MEDIUM: "🟡", RiskLevel.LOW: "🟢"}

MAX_SOURCES_PER_FINDING = 5
MAX_SNIPPET_CHARS = 160

# Titles/snippets/urls come from the open web (search results, LLM output) and
# reports are downloaded and shared: escape markdown link syntax so a crafted
# page title cannot inject links, and only render http(s) URLs as links.
_MD_ESCAPES = str.maketrans({"[": "\\[", "]": "\\]", "(": "\\(", ")": "\\)", "`": "\\`"})


def escape_markdown(text: str) -> str:
    return text.translate(_MD_ESCAPES)


def render_link(source: Source) -> str:
    title = escape_markdown(source.title)
    if not source.url.startswith(("http://", "https://")):
        return title
    url = source.url.replace("(", "%28").replace(")", "%29")
    return f"[{title}]({url})"


def _render_source(source: Source) -> str:
    line = f"- {render_link(source)}"
    if source.snippet:
        snippet = escape_markdown(source.snippet[:MAX_SNIPPET_CHARS].rstrip())
        ellipsis = "…" if len(source.snippet) > MAX_SNIPPET_CHARS else ""
        line += f" — {snippet}{ellipsis}"
    return line


def score_risk(findings: tuple[Finding, ...]) -> RiskLevel:
    """EOL -> HIGH. NRND -> MEDIUM+. Any two independent signals -> escalate one level."""
    statuses = {f.status for f in findings}
    signal_count = sum(1 for f in findings if f.signal)

    if LifecycleStatus.EOL in statuses:
        return RiskLevel.HIGH
    if LifecycleStatus.NRND in statuses:
        return RiskLevel.HIGH if signal_count >= 2 else RiskLevel.MEDIUM
    if signal_count >= 2:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def render_component_markdown(component_report: ComponentReport) -> str:
    component = component_report.component
    lines = [
        f"## {RISK_ICONS[component_report.risk]} {escape_markdown(component.mpn)} — {component_report.risk.value}",
    ]
    if component.description or component.manufacturer:
        details = escape_markdown(f"{component.manufacturer} {component.description}".strip())
        lines.append(f"*{details}*")
    for finding in component_report.findings:
        lines.append(f"\n### {finding.agent.title()}")
        lines.append(finding.summary)
        if finding.sources:
            lines.append("")
            lines.extend(_render_source(s) for s in finding.sources[:MAX_SOURCES_PER_FINDING])
    return "\n".join(lines)


def render_bom_markdown(reports: tuple[ComponentReport, ...]) -> str:
    order = {RiskLevel.HIGH: 0, RiskLevel.MEDIUM: 1, RiskLevel.LOW: 2}
    ranked = sorted(reports, key=lambda r: order[r.risk])
    high_count = sum(1 for r in reports if r.risk == RiskLevel.HIGH)
    header = [
        "# BOM Guardian Report",
        f"**{len(reports)} components analyzed — {high_count} high risk.**\n",
    ]
    return "\n".join(header + [render_component_markdown(r) + "\n" for r in ranked])
