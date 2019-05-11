.PHONY: start

UID=$(shell id -u)

# TODO activate virtualenv if not running
start:
	adev runserver --app-factory create_app app/app.py

call:
	bash call_app.sh

call-tmux:
	tmux -S /tmp/tmux-$(UID)/default split-window -v "bash call_app.sh"
	tmux -S /tmp/tmux-$(UID)/default split-window -h "bash call_app.sh"
	tmux -S /tmp/tmux-$(UID)/default split-window -v "bash call_app.sh"
	tmux -S /tmp/tmux-$(UID)/default split-window -h "bash call_app.sh"
	bash call_app.sh
