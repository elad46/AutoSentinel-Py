import os
import psutil
import telebot
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

@bot.message_handler(commands=['analyze'])
def analyze_command(message):
    status = get_system_status_raw()
    sent_msg = bot.reply_to(message, "🤖 מנתח את הנתונים עם Gemini 3... רק רגע")
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"נתח את מצב השרת הבא והשב בעברית קצרה: {status}"
        )
        bot.edit_message_text(f"✅ **ניתוח AI (Gemini 3):**\n\n{response.text}", 
                             chat_id=message.chat.id, 
                             message_id=sent_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ שגיאה: {e}", 
                             chat_id=message.chat.id, 
                             message_id=sent_msg.message_id)

if __name__ == "__main__":
    print("🚀 הבוט החדש (Gemini 3) רץ...")
    bot.infinity_polling()
