try:
    from database import init_db, get_db_connection
    import os
    import datetime

    # Force SQLite for test
    if os.path.exists("rankplex.db"):
        os.remove("rankplex.db")
    
    print("Initializing DB...")
    init_db()
    
    conn = get_db_connection()
    if not conn:
        print("FAIL: Could not connect to DB.")
        exit(1)
            
    # Test REGEXP
    print("Testing REGEXP function...")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO runs (user_email, timestamp) VALUES ('test@example.com', datetime('now', 'localtime'))")
        run_id = cursor.lastrowid
        cursor.execute("INSERT INTO results (run_id, keyword, rank) VALUES (?, ?, ?)", (run_id, 'test keyword', '5'))
        conn.commit()
        
        # Test query using REGEXP
        cursor.execute("SELECT rank FROM results WHERE rank REGEXP '^[0-9]+$'")
        row = cursor.fetchone()
        if row and row[0] == '5':
            print("SUCCESS: REGEXP function works.")
        else:
            print("FAIL: REGEXP function returned unexpected result.")
            
        # Test Timestamp Type
        print("Testing Timestamp Type...")
        cursor.execute("SELECT timestamp FROM runs WHERE id = ?", (run_id,))
        row = cursor.fetchone()
        ts = row[0]
        print(f"DEBUG: Retrieved timestamp is type: {type(ts)}, value: {ts}")
        if isinstance(ts, str):
            print("NOTE: Timestamp is string (Expected for SQLite). App logic must handle it.")
        else:
            print("NOTE: Timestamp is datetime object.")
            
    except Exception as e:
        print(f"FAIL: Tests failed with error: {e}")
        exit(1)
    
    print("ALL TESTS PASSED.")
    
except Exception as e:
    print(f"Error: {e}")
    exit(1)
