import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# יצירת לקוח עם הגדרות 2026
client = genai.Client(api_key=GEMINI_KEY)

# רשימת המודלים המעודכנת ביותר
models_to_test = [
    "gemini-3-flash-preview",  # המודל החדש שראינו אצלך במסך
    "gemini-2.0-flash",        # הגרסה היציבה הנוכחית
    "gemini-flash-latest"      # הקיצור שגוגל תמיד מעדכנת
]

print("🚀 בודק מודלים מעודכנים...")

for model in models_to_test:
    print(f"--- מנסה את: {model} ---")
    try:
        response = client.models.generate_content(
            model=model,
            contents="תגיד שלום בעברית"
        )
        print(f"✅ הצלחה! המודל {model} עובד.")
        print(f"תגובה: {response.text}")
        break
    except Exception as e:
        print(f"❌ {model} נכשל: {e}\n")
