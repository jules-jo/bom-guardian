"""YouComClient response-shape validation: a 200 with a degraded body must raise,
never silently return "nothing found" (which would render a false LOW-risk verdict)."""

import httpx
import pytest

from bom_guardian.youcom_client import YouComClient


def make_client(payload: dict, seen_requests: list | None = None) -> YouComClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if seen_requests is not None:
            seen_requests.append(request)
        return httpx.Response(200, json=payload)

    return YouComClient(api_key="test-key", client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))


@pytest.mark.asyncio
async def test_search_raises_on_unexpected_shape():
    client = make_client({"warning": "rate limited"})
    with pytest.raises(ValueError, match="search response"):
        await client.search("NE555P errata")


@pytest.mark.asyncio
async def test_search_parses_expected_shape():
    client = make_client(
        {
            "results": {
                "web": [{"url": "https://a.test", "title": "A", "description": "snip"}],
                "news": [{"url": "https://a.test", "title": "dup ignored"}],
            }
        }
    )
    sources = await client.search("q")
    assert len(sources) == 1
    assert sources[0].snippet == "snip"


@pytest.mark.asyncio
async def test_search_boost_sends_vendor_domains():
    seen: list = []
    client = make_client({"results": {"web": []}}, seen)
    await client.search("STM32 errata", boost=True)
    assert "st.com" in seen[0].url.params.get("boost_domains", "")


@pytest.mark.asyncio
async def test_search_without_boost_omits_domains():
    seen: list = []
    client = make_client({"results": {"web": []}}, seen)
    await client.search("STM32 errata")
    assert "boost_domains" not in seen[0].url.params


@pytest.mark.asyncio
async def test_search_boost_respects_custom_domains():
    seen: list = []
    transport_client = make_client({"results": {"web": []}}, seen)
    custom = YouComClient(
        api_key="test-key",
        client=transport_client._client,
        boost_domains=("example-vendor.com",),
    )
    await custom.search("query", boost=True)
    assert seen[0].url.params.get("boost_domains") == "example-vendor.com"


@pytest.mark.asyncio
async def test_research_raises_on_unexpected_shape():
    client = make_client({"error": "quota exceeded"})
    with pytest.raises(ValueError, match="research response"):
        await client.research("question")


@pytest.mark.asyncio
async def test_research_parses_expected_shape():
    client = make_client(
        {
            "output": {
                "content": "STATUS: EOL\ndone",
                "sources": [{"url": "https://b.test", "title": "B", "snippets": ["s1"]}],
            }
        }
    )
    result = await client.research("question")
    assert result.content.startswith("STATUS: EOL")
    assert result.sources[0].snippet == "s1"
