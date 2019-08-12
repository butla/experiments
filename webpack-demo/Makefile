.PHONY: build start

build:
	npx webpack --mode=production
	cp dist/main.js .

start: build
	chromium-browser index.html
