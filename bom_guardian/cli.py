"""CLI entry point: analyze one part or a whole BOM CSV from the terminal.

Usage:
  python -m bom_guardian.cli --mpn STM32H743ZIT6
  python -m bom_guardian.cli --bom data/demo_bom.csv
"""

import argparse
import asyncio
import sys
from pathlib import Path

from . import config
from .bom_parser import parse_bom_csv
from .models import Component
from .agents.orchestrator import analyze_bom
from .report import render_bom_markdown
from .youcom_client import YouComClient


async def run(components: tuple[Component, ...]) -> str:
    client = YouComClient(api_key=config.get_api_key())
    try:
        reports = await analyze_bom(
            client,
            components,
            on_progress=lambda c, r: print(f"  done: {c.mpn} -> {r.risk.value}", file=sys.stderr),
        )
    finally:
        await client.aclose()
    return render_bom_markdown(reports)


def main() -> None:
    parser = argparse.ArgumentParser(description="BOM Guardian — component risk radar")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mpn", help="Analyze a single manufacturer part number")
    group.add_argument("--bom", help="Path to a BOM CSV (columns: mpn[,manufacturer,description,qty])")
    args = parser.parse_args()

    if args.mpn:
        components: tuple[Component, ...] = (Component(mpn=args.mpn),)
    else:
        components = parse_bom_csv(Path(args.bom).read_text())

    print(f"Analyzing {len(components)} component(s)...", file=sys.stderr)
    print(asyncio.run(run(components)))


if __name__ == "__main__":
    main()
