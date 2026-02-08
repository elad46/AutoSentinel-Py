import os
import time
import psutil
import telebot
import threading
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ADMIN_ID = os.getenv("ADMIN_ID")

cpu_history = []
ram_history = []
timestamps = []

def update_stats():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    current_time = datetime.now().strftime("%H:%M")
    cpu_history.append(cpu)
    ram_history.append(ram)
    if len(cpu_history) > 15:
        cpu_history.pop(0)
        ram_history.pop(0)
        timestamps.pop(0)
    else:
        timestamps.append(current_time)
    return cpu, ram

def alert_monitor():
    while True:
        cpu, ram = update_stats()
        # החזרנו ל-90 כדי שיהיה הגיוני, תשנה ל-1 לבדיקה אם תרצה
        if cpu > 90 or ram > 90:
            try:
                bot.send_message(ADMIN_ID, f"⚠️ התראת עומס מערכת!\nCPU: {cpu}%\nRAM: {ram}%")
            except: pass
        time.sleep(60)

@bot.message_handler(commands=['status'])
def send_status(message):
    if str(message.from_user.id) != ADMIN_ID: return
    cpu, ram = update_stats()
    bot.reply_to(message, f"🖥 מצב שרת:\nCPU: {cpu}%\nRAM: {ram}%")

@bot.message_handler(commands=['top'])
def send_top(message):
    """מחזירה את 5 התהליכים שצורכים הכי הרבה זיכרון"""
    if str(message.from_user.id) != ADMIN_ID: return
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # מיון לפי צריכת זיכרון
    processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    
    response = "🔝 **Top 5 Memory Consumers:**\n"
    for p in processes:
        response += f"🔹 {p['name']} (PID: {p['pid']}): {p['memory_percent']:.1f}%\n"
    
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['graph'])
def send_graph(message):
    if str(message.from_user.id) != ADMIN_ID: return
    if len(cpu_history) < 2:
        bot.reply_to(message, "⏳ אוסף נתונים, נסה שוב בעוד דקה...")
        return
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_history, label='CPU %')
    plt.plot(timestamps, ram_history, label='RAM %')
    plt.legend(); plt.grid(True)
    plt.savefig("graph.png"); plt.close()
    with open("graph.png", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

if __name__ == "__main__":
    threading.Thread(target=alert_monitor, daemon=True).start()
    print("🚀 Bot is running with /top command enabled!")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
