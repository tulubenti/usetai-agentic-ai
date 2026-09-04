# Demo walkthrough

## 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## 2) Demo task A: Retrieval QA over local docs

```bash
python -m usetai_agentic_ai.cli --task docs_qa --query "How do I run this demo project locally?"
```

Expected behavior:
- Step 1 calls `docs_retrieval`
- Step 2 synthesizes a final response from local project docs
- `history.json` is written

## 3) Demo task B: Topic/web brief (with offline fallback)

```bash
python -m usetai_agentic_ai.cli --task topic_brief --query "autonomous agents"
```

Expected behavior:
- Step 1 calls `web_summary`
- If online, uses Wikipedia summary
- If offline, returns deterministic fallback summary text

## 4) Optional provider switch

### Ollama (local OSS runtime)

```bash
USETAI_PROVIDER=ollama python -m usetai_agentic_ai.cli --task docs_qa --query "Summarize this repo"
```

### Hugging Face inference (optional token-gated)

```bash
USETAI_PROVIDER=hf_inference USETAI_HF_API_TOKEN=<token> python -m usetai_agentic_ai.cli --task topic_brief --query "agentic ai"
```
