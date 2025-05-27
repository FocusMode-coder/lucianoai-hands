from flask import Flask, render_template, request, jsonify
import json
import datetime
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    try:
        with open("status_log.json", "r") as f:
            estado = json.load(f)
    except:
        estado = {
            "luciano_ai": "No disponible",
            "bots_activos": [],
            "estado_telegram": "Desconocido",
            "mexc_balance": "???",
            "ultimas_ordenes": [],
            "stocks": {},
            "construccion": "No iniciado"
        }
    return render_template("dashboard.html", estado=estado)

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
        data = {
            "luciano_ai": "No disponible",
            "bots_activos": [],
            "estado_telegram": "Desconocido",
            "mexc_balance": "???",
            "ultimas_ordenes": [],
            "stocks": {},
            "construccion": "No iniciado"
        }
    return jsonify(data)

# Endpoint futuro para obtener estado real de MEXC (TODO)
# @app.route("/api_estado_mexc")
# def api_estado_mexc():
#     # TODO: Implementar lectura de balance real de MEXC usando API key almacenadas
#     return jsonify({"mexc_balance": "TODO"})

@app.route("/log")
def log():
    try:
        with open("system_log.txt", "r") as f:
            contenido = f.read()
    except:
        contenido = "No hay logs disponibles."
    return f"<pre>{contenido}</pre>"

if __name__ == "__main__":
    from threading import Thread
    def run_flask():
        app.run(host="0.0.0.0", port=10000)
    Thread(target=run_flask).start()
