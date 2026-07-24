import pytest

from bom_guardian import cli
from bom_guardian.models import Component, ResearchResult, Source


class FakeClient:
    def __init__(self, *args, **kwargs):
        pass

    async def aclose(self):
        pass

    async def search(self, query, count=5, freshness=None):
        return (
            Source(
                title="NE555P errata sheet",
                url="https://vendor.test/ne555p-errata.pdf",
                snippet="device limitations",
            ),
        )

    async def contents(self, urls):
        return [{"url": urls[0], "markdown": "## 2.1 I2C glitch\nWorkaround: none."}]

    async def research(self, question):
        return ResearchResult(content="STATUS: ACTIVE\nIn production.")


@pytest.fixture(autouse=True)
def fake_client(monkeypatch):
    monkeypatch.setattr(cli, "YouComClient", FakeClient)
    monkeypatch.setattr(cli.config, "get_api_key", lambda: "test-key")


@pytest.mark.asyncio
async def test_cli_run_renders_bom_report():
    markdown = await cli.run((Component(mpn="NE555P"),))
    assert "NE555P" in markdown
    assert "LOW" in markdown  # ACTIVE + errata signal only -> LOW


@pytest.mark.asyncio
async def test_cli_run_sentinel_renders_report():
    markdown = await cli.run_sentinel("NE555P", "hi2c1.Instance = I2C1;")
    assert "Silicon Sentinel" in markdown
    assert "I2C" in markdown
