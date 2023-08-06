# simple makefile to simplify repetetive build env management tasks under posix

# caution: testing won't work on windows, see README

PYTHON ?= python
PYTESTS ?= pytest

all: clean inplace test

clean-pyc:
	find . -name "*.pyc" | xargs rm -f

clean-so:
	find . -name "*.so" | xargs rm -f
	find . -name "*.pyd" | xargs rm -f

clean-build:
	rm -rf _build

clean-ctags:
	rm -f tags

clean-cache:
	find . -name "__pycache__" | xargs rm -rf

clean: clean-build clean-pyc clean-so clean-ctags clean-cache

inplace:
	$(PYTHON) setup.py develop

test: inplace check-manifest
	rm -f .coverage
	$(PYTESTS) pd_parser

test-doc:
	$(PYTESTS) --doctest-modules --doctest-ignore-import-errors pd_parser

test-coverage:
	rm -rf coverage .coverage
	$(PYTESTS) --cov=anonymizer --cov-report html:coverage

trailing-spaces:
	find . -name "*.py" | xargs perl -pi -e 's/[ \t]*$$//'

upload-pipy:
	python setup.py sdist bdist_egg register upload

check-manifest:
	check-manifest --ignore .circleci/*,doc,.DS_Store

flake:
	@if command -v flake8 > /dev/null; then \
		echo "Running flake8"; \
		flake8 --count pd_parser pd_parser/tests; \
	else \
		echo "flake8 not found, please install it!"; \
		exit 1; \
	fi;
	@echo "flake8 passed"

pydocstyle:
	@echo "Running pydocstyle"
	@pydocstyle

pep:
	@$(MAKE) -k flake pydocstyle check-manifest

build-doc:
	cd docsrc; make clean
	cd docsrc; make html
