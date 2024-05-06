lint:
	black --check .
	isort --check .
	ruff check .

format:
	black .
	isort .
	ruff check --fix .

test:
	pytest ./tests

clean:
	rm -rf dist/
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -f .coverage