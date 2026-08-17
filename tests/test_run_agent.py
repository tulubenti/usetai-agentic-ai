import json
from agent import Tools, Agent


def test_agent_writes_history_and_notes(tmp_path, monkeypatch):
    # Run inside a temporary directory to avoid touching repo files
    monkeypatch.chdir(tmp_path)

    # Replace the wiki search with a deterministic short summary (no network)
    monkeypatch.setattr(Tools, "wiki_search", lambda query, sentences=2: "FAKE SUMMARY: autonomous agents are ...")

    # Create agent forcing fallback so no heavy models are required
    agent = Agent(
        goal="Gather a short summary about autonomous agents and save it to agent_notes.txt",
        max_steps=6,
        force_fallback=True
    )

    history = agent.run()

    # Write history.json as example.py would
    hist_file = tmp_path / "history.json"
    hist_file.write_text(json.dumps(history, indent=2), encoding="utf-8")

    notes_file = tmp_path / "agent_notes.txt"

    assert hist_file.exists(), "history.json should be created"
    assert notes_file.exists(), "agent_notes.txt should be created"

    notes = notes_file.read_text(encoding="utf-8")
    assert "FAKE SUMMARY" in notes
