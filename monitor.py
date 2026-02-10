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
import subprocess

# טעינת הגדרות
load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ADMIN_ID = os.getenv("ADMIN_ID")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SITES_FILE = "monitored_sites.txt"

# Gemini AI Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# --- אבטחה (Authorization) ---

def is_authorized(message):
    """בודק הרשאות ושולח התראה על גישה לא מורשת"""
    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        return True
    
    user_info = f"👤 שם: {message.from_user.first_name} | ID: {user_id}"
    if message.from_user.username:
        user_info += f" | @{message.from_user.username}"
        
    alert_msg = f"🚫 **ניסיון גישה לא מורשה!**\n{user_info}\nהמשתמש נחסם."
    try:
        bot.send_message(ADMIN_ID, alert_msg, parse_mode="Markdown")
    except:
        pass
    
    bot.reply_to(message, "❌ Access Denied. Your ID is not authorized.")
    return False

# --- ניהול אתרים (Persistence) ---

def load_sites():
    """טוען אתרים מ-ENV ומהקובץ"""
    sites = [s.strip() for s in os.getenv("SITES_TO_CHECK", "").split(",") if s.strip()]
    if os.path.exists(SITES_FILE):
        with open(SITES_FILE, "r") as f:
            file_sites = [line.strip() for line in f.readlines() if line.strip()]
            sites.extend(file_sites)
    return list(dict.fromkeys(sites))

def save_site_to_file(url):
    with open(SITES_FILE, "a") as f:
        f.write(url + "\n")

def rewrite_sites_file(sites_list):
    env_sites = [s.strip() for s in os.getenv("SITES_TO_CHECK", "").split(",") if s.strip()]
    with open(SITES_FILE, "w") as f:
        for site in sites_list:
            if site not in env_sites:
                f.write(site + "\n")

MONITORED_SITES = load_sites()
cpu_history, ram_history, timestamps = [], [], []

# --- ניטור ולוגיקה ---

def update_stats():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    current_time = datetime.now().strftime("%H:%M")
    cpu_history.append(cpu); ram_history.append(ram); timestamps.append(current_time)
    if len(cpu_history) > 15:
        cpu_history.pop(0); ram_history.pop(0); timestamps.pop(0)
    return cpu, ram

def get_ai_analysis(cpu, ram):
    try:
        prompt = f"Server status: CPU {cpu}%, RAM {ram}%. Provide a 1-sentence professional insight."
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI insight unavailable (Check API Key)."

def get_system_logs():
    try:
        # פקודה לקריאת לוגים - וודא שהווליום מחובר ב-Docker
        return subprocess.check_output(["tail", "-n", "20", "/var/log/syslog"], encoding="utf-8")
    except:
        return "System logs unreachable. Verify volume mounting in Docker."

def analyze_logs_ai(logs):
    try:
        prompt = f"Analyze these Linux logs and identify any issues or errors briefly:\n\n{logs}"
        return model.generate_content(prompt).text
    except:
        return "AI Log Analysis failed."

def check_uptime():
    report, issues = [], []
    for url in MONITORED_SITES:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200: report.append(f"✅ {url}")
            else:
                m = f"❌ {url} (Code: {r.status_code})"; report.append(m); issues.append(m)
        except:
            m = f"❌ {url} (Down)"; report.append(m); issues.append(m)
    return "\n".join(report) if report else "No sites monitored.", issues

def alert_monitor():
    counter = 0
    while True:
        cpu, ram = update_stats()
        if cpu > 90 or ram > 90:
            msg = f"⚠️ **High Usage Alert!**\nCPU: {cpu}% | RAM: {ram}%"
            try: bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
            except: pass
            if SLACK_WEBHOOK_URL:
                try: requests.post(SLACK_WEBHOOK_URL, json={"text": msg})
                except: pass
        
        if counter % 5 == 0:
            _, issues = check_uptime()
            if issues:
                msg = "🚨 **Uptime Alert!**\n" + "\n".join(issues)
                try: bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
                except: pass
        counter += 1
        time.sleep(60)

# --- ממשק טלגרם ---

@bot.message_handler(commands=['start', 'manage'])
def manage_panel(message):
    if not is_authorized(message): return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("➕ הוסף אתר", callback_data="add_site"),
        types.InlineKeyboardButton("🗑️ הסר אתר", callback_data="remove_site"),
        types.InlineKeyboardButton("📋 סטטוס אתרים", callback_data="list_sites"),
        types.InlineKeyboardButton("🖥️ סטטוס שרת", callback_data="server_status"),
        types.InlineKeyboardButton("🔍 ניתוח לוגים (AI)", callback_data="analyze_logs"),
        types.InlineKeyboardButton("📈 גרף ביצועים", callback_data="send_graph")
    )
    bot.send_message(message.chat.id, "🛡️ **AutoSentinel Control Panel**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if str(call.from_user.id) != ADMIN_ID: return
    
    if call.data == "add_site":
        msg = bot.send_message(call.message.chat.id, "אנא שלח את כתובת ה-URL (כולל http/https):")
        bot.register_next_step_handler(msg, process_add_site)
        
    elif call.data == "remove_site":
        if not MONITORED_SITES:
            bot.send_message(call.message.chat.id, "אין אתרים ברשימה.")
            return
        menu = "בחר מספר אתר להסרה:\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(MONITORED_SITES)])
        msg = bot.send_message(call.message.chat.id, menu)
        bot.register_next_step_handler(msg, process_remove_site)
        
    elif call.data == "list_sites":
        report, _ = check_uptime()
        bot.send_message(call.message.chat.id, f"🌐 **Uptime Report:**\n\n{report}", parse_mode="Markdown")
        
    elif call.data == "server_status":
        cpu, ram = update_stats()
        insight = get_ai_analysis(cpu, ram)
        bot.send_message(call.message.chat.id, f"🖥 **סטטוס מערכת:**\nCPU: {cpu}% | RAM: {ram}%\n\n🤖 **תובנת AI:**\n{insight}", parse_mode="Markdown")
        
    elif call.data == "analyze_logs":
        bot.answer_callback_query(call.id, "מנתח לוגים...")
        logs = get_system_logs()
        analysis = analyze_logs_ai(logs)
        bot.send_message(call.message.chat.id, f"🔍 **ניתוח לוגים חכם:**\n\n{analysis}", parse_mode="Markdown")
        
    elif call.data == "send_graph":
        send_performance_graph(call.message)

def process_add_site(message):
    url = message.text.strip()
    if url.startswith("http"):
        if url not in MONITORED_SITES:
            MONITORED_SITES.append(url)
            save_site_to_file(url)
            bot.reply_to(message, f"✅ האתר {url} נוסף בהצלחה.")
        else:
            bot.reply_to(message, "האתר כבר קיים במערכת.")
    else:
        bot.reply_to(message, "URL לא תקין. וודא שהוא מתחיל ב-http.")

def process_remove_site(message):
    try:
        idx = int(message.text.strip()) - 1
        if 0 <= idx < len(MONITORED_SITES):
            removed = MONITORED_SITES.pop(idx)
            rewrite_sites_file(MONITORED_SITES)
            bot.reply_to(message, f"🗑️ {removed} הוסר מהרשימה.")
        else:
            bot.reply_to(message, "מספר לא קיים ברשימה.")
    except:
        bot.reply_to(message, "נא לשלוח מספר בלבד.")

def send_performance_graph(message):
    if len(cpu_history) < 2:
        bot.send_message(message.chat.id, "ממתין לאיסוף נתונים נוספים...")
        return
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_history, label='CPU %', color='red', marker='o')
    plt.plot(timestamps, ram_history, label='RAM %', color='blue', marker='o')
    plt.ylim(0, 100); plt.legend(); plt.grid(True); plt.title("System Resources Over Time")
    plt.savefig("graph.png"); plt.close()
    with open("graph.png", 'rb') as f:
        bot.send_photo(message.chat.id, f)

if __name__ == "__main__":
    threading.Thread(target=alert_monitor, daemon=True).start()
    print("🛡️ AutoSentinel V2.5 is Online")
    bot.infinity_polling()
