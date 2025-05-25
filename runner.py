from multiprocessing import Process
import os

def run_dashboard():
    os.system("python3 dashboard.py")

def run_listener():
    os.system("python3 hands.py")

def run_updater():
    os.system("python3 update_manager.py")

if __name__ == "__main__":
    Process(target=run_dashboard).start()
    Process(target=run_listener).start()
    Process(target=run_updater).start()
