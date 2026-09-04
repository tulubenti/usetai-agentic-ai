# usetai-agentic-ai

Demo-focused Agentic AI project with **open-source/free defaults**. It is structured for local demos, rapid onboarding, and low-cost experimentation.

## Project overview

This repository demonstrates an end-to-end agent loop:
1. User query intake
2. Planner/provider picks next step
3. Tool invocation
4. Final response synthesis

Default behavior uses a deterministic offline planner (`heuristic`) so demos run without paid APIs.

## Architecture

```text
src/usetai_agentic_ai/
  agents/        # demo agent orchestration
  providers/     # planner provider abstraction (heuristic, ollama, hf_inference)
  tools/         # docs retrieval + web summary tools
  workflows/     # explicit reasoning/planning loop
  memory/        # run history persistence
  utils/         # shared utilities
examples/        # runnable demo scripts
docs/            # walkthrough docs
scripts/         # helper scripts
tests/           # unit tests
```

## Quickstart (5-minute local demo)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
python -m usetai_agentic_ai.cli --task docs_qa --query "How do I run this demo project locally?"
```

## Demo tasks

### 1) Retrieval QA over local docs

```bash
python -m usetai_agentic_ai.cli --task docs_qa --query "What are the default providers?"
```

### 2) Topic/web brief with offline fallback

```bash
python -m usetai_agentic_ai.cli --task topic_brief --query "autonomous agents"
```

## Provider options (open-source first)

- `heuristic` (default): deterministic, offline, free.
- `ollama` (optional): local OSS model runtime (`USETAI_PROVIDER=ollama`).
- `hf_inference` (optional): token-gated (`USETAI_PROVIDER=hf_inference` + `USETAI_HF_API_TOKEN`).

## Configuration

Use `.env.example` and set only needed values. Main flags:
- `USETAI_PROVIDER`
- `USETAI_ENABLE_DOCS_TOOL`
- `USETAI_ENABLE_WEB_TOOL`
- `USETAI_DOCS_PATHS`

## Developer experience

```bash
make setup
make lint
make test
make demo
```

If your environment does not have `make` (common on Windows), use the equivalent commands below.

Without `make`, run:

```bash
pip install -e .[dev]
ruff check .
pytest -q
python -m usetai_agentic_ai.cli --task docs_qa --query "How do I run this demo project locally?"
```

## Troubleshooting

- If imports fail, ensure editable runtime install ran: `pip install -e .`
- If `ollama` provider fails, check local runtime and model availability.
- If web calls are blocked/offline, `topic_brief` uses fallback text.

## Backward compatibility

Legacy `agent.py` and `example.py` remain as compatibility entrypoints.
