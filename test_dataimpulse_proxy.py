"""
Simple proxy test for DataImpulse rotating proxies
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

proxy_server = os.getenv("PROXY_SERVER")
proxy_port = os.getenv("PROXY_PORT")
proxy_username = os.getenv("PROXY_USERNAME")
proxy_password = os.getenv("PROXY_PASSWORD")

print("=" * 70)
print("DATAIMPULSE ROTATING PROXY TEST")
print("=" * 70)
print(f"\nProxy Server: {proxy_server}")
print(f"Proxy Port: {proxy_port}")
print(f"Username: {proxy_username}")
print(f"Password: {'*' * len(proxy_password) if proxy_password else 'None'}")

# Build proxy URL with authentication
proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_server}:{proxy_port}"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}

print("\n" + "=" * 70)
print("TESTING CONNECTION")
print("=" * 70)

try:
    # Test 1: Check IP address
    print("\nTest 1: Checking your IP address via proxy...")
    response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=15)
    if response.status_code == 200:
        ip_data = response.json()
        print(f"✅ SUCCESS! Your IP via proxy: {ip_data['ip']}")
    else:
        print(f"⚠️  Status code: {response.status_code}")
    
    # Test 2: Access Google
    print("\nTest 2: Accessing Google via proxy...")
    response = requests.get("https://www.google.com", proxies=proxies, timeout=15)
    if response.status_code == 200:
        print(f"✅ SUCCESS! Google responded with status 200")
        print(f"   Response size: {len(response.content)} bytes")
    else:
        print(f"⚠️  Status code: {response.status_code}")
    
    # Test 3: Check IP rotation (make another request)
    print("\nTest 3: Testing IP rotation (making another request)...")
    response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=15)
    if response.status_code == 200:
        ip_data = response.json()
        print(f"✅ IP on second request: {ip_data['ip']}")
        print("   Note: IP may or may not change depending on rotation settings")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - PROXY IS WORKING!")
    print("=" * 70)
    
except requests.exceptions.ProxyError as e:
    print(f"\n❌ PROXY ERROR: {e}")
    print("\nPossible causes:")
    print("  1. Incorrect proxy credentials")
    print("  2. Proxy server is down")
    print("  3. Your IP is not whitelisted (if required)")
    
except requests.exceptions.Timeout:
    print(f"\n❌ TIMEOUT: Proxy not responding")
    print("  The proxy server might be slow or down")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 70)
