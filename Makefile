VENV = venv
PYTHON = $(VENV)/Scripts/python
PIP = $(VENV)/Scripts/pip

.PHONY: setup run

setup: $(VENV)/Scripts/activate
	$(PIP) install -r requirements.txt
	$(PYTHON) src/solver/setup.py
	@echo "Ready."

$(VENV)/Scripts/activate:
	python -m venv $(VENV)

run: kill setup
	cd src && ../$(VENV)/Scripts/uvicorn main:app --reload

kill:
	-taskkill /F /IM uvicorn.exe