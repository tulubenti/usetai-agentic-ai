"""Example script to run the Agent with a custom goal and save history to a JSON file."""
import argparse
import json
import os

from agent import Agent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", type=str, default="Gather a short summary about autonomous agents and save it to agent_notes.txt")
    parser.add_argument("--model", type=str, default="google/flan-t5-small")
    parser.add_argument("--steps", type=int, default=6)
    parser.add_argument("--use-hf", action="store_true", help="Use Hugging Face Inference API (requires HF_API_TOKEN)")
    parser.add_argument("--force-fallback", action="store_true", help="Force deterministic fallback model even if transformers are available")
    args = parser.parse_args()

    hf_token = os.environ.get("HF_API_TOKEN")
    agent = Agent(
        goal=args.goal,
        model_name=args.model,
        max_steps=args.steps,
        use_hf_api=args.use_hf,
        hf_token=hf_token,
        force_fallback=args.force_fallback,
    )
    history = agent.run()

    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
    print("Saved history.json")


if __name__ == "__main__":
    main()
