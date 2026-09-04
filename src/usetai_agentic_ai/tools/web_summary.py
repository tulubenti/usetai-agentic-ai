from __future__ import annotations

import wikipedia


class WebSummaryTool:
    name = "web_summary"

    def run(self, query: str) -> str:
        try:
            return wikipedia.summary(query, sentences=3)
        except Exception:
            return (
                "Offline fallback summary: web lookup unavailable. "
                f"For '{query}', provide a high-level explanation "
                "using your local knowledge and docs context."
            )
