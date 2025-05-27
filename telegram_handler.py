import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_USE_WEBHOOK = os.getenv("TELEGRAM_USE_WEBHOOK", "false").lower() == "true"
TELEGRAM_WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")

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


# Webhook configuration function
def set_telegram_webhook():
    if TELEGRAM_USE_WEBHOOK and TELEGRAM_WEBHOOK_URL:
        print("🔧 Configurando webhook de Telegram...")
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        data = {"url": TELEGRAM_WEBHOOK_URL}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Webhook configurado correctamente.")
            else:
                print("❌ Error al configurar webhook:", response.text)
        except Exception as e:
            print("❌ Excepción al configurar webhook:", e)



# Run webhook setup if executed directly
if __name__ == "__main__":
    set_telegram_webhook()
