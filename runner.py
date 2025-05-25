from multiprocessing import Process
import os

def run_dashboard():
    print("🚀 Iniciando dashboard Flask...")
    os.system("python3 dashboard.py")

def run_listener():
    print("🧤 Iniciando manos ejecutoras...")
    os.system("python3 hands.py")

def run_updater():
    print("🔄 Activando update manager...")
    os.system("python3 update_manager.py")

def run_commander():
    print("🧠 Iniciando núcleo LucianoAI...")
    os.system("python3 openai_commander.py")

if __name__ == "__main__":
    print("⚡ LucianoAI Modo Dios corriendo...")
    Process(target=run_dashboard).start()
    Process(target=run_listener).start()
    Process(target=run_updater).start()
    Process(target=run_commander).start()
