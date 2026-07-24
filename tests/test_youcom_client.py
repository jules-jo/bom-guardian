"""Client parsing tests against recorded real API response shapes (no network)."""

import httpx
import pytest

from bom_guardian import config
from bom_guardian.youcom_client import YouComClient

SEARCH_RESPONSE = {
    "results": {
        "web": [
            {
                "url": "https://vendor.test/errata",
                "title": "STM32F103C8T6",
                "description": "Errata sheet: known problems with the built-in I2C peripherals.",
                "snippets": [],
            },
            {
                "url": "https://dup.test/page",
                "title": "Duplicate",
                "description": "seen in both sections",
            },
        ],
        "news": [
            {
                "url": "https://dup.test/page",
                "title": "Duplicate",
                "description": "seen in both sections",
            },
            {
                "url": "https://news.test/shortage",
                "title": "MCU shortage update",
                "description": "Lead times stretch to 40 weeks.",
            },
        ],
    },
    "metadata": {"query": "q", "search_uuid": "u", "latency": 0.1},
}

RESEARCH_RESPONSE = {
    "output": {
        "content": "STATUS: EOL\nDiscontinued per PCN [[1, 2]].",
        "content_type": "text",
        "sources": [
            {
                "url": "https://vendor.test/pcn",
                "title": "PCN notice",
                "snippets": ["Product change notice for ...", "second snippet"],
            },
            {"url": "https://vendor.test/eol", "title": "EOL list", "snippets": []},
        ],
    },
    "warnings": [],
}


def make_client(payload) -> YouComClient:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    return YouComClient(api_key="test-key", client=httpx.AsyncClient(transport=transport))


@pytest.mark.asyncio
async def test_search_captures_description_as_snippet_and_dedupes():
    client = make_client(SEARCH_RESPONSE)
    sources = await client.search("query")
    urls = [s.url for s in sources]
    assert urls == [
        "https://vendor.test/errata",
        "https://dup.test/page",
        "https://news.test/shortage",
    ]
    assert "I2C peripherals" in sources[0].snippet


@pytest.mark.asyncio
async def test_research_returns_content_and_sources():
    client = make_client(RESEARCH_RESPONSE)
    result = await client.research("lifecycle of X?")
    assert result.content.startswith("STATUS: EOL")
    assert [s.url for s in result.sources] == [
        "https://vendor.test/pcn",
        "https://vendor.test/eol",
    ]
    assert result.sources[0].snippet == "Product change notice for ..."
    assert result.sources[1].snippet == ""


@pytest.mark.asyncio
async def test_research_tolerates_plain_string_output():
    client = make_client({"output": "just text"})
    result = await client.research("q")
    assert result.content == "just text"
    assert result.sources == ()
