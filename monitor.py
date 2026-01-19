import psutil
import platform
import datetime

def check_system_health():
    # קבלת זמן נוכחי
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"--- AutoSentinel Report [{now}] ---")
    print(f"OS: {platform.system()} {platform.release()}")
    
    # בדיקת מעבד (CPU) - ממתין שנייה אחת כדי לקבל דגימה מדויקת
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    
    # בדיקת זיכרון (RAM)
    memory = psutil.virtual_memory()
    print(f"Memory Usage: {memory.percent}%")
    
    # בדיקת שטח דיסק (Disk)
    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent}%")
    
    # לוגיקה בסיסית להתראות (נרחיב אותה בהמשך לטלגרם)
    if cpu > 80:
        print("⚠️ ALERT: High CPU usage detected!")
    elif memory.percent > 90:
        print("⚠️ ALERT: Running out of memory!")
    else:
        print("✅ System Status: Healthy")

if __name__ == "__main__":
    check_system_health()
