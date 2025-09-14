# pinger.py for 254 Kenya Safaris
import threading
import time
import requests

# URL of the other site to ping
PING_URL = "https://pinger-b1rg.onrender.com/health"
PING_INTERVAL = 8 * 60  # 8 minutes

def ping_site():
    """Continuously ping the other site every 8 minutes."""
    while True:
        try:
            response = requests.get(PING_URL)
            print(f"Pinged {PING_URL} - Status code: {response.status_code}")
        except Exception as e:
            print(f"Error pinging {PING_URL}: {e}")
        time.sleep(PING_INTERVAL)

def start_pinger():
    """Start the pinging in a background thread."""
    thread = threading.Thread(target=ping_site, daemon=True)
    thread.start()
