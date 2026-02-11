# 🛡️ AutoSentinel-Py: Smart AI-Driven Infrastructure Monitor

AutoSentinel is a proactive **AI-Driven System Administrator** in your pocket. It monitors Linux environments via Telegram with real-time AI diagnostics and built-in security.

## 🚀 Key Features
* **🧠 AI Log Intelligence:** Analyzes system logs (`/var/log/syslog`) using **Google Gemini 1.5 Flash** to diagnose errors.
* **🔐 Admin Security:** Authorization middleware ensuring only the owner can access the system.
* **💾 Persistent Monitoring:** Dynamically manage URLs. Monitoring lists survive container restarts.
* **🌐 Hybrid Alerts:** Real-time notifications via **Slack** and **Telegram** for any downtime.
* **📈 Visual Analytics:** Generate on-demand CPU/RAM performance graphs.
* **🐳 Dockerized:** One-command setup with host-level log visibility.

## 🛠️ Tech Stack
- **AI:** Google Gemini 1.5 Flash API
- **Backend:** Python 3.12 (`psutil`, `pyTelegramBotAPI`)
- **Infrastructure:** Docker & Docker Compose
- **Alerting:** Slack Webhooks & Telegram Bot API

## 📦 Quick Start
1. **Clone & Configure:**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
   cp .env.example .env # Add your API keys
