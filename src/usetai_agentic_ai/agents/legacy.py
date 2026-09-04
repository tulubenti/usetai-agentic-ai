from __future__ import annotations

from usetai_agentic_ai.agents.demo_agent import DemoAgent
from usetai_agentic_ai.settings import AppSettings
from usetai_agentic_ai.tools.web_summary import WebSummaryTool


class Tools:
    @staticmethod
    def wiki_search(query: str, sentences: int = 2) -> str:  # noqa: ARG004
        return WebSummaryTool().run(query)


class Agent:
    """Backward-compatible minimal Agent facade."""

    def __init__(
        self,
        goal: str,
        model_name: str = "google/flan-t5-small",  # noqa: ARG002
        max_steps: int = 6,
        device: int = -1,  # noqa: ARG002
        use_hf_api: bool = False,
        hf_token: str | None = None,
        force_fallback: bool = False,  # noqa: ARG002
    ):
        provider = "hf_inference" if use_hf_api else "heuristic"
        self.settings = AppSettings(max_steps=max_steps, provider=provider, hf_api_token=hf_token)
        self.goal = goal
        self._agent = DemoAgent(self.settings)
        self.history: list[dict] = []

    def run(self) -> list[dict]:
        result = self._agent.run(task="topic_brief", query=self.goal)
        self.history = [
            {"action": entry["action"], "result": entry["output"]} for entry in result["history"]
        ]
        return self.history
