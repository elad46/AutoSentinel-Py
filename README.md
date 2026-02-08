# 🛡️ AutoSentinel-Py: Smart Infrastructure Monitoring

AutoSentinel is a professional monitoring engine designed for Linux Systems and Cloud Infrastructure. It combines real-time hardware telemetry with **Google Gemini 3.0 AI** to provide actionable intelligence.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![OS](https://img.shields.io/badge/OS-Linux-black)
![Environment](https://img.shields.io/badge/Env-Cloud/On--Prem-blue)

## 🌟 Overview
AutoSentinel tracks system health, visualizes trends, and uses AI to troubleshoot spikes. Designed for System Administrators to manage servers efficiently via Telegram without needing SSH for every check.

## 🚀 Key Features
- **📊 Performance Graphing:** Visualizes CPU/RAM trends (Matplotlib).
- **🚨 Automated Alerts:** Multi-threaded background monitor for instant notifications.
- **🔝 Process Insights:** `/top` command to identify resource-heavy applications.
- **🧠 AI Diagnostics:** Gemini 3 Flash integration for heuristic system analysis.
- **🐳 Dockerized:** Full containerization with host PID access for complete visibility.

## 🛠️ Tech Stack
- **OS:** Linux (Ubuntu/Debian/RHEL)
- **Runtime:** Python 3.12, Docker & Docker Compose
- **Libraries:** `psutil`, `Matplotlib`, `PyTelegramBotAPI`

## 📦 Deployment
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
