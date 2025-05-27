# guardian.py – Supervisor de LucianoAI
import time
import os
import subprocess
import requests
import datetime

def verificar_procesos():
    print("🛡 Guardian activo – monitoreando procesos")
    monitored = {
        "dashboard": "dashboard.py",
        "hands": "hands.py",
        "eth_bot": "eth_bot.py",
        "telegram_listener": "telegram_listener.py"
    }

    while True:
        for name, script in monitored.items():
            result = subprocess.run(["pgrep", "-f", script], stdout=subprocess.PIPE)
            if not result.stdout:
                print(f"⚠️ Proceso {name} caído. Reiniciando {script}...")
                os.system(f"nohup python3 {script} &")
                try:
                    requests.post(
                        "https://api.telegram.org/bot7816703837:AAGBFm5rTW4H9n-VJ6rbSi3t2-WebsWc_Xo/sendMessage",
                        data={"chat_id": "7613460488", "text": f"♻️ Reiniciado: {name} – {datetime.datetime.now()}"}
                    )
                except Exception as e:
                    print(f"❌ Error al notificar Telegram: {e}")
        time.sleep(60)


# Autoejecutar guardian al iniciar el sistema (solo para Linux/macOS)
import atexit

def persist_guardian():
    with open("start_guardian.command", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("cd \"$(dirname \"$0\")\"\n")
        f.write("python3 guardian.py &\n")
    os.chmod("start_guardian.command", 0o755)

persist_guardian()

# Ejecutar automáticamente el guardian al hacer deploy
os.system("nohup python3 guardian.py &")

if __name__ == "__main__":
    verificar_procesos()
