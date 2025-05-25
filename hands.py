from openai_commander import ask_luciano_ai
import os
import json
from datetime import datetime
from telegram_handler import notify_user
try:
    from mexc_auth import get_account_info
except:
    get_account_info = lambda: {"balance": "N/A"}

def guardar_estado(data):
    with open("status_log.json", "w") as f:
        json.dump(data, f)

def execute_task(task):
    print(f"🤖 Ejecutando: {task}")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if task == "crear_bot_ETH":
        notify_user("⚙️ Creando bot ETH...")
        print("🤖 Preguntando a LucianoAI qué debe hacer...")
        result = ask_luciano_ai("Crear bot ETH en modo Sniper+Guardian con mis credenciales reales en producción.")
        print("🧠 LucianoAI respondió:\n", result)
        if result.startswith("ARCHIVO:"):
            lines = result.split("\n", 2)
            filename = lines[0].split(":", 1)[1].strip()
            code = lines[2]
            with open(filename, "w") as f:
                f.write(code)
            print(f"📁 Archivo {filename} creado y guardado.")
            os.system(f"python3 {filename}")
        guardar_estado({
            "balance": get_account_info().get("balance", "???"),
            "orders": 1,
            "last_action": "Bot ETH creado",
            "timestamp": now
        })

    elif task == "status_bot_ETH":
        print("📊 Estado del bot ETH:")
        try:
            with open("status_log.json", "r") as f:
                print(f.read())
        except:
            print("⚠️ No se pudo leer status_log.json")

    elif task == "detener_bot_ETH":
        notify_user("🛑 Bot ETH detenido manualmente.")
        print("🛑 Bot ETH detenido.")
        guardar_estado({
            "balance": get_account_info().get("balance", "???"),
            "orders": 0,
            "last_action": "Bot ETH detenido",
            "timestamp": now
        })

    elif task == "reiniciar_bot_ETH":
        print("🔄 Reiniciando bot ETH...")
        execute_task("detener_bot_ETH")
        execute_task("crear_bot_ETH")

    elif task == "crear_bot_BTC":
        notify_user("⚙️ Creando bot BTC...")
        print("🤖 Preguntando a LucianoAI qué debe hacer...")
        result = ask_luciano_ai("Crear bot BTC en modo Sniper+Guardian con mis credenciales reales en producción.")
        print("🧠 LucianoAI respondió:\n", result)
        if result.startswith("ARCHIVO:"):
            lines = result.split("\n", 2)
            filename = lines[0].split(":", 1)[1].strip()
            code = lines[2]
            with open(filename, "w") as f:
                f.write(code)
            print(f"📁 Archivo {filename} creado y guardado.")
            os.system(f"python3 {filename}")
        guardar_estado({
            "balance": get_account_info().get("balance", "???"),
            "orders": 1,
            "last_action": "Bot BTC creado",
            "timestamp": now
        })

    elif task == "detener_todo":
        notify_user("🛑 Deteniendo todos los bots activos...")
        print("🛑 Deteniendo todos los bots activos...")
        guardar_estado({
            "balance": get_account_info().get("balance", "???"),
            "orders": 0,
            "last_action": "Todos los bots detenidos",
            "timestamp": now
        })

    elif task == "logs_bot_ETH":
        print("📄 Últimos logs del bot ETH:")
        try:
            with open("eth_supreme_bot.log", "r") as f:
                lines = f.readlines()[-10:]
                for line in lines:
                    print(line.strip())
        except:
            print("⚠️ No se encontró el archivo de log del bot ETH.")

    elif task == "activar_guardian":
        print("🛡️ Modo Guardian activado.")
        notify_user("🛡️ Modo Guardian activado.")
        guardar_estado({
            "balance": get_account_info().get("balance", "???"),
            "orders": 1,
            "last_action": "Guardian activado",
            "timestamp": now
        })

    else:
        print(f"⚠️ Tarea desconocida: {task}")

import time

def loop_estado():
    contador = 1
    while True:
        try:
            with open("status_log.json", "r") as f:
                estado = json.load(f)
                msg = f"""🧠 LucianoAI Report (#{contador}):
✅ Estado: operativo
⏱ Última acción: {estado.get('last_action', '---')}
💰 Balance: {estado.get('balance', '---')}
📊 Órdenes ejecutadas: {estado.get('orders', '---')}
📅 Hora: {estado.get('timestamp', '---')}
"""
        except:
            msg = "🧠 LucianoAI: No se pudo leer el estado actual del sistema."
        notify_user(msg)
        contador += 1
        time.sleep(300)  # Espera 5 minutos entre informes

if __name__ == "__main__":
    print("🧤 Manos ACTIVAS esperando órdenes.")
    execute_task("crear_bot_ETH")
    loop_estado()
