import time
import os
import psutil
import telebot
import threading
import socket
import datetime
from dotenv import load_dotenv

# טעינה
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TOKEN)

# --- פונקציות עזר ---
def get_system_status():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"📊 *Current Status:*\n\n🖥 CPU: {cpu}%\n🧠 RAM: {memory}%\n💾 Disk: {disk}%"

def get_system_info():
    hostname = socket.gethostname()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    return f"ℹ️ *System Info:*\n\n🏠 Hostname: {hostname}\n🕒 Boot Time: {boot_time}"

# --- טיפול בפקודות טלגרם ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 I'm AutoSentinel! Use the menu or send /status to check the server.")

@bot.message_handler(commands=['status'])
def status_command(message):
    bot.send_message(CHAT_ID, get_system_status(), parse_mode="Markdown")

@bot.message_handler(commands=['info'])
def info_command(message):
    bot.send_message(CHAT_ID, get_system_info(), parse_mode="Markdown")

# --- לולאת הניטור (רצה ברקע) ---
def monitoring_loop():
    print("🚀 Monitoring loop started...")
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        if cpu > 80 or memory > 80 or disk > 90:
            msg = f"⚠️ *CRITICAL ALERT*\nCPU: {cpu}%\nRAM: {memory}%\nDisk: {disk}%"
            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        
        time.sleep(60)

# --- הפעלה ---
if __name__ == "__main__":
    monitor_thread = threading.Thread(target=monitoring_loop)
    monitor_thread.daemon = True
    monitor_thread.start()

    print("🤖 Bot is listening...")
    bot.infinity_polling()
