.PHONY: all test

all: .venv/Lib/site-packages

ifeq ($(OS), Windows_NT)
activate=.venv/Scripts/activate
else
activate=.venv/bin/activate
endif

.venv/Lib/site-packages: requirements.txt dev-requirements.txt .venv
	. $(activate) && pip install -r requirements.txt -r dev-requirements.txt

.venv:
	virtualenv .venv

test: .venv/Lib/site-packages
	. $(activate) && tox
