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
from telebot import types

# טעינת הגדרות מה-.env
load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ADMIN_ID = os.getenv("ADMIN_ID")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# הגדרת Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# רשימת אתרים לניטור (נטענת מה-ENV וניתנת לשינוי דינמי)
MONITORED_SITES = [s.strip() for s in os.getenv("SITES_TO_CHECK", "").split(",") if s.strip()]

# היסטוריה לגרפים
cpu_history, ram_history, timestamps = [], [], []

def update_stats():
    """מעדכן נתוני מערכת ושומר היסטוריה לגרף"""
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    current_time = datetime.now().strftime("%H:%M")
    
    cpu_history.append(cpu)
    ram_history.append(ram)
    timestamps.append(current_time)
    
    if len(cpu_history) > 15:
        cpu_history.pop(0)
        ram_history.pop(0)
        timestamps.pop(0)
    return cpu, ram

def get_ai_analysis(cpu, ram):
    """מבקש מ-Gemini ניתוח של מצב השרת"""
    try:
        prompt = f"The server is at {cpu}% CPU and {ram}% RAM. Give a very short, professional insight for a sysadmin."
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "AI Analysis currently unavailable."

def send_slack_alert(message):
    """שליחת התראה לסלאק"""
    if not SLACK_WEBHOOK_URL: return
    payload = {"text": f"🚨 *AutoSentinel Alert:*\n{message}"}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except:
        pass

def check_uptime():
    """בודק זמינות אתרים ומחזיר דו"ח"""
    report, issues = [], []
    for url in MONITORED_SITES:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                report.append(f"✅ {url}")
            else:
                m = f"❌ {url} (Status: {r.status_code})"
                report.append(m); issues.append(m)
        except:
            m = f"❌ {url} (Unreachable)"
            report.append(m); issues.append(m)
    return "\n".join(report) if report else "No sites monitored.", issues

def alert_monitor():
    """לופ ניטור שרץ ברקע כל דקה"""
    counter = 0
    while True:
        cpu, ram = update_stats()
        
        # התראת משאבים (מעל 90%)
        if cpu > 90 or ram > 90:
            msg = f"Server Stress Alert! CPU: {cpu}% RAM: {ram}%"
            try: bot.send_message(ADMIN_ID, f"⚠️ {msg}")
            except: pass
            send_slack_alert(msg)
        
        # בדיקת אתרים אוטומטית (כל 5 דקות)
        if counter % 5 == 0:
            _, issues = check_uptime()
            if issues:
                alert_msg = "🌐 **Uptime Alert!**\n" + "\n".join(issues)
                try: bot.send_message(ADMIN_ID, alert_msg, parse_mode="Markdown")
                except: pass
                send_slack_alert(alert_msg)
        
        counter += 1
        time.sleep(60)

# --- פקודות טלגרם וממשק כפתורים ---

@bot.message_handler(commands=['start', 'manage'])
def manage_panel(message):
    if str(message.from_user.id) != ADMIN_ID: return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("➕ הוסף אתר", callback_data="add_site"),
        types.InlineKeyboardButton("📋 רשימת אתרים", callback_data="list_sites"),
        types.InlineKeyboardButton("📊 סטטוס שרת", callback_data="server_status"),
        types.InlineKeyboardButton("🔝 Top 5", callback_data="top_procs"),
        types.InlineKeyboardButton("📈 גרף ביצועים", callback_data="send_graph")
    )
    
    bot.send_message(message.chat.id, "🛡️ **לוח הבקרה של AutoSentinel**\nבחר פעולה מהתפריט:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if str(call.from_user.id) != ADMIN_ID: return
    
    if call.data == "add_site":
        msg = bot.send_message(call.message.chat.id, "שלח לי את כתובת האתר להוספה (למשל https://google.com):")
        bot.register_next_step_handler(msg, process_add_site)
    
    elif call.data == "list_sites":
        report, _ = check_uptime()
        bot.send_message(call.message.chat.id, f"🌐 **סטטוס זמינות אתרים:**\n\n{report}")
    
    elif call.data == "server_status":
        cpu, ram = update_stats()
        ai_insight = get_ai_analysis(cpu, ram)
        status_msg = f"🖥 **סטטוס שרת:**\n\n🔹 CPU: {cpu}%\n🔹 RAM: {ram}%\n\n🤖 **ניתוח AI:**\n{ai_insight}"
        bot.send_message(call.message.chat.id, status_msg, parse_mode="Markdown")
    
    elif call.data == "top_procs":
        procs = sorted([p.info for p in psutil.process_iter(['pid', 'name', 'memory_percent'])], 
                       key=lambda x: x['memory_percent'], reverse=True)[:5]
        res = "🔝 **Top 5 Memory Consumers:**\n" + "\n".join([f"🔹 {p['name']}: {p['memory_percent']:.1f}%" for p in procs])
        bot.send_message(call.message.chat.id, res, parse_mode="Markdown")
        
    elif call.data == "send_graph":
        send_graph_file(call.message)

def process_add_site(message):
    url = message.text.strip()
    if url.startswith("http"):
        MONITORED_SITES.append(url)
        bot.reply_to(message, f"✅ האתר {url} נוסף לרשימת הניטור!")
    else:
        bot.reply_to(message, "❌ כתובת לא תקינה. שלח כתובת שמתחילה ב-http.")

def send_graph_file(message):
    if len(cpu_history) < 2:
        bot.send_message(message.chat.id, "⏳ Gathering data... wait a minute.")
        return
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_history, label='CPU', color='red')
    plt.plot(timestamps, ram_history, label='RAM', color='blue')
    plt.legend(); plt.grid(True); plt.title("System Performance")
    plt.savefig("graph.png"); plt.close()
    with open("graph.png", 'rb') as f:
        bot.send_photo(message.chat.id, f)

if __name__ == "__main__":
    # הפעלת המוניטור ב-Thread נפרד
    threading.Thread(target=alert_monitor, daemon=True).start()
    print("🚀 AutoSentinel V2.1 is active!")
    bot.infinity_polling()
