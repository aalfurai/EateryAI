# EateryAI
[Demo Video](#demo-video) | [Deployment Status](#deployment-status) | [Dependencies](#dependencies) | [Prerequisites](#prerequisites) | [Environment Variables](#environment-variables) | [Backend Setup](#backend-setup) | [Frontend Setup](#frontend-setup) | [Physical Device](#running-on-a-physical-device) | [Testing](#testing) | [Known Limitations](#known-limitations)

### CS 180A/B Capstone Project

Pursuing goal-oriented meals is inconvenient and difficult when eating out. Other apps track nutrition and financial goals, but require tedious manual data entry. **EateryAI** solves this by providing goal-based meal recommendations and automatic nutrition tracking directly tied to restaurant menus. The centerpiece feature, the **EatAI Mealbuilder**, lets users interactively plan meals before ordering - delivering personalized, goal-aligned suggestions through a conversational AI experience.

### Team Members

- Elisha Nguyen
- Tyler Nguyen
- Abdullah Alfuraih
- Nicholas Huang
- Samuel Lee

---

## Demo Video
[![Demo Video](https://lh3.googleusercontent.com/rd-d/ALs6j_GGlHgOzrZEybSBHebCSJYE1hetWt1wep94MlaJndv8Hkmubw5nfDRCYNuv1QYsQlAw4cNIyLUNVXHpSDkjTiSWZhgDVlL4Fs6AF0MQKo3K7yeKRhhwW-g5L6XivW0QtSTM_xqqKAbG_kLCkxQdaeX6ieEnspMZBjvLoj_opkJOzGrGhD1WZ4AN4ykL3Wjjus5an5bR8lwjlGWSpjReAtjOZDhu99lEE8sguQv5kgAFcrBQCqotjeSB4pqbqAEUa4bp7ltfPmLtdMc353mhcqpp6aPky4UR8hPDfbretsNj9ke7jrOtXPGk5caqNdMkzhZbSFLqnxERR14q_hQGkA2O3MhJn7fcmeSqen5ccrjhDY3UAggwWETj_mT6u0Yoje2lmBFVRao-23moxsiYOUQWWwqom7HHa2368oYUfIfN5mHfunp3f0IvXHu1_w9rMY37h3oizZRke_U92Xab7TJyrCbhR-HWHKA-CzciutC519B8U2C32fYfEmgpel0OhDPzk6Cf7IlD9o1xRDTM2FUJs8pnVmPbzC26CjAZwpJyPRGjjNXAMqsalruLe7RC_n--3TJA_Q7AOsJ6RNQ1P4oZv_02E1Ker5C82Y7hJUojbtOUXEpmLJaWQeQq9bri7urqqfv3bcez-t-Gla-LQ-yyk165ZUOyt2Ff03UHn0yoY8GSjuZ6pBW0wahxsgGsqyNoxkOHUj0o6n12XSLkdngHb7lhT34ciCNSmiK4us4Omqb8xJAsADVi3MQ-nPHEaezeMZFtK2KRlmSf71d8re9MzMD62OM3yJ8865riGV-uRAiPOvjypTlPgaYPJSDVQLxoPGMtPZYXU4j9rlgplH3Xy4OeYi2PpgP-lSmfoYNqsEubqk8qoUbjcv7Kw9X_ikf0fp882hJ2zXpJYRs9dCW6HnghUlWu73T_JD17pUFyNrULTB89KT4EPcn_Gwo52PRnsOE5QjViol265bYU-vOGp9TcLYodc0RNk95dDx6Y37tXhLI44E0RnK_ZX9rFNrq1DDW7i6-B9dw8SXQhm-NCeaalIvhVEMmmdXI0sTr-dGXJSB6KH-uFBuHs1tjtAubltjFfMHkFLKZ0PNazxqFvLldDIfUcKK7-HMy0sE5taSMU4WE5_FxhGY-H_84y_JU1QG17rmurUWKLgb5ooltsNzfZ-des=k)](https://drive.google.com/file/d/1ObkiRD5jrZezDe8r0b6o4XEKHTX-mdXm/view)

---

## Deployment Status

| Component | Status |
|-----------|--------|
| Backend | Deployed on [Render](https://render.com) (free tier - cold starts may cause a ~30s delay on first request) |
| Database | Render-managed PostgreSQL |
| Frontend | Local only - demoed via **Expo Go** using a tunnel or local network connection |

> **Note:** The Expo frontend is not deployed to an app store and can only run on a physical device or emulator via Expo Go.

---

## Dependencies

### Backend

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Runtime |
| `fastapi[standard]` | latest | Web framework + Uvicorn server |
| `psycopg2-binary` | latest | PostgreSQL driver |
| `pydantic` | latest | Data validation and settings |
| `python-dotenv` | latest | `.env` file loading |
| `PyJWT` | latest | JWT auth token encoding/decoding |
| `google-genai` | latest | Gemini LLM integration |
| `pandas` | latest | Data manipulation |
| `numpy` | 1.26.4 | Numerical computing (pinned for compatibility) |
| `pytest` | latest | Test runner |
 
> Full list in `backend/requirements.txt`.

### Frontend

| Dependency | Version | Purpose |
|------------|---------|---------|
| Node.js | 18+ | Runtime |
| TypeScript | ~5.9.2 | Type checking |
| `expo` | ~54.0.33 | Expo SDK / React Native framework |
| `expo-router` | ~6.0.23 | File-based navigation |
| `react` / `react-native` | 19.1.0 / 0.81.5 | UI framework |
| `react-native-web` | ^0.21.0 | Web target support |
| `expo-linear-gradient` | ~15.0.8 | Gradient UI components |
| `expo-font` | ~14.0.12 | Custom font loading |
| `expo-linking` | ~8.0.12 | Deep linking |
| `expo-constants` | ~18.0.13 | App config and device constants |
| `expo-status-bar` | ~3.0.9 | Status bar control |
| `@expo/vector-icons` | ^15.0.3 | Icon library |
| `@react-native-community/slider` | 5.0.1 | Slider input component |
| `react-native-svg` | 15.12.1 | SVG rendering |
| `react-native-screens` | ~4.16.0 | Native screen management |
| `react-native-safe-area-context` | ~5.6.0 | Safe area insets |
 
> Full list in `frontend/package.json`.

---

## Prerequisites

- Python 3.11
- Node.js 18+ and npm
- PostgreSQL (only required for local database; production uses Render-managed PostgreSQL)
- Expo Go app installed on your mobile device (for physical device testing)

---

## Environment Variables

### Backend (`backend/.env`)

Create a `.env` file in the `backend/` directory:

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

> For local development, fill in your local PostgreSQL credentials.  
> For production, use the **external** connection string values from your Render PostgreSQL dashboard.

### Frontend (`frontend/.env`)

Create a `.env` file in the `frontend/` directory:

```env
# Backend API URL
EXPO_PUBLIC_API_URL=
```

> Set this to your Render backend URL for production, or your machine's local IP for local development (see Running on a Physical Device below).

---

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

Create and activate a virtual environment:

```bash
py -3.11 -m venv venv
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

Create and activate a virtual environment:

```bash
python3.11 -m venv venv
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

If using **Expo Go** on a phone over your local network:

1. Start the backend:

```bash
fastapi dev main.py --host 0.0.0.0 --port 8000
```

2. Set `EXPO_PUBLIC_API_URL` in `frontend/.env` to your machine's local IP:

```env
EXPO_PUBLIC_API_URL=http://192.168.x.x:8000
```

3. Ensure your phone and computer are on the **same Wi-Fi network**.

4. Scan the QR code shown by `npx expo start` using Expo Go.

If your network blocks device-to-device traffic (e.g., a university network), use the tunnel option:

```bash
npx expo start --tunnel
```

> Tunnel mode requires a configured ngrok auth token. If you hit a `CommandError: TypeError [ERR_INVALID_ARG_TYPE]`, pin the ngrok package and clear the cache:
> ```bash
> npm install @expo/ngrok@^4.1.0
> npx expo start --tunnel --clear
> ```

---

## Testing

Currently, the project does not have an automated test suite. Manual testing is performed by:

1. Starting the backend and confirming the API responds at `http://localhost:8000/docs` (FastAPI auto-generated Swagger UI).
2. Running the Expo frontend and exercising each screen manually.
3. Verifying database reads/writes via the Swagger UI or a PostgreSQL client (pgAdmin).

---

## Known Limitations

- **No automated tests** - the project lacks unit and integration test coverage. All QA is manual.
- **Render free-tier cold starts** - the backend spins down after inactivity; the first request after idle may take up to 30 seconds.
- **Frontend not published to app stores** - the Expo app must be run via Expo Go and cannot be installed as a standalone app without an Expo/EAS build.
- **Tunnel instability** - `npx expo start --tunnel` can be unreliable depending on network conditions. Local IP mode is preferred when possible.
- **Limited restaurant coverage** - menu and nutrition data is scoped to a subset of restaurants populated during development. Real-time menu fetching is not implemented.
- **No offline support** - the app requires an active internet connection to communicate with the backend.
- **Single-user session model** - JWT tokens are not refreshed automatically; sessions expire and require re-login.