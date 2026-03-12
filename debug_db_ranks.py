import sqlite3
conn = sqlite3.connect('rankplex.db')
c = conn.cursor()
c.execute("SELECT r.target_domain, res.keyword, res.rank FROM results res JOIN runs r ON res.run_id = r.id WHERE res.rank = 'Not found in top 100' ORDER BY res.id DESC LIMIT 20")
for row in c.fetchall():
    print(row)
conn.close()
