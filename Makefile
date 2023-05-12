# Conda-related paths
conda_env_dir ?= ./env
env_file := environment-dev.yml

# Command aliases
conda_exe ?= conda
conda_run := $(conda_exe) run --prefix $(conda_env_dir) --no-capture-output

help:  ## Display help on all Makefile targets
	@@grep -h '^[a-zA-Z]' $(MAKEFILE_LIST) | awk -F ':.*?## ' 'NF==2 {printf "   %-20s%s\n", $$1, $$2}' | sort

setup:  ## Setup local dev conda environment
	$(conda_exe) env $(shell [ -d $(conda_env_dir) ] && echo update || echo create) -p $(conda_env_dir) --file $(env_file)

test:  ## Run all the unit tests
	$(conda_run) pytest

tox:  ## Run tox to test in isolated environments
	$(conda_run) tox

clean:  ## Clean up cache and temporary files
	find . -name \*.py[cod] -delete
	rm -rf .pytest_cache .mypy_cache .tox build dist

clean-all: clean  ## Clean up, including build files and conda environment
	find . -name \*.egg-info -delete
	rm -rf $(conda_env_dir)

.PHONY: $(MAKECMDGOALS)
