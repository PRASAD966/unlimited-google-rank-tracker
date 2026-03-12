import requests
import os
from dotenv import load_dotenv

load_dotenv()

PROXY_SERVER = os.environ.get('PROXY_SERVER')
PROXY_PORT = os.environ.get('PROXY_PORT')
PROXY_USERNAME = os.environ.get('PROXY_USERNAME')
PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')

proxyip = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_SERVER}:{PROXY_PORT}"
url = "https://api.ip.cc"
proxies = {
    'http': proxyip,
    'https': proxyip,
}

print(f"Testing proxy: {proxyip}")

try:
    data = requests.get(url=url, proxies=proxies, timeout=10)
    print(data.text)
except Exception as e:
    print(f"Error: {e}")
