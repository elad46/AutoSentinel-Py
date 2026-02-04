import os
import sqlite3
import psutil
import time
import threading
from datetime import datetime
from dotenv import load_dotenv
import telebot
import google.generativeai as genai

# טעינת הגדרות
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

# הגדרת ה-AI
genai.configure(api_key=GEMINI_KEY)
MODEL_NAME = 'gemini-2.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

bot = telebot.TeleBot(TOKEN)

# משתנה גלובלי לשמירת ה-ID שלך להתראות
MY_CHAT_ID = None

# --- פונקציות עזר ---

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

# --- מערכת התראות (רצה ברקע) ---

def monitor_loop():
    """בודק את השרת כל 5 דקות ושולח התראה אם יש עומס"""
    print("📢 Background monitoring thread started.")
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            save_to_db(cpu, ram)
            
            # אם ה-ID ידוע ויש עומס מעל 90%
            if MY_CHAT_ID and (cpu > 90 or ram > 95):
                alert_msg = f"⚠️ התראת עומס!\nCPU: {cpu}%\nRAM: {ram}%"
                bot.send_message(MY_CHAT_ID, alert_msg)
            
            time.sleep(300) # בדיקה כל 5 דקות
        except Exception as e:
            print(f"Monitor Loop Error: {e}")
            time.sleep(10)

# --- פקודות בוט ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global MY_CHAT_ID
    MY_CHAT_ID = message.chat.id
    print(f"📡 Chat ID linked: {MY_CHAT_ID}")
    welcome_text = (
        "הבוט הופעל בהצלחה! 🚀\n\n"
        "פקודות:\n"
        "/status - מצב שרת נוכחי\n"
        "/analyze - ניתוח AI חכם\n"
        "/graph - גרף ביצועים\n\n"
        "אני אשלח לך התראה אוטומטית אם העומס יעבור את ה-90%."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['status'])
def send_status(message):
    global MY_CHAT_ID
    MY_CHAT_ID = message.chat.id # עדכון ה-ID בכל פקודה ליתר ביטחון
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    save_to_db(cpu, ram)
    bot.reply_to(message, f"🖥 מצב שרת:\nCPU: {cpu}%\nRAM: {ram}%")

@bot.message_handler(commands=['analyze'])
def analyze_performance(message):
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stats ORDER BY timestamp DESC LIMIT 15")
        data = c.fetchall()
        conn.close()
        
        if not data:
            bot.reply_to(message, "אין מספיק נתונים בבסיס הנתונים.")
            return

        prompt = f"נתח בקצרה בעברית את הנתונים הבאים (בלי עיצוב Markdown): {str(data)}"
        response = model.generate_content(prompt)
        bot.reply_to(message, f"🤖 ניתוח AI:\n\n{response.text}")
    except Exception as e:
        bot.reply_to(message, f"❌ שגיאה בניתוח: {str(e)}")

@bot.message_handler(commands=['graph'])
def send_graph(message):
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stats ORDER BY timestamp DESC LIMIT 20")
        data = c.fetchall()[::-1]
        conn.close()
        
        if len(data) < 2:
            bot.reply_to(message, "צריך לפחות 2 נקודות נתונים לגרף.")
            return

        times = [d[0].split(' ')[1] for d in data]
        plt.figure(figsize=(10, 5))
        plt.plot(times, [d[1] for d in data], label='CPU %', color='red', marker='o')
        plt.plot(times, [d[2] for d in data], label='RAM %', color='blue', marker='s')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('status.png')
        plt.close()
        
        with open('status.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.reply_to(message, f"❌ שגיאה בגרף: {e}")

# --- הפעלה ---

if __name__ == "__main__":
    # הפעלת תהליך הניטור ברקע
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    
    print(f"✅ Bot is running with {MODEL_NAME}...")
    bot.infinity_polling()
