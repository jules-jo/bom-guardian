"""Thin async client for the You.com Search, Contents, and Research APIs."""

import httpx

from . import config
from .models import Source


class YouComClient:
    def __init__(self, api_key: str, client: httpx.AsyncClient | None = None):
        self._headers = {"X-API-Key": api_key}
        self._client = client or httpx.AsyncClient(timeout=config.HTTP_TIMEOUT_SECONDS)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def search(
        self, query: str, count: int = config.SEARCH_RESULT_COUNT, freshness: str | None = None
    ) -> tuple[Source, ...]:
        """Web+news search; returns deduplicated sources from both sections."""
        params: dict = {"query": query, "count": count}
        if freshness:
            params["freshness"] = freshness
        response = await self._client.get(config.SEARCH_URL, headers=self._headers, params=params)
        response.raise_for_status()
        results = response.json().get("results", {})
        sources = []
        seen_urls = set()
        for section in ("web", "news"):
            for item in results.get(section, []):
                url = item.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    sources.append(Source(title=item.get("title", url), url=url))
        return tuple(sources)

    async def contents(self, urls: list[str]) -> list[dict]:
        response = await self._client.post(
            config.CONTENTS_URL,
            headers=self._headers,
            json={"urls": urls, "formats": ["markdown"]},
        )
        response.raise_for_status()
        return response.json()

    async def research(self, question: str) -> str:
        """Citation-backed synthesis. Returns markdown with [[n]] citations."""
        response = await self._client.post(
            config.RESEARCH_URL,
            headers=self._headers,
            json={"input": question, "research_effort": config.RESEARCH_EFFORT},
            timeout=config.RESEARCH_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        output = response.json().get("output", {})
        if isinstance(output, dict):
            return output.get("content", "")
        return str(output)
