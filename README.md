# EateryAI

CS 180A/B Capstone Project

- Elisha Nguyen
- Tyler Nguyen
- Abdullah Alfuraih
- Nicholas Huang
- Samuel Lee

## Prerequisites

- Python 3.11
- Node.js and npm
- PostgreSQL (if running with a local database)

## Environment Variables

### Backend (`backend/.env`)

Create a `.env` file in the backend directory:

```env
# Database Configuration
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# JWT Secret
SECRET_KEY=

# LLM Key
GEMINI_API_KEY=
```

### Frontend (`frontend/.env`)

Create a `.env` file in the frontend directory:

```env
# Backend API URL
EXPO_PUBLIC_API_URL=
```

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

### Option 1: Automatic Setup (Makefile)

```bash
make run
```

### Option 2: Manual Setup (Windows)

Create a virtual environment:

```bash
py -3.11 -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
cd src
..\venv\Scripts\fastapi.exe dev main.py --host 0.0.0.0 --port 8000
```

### Option 3: Manual Setup (macOS/Linux)

Create a virtual environment:

```bash
python3.11 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
cd src
../venv/bin/fastapi dev main.py --host 0.0.0.0 --port 8000
```

---

## Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Expo:

```bash
npx expo start
```

---

## Running on a Physical Device

If using Expo Go on a phone:

1. Start the backend with:

```bash
fastapi dev main.py --host 0.0.0.0 --port 8000
```

2. Set `EXPO_PUBLIC_API_URL` to your computer's local IP address:

```env
EXPO_PUBLIC_API_URL=http://192.168.x.x:8000
```

3. Ensure your phone and computer are connected to the same network.