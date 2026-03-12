"""
Quick Proxy Verification - DataImpulse
Tests if proxy credentials are working
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Build proxy URL
username = os.getenv("PROXY_USERNAME")
password = os.getenv("PROXY_PASSWORD")
server = os.getenv("PROXY_SERVER")
port = os.getenv("PROXY_PORT")

proxy_url = f"http://{username}:{password}@{server}:{port}"

print("=" * 60)
print("QUICK PROXY TEST")
print("=" * 60)
print(f"Server: {server}:{port}")
print(f"Testing connection...")
print()

try:
    # Test 1: Get IP
    response = requests.get(
        "https://api.ipify.org?format=json",
        proxies={"http": proxy_url, "https": proxy_url},
        timeout=15
    )
    
    if response.status_code == 200:
        ip = response.json()['ip']
        print(f"✅ SUCCESS!")
        print(f"   Your IP via proxy: {ip}")
        print(f"   Proxy is working correctly!")
        
        # Test 2: Second request to check rotation
        print(f"\n   Testing IP rotation...")
        response2 = requests.get(
            "https://api.ipify.org?format=json",
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=15
        )
        ip2 = response2.json()['ip']
        print(f"   Second request IP: {ip2}")
        
        if ip != ip2:
            print(f"   ✅ IP ROTATED! Rotation is working!")
        else:
            print(f"   ℹ️  Same IP (rotation may happen per session)")
        
    else:
        print(f"❌ Error: Status {response.status_code}")
        
except requests.exceptions.ProxyError as e:
    print(f"❌ PROXY ERROR")
    print(f"   Check credentials or bandwidth limit")
    
except Exception as e:
    print(f"❌ ERROR: {e}")

print()
print("=" * 60)
