from bom_guardian.models import (
    Component,
    ComponentReport,
    Finding,
    LifecycleStatus,
    RiskLevel,
    Source,
)
from bom_guardian.report import render_bom_markdown, render_component_markdown, score_risk


def finding(agent="lifecycle", status=LifecycleStatus.UNKNOWN, signal=False, sources=()):
    return Finding(agent=agent, summary="summary", status=status, signal=signal, sources=sources)


def test_eol_is_high_risk():
    assert score_risk((finding(status=LifecycleStatus.EOL, signal=True),)) == RiskLevel.HIGH


def test_nrnd_alone_is_medium():
    assert score_risk((finding(status=LifecycleStatus.NRND, signal=True),)) == RiskLevel.MEDIUM


def test_nrnd_plus_second_signal_is_high():
    findings = (
        finding(status=LifecycleStatus.NRND, signal=True),
        finding(agent="availability", signal=True),
    )
    assert score_risk(findings) == RiskLevel.HIGH


def test_active_with_no_signals_is_low():
    assert score_risk((finding(status=LifecycleStatus.ACTIVE),)) == RiskLevel.LOW


def test_two_signals_without_lifecycle_flag_is_medium():
    findings = (
        finding(agent="errata", signal=True),
        finding(agent="availability", signal=True),
    )
    assert score_risk(findings) == RiskLevel.MEDIUM


def test_component_markdown_includes_sources_and_risk():
    report = ComponentReport(
        component=Component(mpn="NE555P", manufacturer="TI"),
        findings=(
            finding(agent="errata", signal=True, sources=(Source("Errata sheet", "https://x.test/e"),)),
        ),
        risk=RiskLevel.MEDIUM,
    )
    markdown = render_component_markdown(report)
    assert "NE555P" in markdown
    assert "MEDIUM" in markdown
    assert "https://x.test/e" in markdown


def test_component_markdown_shows_source_snippet():
    report = ComponentReport(
        component=Component(mpn="NE555P"),
        findings=(
            finding(
                agent="errata",
                signal=True,
                sources=(Source("Errata sheet", "https://x.test/e", snippet="Known I2C issue."),),
            ),
        ),
        risk=RiskLevel.MEDIUM,
    )
    assert "Known I2C issue." in render_component_markdown(report)


def test_bom_markdown_sorts_high_risk_first():
    low = ComponentReport(Component(mpn="LOWPART"), (finding(),), RiskLevel.LOW)
    high = ComponentReport(Component(mpn="HIGHPART"), (finding(),), RiskLevel.HIGH)
    markdown = render_bom_markdown((low, high))
    assert markdown.index("HIGHPART") < markdown.index("LOWPART")
    assert "1 high risk" in markdown
