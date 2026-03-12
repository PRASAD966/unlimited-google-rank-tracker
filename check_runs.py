import database
conn = database.get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_email, project_name, location, timestamp FROM runs ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    for r in rows:
        print(f"ID: {r[0]}, User: {r[1]}, Project: {r[2]}, Location: {r[3]}, Time: {r[4]}")
    conn.close()
