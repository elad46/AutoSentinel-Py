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

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_KEY, http_options={'api_version': 'v1beta'})

def send_slack_alert(message):
    payload = {"text": f"🚨 *AutoSentinel Alert:* \n{message}"}
    try:
        requests.post(SLACK_URL, json=payload)
    except Exception as e:
        print(f"Error sending to Slack: {e}")

def monitor_system_background():
    print("🕵️ Background monitoring started...")
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            if cpu > 90 or ram > 90:
                send_slack_alert(f"⚠️ High resource usage!\nCPU: {cpu}%\nRAM: {ram}%")
            time.sleep(60)
        except Exception as e:
            print(f"Monitor error: {e}")
            time.sleep(10)

threading.Thread(target=monitor_system_background, daemon=True).start()

@bot.message_handler(commands=['status'])
def status(message):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    bot.reply_to(message, f"📊 מצב שרת:\nCPU: {cpu}%\nRAM: {ram}%")

@bot.message_handler(commands=['test_slack'])
def test_slack(message):
    send_slack_alert("🔔 בדיקה מהשרת לסלאק - הכל עובד!")
    bot.reply_to(message, "הודעת בדיקה נשלחה לסלאק! בדוק את ערוץ #alerts.")

if __name__ == "__main__":
    print("🚀 AutoSentinel is LIVE...")
    bot.infinity_polling()
