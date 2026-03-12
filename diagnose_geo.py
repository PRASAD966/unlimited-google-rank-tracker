
import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

def get_coordinates_and_country(location_name):
    if not location_name or location_name in ["Global", ""]:
        return None, None
    
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': location_name,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'RankPlex/1.0'
        }
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        data = resp.json()
        if data and len(data) > 0:
            item = data[0]
            country_code = item.get('address', {}).get('country_code', 'us')
            return item, country_code
    except Exception as e:
        print(f"Error Geocoding {location_name}: {e}")
            
    return None, None

def test_targeting(location):
    print(f"\nTesting location: {location}")
    item, cc = get_coordinates_and_country(location)
    if not item:
        print("Geocoding failed.")
        return
    
    print(f"Detected Country Code: {cc}")
    
    PROXY_USERNAME = os.getenv("PROXY_USERNAME")
    target_country = cc
    country_code_lower = target_country.strip().lower()
    
    # The format used in server.py
    proxy_username_with_targeting = f"{PROXY_USERNAME}__cr.{country_code_lower};sid.FRESH_SESSION"
    
    print(f"Proxy Username with targeting: {proxy_username_with_targeting}")

if __name__ == "__main__":
    test_targeting("India")
    test_targeting("Mumbai, India")
    test_targeting("USA")
