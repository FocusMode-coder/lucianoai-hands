# pyright: reportMissingImports=false
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_luciano_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos LucianoAI, un arquitecto de bots."},
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

    resultado = ask_luciano_ai(f"Ejecutar esta orden: {orden}")

    return jsonify({"status": "ok", "resultado": resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)