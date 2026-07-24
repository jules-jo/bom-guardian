"""Locate, fetch, and section the errata document for a part via Search + Contents."""

import re
from dataclasses import dataclass

from ..models import Source
from ..agents.relevance import mentions_component
from ..youcom_client import YouComClient

ERRATA_DOC_TERMS = ("errata", "device limitation", "device errata")
PREFERRED_URL_HINTS = (".pdf", "st.com", "microchip.com", "ti.com", "nxp.com", "infineon.com")

# Errata PDFs render as markdown headings ("## 2.3.1 ...") or bare numbered lines.
_MD_HEADING = re.compile(r"^\s*#{1,6}\s+(?P<title>\S.*)$")
_NUMBERED_HEADING = re.compile(r"^\s*(?P<title>\d+\.\d+(?:\.\d+)?\s+[A-Za-z].*)$")

MAX_EXCERPT_CHARS = 600


@dataclass(frozen=True)
class ErrataSection:
    title: str
    body: str


async def find_errata_url(client: YouComClient, mpn: str) -> Source | None:
    """Best candidate errata document for the part, vendor PDFs first."""
    sources = await client.search(f"{mpn} errata sheet device limitations pdf")
    candidates = [
        s
        for s in sources
        if mentions_component(s, mpn)
        and any(term in f"{s.title} {s.snippet}".lower() for term in ERRATA_DOC_TERMS)
    ]
    if not candidates:
        return None
    candidates.sort(
        key=lambda s: sum(hint in s.url.lower() for hint in PREFERRED_URL_HINTS), reverse=True
    )
    return candidates[0]


async def fetch_errata_markdown(client: YouComClient, url: str) -> str:
    documents = await client.contents([url])
    if not documents or not isinstance(documents, list):
        return ""
    return documents[0].get("markdown") or ""


def split_sections(markdown: str) -> tuple[ErrataSection, ...]:
    sections: list[ErrataSection] = []
    title: str | None = None
    body: list[str] = []
    for line in markdown.splitlines():
        match = _MD_HEADING.match(line) or _NUMBERED_HEADING.match(line)
        if match:
            if title is not None:
                sections.append(ErrataSection(title=title, body="\n".join(body).strip()))
            title = match.group("title").strip()
            body = []
        elif title is not None:
            body.append(line)
    if title is not None:
        sections.append(ErrataSection(title=title, body="\n".join(body).strip()))
    return tuple(sections)


MAX_TITLE_CHARS = 120  # a PDF table-of-contents rendered as one line is not a section


def match_sections(
    sections: tuple[ErrataSection, ...], aliases: tuple[str, ...]
) -> tuple[ErrataSection, ...]:
    """Sections whose title mentions any alias as a whole word.

    Word boundaries matter: "DMA" must not match "DMA2D" (a different
    peripheral) and "TIM" must not match "timing".
    """
    patterns = [re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE) for alias in aliases]
    return tuple(
        ErrataSection(title=s.title, body=s.body[:MAX_EXCERPT_CHARS])
        for s in sections
        if len(s.title) <= MAX_TITLE_CHARS
        and any(pattern.search(s.title) for pattern in patterns)
    )
