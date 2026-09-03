.PHONY: setup check test lint format manifest install-hooks protect-sources

setup:
	uv sync --all-groups

check: lint test

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run mypy

format:
	uv run ruff format .
	uv run ruff check --fix .

manifest:
	uv run python scripts/build_corpus_manifest.py

install-hooks:
	./scripts/install_git_hooks.sh

protect-sources:
	./scripts/protect_sources.sh

