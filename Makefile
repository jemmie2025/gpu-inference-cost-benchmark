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
> $(PYTHON) -m src.model_compatibility
> $(PYTHON) -m src.model_cost
> $(PYTHON) -m src.assumption_report
> $(PYTHON) -m src.pricing_normalization
> $(PYTHON) -m src.recommendations

check: validate analyze test
