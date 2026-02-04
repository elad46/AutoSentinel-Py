import os
import sqlite3
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import telebot
import google.generativeai as genai

# טעינת משתני סביבה
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

# הגדרת ה-AI עם המודל הספציפי שעובד בחשבון שלך
genai.configure(api_key=GEMINI_KEY)
MODEL_NAME = 'gemini-2.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

bot = telebot.TeleBot(TOKEN)

def save_to_db(cpu, ram):
    """שמירת נתונים לבסיס הנתונים"""
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS stats (timestamp DATETIME, cpu REAL, ram REAL)")
        c.execute("INSERT INTO stats VALUES (?, ?, ?)", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cpu, ram))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving to DB: {e}")

@bot.message_handler(commands=['status'])
def send_status(message):
    """שליחת מצב שרת נוכחי"""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    save_to_db(cpu, ram)
    response = f"🖥 מצב שרת נוכחי:\n\nCPU: {cpu}%\nRAM: {ram}%"
    bot.reply_to(message, response)

@bot.message_handler(commands=['graph'])
def send_graph(message):
    """יצירת גרף ביצועים ושליחתו"""
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stats ORDER BY timestamp DESC LIMIT 20")
        data = c.fetchall()[::-1]
        conn.close()
        
        if len(data) < 2:
            bot.reply_to(message, "צריך לפחות 2 נקודות נתונים. תריץ /status כמה פעמים.")
            return

        times = [d[0].split(' ')[1] for d in data]
        cpus = [d[1] for d in data]
        rams = [d[2] for d in data]

        plt.figure(figsize=(10, 5))
        plt.plot(times, cpus, label='CPU %', color='red', marker='o')
        plt.plot(times, rams, label='RAM %', color='blue', marker='s')
        plt.title('Server Performance (Last 20 checks)')
        plt.ylabel('Percentage')
        plt.xlabel('Time')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('status.png')
        plt.close()
        
        with open('status.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="📈 גרף ביצועים אחרונים")
    except Exception as e:
        bot.reply_to(message, f"❌ שגיאה ביצירת גרף: {e}")

@bot.message_handler(commands=['analyze'])
def analyze_performance(message):
    """ניתוח נתונים באמצעות Gemini"""
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stats ORDER BY timestamp DESC LIMIT 15")
        data = c.fetchall()
        conn.close()
        
        if not data:
            bot.reply_to(message, "אין נתונים לניתוח. תריץ קודם /status.")
            return

        prompt = f"נתח את נתוני השרת הבאים ותן סיכום קצר בעברית. אל תשתמש בעיצוב מיוחד (בלי כוכביות): {str(data)}"
        response = model.generate_content(prompt)
        
        # שלח כטקסט פשוט כדי למנוע שגיאות Parse של טלגרם
        bot.reply_to(message, f"🤖 ניתוח AI ({MODEL_NAME}):\n\n{response.text}")
    except Exception as e:
        bot.reply_to(message, f"❌ שגיאה בניתוח AI: {str(e)}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "ברוך הבא לבוט המוניטור! 🚀\n\n"
        "פקודות זמינות:\n"
        "/status - הצגת עומס נוכחי\n"
        "/graph - הצגת גרף היסטורי\n"
        "/analyze - ניתוח חכם ע\"י AI"
    )
    bot.reply_to(message, help_text)

if __name__ == "__main__":
    print(f"✅ Bot is running with model: {MODEL_NAME}")
    print("Press Ctrl+C to stop.")
    bot.infinity_polling()
