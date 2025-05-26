

import os
import time
import requests

MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_SECRET_KEY = os.getenv("MEXC_SECRET_KEY")

SYMBOL = "BTCUSDT"

def get_market_price():
    try:
        response = requests.get(f"https://api.mexc.com/api/v3/ticker/price?symbol={SYMBOL}")
        return float(response.json()["price"])
    except Exception as e:
        print(f"[BTC BOT] Error getting price: {e}")
        return None

def make_trade():
    print("[BTC BOT] Ejecutando lógica de trading para BTC...")
    price = get_market_price()
    if price is None:
        print("[BTC BOT] Precio no disponible, abortando operación.")
        return
    # Lógica de ejemplo (futura mejora: señales, volumen, whale tracking, etc.)
    if price < 60000:  # Simulación de compra
        print(f"[BTC BOT] Precio actual ${price} parece bajo. Ejecutando COMPRA.")
    elif price > 68000:  # Simulación de venta
        print(f"[BTC BOT] Precio actual ${price} parece alto. Ejecutando VENTA.")
    else:
        print(f"[BTC BOT] Precio estable (${price}), esperando mejor señal.")

if __name__ == "__main__":
    print("[BTC BOT] Iniciando BTC Bot en modo sniper+guardian...")
    while True:
        make_trade()
        time.sleep(60)