"""Fan out the agent trio over every BOM component with bounded concurrency."""

import asyncio
from collections.abc import Callable

from .. import config
from ..models import Component, ComponentReport, Finding
from ..report import score_risk
from ..youcom_client import YouComClient
from . import availability, errata, lifecycle

AGENTS = (lifecycle.run, errata.run, availability.run)

ProgressCallback = Callable[[Component, ComponentReport], None]


def _error_finding(agent_name: str, error: BaseException) -> Finding:
    return Finding(agent=agent_name, summary=f"Agent failed: {error}", signal=False)


async def analyze_component(client: YouComClient, component: Component) -> ComponentReport:
    results = await asyncio.gather(
        *(agent(client, component) for agent in AGENTS), return_exceptions=True
    )
    findings = tuple(
        result
        if isinstance(result, Finding)
        else _error_finding(agent.__module__.rsplit(".", 1)[-1], result)
        for agent, result in zip(AGENTS, results)
    )
    return ComponentReport(component=component, findings=findings, risk=score_risk(findings))


async def analyze_bom(
    client: YouComClient,
    components: tuple[Component, ...],
    on_progress: ProgressCallback | None = None,
) -> tuple[ComponentReport, ...]:
    semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_COMPONENTS)

    async def bounded(component: Component) -> ComponentReport:
        async with semaphore:
            component_report = await analyze_component(client, component)
        if on_progress:
            on_progress(component, component_report)
        return component_report

    return tuple(await asyncio.gather(*(bounded(c) for c in components)))
