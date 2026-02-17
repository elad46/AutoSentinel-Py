import os
import psutil
import telebot
from telebot import types
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

def create_status_graph():
    try:
        cpu_val = psutil.cpu_percent(interval=0.5)
        ram_val = psutil.virtual_memory().percent
        plt.figure(figsize=(6, 4))
        plt.bar(['CPU', 'RAM'], [cpu_val, ram_val], color=['orange', 'blue'])
        plt.ylim(0, 100)
        plt.title('System Metrics')
        graph_path = os.path.join(basedir, 'status.png')
        plt.savefig(graph_path)
        plt.close()
        return graph_path, cpu_val, ram_val
    except Exception as e:
        print(f"Graph Error: {e}")
        return None, psutil.cpu_percent(), psutil.virtual_memory().percent

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('📊 View Status', '🤖 AI Insights')
    bot.send_message(message.chat.id, "🛡️ **AutoSentinel-Py is Online**\nChoose an option:", reply_markup=markup, parse_mode='Markdown')

# טיפול גם בפקודה /status וגם בכפתור "View Status"
@bot.message_handler(commands=['status'])
@bot.message_handler(func=lambda m: 'Status' in m.text)
def show_status(message):
    bot.send_message(message.chat.id, "📊 Fetching live metrics...")
    graph, cpu, ram = create_status_graph()
    if graph:
        with open(graph, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=f"📉 CPU: {cpu}% | RAM: {ram}%")
    else:
        bot.send_message(message.chat.id, f"📈 CPU: {cpu}% | RAM: {ram}%")

# טיפול גם בפקודה /ai וגם בכפתור "AI Insights"
@bot.message_handler(commands=['ai'])
@bot.message_handler(func=lambda m: 'AI' in m.text)
def show_ai(message):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    status = "HEALTHY" if cpu < 70 else "UNDER LOAD"
    bot.send_message(message.chat.id, f"🧠 **AI Analysis:**\nStatus: {status}\nCPU: {cpu}%\nRAM: {ram}%", parse_mode='Markdown')

if __name__ == "__main__":
    print("✅ AutoSentinel is running! Press Ctrl+C to stop.")
    bot.polling(none_stop=True)
