build:
	uv build

clean:
	rm -rf *.egg-info
	rm -rf dist/
	rm -rf .ruff_cache
	rm -f .coverage

format:
	ruff check --select F401 --select TID252 --select I --fix .
	ruff format .

lint:
	ruff format --check .
	ruff check .

test:
	python -m unittest discover -s tests

test-coverage:
	coverage run -m unittest discover -s tests

