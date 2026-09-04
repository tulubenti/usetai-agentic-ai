"""Legacy example.py entrypoint kept for backward compatibility."""

from __future__ import annotations

import argparse
import json
import os

from agent import Agent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--goal",
        type=str,
        default="Gather a short summary about autonomous agents and save it to agent_notes.txt",
    )
    parser.add_argument("--model", type=str, default="google/flan-t5-small")
    parser.add_argument("--steps", type=int, default=6)
    parser.add_argument(
        "--use-hf",
        action="store_true",
        help="Use Hugging Face Inference API (requires HF_API_TOKEN)",
    )
    parser.add_argument(
        "--force-fallback",
        action="store_true",
        help="Retained for compatibility; ignored by the legacy wrapper.",
    )
    args = parser.parse_args()

    history = Agent(
        goal=args.goal,
        model_name=args.model,
        max_steps=args.steps,
        use_hf_api=args.use_hf,
        hf_token=os.environ.get("HF_API_TOKEN"),
        force_fallback=args.force_fallback,
    ).run()

    with open("history.json", "w", encoding="utf-8") as handle:
        json.dump(history, handle, indent=2)
    print("Saved history.json")


if __name__ == "__main__":
    main()
