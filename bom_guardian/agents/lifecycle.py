"""Lifecycle agent: EOL/NRND status plus drop-in alternates, via the Research API."""

import re

from ..models import Component, Finding, LifecycleStatus
from ..youcom_client import YouComClient

AGENT_NAME = "lifecycle"

PROMPT_TEMPLATE = (
    "You are checking the production lifecycle of the electronic component "
    "{mpn}{manufacturer_clause}. Specifically search for official manufacturer "
    "Product Discontinuance Notifications (PDN), Product Change Notices (PCN), "
    "end-of-life announcements, and NRND markings covering this part or its "
    "family; distributor stock alone does not prove a part is active. "
    "The FIRST line of your answer must be exactly one of: "
    "STATUS: ACTIVE, STATUS: NRND, STATUS: EOL, or STATUS: UNKNOWN. "
    "Then explain: current lifecycle status, any PCN or end-of-life "
    "announcements with dates, and if the part is NRND or EOL, suggest "
    "up to 3 drop-in or near-drop-in replacement part numbers. Cite sources."
)

STATUS_PATTERN = re.compile(r"STATUS:\s*(ACTIVE|NRND|EOL|UNKNOWN)", re.IGNORECASE)
STATUS_SEARCH_WINDOW_CHARS = 300  # verdict is required on the first line; allow preamble noise


def parse_status(research_markdown: str) -> LifecycleStatus:
    match = STATUS_PATTERN.search(research_markdown[:STATUS_SEARCH_WINDOW_CHARS])
    if not match:
        return LifecycleStatus.UNKNOWN
    return LifecycleStatus(match.group(1).upper())


async def run(client: YouComClient, component: Component) -> Finding:
    manufacturer_clause = f" by {component.manufacturer}" if component.manufacturer else ""
    result = await client.research(
        PROMPT_TEMPLATE.format(mpn=component.mpn, manufacturer_clause=manufacturer_clause)
    )
    status = parse_status(result.content)
    return Finding(
        agent=AGENT_NAME,
        summary=result.content,
        sources=result.sources,
        status=status,
        signal=status in (LifecycleStatus.NRND, LifecycleStatus.EOL),
    )
