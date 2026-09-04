from __future__ import annotations

from typing import Any

from usetai_agentic_ai.providers.base import BasePlannerProvider
from usetai_agentic_ai.workflows.models import WorkflowState


class DemoWorkflow:
    def __init__(self, provider: BasePlannerProvider, tools: dict[str, object], max_steps: int = 4):
        self.provider = provider
        self.tools = tools
        self.max_steps = max_steps

    def run(self, task: str, query: str) -> dict[str, Any]:
        history: list[dict[str, Any]] = []
        final_response = ""

        for index in range(self.max_steps):
            state = WorkflowState(task=task, query=query, history=history)
            step = self.provider.next_step(state)

            if step.kind == "tool" and step.tool:
                tool = self.tools.get(step.tool)
                if tool is None:
                    output = f"Requested tool '{step.tool}' is not enabled."
                else:
                    output = tool.run(step.input_text or query)
                history.append(
                    {
                        "step": index + 1,
                        "reasoning": step.reasoning,
                        "action": step.tool,
                        "input": step.input_text or query,
                        "output": output,
                    }
                )
                continue

            final_response = step.input_text or "No final response provided by planner."
            history.append(
                {
                    "step": index + 1,
                    "reasoning": step.reasoning,
                    "action": "final",
                    "input": query,
                    "output": final_response,
                }
            )
            break

        if not final_response:
            final_response = "Workflow ended without an explicit final response."

        return {
            "task": task,
            "query": query,
            "response": final_response,
            "history": history,
        }
