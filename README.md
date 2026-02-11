# 🛡️ AutoSentinel-Py: Smart AI-Driven Infrastructure Monitor

AutoSentinel is a proactive **AI-Driven System Administrator** in your pocket. Built with Python, it monitors Linux environments and production services via Telegram, leveraging **Google Gemini 1.5 Flash** for real-time diagnostics.



## 🚀 Key Features

* **🧠 AI Log Intelligence:** Deep analysis of system logs (`/var/log/syslog`) using LLM to identify root causes of failures instantly.
* **🔐 Enterprise-Grade Security:** Custom **Authorization Middleware** that validates User IDs and triggers "Security Breach" alerts for unauthorized access.
* **💾 Persistent Storage:** Dynamic URL management where monitored sites are saved to a local database/file, surviving container lifecycles.
* **🌐 Hybrid Alerting Pipeline:** Dual-channel redundancy using **Slack Webhooks** and **Telegram Bot API** for critical downtime alerts.
* **📈 Real-time Visualization:** On-demand generation of system resource trends (CPU/RAM) using `matplotlib`.
* **🐳 Robust Containerization:** Fully Dockerized environment with optimized volume mapping for host log access.

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **AI Engine:** Google Gemini 1.5 Flash API
- **Monitoring:** `psutil` (System Resources), `requests` (Uptime)
- **Visualization:** `matplotlib`
- **Infrastructure:** Docker, Docker Compose
- **Communication:** Telegram Bot API, Slack Webhooks

## 📋 Architecture Overview
The system runs in a decoupled environment where a background thread continuously monitors resources and connectivity, while the main thread handles the interactive Telegram interface and AI processing.



## 📦 Quick Start

1. **Clone & Configure :**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
   cp .env.example .env  # Add your API keys and Admin ID


2. **Clone & Configure :**
   ```bash
   sudo docker compose up -d --build
