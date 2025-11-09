setup: # setup the environment with poetry
	pip install pipx
	pipx install poetry>=2
	poetry install
	poetry run pre-commit install
	poetry env activate

test:
	poetry run pytest --cov --cov-config=pyproject.toml --cov-report=html tests/
