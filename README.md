# 🛡️ AutoSentinel-Py: Smart AI-Driven Infrastructure Monitor

AutoSentinel is a proactive **AI-Driven System Administrator** in your pocket. Designed for DevOps to monitor Linux environments via Telegram with real-time AI diagnostics.

![Dashboard](screenshots/menu.png)

## 🚀 Key Features
* **🧠 AI Log Intelligence:** Analyzes system logs (`/var/log/syslog`) using **Google Gemini 1.5 Flash** to diagnose and explain errors.
* **💾 Persistent Monitoring:** Dynamically add/remove URLs via Telegram. Sites are saved to local storage and survive container restarts.
* **🌐 Hybrid Uptime Checks:** Instant alerts on **Slack** (Redundancy) and **Telegram** (Management) when a service goes down.
* **📊 Interactive UI:** Complete control via Inline Telegram Buttons—no CLI needed for daily tasks.
* **📈 Resource Visualization:** Generate on-demand performance graphs for CPU/RAM trends.
* **🐳 Dockerized:** One-command setup with host-level log visibility.

## 🛠️ Tech Stack
- **AI:** Google Gemini 1.5 Flash
- **Backend:** Python 3.12 (`psutil`, `pyTelegramBotAPI`)
- **Visuals:** `matplotlib`
- **Infrastructure:** Docker & Docker Compose
- **Alerting:** Slack Webhooks & Telegram Bot API

## 📦 Quick Start
1. **Clone & Configure:**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
   cp .env.example .env # Add your keys (Telegram, Gemini, Slack)
