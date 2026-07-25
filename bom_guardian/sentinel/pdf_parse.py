"""LlamaParse (LlamaIndex Cloud) fallback for errata PDFs.

Vendor errata sheets are dense, multi-column PDFs; when the Contents API
returns nothing sectionable, LlamaParse takes a pass before we give up on
document grounding. Activates only when LLAMA_CLOUD_API_KEY is configured —
without a key this module is a silent no-op.
"""

import logging
import os

logger = logging.getLogger(__name__)

PARSE_TIER = "cost_effective"
PARSE_TIMEOUT_SECONDS = 120


def get_api_key() -> str:
    return os.environ.get("LLAMA_CLOUD_API_KEY", "")


async def parse_pdf_url(url: str) -> str:
    """Parse a document URL to markdown via LlamaParse; '' on any failure."""
    api_key = get_api_key()
    if not api_key:
        return ""
    try:
        from llama_cloud import AsyncLlamaCloud
    except ImportError:
        logger.warning("llama-cloud SDK not installed; skipping PDF fallback")
        return ""
    try:
        async with AsyncLlamaCloud(api_key=api_key) as client:
            result = await client.parsing.parse(
                tier=PARSE_TIER,
                version="latest",
                source_url=url,
                expand=["markdown", "text"],
                timeout=PARSE_TIMEOUT_SECONDS,
            )
    except Exception as exc:
        logger.warning("LlamaParse failed for %s: %s", url, exc)
        return ""
    return result.markdown_full or result.text_full or ""
