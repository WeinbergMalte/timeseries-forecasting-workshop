.PHONY: .ALWAYS
.ALWAYS:

.DEFAULT_GOAL := help

help:  ## Print all targets
	@echo "\033[1mUsage:\033[0m make <target>"
	@echo "\033[1mAvailable targets\033[0m"
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}' | egrep -v '^[^#]+/' | sort; true

black: .ALWAYS ## Runs black formatting
	poetry run black .

cleanup: .ALWAYS ## Removes .ipynb_checkpoint, .pytest_cache, and __pycache__ folders and .coverage files
	find . -type d -name '.ipynb_checkpoints' -exec rm -r {} +
	find . -type d -name '.pytest_cache' -exec rm -r {} +
	find . -type d -name '*pycache*' -exec rm -r {} +
	find . -type d -name '.mypy_cache' -exec rm -r {} +
	find . -type f -name '.coverage' -exec rm -r {} +
	find . -type f -name '.coverage.*' -exec rm -r {} +

format: .ALWAYS ## Runs isort and black formatting
	poetry run isort .
	poetry run black .

mypy: .ALWAYS ## Runs mypy
	poetry run mypy . --ignore-missing-imports

pytest: .ALWAYS ## Runs pytest
	poetry run pytest

