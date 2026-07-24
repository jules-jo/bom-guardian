"""Errata agent: finds published errata / known-issue documents via the Search API."""

from ..models import Component, Finding
from ..youcom_client import YouComClient
from .relevance import filter_relevant

AGENT_NAME = "errata"

ERRATA_TERMS = ("errata", "device limitation", "known issue", "advisory")


async def run(client: YouComClient, component: Component) -> Finding:
    sources = await client.search(f"{component.mpn} errata sheet device limitations")
    relevant = filter_relevant(sources, ERRATA_TERMS, component.mpn)
    if relevant:
        titles = "; ".join(s.title for s in relevant[:3])
        summary = f"Published errata/advisories found: {titles}"
    else:
        summary = "No published errata documents surfaced in search."
    return Finding(agent=AGENT_NAME, summary=summary, sources=relevant, signal=bool(relevant))
