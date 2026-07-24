"""Errata agent: finds published errata / known-issue documents via the Search API."""

from ..models import Component, Finding
from ..youcom_client import YouComClient

AGENT_NAME = "errata"

ERRATA_TERMS = ("errata", "device limitation", "known issue", "advisory")


async def run(client: YouComClient, component: Component) -> Finding:
    sources = await client.search(f"{component.mpn} errata sheet device limitations")
    relevant = tuple(
        s for s in sources if any(term in s.title.lower() for term in ERRATA_TERMS)
    )
    if relevant:
        titles = "; ".join(s.title for s in relevant[:3])
        summary = f"Published errata/advisories found: {titles}"
    else:
        summary = "No published errata documents surfaced in search."
    return Finding(agent=AGENT_NAME, summary=summary, sources=relevant, signal=bool(relevant))
