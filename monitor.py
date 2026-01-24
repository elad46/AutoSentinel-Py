import os
import psutil
import telebot
import requests
import threading
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SLACK_URL = os.getenv("SLACK_WEBHOOK_URL")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3-flash-preview"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_KEY, http_options={'api_version': 'v1beta'})

def send_slack_alert(message):
    payload = {"text": f"🚨 *AutoSentinel Alert:* \n{message}"}
    try:
        requests.post(SLACK_URL, json=payload)
    except Exception as e:
        print(f"Error sending to Slack: {e}")

def monitor_system_background():
    """פונקציה שרצה ברקע ובודקת חריגות כל דקה"""
    print("🕵️ Background monitoring started...")
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        
        if cpu > 90 or ram > 90:
            alert_msg = f"⚠️ High resource usage detected!\nCPU: {cpu}%\nRAM: {ram}%"
            send_slack_alert(alert_msg)
        
        time.sleep(60)

# הפעלת הניטור ברקע בנפרד מהבוט
threading.Thread(target=monitor_system_background, daemon=True).start()

@bot.message_handler(commands=['start', 'analyze', 'status', 'top', 'info'])
def handle_commands(message):
    # הפונקציות הקיימות שלך נשארות כאן (למען הקיצור לא נשנה אותן)
    if message.text == '/status':
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        bot.reply_to(message, f"📊 מצב שרת:\nCPU: {cpu}%\nRAM: {ram}%")
    elif message.text == '/analyze':
        sent_msg = bot.reply_to(message, "🤖 מנתח עם Gemini 3...")
        status = f"CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%"
        response = client.models.generate_content(model=MODEL_NAME, contents=f"נתח בעברית: {status}")
        bot.edit_message_text(f"✅ ניתוח AI:\n{response.text}", message.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    print("🚀 AutoSentinel with Slack Integration is running...")
    bot.infinity_polling()
