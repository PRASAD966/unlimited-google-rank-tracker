
import os
import requests
from dotenv import load_dotenv
import uuid

load_dotenv()

def verify_proxy_targeting(target_country_code):
    PROXY_USERNAME = os.getenv("PROXY_USERNAME")
    PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
    PROXY_SERVER = os.getenv("PROXY_SERVER")
    PROXY_PORT = os.getenv("PROXY_PORT")

    if not all([PROXY_USERNAME, PROXY_PASSWORD, PROXY_SERVER, PROXY_PORT]):
        print("Error: Proxy credentials or server info missing in .env")
        return

    fresh_session_id = uuid.uuid4().hex[:10]
    # The NEW format we just implemented
    targeted_username = f"{PROXY_USERNAME}__cr.{target_country_code}__sid.{fresh_session_id}"
    
    proxy_url = f"http://{targeted_username}:{PROXY_PASSWORD}@{PROXY_SERVER}:{PROXY_PORT}"
    proxies = {"http": proxy_url, "https": proxy_url}

    print(f"Testing proxy with targeting: {targeted_username}")
    
    try:
        # Check IP and location via api.myip.com
        response = requests.get("http://api.myip.com", proxies=proxies, timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Reported IP: {data.get('ip')}")
            print(f"✅ Reported Country: {data.get('country')} ({data.get('cc')})")
            
            if data.get('cc', '').lower() == target_country_code.lower():
                print(f"🎯 VERIFIED: Targeting for '{target_country_code}' is working!")
            else:
                print(f"⚠️ MISMATCH: Targeted '{target_country_code}' but got '{data.get('cc')}'")
        else:
            print(f"❌ Proxy returned status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error during proxy test: {e}")

if __name__ == "__main__":
    verify_proxy_targeting("in")
