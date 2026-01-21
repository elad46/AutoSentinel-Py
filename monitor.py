import time
import os
import psutil
import requests
import datetime

# משיכת הסודות מהמערכת (אבטחת מידע)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TOKEN or not CHAT_ID:
        print("Error: Token or Chat ID not found!")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send: {e}")

def check_system_health():
    print("🚀 AutoSentinel is running... (Press Ctrl+C to stop)")
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent

        if cpu > 80 or memory > 80:
            msg = f"⚠️ *CRITICAL ALERT*\nCPU: {cpu}%\nRAM: {memory}%"
            send_telegram_message(msg)
            print(f"ALERT SENT! CPU: {cpu}%")
        else:
            print(f"Check passed: CPU is {cpu}%, RAM is {memory}%")

        time.sleep(10)

if __name__ == "__main__":
    check_system_health()
