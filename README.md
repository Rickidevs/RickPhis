<div align="center">

```
██████╗ ██╗ ██████╗██╗  ██╗██████╗ ██╗  ██╗██╗███████╗
██╔══██╗██║██╔════╝██║ ██╔╝██╔══██╗██║  ██║██║██╔════╝
██████╔╝██║██║     █████╔╝ ██████╔╝███████║██║███████╗
██╔══██╗██║██║     ██╔═██╗ ██╔═══╝ ██╔══██║██║╚════██║
██║  ██║██║╚██████╗██║  ██╗██║     ██║  ██║██║███████║
╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝
```

### Phishing Simulation Framework for Security Professionals

<br/>

[![Python](https://img.shields.io/badge/Python-3.8%2B-FFD43B?style=flat-square&logo=python&logoColor=white&labelColor=306998)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-white?style=flat-square&logo=flask&logoColor=white&labelColor=000000)](https://flask.palletsprojects.com)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.2-43B02A?style=flat-square&logo=selenium&logoColor=white)](https://selenium.dev)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-22.0.0-499848?style=flat-square&logo=gunicorn&logoColor=white)](https://gunicorn.org)
[![Stars](https://img.shields.io/github/stars/Rickidevs/RickPhis?style=flat-square&color=gold&label=⭐%20Stars)](https://github.com/Rickidevs/RickPhis/stargazers)
[![Forks](https://img.shields.io/github/forks/Rickidevs/RickPhis?style=flat-square&color=blue&label=🍴%20Forks)](https://github.com/Rickidevs/RickPhis/network/members)
[![Education Only](https://img.shields.io/badge/Use-Educational%20Only-red?style=flat-square)](/)

<br/>

*A lightweight, customizable phishing simulation tool built with Python, Flask, and Selenium —*  
*designed for ethical hackers, red team operators, and cybersecurity educators.*

<br/>

[Overview](#-overview) · [Features](#-features) · [Tech Stack](#-tech-stack) · [Installation](#-installation) · [Usage](#-usage) · [Admin Panel](#-admin-panel) · [Architecture](#-architecture) · [Configuration](#-configuration) · [Contributing](#-contributing)

</div>

---

## ⚠️ Legal Disclaimer

> **This tool is strictly for educational and authorized security testing purposes only.**  
> The author bears **no responsibility** for any misuse, damage, or illegal activity resulting from use of this software.  
> You must only use RickPhis on systems you **own** or have **explicit written permission** to test.  
> Unauthorized use against third-party systems is a **criminal offense** in most jurisdictions.

---

## 🧭 Overview

**RickPhis** is a modular phishing simulation framework that spins up a local Flask web server, exposes it to the internet via **Ngrok tunneling**, and leverages **Selenium** for browser automation — all in one lightweight Python package.

It allows security professionals to:

- Rapidly deploy convincing credential-harvesting pages for awareness training
- Simulate real-world phishing attack vectors in controlled environments
- Conduct red team exercises against organizational security posture
- Educate users about social engineering threats through hands-on demonstrations

---

## ✨ Features

-  **Flask-powered web server** — lightweight, fast, and fully customizable
-  **Ngrok tunneling** — instantly expose local pages via HTTPS public URLs
-  **Selenium integration** — real browser automation that attempts live logins
-  **2FA interception** — captures two-factor authentication codes mid-session
-  **Web Admin Panel** — view all captured credentials directly in your browser
-  **Admin REST API** — programmatically retrieve captured data via JSON endpoint
-  **Persistent logging** — all captures saved to `captured_credentials.json`
-  **Custom HTML/CSS templates** — realistic Instagram login page clone
-  **Gunicorn support** — production-grade WSGI server for stable deployments
-  **webdriver-manager** — automatic ChromeDriver management, no manual setup
-  **Animated ASCII art banner** — color terminal startup animation via `colorama`

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Role |
|---|---|---|---|
| Language | Python | 3.8+ | Core runtime |
| Web Framework | Flask | 3.1.3 | HTTP server, routing & session management |
| Browser Automation | Selenium | 4.15.2 | Live Instagram login attempts |
| Production Server | Gunicorn | 22.0.0 | WSGI deployment |
| Driver Management | webdriver-manager | 4.0.1 | Auto ChromeDriver setup |
| Tunneling | Ngrok | latest | HTTPS public URL exposure |
| Terminal Colors | colorama | latest | Startup ASCII art animation |
| Frontend | HTML5 + CSS3 | — | Phishing page & admin panel templates |

---

## 📁 Project Structure

```
RickPhis/
│
├── app.py                        # Main Flask app — routes, Selenium logic, admin panel
├── requirements.txt              # Python dependencies
├── captured_credentials.json     # Auto-generated — stores all captured data
│
├── templates/
│   ├── login.html                # Fake Instagram login page
│   ├── 2fa.html                  # Fake 2FA verification page
│   ├── admin.html                # Admin login page
│   └── admin_panel.html          # Admin dashboard (credential viewer)
│
├── static/                       # CSS, JS, and static assets
│   └── ...
│
├── RİckPhis.png                  # Project logo
├── Screenshot.png                # Application screenshot
└── README.md                     # You are here
```

---

## ⚙️ Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.8+](https://python.org/downloads)
- [Google Chrome](https://www.google.com/chrome) or Chromium
- [Ngrok](https://ngrok.com/download) (with a free account)
- `pip` package manager

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Rickidevs/RickPhis.git
cd RickPhis
```

### Step 2 — Create a Virtual Environment *(Recommended)*

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Ngrok

Sign up at [ngrok.com](https://ngrok.com) and authenticate:

```bash
# macOS
brew install ngrok/ngrok/ngrok

# Linux (snap)
sudo snap install ngrok

# Add your auth token
ngrok config add-authtoken <YOUR_AUTHTOKEN>
```

---

## 🚀 Usage

### 1. Start the Server

```bash
python app.py
```

The animated ASCII banner will appear on startup, then the server launches at `http://localhost:5000`.

---

### 2. Expose via Ngrok

Open a **new terminal window**:

```bash
ngrok http 5000
```

You will receive a public HTTPS URL:

```
Forwarding   https://abcd-1234-5678.ngrok-free.app -> http://localhost:5000
```

Share this URL as the phishing link in your simulation.

---

### 3. Production Deployment with Gunicorn

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

| Flag | Description |
|------|-------------|
| `--workers 4` | Number of worker processes |
| `--bind 0.0.0.0:5000` | Bind to all interfaces on port 5000 |

---

## 🖥️ Admin Panel

RickPhis includes a **built-in web admin panel** that lets you view all captured credentials directly in your browser — no terminal required.

### Accessing the Admin Panel

Navigate to:

```
http://localhost:5000/adminpage
```

Or via your Ngrok URL:

```
https://xxxx.ngrok-free.app/adminpage
```

### Default Admin Credentials

> ⚠️ **Change these before any real deployment** (see [Configuration](#-configuration))

| Field | Default Value |
|-------|--------------|
| Username | `admin` |
| Password | `admin` |

---

### Admin Panel Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/adminpage` | `GET` | Admin login page |
| `/admin/auth` | `POST` | Authenticate as admin |
| `/admin/panel` | `GET` | Dashboard — view all captured credentials |
| `/admin/api/data` | `GET` | JSON API — returns all captures programmatically |
| `/admin/logout` | `GET` | End admin session |

### Admin API Example

Once authenticated, you can fetch all captured data as JSON:

```bash
curl http://localhost:5000/admin/api/data
```

**Response format:**

```json
[
  {
    "timestamp": "2025-01-15T14:32:11.123456",
    "username": "target_user",
    "password": "captured_pass",
    "session_id": "IGsessioncookievalue",
    "two_fa_code": "123456",
    "status": "success",
    "ip_address": "192.168.1.10",
    "user_agent": "Mozilla/5.0 ..."
  }
]
```

### Capture Status Types

| Status | Meaning |
|--------|---------|
| `captured` | Form submitted, awaiting login attempt |
| `success` | Login successful — session cookie captured |
| `failed_login` | Wrong username or password |
| `2fa_required` | Credentials valid, 2FA was triggered |
| `2fa_success` | 2FA code captured, session cookie obtained |
| `2fa_failed` | Wrong 2FA code entered |

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────────────┐
                    │              TARGET BROWSER              │
                    └──────────────────┬──────────────────────┘
                                       │  HTTPS Request
                    ┌──────────────────▼──────────────────────┐
                    │            NGROK TUNNEL                  │
                    │    https://xxxx.ngrok-free.app           │
                    └──────────────────┬──────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────────┐
                    │         FLASK WEB SERVER :5000           │
                    │                                          │
                    │  GET  /          → login.html            │
                    │  POST /login     → Selenium login        │
                    │  GET  /2fa       → 2fa.html              │
                    │  POST /verify    → Selenium 2FA verify   │
                    │  GET  /adminpage → admin login           │
                    │  GET  /admin/panel → credential viewer   │
                    └───────────┬──────────────┬──────────────┘
                                │              │
               ┌────────────────▼──┐    ┌──────▼──────────────┐
               │  SELENIUM CHROME  │    │  captured_           │
               │  Real Instagram   │    │  credentials.json    │
               │  login attempt    │    │  (persistent log)    │
               └───────────────────┘    └─────────────────────┘
```

**Flow:**
1. Target visits the Ngrok URL → sees a realistic Instagram login page
2. Credentials are submitted → Flask triggers a **real Selenium browser session** against Instagram
3. If 2FA is required → target is shown the fake 2FA page → code is captured and submitted via Selenium
4. All data (credentials, session cookies, IP, user agent) is saved to `captured_credentials.json`
5. Operator reviews everything at `/admin/panel` in the browser

---

## 🔧 Configuration

All sensitive defaults can be overridden using **environment variables** — no code changes needed.

### Admin Credentials

```bash
# Linux / macOS
export ADMIN_USER=your_custom_username
export ADMIN_PASS=your_strong_password

# Windows (PowerShell)
$env:ADMIN_USER="your_custom_username"
$env:ADMIN_PASS="your_strong_password"
```

Then start the server normally:

```bash
python app.py
```

### Changing Defaults in Code

If you prefer to hardcode values, locate these lines in `app.py`:

```python
# Line ~15 in app.py
ADMIN_USERNAME = os.getenv('ADMIN_USER', 'admin')   # ← change 'admin'
ADMIN_PASSWORD = os.getenv('ADMIN_PASS', 'admin')   # ← change 'admin'
```

Replace `'admin'` with your preferred credentials:

```python
ADMIN_USERNAME = os.getenv('ADMIN_USER', 'mySecureUser')
ADMIN_PASSWORD = os.getenv('ADMIN_PASS', 'myStr0ngP@ss!')
```

> 💡 **Best practice:** Always use environment variables over hardcoded secrets, especially in shared or production environments.

### Other Configurable Constants

| Variable | Default | Description |
|----------|---------|-------------|
| `CAPTURE_FILE` | `captured_credentials.json` | Output file for captured data |
| `MAX_INPUT_LENGTH` | `150` | Max allowed length for form fields |
| `PERMANENT_SESSION_LIFETIME` | `30 minutes` | Flask session expiry time |
| `host` | `0.0.0.0` | Server bind address |
| `port` | `5000` | Server port |

---

## 🛡️ Ethical Use Guidelines

| ✅ DO | ❌ DON'T |
|-------|---------|
| Test only on systems you own | Use against unauthorized third parties |
| Obtain written consent before red team ops | Harvest real user credentials |
| Disclose findings responsibly | Share or sell captured data |
| Use for awareness training | Deploy without legal clearance |
| Change default admin credentials | Leave `admin/admin` in production |
| Follow your organization's security policies | Violate local cybercrime laws |

---

## 📦 Dependencies

```txt
Flask==3.1.3
selenium==4.15.2
gunicorn==22.0.0
webdriver-manager==4.0.1
```

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

```bash
# 1. Fork the repository on GitHub

# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Commit your changes
git commit -m "feat: add your feature description"

# 4. Push to your fork
git push origin feature/your-feature-name

# 5. Open a Pull Request on GitHub
```

---

## 📄 License

This project is provided **for educational and research purposes only.**  
Commercial use, malicious deployment, or distribution of harvested data is strictly prohibited.

---

<div align="center">

**Built by [Rickidevs](https://github.com/Rickidevs)**

*If this project helped you, consider giving it a ⭐ — it means a lot!*

</div>
