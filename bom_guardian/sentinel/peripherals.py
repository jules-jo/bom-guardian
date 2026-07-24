"""Detect which MCU peripherals a firmware source file actually uses.

Deterministic pattern matching over identifiers (HAL_I2C_..., SPI1, DMA2_Stream0)
rather than an LLM: testable, instant, and wrong in auditable ways.
"""

import re
from dataclasses import dataclass

# Case-sensitive: peripheral identifiers in C firmware are uppercase; prose is not.
# C identifiers continue with digits/underscores ("I2C_HandleTypeDef", "HAL_DMA_Init"),
# where \b never fires — so cores are anchored at the start and continued by a
# lookahead: [\d_] for use inside an identifier, \W/$ for a bare register name.
_LOOSE = r"(?=[\d_\W]|$)"  # bare word also counts (I2C, SPI as standalone tokens)
_STRICT = r"(?=[\d_])"  # must continue as an identifier (avoids the words CAN, TIM...)

PERIPHERAL_PATTERNS: dict[str, str] = {
    "I2C": rf"\b(?:HAL_|LL_)?I2C{_LOOSE}",
    "SPI": rf"\b(?:HAL_|LL_)?SPI{_LOOSE}",
    "UART": rf"\b(?:HAL_|LL_)?(?:LP)?US?ART{_LOOSE}",
    "DMA": rf"\b(?:HAL_|LL_)?[BM]?DMA{_LOOSE}",
    "ADC": rf"\b(?:HAL_|LL_)?ADC{_LOOSE}",
    "DAC": rf"\b(?:HAL_|LL_)?DAC{_LOOSE}",
    "TIM": rf"\b(?:HAL_|LL_)?TIM{_STRICT}",
    "CAN": rf"\bbxCAN\b|\b(?:HAL_|LL_)?(?:FD)?CAN{_STRICT}",
    "USB": r"\bUSB(?=[\d_\W]|$)|\bOTG_[FH]S",
    "RTC": rf"\b(?:HAL_|LL_)?RTC{_STRICT}",
    "ETH": r"\bHAL_ETH(?=[\d_\W]|$)|\bETH_\w+",
    "QSPI": rf"\b(?:HAL_|LL_)?(?:QUADSPI|QSPI|OCTOSPI){_LOOSE}",
    "SDMMC": rf"\bSDMMC{_LOOSE}|\bSDIO\b",
    "FMC": r"\bFMC_\w+|\bFSMC\b",
    "EXTI": rf"\bEXTI{_LOOSE}",
    "WDG": rf"\b[IW]WDG{_LOOSE}",
}

# Terms an errata document may use for each detected peripheral.
ERRATA_ALIASES: dict[str, tuple[str, ...]] = {
    "I2C": ("i2c",),
    "SPI": ("spi",),
    "UART": ("usart", "uart", "lpuart"),
    "DMA": ("dma", "bdma", "mdma"),
    "ADC": ("adc",),
    "DAC": ("dac",),
    "TIM": ("tim", "timer"),
    "CAN": ("can", "fdcan"),
    "USB": ("usb", "otg"),
    "RTC": ("rtc",),
    "ETH": ("ethernet", "emac"),
    "QSPI": ("quadspi", "qspi", "octospi"),
    "SDMMC": ("sdmmc", "sdio"),
    "FMC": ("fmc", "fsmc"),
    "EXTI": ("exti",),
    "WDG": ("iwdg", "wwdg", "watchdog"),
}

_COMPILED = {name: re.compile(pattern) for name, pattern in PERIPHERAL_PATTERNS.items()}


@dataclass(frozen=True)
class PeripheralHit:
    name: str
    line_number: int
    line: str


def extract_peripherals(code: str) -> tuple[PeripheralHit, ...]:
    """First occurrence of each peripheral family, in source order."""
    hits: dict[str, PeripheralHit] = {}
    for line_number, line in enumerate(code.splitlines(), start=1):
        for name, pattern in _COMPILED.items():
            if name not in hits and pattern.search(line):
                hits[name] = PeripheralHit(name=name, line_number=line_number, line=line.strip())
    return tuple(sorted(hits.values(), key=lambda h: h.line_number))
