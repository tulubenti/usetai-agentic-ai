"""Improved agent implementation with a safer RUN sandbox and optional HF Inference API support."""
import os
import sys
import tempfile
import subprocess
import json
import time
from typing import List, Dict, Any, Optional

# Keep heavy ML imports lazy to make the module import lightweight for tests

import wikipedia
import requests


class Tools:
    @staticmethod
    def wiki_search(query: str, sentences: int = 2) -> str:
        try:
            return wikipedia.summary(query, sentences=sentences)
        except Exception as e:
            return f"WIKI_ERROR: {e}"

    @staticmethod
    def run_python(code: str, timeout: int = 5, mem_limit_bytes: int = 256 * 1024 * 1024) -> str:
        """Execute Python code in a separate subprocess with resource limits where available.

        This is still NOT a secure sandbox. It limits CPU time and address space on Unix-like
        systems using the resource module and runs the code in a temporary file via a subprocess.
        """
        # Write code to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
        try:
            # Build the command using the same Python interpreter
            cmd = [sys.executable, path]
            # On Unix we can set resource limits in the child process
            preexec_fn = None
            if os.name == "posix":
                try:
                    import resource

                    def _limit_child():
                        # CPU time (seconds)
                        try:
                            resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
                        except Exception:
                            pass
                        # Address space (virtual memory)
                        try:
                            resource.setrlimit(resource.RLIMIT_AS, (mem_limit_bytes, mem_limit_bytes))
                        except Exception:
                            pass
                    preexec_fn = _limit_child
                except Exception:
                    preexec_fn = None

            completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 1, preexec_fn=preexec_fn)
            out = (completed.stdout or "") + ("\n" + completed.stderr if completed.stderr else "")
            return out.strip()
        except subprocess.TimeoutExpired:
            return "ERROR: python execution timed out"
        except Exception as e:
            return f"ERROR: {e}"
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
    def __init__(self, goal: str, model_name: str = "google/flan-t5-small", max_steps: int = 6, device: int = -1, use_hf_api: bool = False, hf_token: Optional[str] = None):
        self.goal = goal
        self.history: List[Dict[str, Any]] = []
        self.max_steps = max_steps
        self.model_name = model_name
        self.device = device
        self.use_hf_api = use_hf_api
        self.hf_token = hf_token
        self.pipe = None

        if self.use_hf_api and not self.hf_token:
            # If user requested HF API but no token provided, fall back to local
            print("Warning: HF API requested but HF_API_TOKEN not provided — falling back to local model")
            self.use_hf_api = False

        # Lazy initialize local pipeline only when needed
        if not self.use_hf_api:
            try:
                # Import transformers here to avoid heavy import on module load
                from transformers import pipeline as _pipeline
                # Create a text2text pipeline
                self.pipe = _pipeline("text2text-generation", model=self.model_name, device=self.device)
            except Exception as e:
                print(f"Could not initialize local model pipeline: {e}")
                self.pipe = None

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

    def _call_hf_inference(self, prompt: str) -> str:
        assert self.hf_token, "HF token is required for HF inference"
        url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        data = {"inputs": prompt, "options": {"wait_for_model": True}}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            j = resp.json()
            # The API may return a string or a list of generated objects
            if isinstance(j, dict) and "error" in j:
                return f"HF_ERROR: {j['error']}"
            if isinstance(j, list):
                first = j[0]
                if isinstance(first, dict) and "generated_text" in first:
                    return first["generated_text"]
                if isinstance(first, dict) and "content" in first:
                    return first["content"]
                return str(first)
            return str(j)
        except Exception as e:
            return f"HF_ERROR: {e}"

    def _call_local_model(self, prompt: str) -> str:
        if not self.pipe:
            return "MODEL_ERROR: local model pipeline not available"
        try:
            out = self.pipe(prompt, max_length=256, do_sample=False)
            if isinstance(out, list) and len(out) > 0 and "generated_text" in out[0]:
                return out[0]["generated_text"].strip()
            # Fallback
            return str(out)
        except Exception as e:
            return f"MODEL_ERROR: {e}"

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
        if self.use_hf_api:
            action = self._call_hf_inference(prompt)
        else:
            action = self._call_local_model(prompt)
        action = action.strip()
        result = self._parse_and_execute(action)
        entry = {"action": action, "result": result}
        self.history.append(entry)
        return entry

    def run(self) -> List[Dict[str, Any]]:
        for i in range(self.max_steps):
            entry = self.step()
            print(f"STEP {i+1}: {entry['action']}\nRESULT:\n{entry['result']}\n{'-'*40}")
            if entry['action'].upper().startswith("DONE:"):
                break
        return self.history


if __name__ == "__main__":
    goal = "Gather a short summary about autonomous agents and save it to agent_notes.txt"
    agent = Agent(goal=goal)
    agent.run()
