LINUX_BUILD_DIR = builds/linux

run:
	python -m kivy_app

build_linux:
	pyinstaller --workpath $(LINUX_BUILD_DIR)/build \
		--distpath $(LINUX_BUILD_DIR)/dist \
		-y $(LINUX_BUILD_DIR)/kivy_app.spec

clean:
	rm -rf $(LINUX_BUILD_DIR)/build
	rm -rf $(LINUX_BUILD_DIR)/dist
