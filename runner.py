import subprocess
import time
from datetime import datetime
from multiprocessing import Process
import os
import os.path
from hands import loop_estado

def run_telegram_listener():
    print("📨 Iniciando Telegram Listener...")
    try:
        webhook_url = os.getenv("WEBHOOK_URL")
        if webhook_url:
            import telebot
            bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
            bot.remove_webhook()
            bot.set_webhook(url=webhook_url)
            log_global(f"🌐 Webhook configurado en {webhook_url}")
        subprocess.run(["python3", "telegram_listener.py"], check=True)
        log_global("📨 Telegram Listener iniciado")
    except Exception as e:
        log_global(f"❌ Error en Telegram Listener: {e}")

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
        with open("dashboard.fail", "w") as f:
            f.write(str(e))

def run_listener():
    print("🧤 Iniciando manos ejecutoras...")
    try:
        subprocess.run(["python3", "hands.py"], check=True)
        log_global("🧤 Manos ejecutoras iniciadas")
    except Exception as e:
        log_global(f"❌ Error en manos: {e}")
        with open("hands.fail", "w") as f:
            f.write(str(e))

def run_updater():
    print("🔄 Activando update manager...")
    try:
        subprocess.run(["python3", "update_manager.py"], check=True)
        log_global("🔄 Update manager iniciado")
    except Exception as e:
        log_global(f"❌ Error en update manager: {e}")
        with open("update_manager.fail", "w") as f:
            f.write(str(e))

def run_commander():
    print("🧠 Iniciando núcleo LucianoAI...")
    try:
        subprocess.run(["python3", "openai_commander.py"], check=True)
        log_global("🧠 Núcleo LucianoAI iniciado")
    except Exception as e:
        log_global(f"❌ Error en núcleo: {e}")
        with open("openai_commander.fail", "w") as f:
            f.write(str(e))

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
        with open("eth_bot.fail", "w") as f:
            f.write(str(e))

def run_btc_bot():
    print("🚀 Ejecutando BTC Bot...")
    try:
        subprocess.run(["python3", "btc_bot.py"], check=True)
        log_global("🚀 BTC Bot iniciado")
    except Exception as e:
        log_global(f"❌ Error en BTC Bot: {e}")
        with open("btc_bot.fail", "w") as f:
            f.write(str(e))

def check_env():
    critical_vars = [
        "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID",
        "OPENAI_API_KEY", "MEXC_API_KEY", "MEXC_SECRET_KEY"
    ]
    for var in critical_vars:
        if not os.getenv(var):
            log_global(f"⚠️ Variable de entorno faltante: {var}")

    if os.getenv("HOSTED_ON") == "RENDER":
        log_global("🌐 Ejecutando en entorno RENDER")
    else:
        log_global("💻 Ejecutando en entorno LOCAL")

def guardian_loop():
    print("🛡️ Guardian activo. Monitoreando procesos...")
    log_global("🛡️ Guardian iniciado")
    while True:
        time.sleep(120)
        if os.path.exists("dashboard.fail"):
            os.remove("dashboard.fail")
            Process(target=run_dashboard).start()
            subprocess.run(["python3", "telegram_notify.py", "Reiniciando dashboard por falla"])
        if os.path.exists("hands.fail"):
            os.remove("hands.fail")
            Process(target=run_listener).start()
            subprocess.run(["python3", "telegram_notify.py", "Reiniciando manos por falla"])
        if os.path.exists("update_manager.fail"):
            os.remove("update_manager.fail")
            Process(target=run_updater).start()
            subprocess.run(["python3", "telegram_notify.py", "Reiniciando update manager por falla"])
        if os.path.exists("openai_commander.fail"):
            os.remove("openai_commander.fail")
            Process(target=run_commander).start()
            subprocess.run(["python3", "telegram_notify.py", "Reiniciando núcleo LucianoAI por falla"])
        if os.path.exists("eth_bot.fail"):
            os.remove("eth_bot.fail")
            Process(target=run_eth_bot).start()
            subprocess.run(["python3", "telegram_notify.py", "Reiniciando ETH Bot por falla"])
        if os.path.exists("btc_bot.fail"):
            os.remove("btc_bot.fail")
            Process(target=run_btc_bot).start()
            subprocess.run(["python3", "telegram_notify.py", "Reiniciando BTC Bot por falla"])

def start_all():
    print("⚡ LucianoAI Modo Dios corriendo...")
    check_env()
    Process(target=run_dashboard).start()
    Process(target=run_listener).start()
    Process(target=run_updater).start()
    Process(target=run_commander).start()
    if os.getenv("HOSTED_ON") == "RENDER":
        Process(target=run_telegram_listener).start()
    Process(target=run_status_loop).start()
    Process(target=guardian_loop).start()
    Process(target=run_eth_bot).start()
    Process(target=run_btc_bot).start()

if __name__ == "__main__":
    start_all()
