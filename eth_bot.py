# ETH Bot real – Modo Sniper + Guardian + Whale
import time
import requests
import traceback

TELEGRAM_TOKEN = "7816703837:AAGBFm5rTW4H9n-VJ6rbSi3t2-WebsWc_Xo"
CHAT_ID = "7613460488"

def enviar_mensaje_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensaje}
    requests.post(url, data=data)

def obtener_precio_eth():
    try:
        url = "https://api.mexc.com/api/v3/ticker/price?symbol=ETHUSDT"
        response = requests.get(url)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        raise Exception(f"Error al obtener precio ETH: {str(e)}")

def ejecutar_orden_mexc(side, cantidad=0.01):
    try:
        import hmac, hashlib, time
        API_KEY = "mx0vglkIg3tLCl4h2A"
        SECRET_KEY = "fa88e2a7139542b3824139d971bd6100"

        endpoint = "https://api.mexc.com/api/v3/order"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": "ETHUSDT",
            "side": side,
            "type": "MARKET",
            "quantity": cantidad,
            "timestamp": timestamp
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        headers = {"X-MEXC-APIKEY": API_KEY}
        final_url = f"{endpoint}?{query_string}&signature={signature}"
        response = requests.post(final_url, headers=headers)
        return response.json()
    except Exception as e:
        raise Exception(f"Error al ejecutar orden: {str(e)}")

def evaluar_estrategia(precio):
    # Ejemplo simple de lógica Sniper + Guardian
    if precio < 3300:
        return "BUY"
    elif precio > 3500:
        return "SELL"
    else:
        return "HOLD"

def analizar_y_operar_eth():
    try:
        precio_actual = obtener_precio_eth()
        señal = evaluar_estrategia(precio_actual)
        resultado = None

        if señal in ["BUY", "SELL"]:
            intento = 0
            while intento < 3:
                try:
                    resultado = ejecutar_orden_mexc(señal)
                    # Lógica ganadora: si la orden fue exitosa, salir del bucle
                    if resultado and not resultado.get("code"):
                        break
                except Exception as e:
                    intento += 1
                    time.sleep(3)
            # Autocorrección: si tras 3 intentos falla, enviar alerta
            if not resultado or resultado.get("code"):
                enviar_mensaje_telegram(f"⚠️ Fallo al ejecutar orden {señal} tras 3 intentos.")

        mensaje = (
            f"📡 ETH Update\n"
            f"💰 Precio actual: ${precio_actual}\n"
            f"📊 Acción sugerida: {señal}\n"
            f"🛒 Orden ejecutada: {resultado if resultado else 'Ninguna'}\n"
            f"🕐 Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        enviar_mensaje_telegram(mensaje)

    except Exception as e:
        error_msg = f"❌ Error crítico ETH:\n{str(e)}\n{traceback.format_exc()}"
        enviar_mensaje_telegram(error_msg)

def ejecutar_bot_eth():
    print("🚀 ETH Bot iniciado - Estrategia Sniper + Guardian + Whale")
    while True:
        try:
            print("🔄 Monitoreando ETH en modo silencioso...")
            analizar_y_operar_eth()
        except Exception as e:
            error_msg = f"❌ Error en bot ETH:\n{str(e)}\n{traceback.format_exc()}"
            enviar_mensaje_telegram(error_msg)
        time.sleep(20)  # intervalo de chequeo

if __name__ == "__main__":
    ejecutar_bot_eth()