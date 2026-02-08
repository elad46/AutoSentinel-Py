# 🛡️ AutoSentinel-Py: Smart Infrastructure Monitoring

AutoSentinel is a robust monitoring solution for Linux Systems and Cloud Infrastructure. It bridges the gap between raw hardware telemetry and actionable intelligence using **Google Gemini 3.0 AI**.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![OS](https://img.shields.io/badge/OS-Linux-black)
![Environment](https://img.shields.io/badge/Env-Cloud/On--Prem-blue)
![AI](https://img.shields.io/badge/AI-Gemini_Flash-orange)

## 🌟 Overview
Unlike standard monitoring tools, AutoSentinel tracks system health, visualizes performance trends, and uses AI to troubleshoot spikes. It is designed for System Administrators who need to manage servers efficiently via Telegram.

## 🚀 Key Features
- **📊 Performance Graphing:** Visualizes CPU/RAM trends over time (Matplotlib).
- **🚨 Automated System Alerts:** Background monitoring that triggers instant notifications for resource exhaustion.
- **🧠 Intelligent Diagnostics:** Uses Gemini 3 Flash to analyze system logs and metrics in real language.
- **🐳 Containerized Deployment:** Fully Dockerized for consistent deployment across any Linux distribution.
- **📈 Infrastructure Health:** Real-time metrics for CPU, Memory, and Disk.

## 🛠️ Tech Stack
- **OS/Environment:** Linux (Ubuntu/Debian/RHEL), Docker
- **Monitoring:** `psutil` (Hardware abstraction layer)
- **Data Visualization:** `Matplotlib`
- **Automation:** Python 3.12, Multi-threading
- **Interface:** Telegram Bot API

## 📦 Deployment
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/elad46/AutoSentinel-Py.git](https://github.com/elad46/AutoSentinel-Py.git)
   cd AutoSentinel-Py
