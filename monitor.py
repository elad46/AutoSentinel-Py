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
    requests.post(url, json=payload)

def check_system_health():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    
    report = f"🛡️ *AutoSentinel Report*\n📅 Time: {now}\n💻 CPU: {cpu}%\n🧠 RAM: {memory}%"
    
    # נשלח תמיד בשביל הבדיקה
    send_telegram_message(report)
    print("Command executed. Check your Telegram!")

if __name__ == "__main__":
    check_system_health()
