from usetai_agentic_ai.providers.heuristic import HeuristicPlannerProvider
from usetai_agentic_ai.workflows.demo import DemoWorkflow


class EchoTool:
    def run(self, text: str) -> str:
        return f"evidence::{text}"


def test_demo_workflow_docs_qa_runs_tool_then_final() -> None:
    workflow = DemoWorkflow(
        provider=HeuristicPlannerProvider(),
        tools={"docs_retrieval": EchoTool(), "web_summary": EchoTool()},
        max_steps=3,
    )

    result = workflow.run(task="docs_qa", query="how to run demo")

    assert result["history"][0]["action"] == "docs_retrieval"
    assert result["history"][-1]["action"] == "final"
    assert "Final answer" in result["response"]
