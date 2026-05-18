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
pip install -r requirements.txt
cd src
fastapi dev main.py
```

### Maunal setup and run backend (Mac/Linux)
```bash
python3.11 -m venv venv
[source] venv/bin/activate
pip install -r requirements.txt
cd src
fastapi dev main.py
```

## Starting The Frontend
```bash
npm install
npx expo start
```