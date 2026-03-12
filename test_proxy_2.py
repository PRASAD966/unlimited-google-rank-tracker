import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\kadiy\Downloads\rankproxy 3\rankproxy\.env")

PROXY_SERVER = os.getenv("PROXY_SERVER")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

def test_proxy():
    import urllib.request
    import urllib.error
    
    username_string = f"{PROXY_USERNAME}-session-abcdee"
    proxy_url = f"http://{username_string}:{PROXY_PASSWORD}@{PROXY_SERVER}:{PROXY_PORT}"
    
    print(f"Connecting to: {proxy_url}")
    try:
        handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
        opener = urllib.request.build_opener(handler)
        resp = opener.open('http://httpbin.org/ip', timeout=15)
        print("Response:", resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code)
        print("Body:", e.read().decode('utf-8', errors='ignore'))
    except Exception as e:
        print("Error:", e)
        
if __name__ == "__main__":
    test_proxy()
