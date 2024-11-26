VENV = books

ifeq ($(OS), Windows_NT)
	VENV_ACTIVATE = $(VENV)\\Scripts\\activate.bat
	VENV_ACTIVATE_COMMAND = call $(VENV_ACTIVATE)
else
	VENV_ACTIVATE = $(VENV)/bin/activate
	VENV_ACTIVATE_COMMAND = source $(VENV_ACTIVATE)
endif

$(VENV):
	python -m venv $(VENV)

install: $(VENV)
	$(VENV_ACTIVATE_COMMAND) && pip install -r requirements.txt

run: install
	$(VENV_ACTIVATE_COMMAND) && python -m app.app
