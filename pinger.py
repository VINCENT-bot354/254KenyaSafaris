# pinger_module.py
import threading
import time
import requests

# URL of the other site
PINGER_URL = "https://skillbridge-ajqf.onrender.com/health"

def ping_other_site(interval=660):
    """Background pinger that runs indefinitely."""
    while True:
        try:
            r = requests.get(PINGER_URL, timeout=10)
            print(f"Pinged SkillBridge -> {r.status_code}")
        except Exception as e:
            print(f"Error pinging SkillBridge: {e}")
        time.sleep(interval)  # default every 11 minutes

def start_pinger(interval=660):
    """Start the pinger in a background thread."""
    thread = threading.Thread(target=ping_other_site, args=(interval,), daemon=True)
    thread.start()

def register_routes(app):
    """Register routes to an existing Flask app."""
    @app.route("/health")
    def health():
        return "OK from 254 Kenya Safaris"
