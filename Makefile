## Commands to ease development

cephalon: # Run main cephalon module
	python -m src.cephalon

webui: # Run nicegui web UI
	python -m src.ui.ui

mainui: # Run tkinter main UI
	python -m src.main_ui

build: # Install python dependencies 🐍
	pip install -r requirements/requirements.txt

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done