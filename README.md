# 🛡️ AutoSentinel-Py: AI-Driven Infrastructure Monitor

AutoSentinel is a proactive **AI-Driven System Administrator**. Built with Python, it monitors Linux environments and production services via Telegram, leveraging **Google Gemini 1.5 Flash** for real-time diagnostics and log analysis.

---

## 🚀 Key Features

* **🧠 AI Log Intelligence:** Analyzes system logs (`/var/log/syslog`) using LLMs to identify root causes and suggest fixes instantly.
* **🔐 Authorization Middleware:** Robust security layer that validates Telegram User IDs, preventing unauthorized access.
* **💾 Persistent Storage:** Monitored targets are saved locally, ensuring data persistence across container restarts.
* **🌐 Hybrid Alerting:** Dual-channel alerts via **Slack** and **Telegram** for 100% uptime visibility.
* **📈 Resource Trends:** On-demand system health charts (CPU/RAM) generated using `matplotlib`.
* **🐳 Docker-Ready:** Optimized volume mapping for seamless host-to-container log monitoring.

## 🛠️ Tech Stack

- **Core:** Python 3.12, `psutil`, `requests`
- **AI Engine:** Google Gemini 1.5 Flash API
- **Visuals:** `matplotlib`
- **Ops:** Docker & Docker Compose
- **Alerts:** Telegram Bot API, Slack Webhooks

---

## 📋 Architecture Overview
The system employs a **Multi-threaded approach**:
1. **Monitor Thread:** Continuous heartbeat checks for services and system health.
2. **Interactive Thread:** Handles Telegram commands and AI-powered log forensics.

---

## 📦 Quick Start

1. **Clone & Configure:**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
   cp .env.example .env  # Add your API keys and Admin ID

2. **Spin Up with Docker:**
   ```bash
   docker-compose up -d --build
