"""Parse a BOM from CSV text into Components. Validates at the boundary."""

import csv
import io

from .models import Component

REQUIRED_COLUMNS = frozenset({"mpn"})
OPTIONAL_COLUMNS = ("manufacturer", "description", "qty")
MAX_COMPONENTS = 50
MAX_CSV_CHARS = 200_000  # public deployment: reject huge uploads before parsing


class BomParseError(ValueError):
    """Raised when the uploaded BOM cannot be parsed."""


def parse_bom_csv(text: str) -> tuple[Component, ...]:
    if len(text) > MAX_CSV_CHARS:
        raise BomParseError(
            f"BOM file is too large ({len(text)} characters; limit {MAX_CSV_CHARS})."
        )
    text = text.lstrip("﻿")  # Excel UTF-8 exports prepend a BOM marker
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
        if qty < 1:
            raise BomParseError(f"Line {line_number}: qty must be at least 1.")
        if len(components) >= MAX_COMPONENTS:
            raise BomParseError(
                f"BOM exceeds the {MAX_COMPONENTS}-component limit for this demo."
            )
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
    return tuple(components)
