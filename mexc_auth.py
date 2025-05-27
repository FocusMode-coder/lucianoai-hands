import os
import hmac
import hashlib
import time
import requests

API_KEY = os.getenv("MEXC_API_KEY", "").strip()
SECRET_KEY = os.getenv("MEXC_SECRET_KEY", "").strip()

if not API_KEY or not SECRET_KEY:
    raise EnvironmentError("🔐 Claves MEXC no encontradas. Asegurate de cargar MEXC_API_KEY y MEXC_SECRET_KEY en Render → Environment.")

BASE_URL = os.getenv("MEXC_API_URL", "https://api.mexc.com")

def sign_params(params):
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY no está definido. Verificá el archivo .env y asegúrate de hacer el deploy con las variables de entorno correctas.")
    query = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"

def get_timestamp():
    return str(int(time.time() * 1000))

def get_account_info():
    path = "/api/v3/account"
    params = {
        "timestamp": get_timestamp()
    }
    signed_query = sign_params(params)
    url = f"{BASE_URL}{path}?{signed_query}"
    headers = {
        "X-MEXC-APIKEY": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if "balances" in data:
            return {"balance": sum(float(asset["free"]) for asset in data["balances"] if float(asset["free"]) > 0)}
        else:
            print(f"⚠️ Error: Clave 'balances' no encontrada en la respuesta. Respuesta completa: {data}")
            return {"balance": "???"}
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener cuenta MEXC: {e}")
        return {"balance": "???"}
