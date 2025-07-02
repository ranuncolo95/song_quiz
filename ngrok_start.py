from pyngrok import ngrok, conf
import os
import time
import requests
from requests.exceptions import RequestException
import atexit
from dotenv import load_dotenv, set_key


from pathlib import Path

# Configuration
ENV_PATH = Path('data/utils') / '.env'  # ← CHANGE THIS TO YOUR PATH

load_dotenv(ENV_PATH)  # Load .env file from specified path

NGROK_AUTHTOKEN = os.getenv("NGROK_AUTHTOKEN")
PORT = 8000
conf.get_default().auth_token = NGROK_AUTHTOKEN
conf.get_default().region = "eu"

class NgrokManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tunnel = None
            atexit.register(cls._instance.cleanup)
        return cls._instance
    
    def get_tunnel(self):
        if self._tunnel is None or not self.is_tunnel_active():
            self._tunnel = self.create_tunnel()
            self._update_spotify_redirect()
        return self._tunnel
    
    def is_tunnel_active(self):
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=3)
            if response.status_code == 200:
                tunnels = response.json().get("tunnels", [])
                return any(str(PORT) in t.get("config", {}).get("addr", "") for t in tunnels)
            return False
        except RequestException:
            return False
    
    def create_tunnel(self):
        for attempt in range(3):
            try:
                tunnel = ngrok.connect(PORT, bind_tls=True)
                print(f"🚀 Ngrok tunnel created: {tunnel.public_url}")
                return tunnel
            except Exception as e:
                if attempt == 2:
                    print(f"⚠️ Failed to create tunnel after 3 attempts: {e}")
                    return None
                time.sleep(1)
    
    def _update_spotify_redirect(self):
        if self._tunnel:
            redirect_uri = f"{self._tunnel.public_url}/callback"
            set_key(ENV_PATH, "SPOTIFY_REDIRECT_URI", redirect_uri)
            print(f"🔁 Updated SPOTIFY_REDIRECT_URI in .env: {redirect_uri}")
    
    def cleanup(self):
        if self._tunnel:
            try:
                ngrok.disconnect(self._tunnel.public_url)
                print("🛑 Disconnected ngrok tunnel")
            except Exception as e:
                print(f"⚠️ Error disconnecting tunnel: {e}")

if __name__ == "__main__":
    manager = NgrokManager()
    tunnel = manager.get_tunnel()
    
    if tunnel:
        print(f"🌐 Active Public URL: {tunnel.public_url}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Script stopped - Tunnel remains active")
    else:
        print(f"⚠️ Could not establish Ngrok connection, using localhost: http://localhost:{PORT}")