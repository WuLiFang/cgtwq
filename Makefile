.PHONY: all test deploy-docs

all: .venv/Lib/site-packages/.make_success

ifeq ($(OS), Windows_NT)
activate=.venv/Scripts/activate
else
activate=.venv/bin/activate
endif

.venv/Lib/site-packages/.make_success: requirements.txt dev-requirements.txt .venv
	. $(activate) && pip install -r requirements.txt -r dev-requirements.txt
	echo > .venv/Lib/site-packages/.make_success

.venv:
	virtualenv .venv

test: .venv/Lib/site-packages/.make_success
	coverage erase
	. $(activate) && tox

docs: docs/* docs/_build/html/.git
	. $(activate) && $(MAKE) -C docs html

deploy-docs:
	cd docs/_build/html ; git add --all && git commit -m 'docs: build' && git push

docs/_build/html/.git:
	git worktree add -f --checkout docs/_build/html gh-pages
