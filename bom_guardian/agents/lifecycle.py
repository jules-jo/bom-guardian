"""Lifecycle agent: EOL/NRND status plus drop-in alternates, via the Research API."""

import re

from ..models import Component, Finding, LifecycleStatus
from ..youcom_client import YouComClient

AGENT_NAME = "lifecycle"

PROMPT_TEMPLATE = (
    "You are checking the production lifecycle of the electronic component "
    "{mpn}{manufacturer_clause}. The FIRST line of your answer must be exactly one of: "
    "STATUS: ACTIVE, STATUS: NRND, STATUS: EOL, or STATUS: UNKNOWN. "
    "Then explain: current lifecycle status, any product change notices (PCN) or "
    "end-of-life announcements with dates, and if the part is NRND or EOL, suggest "
    "up to 3 drop-in or near-drop-in replacement part numbers. Cite sources."
)

STATUS_PATTERN = re.compile(r"STATUS:\s*(ACTIVE|NRND|EOL|UNKNOWN)", re.IGNORECASE)


def parse_status(research_markdown: str) -> LifecycleStatus:
    match = STATUS_PATTERN.search(research_markdown[:300])
    if not match:
        return LifecycleStatus.UNKNOWN
    return LifecycleStatus(match.group(1).upper())


async def run(client: YouComClient, component: Component) -> Finding:
    manufacturer_clause = f" by {component.manufacturer}" if component.manufacturer else ""
    answer = await client.research(
        PROMPT_TEMPLATE.format(mpn=component.mpn, manufacturer_clause=manufacturer_clause)
    )
    status = parse_status(answer)
    return Finding(
        agent=AGENT_NAME,
        summary=answer,
        status=status,
        signal=status in (LifecycleStatus.NRND, LifecycleStatus.EOL),
    )
