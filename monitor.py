import os
import time
import psutil
import telebot
import threading
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# טעינת הגדרות
load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ADMIN_ID = os.getenv("ADMIN_ID")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# הגדרת Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# היסטוריה לגרפים
cpu_history = []
ram_history = []
timestamps = []

def update_stats():
    """מעדכן נתוני מערכת ושומר היסטוריה"""
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    current_time = datetime.now().strftime("%H:%M")
    
    cpu_history.append(cpu)
    ram_history.append(ram)
    
    # שומר רק את ה-15 דקות האחרונות
    if len(cpu_history) > 15:
        cpu_history.pop(0)
        ram_history.pop(0)
        timestamps.pop(0)
    else:
        timestamps.append(current_time)
    
    return cpu, ram

def send_slack_alert(message):
    """שליחת התראה לערוץ הסלאק"""
    if not SLACK_WEBHOOK_URL:
        return
    payload = {"text": f"🚨 *AutoSentinel System Alert*\n{message}"}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Slack Error: {e}")

def get_ai_analysis(cpu, ram):
    """מבקש מ-Gemini ניתוח קצר של מצב המערכת"""
    try:
        prompt = f"The server is currently at {cpu}% CPU and {ram}% RAM. Provide a very brief, professional analysis and one actionable tip for a sysadmin."
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI analysis currently unavailable."

def alert_monitor():
    """רץ ברקע ובודק עומסים כל דקה"""
    while True:
        cpu, ram = update_stats()
        # שנה ל-1 לצורך בדיקה, החזר ל-90 לייצור
        if cpu > 90 or ram > 90:
            msg = f"⚠️ התראת עומס מערכת!\nCPU: {cpu}%\nRAM: {ram}%"
            
            # שליחה לטלגרם
            try: bot.send_message(ADMIN_ID, msg)
            except: pass
            
            # שליחה לסלאק
            send_slack_alert(msg)
            
        time.sleep(60)

# --- פקודות טלגרם ---

@bot.message_handler(commands=['status'])
def send_status(message):
    if str(message.from_user.id) != ADMIN_ID: return
    cpu, ram = update_stats()
    ai_msg = get_ai_analysis(cpu, ram)
    bot.reply_to(message, f"🖥 **System Status:**\nCPU: {cpu}%\nRAM: {ram}%\n\n🤖 **AI Insight:**\n{ai_msg}", parse_mode="Markdown")

@bot.message_handler(commands=['top'])
def send_top(message):
    """מציג 5 תהליכים זוללי זיכרון"""
    if str(message.from_user.id) != ADMIN_ID: return
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied): pass
    
    processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    response = "🔝 **Top 5 Memory Consumers:**\n"
    for p in processes:
        response += f"🔹 {p['name']} (PID: {p['pid']}): {p['memory_percent']:.1f}%\n"
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['graph'])
def send_graph(message):
    if str(message.from_user.id) != ADMIN_ID: return
    if len(cpu_history) < 2:
        bot.reply_to(message, "⏳ Gathering data... try again in a minute.")
        return
    
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_history, label='CPU %', color='red')
    plt.plot(timestamps, ram_history, label='RAM %', color='blue')
    plt.title("System Performance Trend")
    plt.legend(); plt.grid(True)
    plt.savefig("graph.png"); plt.close()
    
    with open("graph.png", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

if __name__ == "__main__":
    threading.Thread(target=alert_monitor, daemon=True).start()
    print("🚀 AutoSentinel is active with Slack & AI support!")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
