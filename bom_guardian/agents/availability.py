"""Availability agent: recent supply/shortage signals via Search with freshness filter."""

from .. import config
from ..models import Component, Finding
from ..youcom_client import YouComClient

AGENT_NAME = "availability"

SHORTAGE_TERMS = ("shortage", "allocation", "lead time", "supply", "discontinu", "obsolete")


async def run(client: YouComClient, component: Component) -> Finding:
    sources = await client.search(
        f"{component.mpn} shortage OR allocation OR \"lead time\" OR discontinued",
        freshness=config.NEWS_FRESHNESS,
    )
    relevant = tuple(
        s for s in sources if any(term in s.title.lower() for term in SHORTAGE_TERMS)
    )
    if relevant:
        titles = "; ".join(s.title for s in relevant[:3])
        summary = f"Recent supply signals in the last {config.NEWS_FRESHNESS}: {titles}"
    else:
        summary = f"No supply-risk signals in the last {config.NEWS_FRESHNESS}."
    return Finding(agent=AGENT_NAME, summary=summary, sources=relevant, signal=bool(relevant))
