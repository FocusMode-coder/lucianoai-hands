import subprocess
import time
from datetime import datetime
from multiprocessing import Process
import os
from hands import loop_estado

def log_global(msg):
    with open("system_log.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def run_dashboard():
    print("🚀 Iniciando dashboard Flask...")
    try:
        subprocess.run(["python3", "dashboard.py"], check=True)
        log_global("🚀 Dashboard iniciado")
    except Exception as e:
        log_global(f"❌ Error en dashboard: {e}")

def run_listener():
    print("🧤 Iniciando manos ejecutoras...")
    try:
        subprocess.run(["python3", "hands.py"], check=True)
        log_global("🧤 Manos ejecutoras iniciadas")
    except Exception as e:
        log_global(f"❌ Error en manos: {e}")

def run_updater():
    print("🔄 Activando update manager...")
    try:
        subprocess.run(["python3", "update_manager.py"], check=True)
        log_global("🔄 Update manager iniciado")
    except Exception as e:
        log_global(f"❌ Error en update manager: {e}")

def run_commander():
    print("🧠 Iniciando núcleo LucianoAI...")
    try:
        subprocess.run(["python3", "openai_commander.py"], check=True)
        log_global("🧠 Núcleo LucianoAI iniciado")
    except Exception as e:
        log_global(f"❌ Error en núcleo: {e}")

def run_status_loop():
    print("📡 Iniciando loop de estado...")
    from hands import loop_estado
    loop_estado()

# --- New bot runners ---
def run_eth_bot():
    print("🚀 Ejecutando ETH Bot...")
    try:
        subprocess.run(["python3", "eth_bot.py"], check=True)
        log_global("🚀 ETH Bot iniciado")
    except Exception as e:
        log_global(f"❌ Error en ETH Bot: {e}")

def run_btc_bot():
    print("🚀 Ejecutando BTC Bot...")
    try:
        subprocess.run(["python3", "btc_bot.py"], check=True)
        log_global("🚀 BTC Bot iniciado")
    except Exception as e:
        log_global(f"❌ Error en BTC Bot: {e}")

def check_env():
    critical_vars = [
        "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID",
        "OPENAI_API_KEY", "MEXC_API_KEY", "MEXC_SECRET_KEY"
    ]
    for var in critical_vars:
        if not os.getenv(var):
            log_global(f"⚠️ Variable de entorno faltante: {var}")

def guardian_loop():
    print("🛡️ Guardian activo. Monitoreando procesos...")
    log_global("🛡️ Guardian iniciado")
    while True:
        time.sleep(120)

if __name__ == "__main__":
    print("⚡ LucianoAI Modo Dios corriendo...")
    check_env()
    Process(target=run_dashboard).start()
    Process(target=run_listener).start()
    Process(target=run_updater).start()
    Process(target=run_commander).start()
    Process(target=run_status_loop).start()
    Process(target=guardian_loop).start()
    Process(target=run_eth_bot).start()
    Process(target=run_btc_bot).start()
