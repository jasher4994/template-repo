.DEFAULT_GOAL := help
SHELL := /bin/bash
VENV := .venv
PY := $(VENV)/bin/python
UV := uv

.PHONY: help init install test lint format doctor clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

init: ## First-time setup: bootstrap template, venv, deps, .env, hooks
	@command -v $(UV) >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@test -f .env || (test -f .env.example && cp .env.example .env && echo "Created .env from .env.example") || true
	$(UV) venv --python 3.12 $(VENV)
	@if [ -d src/_pkg_placeholder ] || grep -q '{{PROJECT_SLUG}}' pyproject.toml 2>/dev/null; then \
		$(PY) scripts/bootstrap.py; \
	fi
	$(UV) pip install -e ".[dev]"
	$(PY) -m pre_commit install
	@echo ""
	@echo "✓ Ready. Activate with: source $(VENV)/bin/activate"

install: ## Install/sync dependencies (assumes venv exists)
	@command -v $(UV) >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@test -d $(VENV) || $(UV) venv --python 3.12 $(VENV)
	$(UV) pip install -e ".[dev]"

test: ## Run pytest
	$(PY) -m pytest

lint: ## Run ruff + mypy
	$(PY) -m ruff check .
	$(PY) -m mypy

format: ## Format code with ruff
	$(PY) -m ruff format .
	$(PY) -m ruff check --fix .

doctor: ## Validate repo conventions (skill names, frontmatter, plan/breadcrumb pairing)
	@python3 scripts/doctor.py
	@python3 -m pytest -c /dev/null -q tests/test_doctor.py

clean: ## Remove caches, build artefacts, and venv
	rm -rf $(VENV) .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
