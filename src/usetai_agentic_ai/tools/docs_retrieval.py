from __future__ import annotations

import re
from pathlib import Path


class DocsRetrievalTool:
    name = "docs_retrieval"

    def __init__(self, paths: list[str]):
        self.paths = paths

    def _iter_documents(self) -> list[tuple[str, str]]:
        docs: list[tuple[str, str]] = []
        for base in self.paths:
            p = Path(base)
            if p.is_file():
                docs.append((str(p), p.read_text(encoding="utf-8", errors="ignore")))
            elif p.is_dir():
                for fp in p.rglob("*.md"):
                    docs.append((str(fp), fp.read_text(encoding="utf-8", errors="ignore")))
                for fp in p.rglob("*.txt"):
                    docs.append((str(fp), fp.read_text(encoding="utf-8", errors="ignore")))
        return docs

    @staticmethod
    def _score(query: str, text: str) -> int:
        words = [w for w in re.findall(r"[a-zA-Z0-9_]+", query.lower()) if len(w) > 2]
        lowered = text.lower()
        return sum(lowered.count(w) for w in words)

    def run(self, query: str) -> str:
        documents = self._iter_documents()
        if not documents:
            return "No local documents found to retrieve from."
        ranked = sorted(documents, key=lambda item: self._score(query, item[1]), reverse=True)
        top_path, top_text = ranked[0]
        excerpt = top_text.strip().replace("\n", " ")[:1200]
        return f"Top local source: {top_path}\nExcerpt: {excerpt}"
