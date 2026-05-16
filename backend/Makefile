VENV = venv
PYTHON311 := $(shell py -3.11 -c "import sys; print(sys.executable)" || python3.11 -c "import sys; print(sys.executable)" || python3 -c "import sys; print(sys.executable)")

$(shell [ -d $(VENV) ] || "$(PYTHON311)" -m venv $(VENV))

VENV_BIN := $(if $(wildcard $(VENV)/Scripts),$(VENV)/Scripts,$(VENV)/bin)
PIP = $(VENV_BIN)/python -m pip

.PHONY: run kill fresh

run: $(VENV_BIN)/fastapi
	-taskkill /F /IM uvicorn.exe 2>nul || true
	cd src && ../$(VENV_BIN)/fastapi dev main.py --host 0.0.0.0 --port 8000

$(VENV_BIN)/fastapi: .installed

.installed: requirements.txt
	$(PIP) install -r requirements.txt
	@touch .installed
	@echo "Ready."

fresh:
	rm -rf $(VENV) .installed
	$(MAKE) run