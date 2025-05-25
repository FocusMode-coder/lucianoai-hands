import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def notify_user(message):
    print(f"📩 Telegram message: {message}")
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code != 200:
                print("❌ Error al enviar mensaje:", response.text)
        except Exception as e:
            print("❌ Excepción al enviar mensaje:", e)
    else:
        print("⚠️ TELEGRAM_TOKEN o CHAT_ID no configurados")
