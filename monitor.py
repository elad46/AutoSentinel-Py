import os
import psutil
import telebot
import platform
from datetime import datetime
from google import genai
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3-flash-preview"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_KEY, http_options={'api_version': 'v1beta'})

def get_system_status_raw():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = (
        "🚀 *AutoSentinel AI v2.1*\n\n"
        "פקודות זמינות:\n"
        "/status - מצב חומרה מהיר\n"
        "/analyze - ניתוח AI מעמיק\n"
        "/info - פרטי שרת מלאים\n"
        "/top - צריכת משאבים לפי אפליקציות"
    )
    bot.reply_to(message, msg, parse_mode='Markdown')

@bot.message_handler(commands=['top'])
def top_command(message):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        processes.append(proc.info)
    
    # מיון לפי צריכת זיכרון והצגת ה-3 המובילים
    top_procs = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:3]
    
    response = "🔝 *צריכת משאבים מובילה:*\n"
    for p in top_procs:
        response += f"🔹 {p['name']}: {p['memory_percent']:.1f}% RAM\n"
    
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(commands=['info'])
def info_command(message):
    uname = platform.uname()
    uptime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    info_text = (
        f"🖥️ *פרטי שרת:*\n"
        f"מערכת: {uname.system}\n"
        f"שם שרת: {uname.node}\n"
        f"גרסת קרנל: {uname.release}\n"
        f"זמן עליה: {uptime}"
    )
    bot.reply_to(message, info_text, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    bot.reply_to(message, f"📊 מצב שרת נוכחי:\n{get_system_status_raw()}")

@bot.message_handler(commands=['analyze'])
def analyze_command(message):
    status = get_system_status_raw()
    sent_msg = bot.reply_to(message, "🤖 מנתח את הנתונים עם Gemini 3... רק רגע")
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"נתח את מצב השרת הבא והשב בעברית קצרה ומקצועית: {status}"
        )
        bot.edit_message_text(f"✅ **ניתוח AI (Gemini 3):**\n\n{response.text}", 
                             chat_id=message.chat.id, 
                             message_id=sent_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ שגיאה: {e}", 
                             chat_id=message.chat.id, 
                             message_id=sent_msg.message_id)

if __name__ == "__main__":
    bot.infinity_polling()
