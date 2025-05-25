import os
import requests
import zipfile
import io

UPDATE_URL = os.getenv("UPDATE_URL", "")
AUTO_UPDATE = os.getenv("AUTO_UPDATE", "false").lower() == "true"

def download_and_extract_zip(url, extract_to="."):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
            print("✅ Update applied from:", url)
    else:
        print("❌ Failed to download update.")

if AUTO_UPDATE and UPDATE_URL:
    print("🔄 Auto-update enabled. Checking for updates...")
    download_and_extract_zip(UPDATE_URL)
else:
    print("🟡 Update manager idle.")
