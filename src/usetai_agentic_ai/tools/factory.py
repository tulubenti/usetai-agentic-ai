from __future__ import annotations

from usetai_agentic_ai.settings import AppSettings
from usetai_agentic_ai.tools.docs_retrieval import DocsRetrievalTool
from usetai_agentic_ai.tools.web_summary import WebSummaryTool


def build_tools(settings: AppSettings) -> dict[str, object]:
    tools: dict[str, object] = {}
    if settings.enable_docs_tool:
        tools["docs_retrieval"] = DocsRetrievalTool(settings.parsed_docs_paths())
    if settings.enable_web_tool:
        tools["web_summary"] = WebSummaryTool()
    return tools
