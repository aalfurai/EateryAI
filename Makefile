VENV = venv
PYTHON311 := $(shell py -3.11 -c "import sys; print(sys.executable)" 2>/dev/null || python3.11 -c "import sys; print(sys.executable)" 2>/dev/null || python3 -c "import sys; print(sys.executable)" 2>/dev/null)

UNAME := $(shell uname -s)

ifeq ($(findstring MINGW, $(UNAME)), MINGW)
    VENV_BIN = $(VENV)/Scripts
else ifeq ($(findstring MSYS, $(UNAME)), MSYS)
    VENV_BIN = $(VENV)/Scripts
else ifeq ($(findstring CYGWIN, $(UNAME)), CYGWIN)
    VENV_BIN = $(VENV)/Scripts
else
    VENV_BIN = $(VENV)/bin
endif

PYTHON = $(VENV_BIN)/python
PIP = $(VENV_BIN)/python -m pip
UVICORN = $(VENV_BIN)/uvicorn

.PHONY: setup run kill fresh

run: kill $(VENV_BIN)/fastapi
	cd src && ../$(VENV_BIN)/fastapi dev main.py --host 0.0.0.0 --port 8000

$(VENV_BIN)/fastapi: requirements.txt
	@[ -d $(VENV) ] || "$(PYTHON311)" -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@echo "Ready."

setup: $(VENV_BIN)/fastapi

kill:
	-taskkill /F /IM uvicorn.exe || true

fresh:
	rm -rf $(VENV)
	$(MAKE) setup