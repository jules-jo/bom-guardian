import pytest

from bom_guardian.models import ResearchResult, Source
from bom_guardian.sentinel.analyzer import analyze, render_markdown
from bom_guardian.sentinel.errata_doc import (
    find_errata_url,
    match_sections,
    split_sections,
)
from bom_guardian.sentinel.peripherals import ERRATA_ALIASES, PERIPHERAL_PATTERNS, extract_peripherals

SAMPLE_CODE = """
I2C_HandleTypeDef hi2c1;
hi2c1.Instance = I2C1;
HAL_DMA_Init(&hdma);
huart3.Instance = USART3;
"""

ERRATA_MARKDOWN = """
# STM32H743 device errata

## 2.3 I2C peripheral limitations

### 2.3.1 I2C analog filter may lock SDA
Workaround: disable the analog filter.

## 2.4 USART

### 2.4.1 USART baud rate glitch
Workaround: none.

## 2.5 Ethernet
Not used by our code.
"""


def test_every_pattern_has_errata_aliases():
    assert set(PERIPHERAL_PATTERNS) == set(ERRATA_ALIASES)


def test_extract_peripherals_finds_used_families_in_order():
    names = [h.name for h in extract_peripherals(SAMPLE_CODE)]
    assert names == ["I2C", "DMA", "UART"]


def test_extract_records_line_evidence():
    hit = extract_peripherals(SAMPLE_CODE)[0]
    assert hit.name == "I2C"
    assert hit.line_number == 2
    assert "I2C_HandleTypeDef" in hit.line


def test_extract_ignores_prose_and_lowercase():
    assert extract_peripherals("// we can adc later, spi maybe\nint can = 1;") == ()


def test_split_sections_handles_markdown_and_numbered_headings():
    titles = [s.title for s in split_sections(ERRATA_MARKDOWN)]
    assert "2.3.1 I2C analog filter may lock SDA" in titles
    assert any("Ethernet" in t for t in titles)


def test_match_sections_by_title_alias():
    sections = split_sections(ERRATA_MARKDOWN)
    matched = match_sections(sections, ERRATA_ALIASES["I2C"])
    assert any("analog filter" in s.title for s in matched)
    assert all("Ethernet" not in s.title for s in matched)


def test_match_sections_requires_word_boundary():
    from bom_guardian.sentinel.errata_doc import ErrataSection

    dma2d = ErrataSection(title="2.2.29 DMA2D swap byte feature is not available", body="")
    timing = ErrataSection(title="2.5.1 Timing glitch on startup", body="")
    real_dma = ErrataSection(title="2.20.4 DMA stream locked when transferring", body="")
    assert match_sections((dma2d, real_dma), ERRATA_ALIASES["DMA"]) == (real_dma,)
    assert match_sections((timing,), ERRATA_ALIASES["TIM"]) == ()


def test_match_sections_skips_table_of_contents_blobs():
    from bom_guardian.sentinel.errata_doc import ErrataSection

    toc = ErrataSection(
        title="2.15 HRTIM ......... 2.19 I2C ......... 2.20 USART ......... " * 4,
        body="contents listing",
    )
    assert match_sections((toc,), ERRATA_ALIASES["I2C"]) == ()


class FakeClient:
    def __init__(self, search_sources=(), contents_markdown="", research_answer=""):
        self.search_sources = tuple(search_sources)
        self.contents_markdown = contents_markdown
        self.research_answer = research_answer
        self.research_calls = []

    async def search(self, query, count=5, freshness=None, boost=False):
        return self.search_sources

    async def contents(self, urls):
        return [{"url": urls[0], "markdown": self.contents_markdown}]

    async def research(self, question):
        self.research_calls.append(question)
        return ResearchResult(content=self.research_answer)


ERRATA_PDF_SOURCE = Source(
    title="STM32H743 Errata sheet",
    url="https://www.st.com/resource/errata/es0392-stm32h743-device-errata.pdf",
    snippet="Device errata",
)


@pytest.mark.asyncio
async def test_find_errata_url_prefers_vendor_pdf():
    shop = Source(title="STM32H743 errata discussion", url="https://forum.test/t/1", snippet="errata")
    client = FakeClient(search_sources=(shop, ERRATA_PDF_SOURCE))
    best = await find_errata_url(client, "STM32H743ZIT6")
    assert best == ERRATA_PDF_SOURCE


@pytest.mark.asyncio
async def test_analyze_matches_used_peripherals_against_errata():
    client = FakeClient(search_sources=(ERRATA_PDF_SOURCE,), contents_markdown=ERRATA_MARKDOWN)
    report = await analyze(client, "STM32H743ZIT6", SAMPLE_CODE)
    matched_names = [m.hit.name for m in report.matches]
    assert "I2C" in matched_names
    assert "UART" in matched_names
    assert client.research_calls == []
    rendered = render_markdown(report)
    assert "analog filter" in rendered
    assert "line 2" in rendered  # I2C_HandleTypeDef declaration evidence


@pytest.mark.asyncio
async def test_analyze_falls_back_to_research_when_doc_unparseable():
    client = FakeClient(
        search_sources=(ERRATA_PDF_SOURCE,),
        contents_markdown="",
        research_answer="I2C: erratum 2.3.1, disable analog filter.",
    )
    report = await analyze(client, "STM32H743ZIT6", SAMPLE_CODE)
    assert report.matches == ()
    assert "analog filter" in report.fallback_summary
    assert len(client.research_calls) == 1
    assert "I2C" in client.research_calls[0]


@pytest.mark.asyncio
async def test_llamaparse_rescues_unparseable_document(monkeypatch):
    from bom_guardian.sentinel import analyzer

    async def fake_parse(url):
        return ERRATA_MARKDOWN

    monkeypatch.setattr(analyzer, "parse_pdf_url", fake_parse)
    client = FakeClient(search_sources=(ERRATA_PDF_SOURCE,), contents_markdown="")
    report = await analyze(client, "STM32H743ZIT6", SAMPLE_CODE)
    assert [m.hit.name for m in report.matches] != []
    assert report.parsed_via == "llamaparse"
    assert client.research_calls == []  # document grounding succeeded, no research needed
    assert "parsed with LlamaParse" in render_markdown(report)


@pytest.mark.asyncio
async def test_contents_success_skips_llamaparse(monkeypatch):
    from bom_guardian.sentinel import analyzer

    async def exploding_parse(url):
        raise AssertionError("LlamaParse must not be called when Contents succeeds")

    monkeypatch.setattr(analyzer, "parse_pdf_url", exploding_parse)
    client = FakeClient(search_sources=(ERRATA_PDF_SOURCE,), contents_markdown=ERRATA_MARKDOWN)
    report = await analyze(client, "STM32H743ZIT6", SAMPLE_CODE)
    assert report.parsed_via == "contents"


@pytest.mark.asyncio
async def test_pdf_parse_noop_without_api_key(monkeypatch):
    from bom_guardian.sentinel.pdf_parse import parse_pdf_url

    monkeypatch.delenv("LLAMA_CLOUD_API_KEY", raising=False)
    assert await parse_pdf_url("https://vendor.test/errata.pdf") == ""


@pytest.mark.asyncio
async def test_analyze_no_peripherals_short_circuits():
    client = FakeClient()
    report = await analyze(client, "NE555P", "int main(void) { return 0; }")
    assert report.peripherals == ()
    assert "No recognizable peripheral usage" in render_markdown(report)


@pytest.mark.asyncio
async def test_analyze_survives_search_failure_via_research_fallback():
    class SearchDownClient(FakeClient):
        async def search(self, query, count=5, freshness=None, boost=False):
            raise RuntimeError("network down")

    client = SearchDownClient(research_answer="I2C: erratum 2.3.1.")
    report = await analyze(client, "STM32H743ZIT6", SAMPLE_CODE)
    assert report.errata_source is None
    assert "2.3.1" in report.fallback_summary


@pytest.mark.asyncio
async def test_analyze_degrades_visibly_when_everything_fails():
    class AllDownClient(FakeClient):
        async def search(self, query, count=5, freshness=None, boost=False):
            raise RuntimeError("network down")

        async def research(self, question):
            raise RuntimeError("research down")

    report = await analyze(AllDownClient(), "STM32H743ZIT6", SAMPLE_CODE)
    assert report.error
    assert "⚠️" in render_markdown(report)


@pytest.mark.asyncio
async def test_analyze_survives_contents_failure():
    class ContentsDownClient(FakeClient):
        async def contents(self, urls):
            raise RuntimeError("fetch failed")

    client = ContentsDownClient(
        search_sources=(ERRATA_PDF_SOURCE,), research_answer="fallback answer"
    )
    report = await analyze(client, "STM32H743ZIT6", SAMPLE_CODE)
    assert report.matches == ()
    assert report.fallback_summary == "fallback answer"
