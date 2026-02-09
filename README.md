# 🛡️ AutoSentinel-Py: Smart AI-Driven Infrastructure Monitor

AutoSentinel is not just a monitor—it's a **proactive system administrator** in your pocket. Built for DevOps and SysAdmins to manage Linux environments via Telegram with real-time AI diagnostics.



## 🚀 Key Features
* **🧠 AI Log Intelligence:** Analyzes system logs (`/var/log/syslog`) using Google Gemini to explain errors in plain English.
* **🌐 Dynamic Uptime Monitoring:** Manage and monitor multiple URLs. Get instant alerts on Slack/Telegram when a site goes down.
* **📊 Interactive UI:** Complete control via Telegram Inline Buttons—no more typing commands.
* **📈 Resource Visualization:** Generate on-demand performance graphs for CPU and RAM trends.
* **🐳 Dockerized Deployment:** One-command setup with host-level visibility.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **Intelligence:** Google Gemini 1.5 Flash API
- **Monitoring:** `psutil`, `requests`
- **Visualization:** `matplotlib`
- **Infrastructure:** Docker & Docker Compose
- **Alerting:** Telegram Bot API & Slack Webhooks

## 📦 Quick Start
1. **Clone & Configure:**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
   cp .env.example .env # Fill in your API keys
