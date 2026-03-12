import database
conn = database.get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT email, total_credits, used_credits FROM user_profiles WHERE email = 'praveenniceinteractive@gmail.com'")
    row = cursor.fetchone()
    if row:
        print(f"Email: {row[0]}, Total: {row[1]}, Used: {row[2]}, Remaining: {row[1]-row[2]}")
    else:
        print("User not found")
    conn.close()
