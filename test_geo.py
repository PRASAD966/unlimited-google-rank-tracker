import requests

def get_coordinates_and_country(location_name):
    if not location_name or location_name in ["Global", ""]:
        return None, None
    
    # Simple retry loop
    for attempt in range(3):
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
                lat = float(item['lat'])
                lon = float(item['lon'])
                country_code = item.get('address', {}).get('country_code', 'us')
                
                return {
                    'latitude': lat,
                    'longitude': lon,
                    'accuracy': 100
                }, country_code
        except Exception as e:
            print(f"Error Geocoding {location_name} (Attempt {attempt+1}): {e}")
            import time
            time.sleep(1)
            
    return None, None

coords, cc = get_coordinates_and_country("India")
print(f"Location: India -> Coords: {coords}, CC: {cc}")

coords, cc = get_coordinates_and_country("india")
print(f"Location: india -> Coords: {coords}, CC: {cc}")
