LINUX_BUILD_DIR = builds/linux

# "run" and "build" commands need to be run in a virtualenv

run:
	python -m kivy_app

build_linux:
	pyinstaller --workpath $(LINUX_BUILD_DIR)/build \
		--distpath $(LINUX_BUILD_DIR)/dist \
		-y $(LINUX_BUILD_DIR)/kivy_app.spec

# linux build looks to be working on mac as well
build_macos: build_linux

clean:
	rm -rf $(LINUX_BUILD_DIR)/build
	rm -rf $(LINUX_BUILD_DIR)/dist
