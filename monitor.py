import os
import sqlite3
import psutil
import time
import threading
import requests  # ספרייה חדשה לשליחת הודעות לסלאק
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import telebot
import google.generativeai as genai

# טעינת הגדרות
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK_URL')

# הגדרת ה-AI
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

# --- פונקציות עזר ---

def is_authorized(message):
    return message.chat.id == ADMIN_ID

def send_slack_alert(text):
    """שליחת הודעה לערוץ הסלאק"""
    if SLACK_WEBHOOK:
        payload = {"text": f"🚀 *AutoSentinel System Alert* 🚀\n{text}"}
        try:
            requests.post(SLACK_WEBHOOK, json=payload)
        except Exception as e:
            print(f"Slack Error: {e}")

def save_to_db(cpu, ram):
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS stats (timestamp DATETIME, cpu REAL, ram REAL)")
        c.execute("INSERT INTO stats VALUES (?, ?, ?)", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cpu, ram))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

# --- מערכת התראות רקע ---

def monitor_loop():
    print("📢 Monitoring started (Telegram + Slack).")
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            save_to_db(cpu, ram)
            
            # אם יש עומס - שלח התראה לשני הערוצים
            if cpu > 90 or ram > 95:
                alert_msg = f"⚠️ עומס גבוה בשרת!\nCPU: {cpu}%\nRAM: {ram}%"
                if ADMIN_ID != 0:
                    bot.send_message(ADMIN_ID, alert_msg)
                send_slack_alert(alert_msg)
            
            time.sleep(300) 
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(10)

# --- פקודות בוט ---

@bot.message_handler(func=lambda message: not is_authorized(message))
def handle_unauthorized(message):
    bot.reply_to(message, "🚫 אין לך הרשאה לבוט זה.")

@bot.message_handler(commands=['status'])
def send_status(message):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    bot.reply_to(message, f"🖥 מצב נוכחי:\nCPU: {cpu}%\nRAM: {ram}%")

@bot.message_handler(commands=['test_slack'])
def test_slack(message):
    """פקודה לבדיקה ידנית שהסלאק עובד"""
    send_slack_alert("🔔 בדיקת חיבור מוצלחת מהשרת של אלעד!")
    bot.reply_to(message, "הודעת בדיקה נשלחה לסלאק! בדוק את ערוץ ה-Alerts שלך.")

@bot.message_handler(commands=['analyze'])
def analyze_performance(message):
    conn = sqlite3.connect('monitor_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stats ORDER BY timestamp DESC LIMIT 10")
    data = c.fetchall()
    conn.close()
    response = model.generate_content(f"Analyze this server data briefly in Hebrew: {str(data)}")
    bot.reply_to(message, f"🤖 ניתוח AI:\n{response.text}")

if __name__ == "__main__":
    threading.Thread(target=monitor_loop, daemon=True).start()
    print("✅ Bot is running with Slack integration.")
    bot.infinity_polling()
