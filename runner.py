# runner.py – loop principal
import time
from hands import execute_task

while True:
    # Simula una tarea entrante
    execute_task("crear_bot_eth")
    time.sleep(60)
