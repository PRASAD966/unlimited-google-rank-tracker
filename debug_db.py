from database import get_db_connection

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, project_name, target_domain, timestamp FROM runs ORDER BY id DESC LIMIT 10")
rows = cursor.fetchall()
print(f"Total rows fetched: {len(rows)}")
for row in rows:
    print(f"Run ID: {row['id']} | Project: '{row['project_name']}' | Domain: {row['target_domain']}")
conn.close()
