PYTHON ?= python3

.PHONY: test
test:
	$(PYTHON) -m unittest -v test_*.py

.PHONY: e2e-test
e2e-test:
	$(PYTHON) sorting_hat.py sample_input.yaml
	$(PYTHON) sorting_hat.py --algorithm annealing sample_input.yaml
