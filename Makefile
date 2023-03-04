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
lint: lint-python lint-rtd-requirements

.PHONY: lint-python lint-rtd-requirements
lint-python lint-rtd-requirements:
	./$@.sh

.PHONY: lint-mypy
lint-mypy:
	mypy -p sphinxcontrib

.PHONY: rtd-requirements
rtd-requirements:
	poetry export --without-hashes --with dev -f requirements.txt > docs/requirements.txt
