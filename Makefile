lint:
	ruff format --check .
	ruff check .

format:
	ruff check --select F401 --select TID252 --select I --fix .
	ruff format .

test:
	python -m unittest tests

test-coverage:
	coverage python -m unittest tests

clean:
	rm -rf dist/
	rm -rf .ruff_cache
	rm -f .coverage
