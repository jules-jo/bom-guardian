"""Availability agent: recent supply/shortage signals via Search with freshness filter."""

from .. import config
from ..models import Component, Finding
from ..youcom_client import YouComClient
from .relevance import filter_relevant

AGENT_NAME = "availability"

SHORTAGE_TERMS = ("shortage", "allocation", "lead time", "supply", "discontinu", "obsolete")


async def run(client: YouComClient, component: Component) -> Finding:
    sources = await client.search(
        f"{component.mpn} shortage OR allocation OR \"lead time\" OR discontinued",
        freshness=config.NEWS_FRESHNESS,
    )
    relevant = filter_relevant(sources, SHORTAGE_TERMS, component.mpn)
    if relevant:
        titles = "; ".join(s.title for s in relevant[:3])
        summary = f"Recent supply signals in the last {config.NEWS_FRESHNESS}: {titles}"
    else:
        summary = f"No supply-risk signals in the last {config.NEWS_FRESHNESS}."
    return Finding(agent=AGENT_NAME, summary=summary, sources=relevant, signal=bool(relevant))
