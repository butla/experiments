.PHONY: build start

build:
	npx webpack --mode=development

build-prod:
	npx webpack --mode=production

start: build
	chromium-browser index.html
