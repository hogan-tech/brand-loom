.PHONY: lint test eval-parity

lint:
	python -m ruff check .

test:
	python -m pytest tests/ -v

eval-parity:
	python scripts/eval_parity.py
