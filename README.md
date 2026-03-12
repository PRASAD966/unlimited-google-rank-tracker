# 🚀 RankPlex — Google Rank Tracker

> **Track your website's Google search rankings across any keyword, location, and country — automatically, accurately, and at scale.**

RankPlex is a full-stack SaaS web application that uses headless browser automation (Playwright + Brave) with rotating residential proxies to check real Google search rankings. It features a multi-user dashboard, real-time live progress via WebSockets, credit-based billing, Excel exports, and full Docker/production deployment support.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Rank Checking** | Checks Google rankings for unlimited keywords across up to 10 pages (100 results) |
| 🌍 **Multi-Country / Location** | Supports 20+ countries with correct Google domain, locale, timezone, and geolocation emulation |
| 🔄 **Proxy Rotation** | Integrates Smartproxy / DataImpulse rotating proxies to bypass CAPTCHAs and rate limits |
| 👤 **Human Behavior Simulation** | Random mouse movements, scrolling, and randomized delays to mimic real users |
| 📊 **Real-time Dashboard** | Live progress updates via Socket.IO — watch each keyword being checked in real time |
| 📁 **Project Management** | Organize rank checks into projects, view history, compare rankings |
| 📥 **Excel Export** | Download results as formatted `.xlsx` reports |
| 🔐 **Auth System** | Email/password signup with email verification + Google OAuth login |
| 💳 **Credits System** | Per-user credit limits with in-app purchase flow |
| 🐳 **Docker Ready** | One-command deployment via Docker Compose |
| 🔔 **Live Notifications** | In-app real-time notifications for task events |
| ⚡ **Concurrent Execution** | Up to 20–40 simultaneous rank-check workers (configurable) |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask, Flask-SocketIO (threading mode) |
| **Browser Automation** | Playwright (sync API) + Brave Browser |
| **Frontend** | HTML5, CSS3, Vanilla JS + Socket.IO client |
| **Database** | SQLite (development) / MySQL (production) |
| **Auth** | Authlib (Google OAuth 2.0) + Email/Password |
| **Proxy** | Smartproxy / DataImpulse rotating residential proxies |
| **Deployment** | Gunicorn + Xvfb (Linux), Docker, Docker Compose |
| **Email** | Gmail SMTP (verification & password reset) |

---

## 📁 Project Structure

```
rankplex/
├── server.py              # Main Flask app + all API routes + Playwright worker logic
├── database.py            # DB abstraction layer (SQLite ↔ MySQL)
├── demo.py                # Alternative/demo version of the server
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose (app + network config)
├── start.sh               # Production startup script (Xvfb + Gunicorn)
├── .env                   # Environment variables (not committed)
│
├── index.html             # Landing page
├── dashboard.html         # Main user dashboard
├── rank-check.html        # Rank check UI (live results)
├── history.html           # Historical results viewer
├── projects.html          # Project management
├── settings.html          # User settings & profile
├── payment.html           # Credits / billing page
├── sign-in.html           # Login page
├── sign-up.html           # Registration page
│
├── css/                   # Global stylesheets
├── js/                    # Frontend JavaScript
├── images/                # Static images & favicon
└── static/                # Other static assets
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root (never commit this to Git):

```env
# Browser
BRAVE_PATH=/usr/bin/brave-browser
EXTENSION_PATH=/app/extensions/raptor_unpacked

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Email (Gmail SMTP)
EMAIL_ADDRESS=your@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

# Proxy (Smartproxy / DataImpulse / any HTTP proxy)
PROXY_SERVER=proxy.smartproxy.net
PROXY_PORT=3120
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password

# Database (production MySQL)
DB_HOST=localhost
DB_USER=rankplexuser
DB_PASS=yourpassword
DB_NAME=rankplexdb
DB_TYPE=mysql  # or "sqlite" for local dev

# App
FLASK_ENV=production     # or development
MAX_CONCURRENT_TASKS=20  # Number of parallel browser workers
```

> **Note:** For development, `DB_TYPE` defaults to `sqlite` — no MySQL setup needed.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js (optional, for frontend tooling)
- Brave Browser (local dev on Windows/Mac)
- MySQL (production) or SQLite (development, zero config)

### Local Development (Windows / Mac)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/rankplex.git
cd rankplex

# 2. Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Copy and configure environment variables
cp .env.example .env
# Edit .env with your values

# 6. Run the development server
python server.py --port 8000
```

Visit `http://localhost:8000` in your browser.

---

## 🐳 Docker Deployment (Production)

### Quick Start

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f
```

The app will be available on port `8000`.

### Manual Linux Server Deployment (without Docker)

```bash
# 1. Set FLASK_ENV
export FLASK_ENV=production

# 2. Run the startup script (starts Xvfb + Gunicorn)
bash start.sh
```

The `start.sh` script:
- Starts **Xvfb** virtual display on `:99` (required for headless Playwright on Linux)
- Launches **Gunicorn** with `gthread` worker class (required for Playwright threading compatibility)
- Runs with 1 worker + 50 threads (SocketIO state is in-process)

> ⚠️ **Important:** Do NOT use `gevent` or `eventlet` workers — they are incompatible with Playwright's synchronous API. Always use `--worker-class gthread`.

---

## 📡 API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Landing page |
| `POST` | `/api/register` | Register new user |
| `POST` | `/api/login` | Login with email/password |
| `GET` | `/auth/google` | Google OAuth login |
| `POST` | `/api/start-rank-check` | Start a new rank check run |
| `POST` | `/api/cancel-run` | Cancel an active run |
| `GET` | `/api/run-status/<run_id>` | Get run status |
| `GET` | `/api/results/<run_id>` | Get rank results |
| `GET` | `/api/download/<run_id>` | Download Excel report |
| `POST` | `/api/buy-credits` | Add credits to account |
| `GET` | `/api/my-runs` | List all user's runs |

**WebSocket Events (Socket.IO):**

| Event | Direction | Description |
|---|---|---|
| `connect` | Client → Server | Establish connection |
| `progress_update` | Server → Client | Live keyword progress |
| `task_complete` | Server → Client | Run finished |
| `new_notification` | Server → Client | In-app notification |

---

## 🌍 Supported Countries

US, UK, Australia, India, Canada, Germany, France, Japan, Brazil, Indonesia, Italy, Mexico, Netherlands, Spain, Turkey, Sweden, UAE, Saudi Arabia, Singapore, and more.

---

## 🔒 Security Notes

- Keep `.env` out of version control — add it to `.gitignore`
- Change `app.secret_key` to a strong random value in production
- Use environment variables for all secrets (never hardcode)
- The `ProxyFix` middleware is enabled in production for correct HTTPS URL generation behind reverse proxies (Nginx/Caddy)

---

## 🧰 Useful Scripts

| Script | Purpose |
|---|---|
| `check_credits.py` | CLI to check user credit balances |
| `verify_db.py` | Verify database integrity |
| `recover_db.py` | Recover corrupted DB entries |
| `quick_proxy_test.py` | Test proxy connectivity |
| `diagnose_geo.py` | Diagnose geolocation emulation |
| `migrate_db.py` | Run DB migrations |

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 👤 Author

Built by [Nice Digitals](mailto:prasadnaik2572@gmail.com)

> Deployed at **[rankplex.cloud](https://rankplex.cloud)**
