import os
import psutil
import telebot
import matplotlib
matplotlib.use('Agg') # פותר את בעיית ה"אין מסך" בדוקר
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ADMIN_ID = os.getenv("ADMIN_ID")

# רשימות לנתונים
cpu_history = []
ram_history = []
timestamps = []

def update_stats():
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

@bot.message_handler(commands=['status'])
def send_status(message):
    if str(message.from_user.id) != ADMIN_ID: return
    cpu, ram = update_stats()
    bot.reply_to(message, f"🖥 CPU: {cpu}% | RAM: {ram}%")

@bot.message_handler(commands=['graph'])
def send_graph(message):
    if str(message.from_user.id) != ADMIN_ID: return
    if len(cpu_history) < 2:
        update_stats()
        bot.reply_to(message, "⏳ אוסף דגימות... נסה שוב בעוד 10 שניות.")
        return

    # יצירת התמונה
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_history, label='CPU %', color='blue', marker='o')
    plt.plot(timestamps, ram_history, label='RAM %', color='green', marker='s')
    plt.title('Server Performance')
    plt.legend()
    plt.grid(True)
    
    plt.savefig("graph.png")
    plt.close()
    
    # שליחת התמונה
    with open("graph.png", 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="📊 גרף ביצועים בזמן אמת")

print("Bot is up!")
bot.infinity_polling()
