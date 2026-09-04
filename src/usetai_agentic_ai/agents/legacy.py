from __future__ import annotations

import re

from usetai_agentic_ai.settings import AppSettings


class Tools:
    @staticmethod
    def wiki_search(query: str, sentences: int = 2) -> str:  # noqa: ARG004
        import wikipedia

        try:
            return wikipedia.summary(query, sentences=sentences)
        except Exception as exc:
            return f"WIKI_ERROR: {exc}"


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
        self.use_hf_api = use_hf_api
        self.hf_token = hf_token
        self.force_fallback = force_fallback
        self.history: list[dict] = []

    def run(self) -> list[dict]:
        query = self.goal
        for marker in ("about", "on", "for"):
            match = re.search(rf"\\b{marker}\\b\\s+(.*)", self.goal, flags=re.IGNORECASE)
            if match and match.group(1).strip():
                query = match.group(1).strip()
                break

        if self.force_fallback:
            evidence = f"FALLBACK SUMMARY: {query}"
        elif self.use_hf_api and not self.hf_token:
            evidence = f"FALLBACK SUMMARY: {query}"
        else:
            evidence = Tools.wiki_search(query)
        if evidence and not evidence.startswith("WIKI_ERROR:"):
            planned = [
                {"action": f"SEARCH: {query}", "result": evidence},
                {
                    "action": "WRITE: agent_notes.txt | <summary excerpt>",
                    "result": "WROTE: agent_notes.txt",
                },
                {"action": "DONE: saved notes to agent_notes.txt", "result": "DONE"},
            ]
            limit = max(1, self.settings.max_steps)
            self.history = planned[:limit]
            if any(item["action"].startswith("WRITE:") for item in self.history):
                with open("agent_notes.txt", "w", encoding="utf-8") as handle:
                    handle.write(evidence[:800])
        else:
            self.history = [
                {
                    "action": f"SEARCH: {query}",
                    "result": evidence or "WIKI_ERROR: empty result",
                }
            ]
        return self.history
