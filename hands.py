from openai_commander import ask_luciano_ai
import os

def execute_task(task):
    print(f"🤖 Ejecutando: {task}")
    if task == "crear_bot_ETH":
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
    elif task == "detener_bot_BTC":
        print("🛑 Bot BTC detenido.")
    elif task == "activar_guardian":
        print("🛡️ Modo Guardian activado.")
    else:
        print(f"⚠️ Tarea desconocida: {task}")

if __name__ == "__main__":
    print("🧤 Manos ACTIVAS esperando órdenes.")
    # Ejemplo estático de ejecución (puede reemplazarse con input dinámico o loop)
    execute_task("crear_bot_ETH")
