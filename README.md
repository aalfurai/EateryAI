# EateryAI
180A project

## Starting The Backend

### Auto setup and run backend (Makefile)
```bash
make run
```

### Maunal setup and run backend (Windows)
```bash
py -3.11 -m venv venv
[source] venv/Scripts/activate
venv/Scripts/pip.exe install -r requirements.txt
cd src
../venv/Scripts/fastapi.exe dev main.py --host 0.0.0.0 --port 8000
```

### Maunal setup and run backend (Mac/Linux)
```bash
python3.11 -m venv venv
[source] venv/bin/activate
venv/bin/pip.exe install -r requirements.txt
cd src
../venv/bin/fastapi.exe dev main.py --host 0.0.0.0 --port 8000
```

## Starting The Frontend
```bash
npm install
npx expo start
```