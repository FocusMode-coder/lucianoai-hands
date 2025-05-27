import os
import requests
import zipfile
import io
import time

UPDATE_URL = os.getenv("UPDATE_URL", "")
AUTO_UPDATE = os.getenv("AUTO_UPDATE", "false").lower() == "true"

def download_and_extract_zip(url, extract_to="."):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(extract_to)
            print("✅ Update aplicado automáticamente desde:", url)
        else:
            print(f"❌ Error al descargar update ({response.status_code})")
    except Exception as e:
        print("❌ Excepción en update:", e)

if AUTO_UPDATE and UPDATE_URL:
    print("🔄 Auto-update activado. Verificando cada 30 min...")
    while True:
        download_and_extract_zip(UPDATE_URL)
        time.sleep(1800)  # 30 minutos
else:
    print("🟡 Auto-update desactivado o sin URL.")

    # Reparación automática si falla algún módulo clave
    try:
        import mexc_auth
        import eth_bot
    except ImportError as e:
        print("🛠 Detectado módulo faltante o corrupto:", e)
        if UPDATE_URL:
            print("🔁 Intentando reparar desde update URL...")
            download_and_extract_zip(UPDATE_URL)
            print("✅ Reparación forzada aplicada.")
        else:
            print("❗ No se pudo reparar: faltan URL de update.")
