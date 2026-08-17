# usetai-agentic-ai

Small demo showing a minimal "agentic" AI implemented in Python. This repository contains three files you need to run the agent locally.

## Files

- `agent.py`
  - Main agent implementation. Provides three simple tools (SEARCH via wikipedia, RUN to execute Python in a limited subprocess, and WRITE to save files). If `transformers`/local model pipeline is available the agent will use it; otherwise a tiny deterministic fallback model runs so the agent can perform a few end-to-end steps without large ML downloads.
- `example.py`
  - Small CLI that constructs an `Agent`, runs it, and writes a `history.json` file. Usage: `python example.py` (see options below).
- `requirements.txt`
  - Optional full dependencies (e.g. `transformers`, `torch`) for running a local model pipeline. The agent also works with only the minimal dependencies listed below.

## Quickstart — Minimal (fast)

1. Clone and enter the repo:

   git clone https://github.com/tulubenti/usetai-agentic-ai
   cd usetai-agentic-ai

2. (Recommended) Create and activate a virtual environment:

   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate

3. Install the minimal packages required for the built-in fallback:

   pip install wikipedia requests

4. Run the example agent:

   python example.py --force-fallback

The agent will print step outputs to the console and produce `history.json`. The deterministic fallback will typically perform a SEARCH, WRITE the top of the summary to `agent_notes.txt`, then finish.

Example expected console output (minimal fallback)

```
STEP 1: SEARCH: autonomous agents
RESULT:
Autonomous agent summary text... (truncated)
----------------------------------------
STEP 2: WRITE: agent_notes.txt | <first part of summary>
RESULT:
WROTE: agent_notes.txt
----------------------------------------
STEP 3: DONE: saved notes to agent_notes.txt
Saved history.json
```

After running `python example.py` you should see the STEP output above and the run will produce:

- `history.json` — agent action/result history
- `agent_notes.txt` — saved search summary (created by the WRITE action)

## Quickstart — Full (optional)

If you want the agent to use a real local transformer model (heavy download and extra packages):

1. Install all requirements:

   pip install -r requirements.txt

2. Run the example (same as above):

   python example.py

Alternatively, to use the Hugging Face Inference API instead of a local model, set `HF_API_TOKEN` in your environment and run:

   export HF_API_TOKEN="your-token"    # Windows: set HF_API_TOKEN=your-token
   python example.py --use-hf

## example.py options

- `--goal`  : change the agent goal (default: gather a short summary and save notes)
- `--model` : model name used by transformers when available (default `google/flan-t5-small`)
- `--steps` : max agent steps (default 6)
- `--use-hf`: use Hugging Face Inference API (requires `HF_API_TOKEN`)
- `--force-fallback`: force the deterministic fallback model even if transformers are available

## Output files

- `history.json` — JSON list of agent actions and results created by `example.py`.
- `agent_notes.txt` — (created by the agent) when the agent writes search results to disk.

## Safety & limitations

- The `RUN` tool executes Python in a subprocess and applies basic resource limits on POSIX systems; it is NOT a secure sandbox and should not be used to run untrusted code.
- The fallback model is deterministic and intentionally simple so the project can run without heavy ML dependencies; it is not a replacement for a real language model.
- The agent performs internet calls (wikipedia). Disable or modify `Tools.wiki_search` if you need offline operation.
