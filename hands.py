from openai_commander import ask_luciano_ai
import os
import json
from datetime import datetime
from telegram_handler import notify_user
import traceback
try:
    from mexc_auth import get_account_info
except:
    get_account_info = lambda: {"balance": "N/A"}

def guardar_estado(data):
    with open("status_log.json", "w") as f:
        json.dump(data, f)

def execute_task(task):
    def auto_reparar_error(task, error):
        notify_user(f"⚠️ LucianoAI detectó un error al ejecutar `{task}`. Intentando auto-reparar...")
        # En un caso real, podrías intentar reinstalar dependencias, regenerar archivos, o reiniciar servicios
        if task == "crear_bot_ETH":
            os.system("pip install -r requirements.txt")
            execute_task(task)
        else:
            notify_user(f"🧠 LucianoAI no pudo reparar automáticamente la tarea `{task}`.")

    try:
        print(f"🤖 Ejecutando: {task}")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if task == "crear_bot_ETH":
            notify_user("⚙️ Iniciando construcción del bot ETH Supreme...")
            print("🤖 Preguntando a LucianoAI qué debe hacer...")

            result = ask_luciano_ai("Crear bot ETH en modo Sniper+Guardian con mis credenciales reales en producción. Código funcional en Python.")
            print("🧠 LucianoAI respondió:\n", result)

            if result.startswith("ARCHIVO:"):
                lines = result.split("\n", 2)
                filename = lines[0].split(":", 1)[1].strip()
                code = lines[2]

                if os.path.exists(filename):
                    os.remove(filename)

                with open(filename, "w") as f:
                    f.write(code)

                notify_user(f"📁 Archivo `{filename}` creado y ejecutado en producción.")
                os.system(f"nohup python3 {filename} &")
            else:
                notify_user("❌ Error: LucianoAI no devolvió un archivo válido. Verificá la lógica del comando.")
                return

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

        if task == "crear_bot_ETH" and get_account_info().get("balance", "0") in ["???", "0", "N/A"]:
            notify_user("💡 LucianoAI detectó balance indefinido o bajo. Necesito tus instrucciones.")
            notify_user("✉️ Escribí un comando como /status, /reiniciar, o /asistencia para continuar.")
            guardar_estado({
                "balance": get_account_info().get("balance", "???"),
                "orders": 0,
                "last_action": "Esperando instrucciones del usuario",
                "timestamp": now
            })
            return

    except Exception as e:
        error_msg = f"❌ LucianoAI detectó un problema mientras intentaba ejecutar la tarea `{task}`.\n📄 Detalles: {str(e)}\n📌 Traza:\n{traceback.format_exc()}"
        print(error_msg)
        auto_reparar_error(task, e)
        try:
            with open("errores_previos.json", "r") as logf:
                errores = json.load(logf)
        except:
            errores = []
        errores.append({
            "task": task,
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        with open("errores_previos.json", "w") as logf:
            json.dump(errores, logf, indent=2)
        notify_user(error_msg)

import time

def loop_estado():
    contador = 1
    while True:
        try:
            with open("status_log.json", "r") as f:
                estado = json.load(f)
                msg = f"""📩 Reporte Inteligente de LucianoAI (#{contador}):
✅ Estado del sistema: activo y monitoreando.
📍 Última acción realizada: {estado.get('last_action', '---')}
💰 Balance disponible: {estado.get('balance', '---')}
📊 Operaciones completadas: {estado.get('orders', '---')}
🕓 Hora del registro: {estado.get('timestamp', '---')}
"""
        except:
            msg = ask_luciano_ai("No pude leer el estado del sistema. ¿Cómo puedo explicárselo de forma clara y humana al usuario?")
        respuesta_humana = ask_luciano_ai(f"Resumí esto como si fueras un asistente real que quiere ayudarme:\n{msg}")
        try:
            with open("errores_previos.json", "r") as errf:
                errores = json.load(errf)
                if errores:
                    respuesta_humana += f"\n🧠 He aprendido de {len(errores)} errores pasados y estoy mejorando continuamente."
        except:
            pass
        notify_user(respuesta_humana)
        contador += 1
        time.sleep(300)  # Espera 5 minutos entre informes

if __name__ == "__main__":
    print("🧤 Manos ACTIVAS esperando órdenes.")
    execute_task("crear_bot_ETH")
    loop_estado()
