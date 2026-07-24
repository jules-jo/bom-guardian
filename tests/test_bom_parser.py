import pytest

from bom_guardian.bom_parser import BomParseError, parse_bom_csv


def test_parses_full_bom():
    csv_text = (
        "mpn,manufacturer,description,qty\n"
        "STM32H743ZIT6,ST,Cortex-M7 MCU,2\n"
        "NE555P,TI,Timer,10\n"
    )
    components = parse_bom_csv(csv_text)
    assert len(components) == 2
    assert components[0].mpn == "STM32H743ZIT6"
    assert components[0].qty == 2
    assert components[1].manufacturer == "TI"


def test_mpn_only_column_is_enough():
    components = parse_bom_csv("mpn\nNE555P\n")
    assert components[0].mpn == "NE555P"
    assert components[0].qty == 1


def test_header_case_and_whitespace_normalized():
    components = parse_bom_csv(" MPN , Qty \nNE555P, 3\n")
    assert components[0].mpn == "NE555P"
    assert components[0].qty == 3


def test_blank_mpn_rows_skipped():
    components = parse_bom_csv("mpn\nNE555P\n\n   \n")
    assert len(components) == 1


def test_missing_mpn_column_raises():
    with pytest.raises(BomParseError, match="mpn"):
        parse_bom_csv("part,qty\nNE555P,1\n")


def test_empty_input_raises():
    with pytest.raises(BomParseError):
        parse_bom_csv("")


def test_bad_qty_raises_with_line_number():
    with pytest.raises(BomParseError, match="Line 2"):
        parse_bom_csv("mpn,qty\nNE555P,many\n")


def test_component_limit_enforced():
    rows = "\n".join(f"PART{i}" for i in range(60))
    with pytest.raises(BomParseError, match="limit"):
        parse_bom_csv("mpn\n" + rows)


def test_oversized_csv_rejected_before_parsing():
    with pytest.raises(BomParseError, match="too large"):
        parse_bom_csv("mpn\n" + "X" * 300_000)


def test_utf8_bom_marker_tolerated():
    components = parse_bom_csv("﻿mpn,qty\nNE555P,2\n")
    assert components[0].mpn == "NE555P"


def test_zero_or_negative_qty_rejected():
    with pytest.raises(BomParseError, match="at least 1"):
        parse_bom_csv("mpn,qty\nNE555P,0\n")
