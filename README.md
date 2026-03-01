# 🛡️ AutoSentinel-Py

> AI-Augmented Infrastructure Monitoring & Automation System  
> Built with Python, Docker & LLM-Based Log Intelligence

AutoSentinel is a lightweight, container-ready infrastructure monitoring system designed to simulate real-world production operations.

It combines proactive health monitoring, AI-powered log diagnostics, and real-time alerting into a practical automation tool focused on system reliability and operational visibility.

---

## 🚀 Core Capabilities

- 🔍 Continuous system & service health monitoring
- 🧠 AI-powered log analysis using Google Gemini 1.5 Flash
- 📡 Real-time alerts via Telegram Bot & Slack Webhooks
- 📊 On-demand CPU & RAM visualization (matplotlib)
- 🔐 Secure Telegram authorization middleware
- 💾 Persistent monitored targets (local storage)
- 🐳 Fully Dockerized deployment with volume mapping

---

## 🏗️ System Architecture

Host Machine  
│  
├── Docker Container  
│   ├── Monitor Thread (heartbeat & health checks)  
│   ├── AI Log Analyzer (Gemini API integration)  
│   ├── Telegram Bot Command Interface  
│   └── Slack Alert Dispatcher  
│  
└── Mounted Host Logs (/var/log/syslog)

The system runs in a multi-threaded architecture to ensure responsiveness between monitoring operations and interactive command handling.

---

## ⚙️ Operational Design Principles

- Threaded architecture for concurrency & responsiveness
- Environment-based configuration via `.env`
- Secure user validation middleware
- Container isolation for portability
- Host-to-container log volume mapping
- Infrastructure-first design mindset

---

## 📊 Example Alert



---

## 🛠️ Tech Stack

Core: Python 3.12, psutil, requests  
AI Engine: Google Gemini 1.5 Flash API  
Visualization: matplotlib  
Containerization: Docker & Docker Compose  
Alerting: Telegram Bot API, Slack Webhooks  

---

## 📋 What This Project Demonstrates

- Infrastructure monitoring concepts
- Observability thinking
- Automation scripting
- Secure API integrations
- Containerized deployment workflows
- AI-assisted diagnostics for system operations

---

## 🎯 Why This Project?

AutoSentinel was built to simulate real-world infrastructure monitoring scenarios.

The goal was to combine automation, AI-driven diagnostics, secure remote alerting, and containerized deployment into a lightweight yet production-inspired monitoring assistant.

It reflects a strong focus on system reliability, proactive operations, and infrastructure automation.

---

## ☁️ Cloud Deployment (Oracle Cloud - OCI)

AutoSentinel is designed to run 24/7 on a Linux VM.

Deployment plan:
- Ubuntu VM on Oracle Cloud Always Free
- Docker Compose runtime
- restart: unless-stopped for resilience
- Secure SSH access (key-based authentication)
- Minimal open firewall rules

---

## 🚧 Roadmap

- [x] Core monitoring engine  
- [x] Telegram alert integration  
- [x] Slack webhook alerts  
- [x] AI-based log diagnostics  
- [ ] Metrics persistence layer  
- [ ] Prometheus integration  
- [ ] Web dashboard interface  

---

## 📦 Quick Start

Clone & Configure:

git clone https://github.com/elad46/AutoSentinel-Py.git  
cd AutoSentinel-Py  
cp .env.example .env  

Add your API keys and Telegram Admin ID inside .env

Launch with Docker:

docker-compose up -d --build  

---

## 👨‍💻 Author

Elad Amar  
Linux & Automation Engineer  
Focused on infrastructure reliability, automation, and AI-assisted operations.
























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
