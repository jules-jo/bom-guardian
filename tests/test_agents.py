import pytest

from bom_guardian.agents import availability, errata, lifecycle
from bom_guardian.agents.orchestrator import analyze_bom, analyze_component
from bom_guardian.models import (
    Component,
    LifecycleStatus,
    ResearchResult,
    RiskLevel,
    Source,
)


class FakeClient:
    """Stands in for YouComClient; returns canned responses."""

    def __init__(
        self,
        research_answer="STATUS: ACTIVE\nAll good.",
        research_sources=(),
        search_sources=(),
    ):
        self.research_answer = research_answer
        self.research_sources = tuple(research_sources)
        self.search_sources = tuple(search_sources)
        self.research_calls = []
        self.search_calls = []

    async def research(self, question):
        self.research_calls.append(question)
        return ResearchResult(content=self.research_answer, sources=self.research_sources)

    async def search(self, query, count=5, freshness=None, boost=False):
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
async def test_lifecycle_finding_carries_research_sources():
    client = FakeClient(
        research_answer="STATUS: NRND\nSee PCN.",
        research_sources=(Source("PCN notice", "https://vendor.test/pcn"),),
    )
    finding = await lifecycle.run(client, Component(mpn="ATMEGA328P"))
    assert finding.status == LifecycleStatus.NRND
    assert finding.sources == (Source("PCN notice", "https://vendor.test/pcn"),)


@pytest.mark.asyncio
async def test_errata_matches_terms_in_snippet_not_just_title():
    source = Source(
        title="STM32F103C8T6",
        url="https://vendor.test/errata",
        snippet="Errata sheet: known problems with the built-in I2C peripherals.",
    )
    finding = await errata.run(FakeClient(search_sources=(source,)), Component(mpn="STM32F103C8T6"))
    assert finding.signal is True
    assert finding.sources == (source,)


@pytest.mark.asyncio
async def test_errata_ignores_irrelevant_results():
    source = Source(title="Buy STM32 boards cheap", url="https://shop.test", snippet="Great deals")
    finding = await errata.run(FakeClient(search_sources=(source,)), Component(mpn="STM32F103C8T6"))
    assert finding.signal is False
    assert finding.sources == ()


@pytest.mark.asyncio
async def test_errata_ignores_errata_for_a_different_part():
    source = Source(
        title="STM8S007xx Errata sheet",
        url="https://st.test/es036.pdf",
        snippet="STM8S007xx and STM8S20xxx device limitations",
    )
    finding = await errata.run(FakeClient(search_sources=(source,)), Component(mpn="EP2C5T144C8N"))
    assert finding.signal is False


@pytest.mark.asyncio
async def test_errata_matches_mpn_with_packaging_suffix_dropped():
    source = Source(
        title="EP2C5T144C8 errata and known issues",
        url="https://vendor.test/errata",
        snippet="Device limitations for the Cyclone II family.",
    )
    finding = await errata.run(FakeClient(search_sources=(source,)), Component(mpn="EP2C5T144C8N"))
    assert finding.signal is True


@pytest.mark.asyncio
async def test_errata_matches_mpn_in_url_only():
    source = Source(
        title="Errata sheet",
        url="https://st.test/es096-stm32f103x8b-device-limitations.pdf",
        snippet="Device limitations.",
    )
    finding = await errata.run(FakeClient(search_sources=(source,)), Component(mpn="STM32F103C8T6"))
    assert finding.signal is True


@pytest.mark.asyncio
async def test_availability_matches_terms_in_snippet():
    source = Source(
        title="MCU market update",
        url="https://news.test/mcu",
        snippet="Lead time for the STM32F103 has stretched to 40 weeks amid allocation.",
    )
    finding = await availability.run(
        FakeClient(search_sources=(source,)), Component(mpn="STM32F103C8T6")
    )
    assert finding.signal is True


@pytest.mark.asyncio
async def test_availability_ignores_generic_shortage_news():
    source = Source(
        title="Drug Shortages | FDA",
        url="https://fda.test/drug-shortages",
        snippet="Information about drug shortages.",
    )
    finding = await availability.run(
        FakeClient(search_sources=(source,)), Component(mpn="EP2C5T144C8N")
    )
    assert finding.signal is False


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
