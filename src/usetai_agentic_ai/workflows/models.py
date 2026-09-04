from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PlanStep:
    kind: str  # tool | final
    reasoning: str
    tool: str | None = None
    input_text: str | None = None


@dataclass
class WorkflowState:
    task: str
    query: str
    history: list[dict[str, Any]]
