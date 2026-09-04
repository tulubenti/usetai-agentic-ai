from pathlib import Path

from usetai_agentic_ai.agents.legacy import Agent, Tools


def _should_not_call(*args, **kwargs):  # noqa: ANN002,ANN003,ARG001
    raise RuntimeError("should not call")


def test_legacy_agent_creates_notes_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Tools, "wiki_search", lambda query, sentences=2: "FAKE SUMMARY")  # noqa: ARG005

    agent = Agent(goal="autonomous agents", max_steps=3)
    history = agent.run()

    notes_file = tmp_path / "agent_notes.txt"
    assert notes_file.exists()
    assert notes_file.read_text(encoding="utf-8") == "FAKE SUMMARY"
    assert history[0]["action"].startswith("SEARCH:")
    assert history[1]["result"] == "WROTE: agent_notes.txt"


def test_legacy_agent_force_fallback_avoids_network(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Tools, "wiki_search", _should_not_call)

    history = Agent(goal="autonomous agents", force_fallback=True).run()

    assert "FALLBACK SUMMARY" in history[0]["result"]


def test_legacy_agent_hf_without_token_falls_back(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Tools, "wiki_search", _should_not_call)

    history = Agent(goal="autonomous agents", use_hf_api=True, hf_token=None).run()

    assert "FALLBACK SUMMARY" in history[0]["result"]
