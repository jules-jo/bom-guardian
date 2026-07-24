"""Immutable domain models."""

from dataclasses import dataclass, field
from enum import Enum


class LifecycleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    NRND = "NRND"  # not recommended for new designs
    EOL = "EOL"
    UNKNOWN = "UNKNOWN"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class Component:
    mpn: str
    manufacturer: str = ""
    description: str = ""
    qty: int = 1


@dataclass(frozen=True)
class Source:
    title: str
    url: str


@dataclass(frozen=True)
class Finding:
    """Output of one agent for one component."""

    agent: str
    summary: str
    sources: tuple[Source, ...] = field(default_factory=tuple)
    status: LifecycleStatus = LifecycleStatus.UNKNOWN
    signal: bool = False  # True when the agent found something noteworthy


@dataclass(frozen=True)
class ComponentReport:
    component: Component
    findings: tuple[Finding, ...]
    risk: RiskLevel
