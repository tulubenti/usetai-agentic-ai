from __future__ import annotations

from usetai_agentic_ai.providers.base import BasePlannerProvider
from usetai_agentic_ai.workflows.models import PlanStep, WorkflowState


class HeuristicPlannerProvider(BasePlannerProvider):
    """Deterministic planner for fast, offline demos."""

    def next_step(self, state: WorkflowState) -> PlanStep:
        if not state.history:
            if state.task == "topic_brief":
                return PlanStep(
                    kind="tool",
                    tool="web_summary",
                    input_text=state.query,
                    reasoning="Gather external context with a web-capable summary tool.",
                )
            return PlanStep(
                kind="tool",
                tool="docs_retrieval",
                input_text=state.query,
                reasoning="Retrieve local repository context first.",
            )

        latest_output = state.history[-1].get("output", "")
        answer = (
            "Final answer:\n"
            f"Task: {state.task}\n"
            f"Query: {state.query}\n"
            "Evidence summary:\n"
            f"{latest_output[:1200]}"
        )
        return PlanStep(
            kind="final",
            input_text=answer,
            reasoning="Synthesize a concise answer from tool evidence.",
        )
