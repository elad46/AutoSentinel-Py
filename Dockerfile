# שימוש בתמונה רשמית וקלה של פייתון
FROM python:3.12-slim

# הגדרת תיקיית עבודה בתוך הקונטיינר
WORKDIR /app

# התקנת תלויות מערכת שדרושות לגרפים (Matplotlib)
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# העתקת קובץ הדרישות
COPY requirements.txt .

# התקנת הספריות של הפרויקט
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל שאר קבצי הפרויקט לתוך התיקייה
COPY . .

# פקודה להרצת הבוט
CMD ["python", "monitor.py"]
