import os
import telebot  # pip install pyTelegramBotAPI
import requests

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

print("🤖 Escuchando en Telegram...")
bot.polling()