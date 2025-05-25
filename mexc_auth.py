import os
import hmac
import hashlib

API_KEY = os.getenv("MEXC_API_KEY")
SECRET_KEY = os.getenv("MEXC_SECRET_KEY")
BASE_URL = os.getenv("MEXC_API_URL", "https://api.mexc.com")

def sign_params(params):
    query = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"
