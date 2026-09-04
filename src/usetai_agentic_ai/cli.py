from __future__ import annotations

import argparse

from usetai_agentic_ai.agents.demo_agent import DemoAgent
from usetai_agentic_ai.settings import AppSettings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run demo Agentic AI workflows with open/free defaults."
    )
    parser.add_argument("--task", choices=["docs_qa", "topic_brief"], default="docs_qa")
    parser.add_argument("--query", required=True)
    parser.add_argument("--provider", choices=["heuristic", "ollama", "hf_inference"], default=None)
    parser.add_argument("--history-out", default=None)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    settings = AppSettings()
    if args.provider:
        settings.provider = args.provider

    agent = DemoAgent(settings=settings)
    result = agent.run(task=args.task, query=args.query, history_file=args.history_out)

    print("=== Final Response ===")
    print(result["response"])
    print("\n=== Tool/Reasoning Trace ===")
    for item in result["history"]:
        print(f"Step {item['step']}: {item['action']} :: {item['reasoning']}")


if __name__ == "__main__":
    main()
