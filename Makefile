PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

all: run

install:
	pip install build mypy flake8 --break-system-packages
	$(PYTHON) -m build
	pip install dist/mazegen-1.0.0-py3-none-any.whl --break-system-packages

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name build -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

.PHONY: all install run debug lint lint-strict clean