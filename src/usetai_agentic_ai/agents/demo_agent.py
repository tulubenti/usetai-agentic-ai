from __future__ import annotations

from usetai_agentic_ai.memory.history import save_history
from usetai_agentic_ai.providers.factory import build_provider
from usetai_agentic_ai.settings import AppSettings
from usetai_agentic_ai.tools.factory import build_tools
from usetai_agentic_ai.workflows.demo import DemoWorkflow


class DemoAgent:
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.provider = build_provider(settings)
        self.tools = build_tools(settings)
        self.workflow = DemoWorkflow(
            provider=self.provider,
            tools=self.tools,
            max_steps=settings.max_steps,
        )

    def run(self, task: str, query: str, history_file: str | None = None) -> dict:
        result = self.workflow.run(task=task, query=query)
        save_history(history_file or self.settings.history_file, result)
        return result
