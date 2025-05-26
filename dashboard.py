from flask import Flask, render_template, request, jsonify
import json
import datetime
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/comando", methods=["POST"])
def comando():
    data = request.get_json()
    orden = data.get("orden", "")

    resultado = ""

    if orden == "crear_bot_ETH":
        resultado = "✅ Bot ETH creado en modo Sniper+Guardian"
        os.system("python3 bots/eth_bot.py &")
    elif orden == "crear_bot_BTC":
        resultado = "✅ Bot BTC creado en modo Sniper+Guardian"
        os.system("python3 bots/btc_bot.py &")
    elif orden == "detener_bot_BTC":
        resultado = "🛑 Bot BTC detenido"
        os.system("pkill -f btc_bot.py")
    elif orden == "detener_bot_ETH":
        resultado = "🛑 Bot ETH detenido"
        os.system("pkill -f eth_bot.py")
    elif orden == "activar_guardian":
        resultado = "🛡️ Modo Guardian activado"
        os.system("python3 guardian.py &")
    else:
        resultado = f"⚠️ Orden desconocida: {orden}"

    print(f"[{datetime.datetime.now()}] 🛰️ Orden recibida: {orden} → Respuesta: {resultado}")

    return jsonify({"status": "ok", "resultado": resultado})

@app.route("/status")
def status():
    try:
        with open("status_log.json", "r") as f:
            data = json.load(f)
    except:
        data = {"balance": "--", "orders": "--", "last_action": "Sin datos"}
    return jsonify(data)

@app.route("/log")
def log():
    try:
        with open("system_log.txt", "r") as f:
            contenido = f.read()
    except:
        contenido = "No hay logs disponibles."
    return f"<pre>{contenido}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
