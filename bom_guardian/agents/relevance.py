"""Shared relevance filtering for search-based agents.

Web search happily returns errata sheets and shortage news for entirely
different parts; a source only counts if it mentions the component itself
(by normalized part-number prefix, since listings often drop packaging
suffixes) AND contains one of the agent's risk terms.
"""

import re
from collections.abc import Iterable

from ..models import Source

MIN_MPN_MATCH_CHARS = 5
MPN_MATCH_FRACTION = 0.6

_NON_ALNUM = re.compile(r"[^a-z0-9]")


def _normalize(text: str) -> str:
    return _NON_ALNUM.sub("", text.lower())


def _mpn_key(mpn: str) -> str:
    """Prefix of the normalized MPN long enough to be distinctive.

    Full MPNs often carry packaging/temperature suffixes ("EP2C5T144C8N" vs
    "EP2C5T144C8") that sources omit, so match on a generous prefix instead.
    """
    normalized = _normalize(mpn)
    length = max(MIN_MPN_MATCH_CHARS, int(len(normalized) * MPN_MATCH_FRACTION))
    return normalized[:length]


def mentions_component(source: Source, mpn: str) -> bool:
    key = _mpn_key(mpn)
    if not key:
        return False  # empty mpn must not degrade the filter to accept-everything
    haystack = _normalize(f"{source.title} {source.url} {source.snippet}")
    return key in haystack


def filter_relevant(sources: Iterable[Source], terms: Iterable[str], mpn: str) -> tuple[Source, ...]:
    """Keep sources that mention the component and any of the given risk terms."""
    terms = tuple(terms)
    return tuple(
        source
        for source in sources
        if mentions_component(source, mpn)
        and any(term in f"{source.title} {source.snippet}".lower() for term in terms)
    )
