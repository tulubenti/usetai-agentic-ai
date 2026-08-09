"""A minimal agentic AI prototype using an open-source instruction model (Flan-T5-small).

This agent uses a simple planning loop: it asks the model for a next action given a goal
and a short history, then executes that action using built-in tools (wikipedia search,
execute python, write files). This is a lightweight, local prototype intended for
experimentation and adaptation.

Requirements: see requirements.txt
"""

from transformers import pipeline
import wikipedia
import subprocess
import tempfile
import os
import time
from typing import List, Dict, Any

class Tools:
    @staticmethod
    def wiki_search(query: str, sentences: int = 2) -> str:
        try:
            return wikipedia.summary(query, sentences=sentences)
        except Exception as e:
            return f"WIKI_ERROR: {e}"

    @staticmethod
    def run_python(code: str, timeout: int = 10) -> str:
        # Execute code in a temporary file and capture output
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
        try:
            completed = subprocess.run(["python", path], capture_output=True, text=True, timeout=timeout)
            out = completed.stdout
            err = completed.stderr
            return (out + "\n" + err).strip()
        except subprocess.TimeoutExpired:
            return "ERROR: python execution timed out"
        finally:
            try:
                os.unlink(path)
            except Exception:
                pass

    @staticmethod
    def write_file(path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"WROTE: {path}"
        except Exception as e:
            return f"WRITE_ERROR: {e}"


class Agent:
    def __init__(self, goal: str, model_name: str = "google/flan-t5-small", max_steps: int = 6, device: int = -1):
        self.goal = goal
        self.history: List[Dict[str, Any]] = []
        self.max_steps = max_steps
        # text2text pipeline
        self.pipe = pipeline("text2text-generation", model=model_name, device=device)

    def _build_prompt(self) -> str:
        hist = "\n".join([f"- {h['action']} -> {h.get('result','')}" for h in self.history[-6:]])
        prompt = (
            "You are an autonomous agent that must achieve a single high-level goal.\n"
            f"Goal: {self.goal}\n"
            "Available tools:\n"
            "- SEARCH: query -> use wikipedia search to get a short summary.\n"
            "- RUN: python code -> execute Python and return output.\n"
            "- WRITE: filename | content -> write a file to disk.\n"
            "Decide on the next single action that moves you toward the goal.\n"
            "Return the action as a single line in one of these forms:\n"
            "SEARCH: <query>\n"
            "RUN: <python code>\n"
            "WRITE: <filename> | <content>\n"
            "If the goal is complete, respond: DONE: <short explanation>\n"
            "Previous actions:\n"
            f"{hist}\n"
            "Now give the next action." 
        )
        return prompt

    def _parse_and_execute(self, action_str: str) -> str:
        action_str = action_str.strip()
        if action_str.upper().startswith("SEARCH:"):
            query = action_str.split("SEARCH:", 1)[1].strip()
            res = Tools.wiki_search(query)
            return res
        if action_str.upper().startswith("RUN:"):
            code = action_str.split("RUN:", 1)[1].strip()
            return Tools.run_python(code)
        if action_str.upper().startswith("WRITE:"):
            payload = action_str.split("WRITE:", 1)[1].strip()
            # Expect: filename | content
            if "|" in payload:
                filename, content = payload.split("|", 1)
                filename = filename.strip()
                content = content.strip()
            else:
                filename = payload
                content = ""
            return Tools.write_file(filename, content)
        if action_str.upper().startswith("DONE:"):
            return action_str
        return f"UNRECOGNIZED_ACTION: {action_str}"

    def step(self) -> Dict[str, str]:
        prompt = self._build_prompt()
        out = self.pipe(prompt, max_length=256, do_sample=False)
        action = out[0]["generated_text"].strip()
        result = self._parse_and_execute(action)
        entry = {"action": action, "result": result}
        self.history.append(entry)
        return entry

    def run(self):
        for i in range(self.max_steps):
            entry = self.step()
            print(f"STEP {i+1}: {entry['action']}\nRESULT:\n{entry['result']}\n{'-'*40}")
            if entry['action'].upper().startswith("DONE:"):
                break
        return self.history


if __name__ == "__main__":
    # Quick interactive demo
    goal = "Gather a short summary about autonomous agents and save it to agent_notes.txt"
    agent = Agent(goal=goal)
    agent.run()
