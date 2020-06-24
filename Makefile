.PHONY: default test deploy-docs build

export POETRY_VIRTUALENVS_IN_PROJECT=true

default: .venv build

.venv: pyproject.toml poetry.lock
	poetry install
	touch .venv

test: .venv
	poetry run coverage erase
	poetry run tox

docs: docs/* docs/_build/html/.git
	$(MAKE) -C docs html

deploy-docs:
	cd docs/_build/html ; git add --all && git commit -m 'docs: build' && git push

docs/_build/html/.git:
	git worktree add -f --checkout docs/_build/html gh-pages

build:
	poetry build
