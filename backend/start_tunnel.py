import time
from pyngrok import ngrok

# Open a HTTP tunnel on port 8000
public_url = ngrok.connect(8000).public_url
print(f"\n==========================================")
print(f"NGROK PUBLIC HTTPS URL: {public_url}")
print(f"WEBHOOK URL: {public_url}/api/v1/webhook/whatsapp")
print(f"==========================================\n", flush=True)

# Keep process alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.disconnect(public_url)
