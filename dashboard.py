from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/comando", methods=["POST"])
def comando():
    data = request.get_json()
    orden = data.get("orden", "")

    if orden == "crear_bot_ETH":
        resultado = "✅ Bot ETH creado en modo Sniper+Guardian"
    elif orden == "detener_bot_BTC":
        resultado = "🛑 Bot BTC detenido"
    elif orden == "activar_guardian":
        resultado = "🛡️ Modo Guardian activado"
    else:
        resultado = f"⚠️ Orden desconocida: {orden}"

    return jsonify({"status": "ok", "resultado": resultado})

@app.route("/status")
def status():
    try:
        with open("status_log.json", "r") as f:
            data = json.load(f)
    except:
        data = {"balance": "--", "orders": "--", "last_action": "Sin datos"}
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
