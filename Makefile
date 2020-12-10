.PHONY: default test deploy-docs build

export POETRY_VIRTUALENVS_IN_PROJECT=true

default: .venv build

.venv:
	virtualenv .venv

test: .venv/lib/site-packages/.make.sentinel
	. ./scripts/activate-venv.sh &&\
		coverage erase &&\
		tox

docs: docs/* docs/_build/html/.git
	$(MAKE) -C docs html

deploy-docs:
	cd docs/_build/html ; git add --all && git commit -m 'docs: build' && git push

docs/_build/html/.git:
	git worktree add -f --checkout docs/_build/html gh-pages

.venv/lib/site-packages/.make.sentinel: .venv dev-requirements.txt
	. ./scripts/activate-venv.sh &&\
		python -m pip install -U -r dev-requirements.txt
	touch .venv/lib/site-packages/.make.sentinel

build: .venv/lib/site-packages/.make.sentinel
	. ./scripts/activate-venv.sh &&\
		python ./setup.py build bdist_wheel
	# https://github.com/pypa/setuptools/issues/1871
	rm -rf build/lib
