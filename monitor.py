import os
import sqlite3
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import telebot
import google.generativeai as genai

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

# הגדרת ה-AI בשיטה הישנה והבטוחה
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

def save_to_db(cpu, ram):
    conn = sqlite3.connect('monitor_data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS stats (timestamp DATETIME, cpu REAL, ram REAL)")
    c.execute("INSERT INTO stats VALUES (?, ?, ?)", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cpu, ram))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['status'])
def send_status(message):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    save_to_db(cpu, ram)
    bot.reply_to(message, f"🖥 מצב שרת:\nCPU: {cpu}%\nRAM: {ram}%")

@bot.message_handler(commands=['graph'])
def send_graph(message):
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stats ORDER BY timestamp DESC LIMIT 20")
        data = c.fetchall()[::-1]
        conn.close()
        if len(data) < 2:
            bot.reply_to(message, "צריך עוד נתונים. תריץ /status.")
            return
        times = [d[0].split(' ')[1] for d in data]
        plt.figure(figsize=(10, 5))
        plt.plot(times, [d[1] for d in data], label='CPU', color='red')
        plt.plot(times, [d[2] for d in data], label='RAM', color='blue')
        plt.savefig('status.png')
        plt.close()
        with open('status.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.reply_to(message, f"טעות בגרף: {e}")

@bot.message_handler(commands=['analyze'])
def analyze_performance(message):
    try:
        conn = sqlite3.connect('monitor_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stats ORDER BY timestamp DESC LIMIT 10")
        data = c.fetchall()
        conn.close()
        
        prompt = f"נתח את הנתונים הבאים בקצרה בעברית: {str(data)}"
        response = model.generate_content(prompt)
        bot.reply_to(message, f"🤖 ניתוח AI:\n{response.text}")
    except Exception as e:
        bot.reply_to(message, f"❌ שגיאה: {str(e)}")

print("🚀 הבוט התחיל לעבוד בגרסה היציבה!")
bot.infinity_polling()
