.PHONY: setup lint test demo format

setup:
	python -m pip install -e .[dev]

lint:
	ruff check .

format:
	ruff format .

test:
	pytest -q

demo:
	python -m usetai_agentic_ai.cli --task docs_qa --query "How do I run this demo project locally?"
