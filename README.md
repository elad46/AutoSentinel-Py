# 🛡️ AutoSentinel-Py: Smart AI-Driven Infrastructure Monitor

AutoSentinel is a proactive **AI-Driven System Administrator** in your pocket. It's a specialized tool designed to monitor Linux environments via Telegram with real-time AI diagnostics and built-in security.

## 🚀 Key Features
* **🧠 AI Log Intelligence:** One-click analysis of system logs (`/var/log/syslog`) using **Google Gemini 1.5 Flash** to diagnose and explain errors in plain English.
* **🔐 Admin Security:** Secure authorization middleware ensuring only the owner can access system commands, with instant alerts on unauthorized access attempts.
* **💾 Persistent Monitoring:** Dynamically manage monitored URLs. All changes are saved to local storage and survive container restarts.
* **🌐 Multi-Channel Alerts:** Reliable notifications via **Slack** (for redundancy) and **Telegram** (for management) on service downtime.
* **📊 Visual Performance:** Generate on-demand graphs for CPU and RAM trends directly in your chat.
* **🐳 Containerized Deployment:** Fully dockerized setup for easy deployment with host-level visibility.

## 🛠️ Tech Stack
- **AI:** Google Gemini 1.5 Flash API
- **Backend:** Python 3.12 (`psutil`, `pyTelegramBotAPI`)
- **Infrastructure:** Docker & Docker Compose
- **Visualization:** `matplotlib`
- **Alerting:** Slack Webhooks & Telegram Bot API

## 📦 Quick Start
1. **Clone & Configure:**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
   cp .env.example .env # Add your API keys here
