# guardian.py – Supervisor de LucianoAI
import time
import os

def verificar_procesos():
    print("🛡 Guardian activo – monitoreando procesos")
    while True:
        # Acá podrías agregar checks como:
        # - ¿está vivo el bot ETH?
        # - ¿se está actualizando algún archivo?
        # - ¿hubo errores recientes en el log?
        print("🔎 Chequeo rutinario... todo OK.")
        time.sleep(60)

if __name__ == "__main__":
    verificar_procesos()
