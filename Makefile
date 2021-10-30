install:
	@poetry install
	@poetry run pre-commit install

reformat:
	@poetry run black .
	@poetry run isort .

lint:
	@poetry run flakehell lint . --count
	@poetry run mypy .

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +