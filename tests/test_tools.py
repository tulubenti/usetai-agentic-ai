from pathlib import Path

from usetai_agentic_ai.tools.docs_retrieval import DocsRetrievalTool


def test_docs_retrieval_returns_top_source(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    file_a = docs_dir / "a.md"
    file_b = docs_dir / "b.md"
    file_a.write_text("agentic workflow has planning and tools", encoding="utf-8")
    file_b.write_text("unrelated content", encoding="utf-8")

    tool = DocsRetrievalTool(paths=[str(docs_dir)])
    result = tool.run("planning tools")

    assert "Top local source:" in result
    assert "a.md" in result
