"""Silicon Sentinel: cross-check firmware peripheral usage against live errata.

Pipeline: extract peripherals from code -> find errata doc (Search) -> pull its
text (Contents) -> intersect sections with used peripherals. If the document
cannot be found or parsed, fall back to a Research query scoped to the used
peripherals. Every network step degrades to a logged, user-visible note rather
than crashing the analysis.
"""

import logging
from dataclasses import dataclass, field

from ..models import Source
from ..report import escape_markdown, render_link
from ..youcom_client import YouComClient
from .errata_doc import (
    ErrataSection,
    fetch_errata_markdown,
    find_errata_url,
    match_sections,
    split_sections,
)
from .pdf_parse import parse_pdf_url
from .peripherals import ERRATA_ALIASES, PeripheralHit, extract_peripherals

logger = logging.getLogger(__name__)

RESEARCH_FALLBACK_TEMPLATE = (
    "List the published silicon errata for {mpn} that affect these peripherals: "
    "{peripherals}. For each: the erratum title/number, the failure condition, "
    "and the documented workaround. Cite the errata sheet. If none exist for a "
    "peripheral, say so."
)

MAX_SECTIONS_PER_PERIPHERAL = 4


@dataclass(frozen=True)
class PeripheralMatch:
    hit: PeripheralHit
    sections: tuple[ErrataSection, ...]


@dataclass(frozen=True)
class SentinelReport:
    mpn: str
    peripherals: tuple[PeripheralHit, ...]
    errata_source: Source | None
    matches: tuple[PeripheralMatch, ...]
    fallback_summary: str = ""
    fallback_sources: tuple[Source, ...] = field(default_factory=tuple)
    parsed_via: str = ""  # "contents" or "llamaparse" when document grounding succeeded
    error: str = ""


async def analyze(client: YouComClient, mpn: str, code: str) -> SentinelReport:
    peripherals = extract_peripherals(code)
    if not peripherals:
        return SentinelReport(mpn=mpn, peripherals=(), errata_source=None, matches=())

    errata_source = None
    try:
        errata_source = await find_errata_url(client, mpn)
    except Exception as exc:
        logger.warning("Errata search failed for %s: %s", mpn, exc)

    sections: tuple[ErrataSection, ...] = ()
    parsed_via = ""
    if errata_source is not None:
        try:
            markdown = await fetch_errata_markdown(client, errata_source.url)
            sections = split_sections(markdown)
            parsed_via = "contents" if sections else ""
        except Exception as exc:
            logger.warning("Errata fetch failed for %s (%s): %s", mpn, errata_source.url, exc)
        if not sections:
            llama_markdown = await parse_pdf_url(errata_source.url)
            sections = split_sections(llama_markdown)
            parsed_via = "llamaparse" if sections else ""

    matches = tuple(
        PeripheralMatch(hit=hit, sections=matched)
        for hit in peripherals
        if (matched := match_sections(sections, ERRATA_ALIASES[hit.name]))
    )
    if matches:
        return SentinelReport(
            mpn=mpn,
            peripherals=peripherals,
            errata_source=errata_source,
            matches=matches,
            parsed_via=parsed_via,
        )

    peripheral_names = ", ".join(hit.name for hit in peripherals)
    try:
        result = await client.research(
            RESEARCH_FALLBACK_TEMPLATE.format(mpn=mpn, peripherals=peripheral_names)
        )
    except Exception as exc:
        logger.warning("Research fallback failed for %s: %s", mpn, exc)
        return SentinelReport(
            mpn=mpn,
            peripherals=peripherals,
            errata_source=errata_source,
            matches=(),
            error="Errata document could not be cross-checked and the research fallback failed. Try again.",
        )
    return SentinelReport(
        mpn=mpn,
        peripherals=peripherals,
        errata_source=errata_source,
        matches=(),
        fallback_summary=result.content,
        fallback_sources=result.sources,
    )


def render_markdown(report: SentinelReport) -> str:
    mpn = escape_markdown(report.mpn)
    if not report.peripherals:
        return f"## Silicon Sentinel — {mpn}\nNo recognizable peripheral usage found in the code."
    lines = [f"## Silicon Sentinel — {mpn}"]
    used = ", ".join(f"{h.name} (line {h.line_number})" for h in report.peripherals)
    lines.append(f"**Peripherals used by your firmware:** {used}\n")
    if report.errata_source:
        parser_note = " · parsed with LlamaParse" if report.parsed_via == "llamaparse" else ""
        lines.append(f"**Errata document:** {render_link(report.errata_source)}{parser_note}\n")
    if report.matches:
        lines.append(f"**⚠️ {len(report.matches)} peripheral(s) you use appear in the errata:**")
        for match in report.matches:
            evidence = match.hit.line.replace("`", "'")
            lines.append(f"\n### {match.hit.name} — used at line {match.hit.line_number}: `{evidence}`")
            for section in match.sections[:MAX_SECTIONS_PER_PERIPHERAL]:
                lines.append(f"- **{escape_markdown(section.title)}**")
                if section.body:
                    lines.append(f"  {escape_markdown(section.body)}")
    elif report.error:
        lines.append(f"**⚠️ {report.error}**")
    elif report.fallback_summary:
        lines.append("**Errata document could not be parsed directly — cited research fallback:**\n")
        lines.append(report.fallback_summary)
        if report.fallback_sources:
            lines.append("")
            lines.extend(f"- {render_link(s)}" for s in report.fallback_sources[:5])
    else:
        lines.append("**✅ No errata sections matched the peripherals your code uses.**")
    return "\n".join(lines)
