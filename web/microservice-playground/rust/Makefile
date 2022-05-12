.PHONY: build build_release run test

build:
	cargo build

build_release:
	cargo build --release
	# TODO needs to actually work
	# https://alexbrand.dev/post/how-to-package-rust-applications-into-minimal-docker-containers/
	docker build -t rust-microservice .

run:
	fd .rs | entr -r cargo run

test:
	http :8080/hellea
