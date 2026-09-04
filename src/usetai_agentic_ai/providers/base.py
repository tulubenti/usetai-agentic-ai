from __future__ import annotations

from abc import ABC, abstractmethod

from usetai_agentic_ai.workflows.models import PlanStep, WorkflowState


class BasePlannerProvider(ABC):
    @abstractmethod
    def next_step(self, state: WorkflowState) -> PlanStep:
        raise NotImplementedError
