PYTHON ?= python3

.RECIPEPREFIX := >

.PHONY: install test validate analyze check

install:
> $(PYTHON) -m pip install -r requirements.txt

test:
> $(PYTHON) -m pytest -q

validate:
> $(PYTHON) -m compileall -q src benchmarks/scripts tests

analyze:
> $(PYTHON) -m src.analyze
> $(PYTHON) -m src.analyze_serverless
> $(PYTHON) -m src.sensitivity
> $(PYTHON) -m src.visualize
> $(PYTHON) -m src.report

check: validate test analyze
