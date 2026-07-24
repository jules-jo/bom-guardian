"""Thin async client for the You.com Search, Contents, and Research APIs."""

import httpx

from . import config
from .models import ResearchResult, Source


def _payload_keys(payload: object) -> list[str]:
    return sorted(payload)[:5] if isinstance(payload, dict) else [type(payload).__name__]


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
        payload = response.json()
        if not isinstance(payload, dict) or "results" not in payload:
            raise ValueError(f"Unexpected search response shape: keys={_payload_keys(payload)}")
        results = payload.get("results") or {}
        sources = []
        seen_urls = set()
        for section in ("web", "news"):
            for item in results.get(section, []):
                url = item.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    sources.append(
                        Source(
                            title=item.get("title") or url,
                            url=url,
                            snippet=item.get("description") or "",
                        )
                    )
        return tuple(sources)

    async def contents(self, urls: list[str]) -> list[dict]:
        response = await self._client.post(
            config.CONTENTS_URL,
            headers=self._headers,
            json={"urls": urls, "formats": ["markdown"]},
        )
        response.raise_for_status()
        return response.json()

    async def research(self, question: str) -> ResearchResult:
        """Citation-backed synthesis: markdown with [[n]] citations plus its sources."""
        response = await self._client.post(
            config.RESEARCH_URL,
            headers=self._headers,
            json={"input": question, "research_effort": config.RESEARCH_EFFORT},
            timeout=config.RESEARCH_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or "output" not in payload:
            raise ValueError(f"Unexpected research response shape: keys={_payload_keys(payload)}")
        output = payload.get("output", {})
        if not isinstance(output, dict):
            return ResearchResult(content=str(output))
        sources = tuple(
            Source(
                title=item.get("title") or item["url"],
                url=item["url"],
                snippet=next(iter(item.get("snippets") or []), ""),
            )
            for item in output.get("sources", [])
            if item.get("url")
        )
        return ResearchResult(content=output.get("content", ""), sources=sources)
