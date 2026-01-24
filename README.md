# 🛡️ AutoSentinel AI: Intelligent Server Monitoring

AutoSentinel is a professional-grade monitoring solution that bridges the gap between raw server metrics and actionable insights using **Google Gemini 3.0 AI**.

## 🧠 Why AutoSentinel?
Unlike traditional monitors that just show numbers, AutoSentinel analyzes the context. It tells you *why* your RAM is high and *what* you should do about it in plain language.

## 🚀 Key Features
- **Real-Time Diagnostics:** Monitors CPU, Memory, and Disk Health.
- **AI-Powered Insights:** Integrated with Gemini 3 Flash for heuristic system analysis.
- **On-the-go Management:** Fully controlled via Telegram Bot API.
- **Process Tracking:** `/top` command to identify resource-heavy applications.

## 🛠️ Architecture
1. **Collector:** Python `psutil` gathers hardware telemetry.
2. **Analyzer:** Data is structured and sent to **Gemini 3 API** with custom prompting.
3. **Interface:** Responses are delivered via **Telegram** with Markdown formatting.

## 📦 Installation
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/AutoSentinel-Py.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up `.env` with your API keys.
4. Run: `python monitor.py`
