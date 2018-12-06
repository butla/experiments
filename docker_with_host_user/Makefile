.PHONY: build run clean

build:
	docker build --build-arg USER_ID=$(shell id -u) --build-arg GROUP_ID=$(shell id -g) -t sraka .

run:
	docker run -it -v $(shell pwd):/app sraka

clean:
	docker rmi sraka
