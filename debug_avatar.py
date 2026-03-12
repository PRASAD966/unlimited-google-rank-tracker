
import sys
import os

# Ensure we can import server.py
sys.path.append(os.getcwd())

from server import get_user_display_info, get_db_connection

email = "prasadniceinteractive@gmail.com"

print(f"--- Debugging for {email} ---")

# 1. Check DB directly
conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_profiles WHERE email = %s", (email,))
    res = cursor.fetchone()
    print(f"Direct DB Fetch: {res}")
    row = dict(res)
    if res:
        print(f"profile_image in DB: '{row.get('profile_image')}'")
    conn.close()
else:
    print("Failed to connect to DB")

# 2. Check function
try:
    display_name, initial, profile_image = get_user_display_info(email)
    print(f"Function Result -> display_name: {display_name}, initial: {initial}, profile_image: {profile_image}")
except Exception as e:
    print(f"Function failed: {e}")
