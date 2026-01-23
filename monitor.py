import time
import os
import psutil
import telebot
import threading
import socket
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# הגדרה מחדש של ה-AI בצורה שתואמת את העדכון האחרון
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    # כאן השתמשנו בשם המדויק והנקי שה-API דורש כרגע
    model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

def get_system_status_raw():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"CPU: {cpu}%, RAM: {mem}%, Disk: {disk}%"

def get_top_processes():
    processes = []
    for proc in psutil.process_iter(['name', 'memory_percent']):
        try: processes.append(proc.info)
        except: continue
    top_5 = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    res = "🔝 *תהליכים:* " + ", ".join([f"{p['name']} ({p['memory_percent']:.1f}%)" for p in top_5])
    return res

@bot.message_handler(commands=['analyze'])
def analyze_command(message):
    bot.reply_to(message, "🔍 מנתח נתונים בעברית...")
    status = get_system_status_raw()
    processes = get_top_processes()
    
    # הנחיה קצרה ופשוטה כדי למנוע שגיאות עיבוד
    prompt = f"נתח את הנתונים הבאים של השרת וענה בעברית בלבד ובקצרה: {status}. {processes}"
    
    try:
        # הוספת safety_settings למניעת חסימות מיותרות של ה-API
        response = model.generate_content(prompt)
        bot.send_message(CHAT_ID, f"🧠 *ניתוח AI:*\n\n{response.text}", parse_mode="Markdown")
    except Exception as e:
        # הדפסה מפורטת ללוגים כדי שנדע בדיוק מה גוגל אומרת
        print(f"DEBUG: {e}")
        bot.send_message(CHAT_ID, f"❌ שגיאה: {e}")

if __name__ == "__main__":
    print("🚀 AutoSentinel is LIVE")
    while True:
        try:
            bot.infinity_polling(timeout=20)
        except Exception:
            time.sleep(10)
