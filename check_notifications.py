import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='rankplex_db'
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT COUNT(*) as count FROM notifications WHERE user_email='akashdhatrika@gmail.com' AND is_read=FALSE")
result = cursor.fetchone()
print(f"Unread notifications for akashdhatrika@gmail.com: {result['count']}")

cursor.execute("SELECT * FROM notifications WHERE user_email='akashdhatrika@gmail.com' ORDER BY timestamp DESC LIMIT 5")
notifications = cursor.fetchall()
print("\nRecent notifications:")
for n in notifications:
    status = "UNREAD" if not n['is_read'] else "READ"
    print(f"  [{status}] {n['message'][:50]}...")

cursor.close()
conn.close()
