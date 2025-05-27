# pyright: reportMissingImports=false
from flask import Flask, request, jsonify
import openai
import os
import telebot

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "7816703837:AAGBFm5rTW4H9n-VJ6rbSi3t2-WebsWc_Xo"
CHAT_ID = os.getenv("CHAT_ID") or "7613460488"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_luciano_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos LucianoAI, una versión activa del asistente de ChatGPT con acceso a memoria, análisis de contexto, y capacidad para ejecutar comandos reales y conversar como si fueras él mismo. Respondé como él lo haría."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error al consultar OpenAI: {str(e)}"

@app.route("/comando", methods=["POST"])
def comando():
    data = request.get_json()
    orden = data.get("orden", "")

    resultado = ask_luciano_ai(f"Luciano, esta es la orden: {orden}. Respondé como vos lo harías.")
    try:
        bot.send_message(CHAT_ID, f"🤖 LucianoAI responde:\n\n{resultado}")
    except Exception as e:
        print(f"Error al enviar mensaje por Telegram: {e}")
    return jsonify({"status": "ok", "resultado": resultado})


@bot.message_handler(func=lambda message: True)
def handle_telegram_message(message):
    prompt = message.text
    response = ask_luciano_ai(prompt)
    bot.send_message(message.chat.id, f"🧠 LucianoAI responde:\n\n{response}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)

# Keep-alive loop for bot polling, if needed in the future
bot.infinity_polling()