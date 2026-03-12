import database
conn = database.get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT keyword, rank, page FROM results WHERE run_id = 409")
    rows = cursor.fetchall()
    for r in rows:
        print(f"Keyword: {r[0]}, Rank: {r[1]}, Page: {r[2]}")
    conn.close()
