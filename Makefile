.PHONY: .ALWAYS
.ALWAYS:

.DEFAULT_GOAL := help

help:  ## Print all targets
	@echo "\033[1mUsage:\033[0m make <target>"
	@echo "\033[1mAvailable targets\033[0m"
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}' | egrep -v '^[^#]+/' | sort; true

format: .ALWAYS ## Runs ruff formatting
	uv run ruff format .

cleanup: .ALWAYS ## Removes .ipynb_checkpoint, .pytest_cache, and __pycache__ folders and .coverage files
	find . -type d -name '.ipynb_checkpoints' -exec rm -r {} +
	find . -type d -name '.pytest_cache' -exec rm -r {} +
	find . -type d -name '*pycache*' -exec rm -r {} +
	find . -type d -name '.mypy_cache' -exec rm -r {} +
	find . -type f -name '.coverage' -exec rm -r {} +
	find . -type f -name '.coverage.*' -exec rm -r {} +

lint: .ALWAYS ## Runs ruff linting
	uv run ruff check .

check: .ALWAYS ## Runs ruff linting and formatting check
	uv run ruff check .
	uv run ruff format --check .

mypy: .ALWAYS ## Runs mypy
	uv run mypy . --ignore-missing-imports

pytest: .ALWAYS ## Runs pytest
	uv run pytest

