"""Parse a BOM from CSV text into Components. Validates at the boundary."""

import csv
import io

from .models import Component

REQUIRED_COLUMNS = frozenset({"mpn"})
OPTIONAL_COLUMNS = ("manufacturer", "description", "qty")
MAX_COMPONENTS = 50


class BomParseError(ValueError):
    """Raised when the uploaded BOM cannot be parsed."""


def parse_bom_csv(text: str) -> tuple[Component, ...]:
    reader = csv.DictReader(io.StringIO(text.strip()))
    if reader.fieldnames is None:
        raise BomParseError("BOM is empty. Expected a CSV with at least an 'mpn' column.")

    columns = {name.strip().lower() for name in reader.fieldnames}
    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise BomParseError(
            f"BOM is missing required column(s): {', '.join(sorted(missing))}. "
            f"Found columns: {', '.join(sorted(columns))}"
        )

    components = []
    for line_number, row in enumerate(reader, start=2):
        normalized = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
        mpn = normalized.get("mpn", "")
        if not mpn:
            continue
        try:
            qty = int(normalized.get("qty") or 1)
        except ValueError as exc:
            raise BomParseError(f"Line {line_number}: qty must be an integer.") from exc
        components.append(
            Component(
                mpn=mpn,
                manufacturer=normalized.get("manufacturer", ""),
                description=normalized.get("description", ""),
                qty=qty,
            )
        )

    if not components:
        raise BomParseError("BOM contained no rows with an mpn value.")
    if len(components) > MAX_COMPONENTS:
        raise BomParseError(
            f"BOM has {len(components)} components; limit is {MAX_COMPONENTS} for this demo."
        )
    return tuple(components)
