import os
from dotenv import load_dotenv
load_dotenv()
import telebot  # pip install pyTelegramBotAPI
import requests
from flask import Flask, request

API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

def ask_luciano(prompt):
    try:
        response = requests.post(
            "http://localhost:10001/comando",  # Asegurate de que este puerto esté bien
            json={"orden": prompt}
        )
        return response.json().get("resultado", "⚠️ No hubo respuesta.")
    except Exception as e:
        return f"❌ Error: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    if user_input.lower() in ["/status", "/reiniciar", "/asistencia"]:
        bot.reply_to(message, f"🧠 Comando recibido: {user_input}")
        requests.post("http://localhost:10001/comando", json={"orden": user_input})
        return
    if message.chat.id != int(CHAT_ID):
        bot.reply_to(message, "⛔ No autorizado.")
        return
    respuesta = ask_luciano(user_input)
    bot.reply_to(message, respuesta)

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-render-url.onrender.com")

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🤖 Webhook configurado y escuchando en Flask...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10001)))