.PHONY: npm-build
npm-build:
	npm run build

.PHONY: poetry-build
poetry-build:
	cz changelog && poetry build
