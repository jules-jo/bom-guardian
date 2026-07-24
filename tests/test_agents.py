import pytest

from bom_guardian.agents import lifecycle
from bom_guardian.agents.orchestrator import analyze_bom, analyze_component
from bom_guardian.models import Component, LifecycleStatus, RiskLevel, Source


class FakeClient:
    """Stands in for YouComClient; returns canned responses."""

    def __init__(self, research_answer="STATUS: ACTIVE\nAll good.", search_sources=()):
        self.research_answer = research_answer
        self.search_sources = tuple(search_sources)
        self.research_calls = []
        self.search_calls = []

    async def research(self, question):
        self.research_calls.append(question)
        return self.research_answer

    async def search(self, query, count=5, freshness=None):
        self.search_calls.append(query)
        return self.search_sources


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("STATUS: ACTIVE\nfine", LifecycleStatus.ACTIVE),
        ("status: eol\ndiscontinued 2024", LifecycleStatus.EOL),
        ("**STATUS: NRND** per PCN", LifecycleStatus.NRND),
        ("no verdict line at all", LifecycleStatus.UNKNOWN),
    ],
)
def test_parse_status(text, expected):
    assert lifecycle.parse_status(text) == expected


@pytest.mark.asyncio
async def test_analyze_component_eol_scores_high():
    client = FakeClient(research_answer="STATUS: EOL\nDiscontinued.")
    report = await analyze_component(client, Component(mpn="EP2C5T144C8N"))
    assert report.risk == RiskLevel.HIGH
    assert len(report.findings) == 3


@pytest.mark.asyncio
async def test_analyze_component_active_quiet_scores_low():
    client = FakeClient()
    report = await analyze_component(client, Component(mpn="NE555P"))
    assert report.risk == RiskLevel.LOW


@pytest.mark.asyncio
async def test_agent_exception_becomes_error_finding_not_crash():
    class ExplodingClient(FakeClient):
        async def research(self, question):
            raise RuntimeError("api down")

    report = await analyze_component(ExplodingClient(), Component(mpn="NE555P"))
    assert len(report.findings) == 3
    assert any("Agent failed" in f.summary for f in report.findings)


@pytest.mark.asyncio
async def test_analyze_bom_reports_progress_for_every_component():
    client = FakeClient(
        search_sources=(Source("STM32 errata sheet", "https://st.test/errata"),)
    )
    components = (Component(mpn="A1"), Component(mpn="B2"), Component(mpn="C3"))
    seen = []
    reports = await analyze_bom(client, components, on_progress=lambda c, r: seen.append(c.mpn))
    assert len(reports) == 3
    assert sorted(seen) == ["A1", "B2", "C3"]
