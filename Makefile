.PHONY: npm-build
npm-build:
	npm run build

.PHONY: poetry-build
poetry-build:
	cz changelog && poetry build

.PHONY: install-git-hooks
install-git-hooks:
	git config --local core.hooksPath 'git-hooks'

.PHONY: lint
lint: lint-python

.PHONY: lint-python
lint-python:
	./$@.sh

.PHONY: lint-mypy
lint-mypy:
	mypy -p sphinxcontrib

.PHONY: test
test:
	pytest
