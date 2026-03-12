import sqlite3
try:
    import mysql.connector
    from mysql.connector import Error, pooling
except ImportError:
    import collections
    Error = Exception
    mysql = collections.namedtuple('mysql', ['connector'])(connector=None)
    pooling = None
import os
import datetime
import json
import re
import threading

# Database Configuration from Environment Variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "")
DB_NAME = os.environ.get("DB_NAME", "rankplexdb")
DB_TYPE = os.environ.get("DB_TYPE", "sqlite") # Default to sqlite for local dev

DB_FILE = "rankplex.db"

# Global Pool for MySQL
_MYSQL_POOL = None
_POOL_LOCK = threading.Lock()

def _init_mysql_pool():
    global _MYSQL_POOL
    with _POOL_LOCK:
        if _MYSQL_POOL is None and pooling is not None:
            try:
                _MYSQL_POOL = pooling.MySQLConnectionPool(
                    pool_name="rankplex_pool",
                    pool_size=10, # Up to 10 connections always ready
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASS,
                    database=DB_NAME,
                    auth_plugin='mysql_native_password',
                    buffered=True
                )
                print(f"DEBUG: MySQL Pool initialized with {DB_HOST}")
            except Exception as e:
                print(f"Error initializing MySQL Pool: {e}")

class MySQLConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            # Try getting from pool first
            if _MYSQL_POOL:
                self.conn = _MYSQL_POOL.get_connection()
                return self.conn
            
            # Fallback to direct connect
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin='mysql_native_password',
                buffered=True
            )
            return self.conn
        except Error as e:
            print(f"MySQL Connection Error: {e}")
            return None

    def cursor(self, dictionary=True):
        return self.conn.cursor(dictionary=dictionary)

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def is_connected(self):
        return self.conn and self.conn.is_connected()

    @property
    def db_type(self):
        return "mysql"

class SQLiteCursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        # Convert %s to ? for SQLite compatibility
        if params:
            query = query.replace("%s", "?")
        return self.cursor.execute(query, params or ())

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        return self.cursor.close()

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    def __iter__(self):
        return iter(self.cursor)

class SQLiteConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            # Performance: Enable WAL mode and synchronous=NORMAL
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=NORMAL")
            # Add REGEXP support
            self.conn.create_function("REGEXP", 2, lambda expr, item: 1 if item and re.search(expr, item) is not None else 0)
            return self.conn
        except sqlite3.Error as e:
            print(f"SQLite Connection Error: {e}")
            return None

    def cursor(self, dictionary=False):
        return SQLiteCursorWrapper(self.conn.cursor())

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def is_connected(self):
        return self.conn is not None

    @property
    def db_type(self):
        return "sqlite"

def get_db_connection():
    # If DB_HOST is set (e.g. in Docker), try MySQL first
    if os.environ.get("FLASK_ENV") == "production" or os.environ.get("DB_HOST"):
        if _MYSQL_POOL is None:
            _init_mysql_pool()
        
        conn = MySQLConnection(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        if conn.connect():
            return conn
    
    # Fallback to SQLite
    conn = SQLiteConnection(DB_FILE)
    if conn.connect():
        return conn
    return None


def init_db():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to Database for initialization.")
        return

    is_mysql = isinstance(conn, MySQLConnection)
    cursor = conn.cursor()
    
    # Primary Key syntax differs
    pk_auto = "INT AUTO_INCREMENT PRIMARY KEY" if is_mysql else "INTEGER PRIMARY KEY AUTOINCREMENT"
    text_type = "TEXT"
    blob_type = "LONGBLOB" if is_mysql else "BLOB"

    # Runs Table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS runs (
            id {pk_auto},
            user_email {text_type},
            project_name {text_type},
            target_domain {text_type},
            location {text_type},
            max_pages INTEGER,
            total_keywords INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            excel_filename {text_type},
            excel_data {blob_type},
            status {text_type} DEFAULT 'pending',
            cancelled BOOLEAN DEFAULT 0,
            keywords_json {text_type},
            sid {text_type}
        )
    """)

    # Migration for new columns
    for col, ctype in [("status", text_type), ("cancelled", "BOOLEAN DEFAULT 0"), ("keywords_json", text_type), ("sid", text_type)]:
        try:
            cursor.execute(f"ALTER TABLE runs ADD COLUMN {col} {ctype}")
            conn.commit()
        except Exception:
            pass # Column likely exists

    # Attempt to add column if it doesn't exist (Migration for existing DB)
    try:
        cursor.execute(f"ALTER TABLE runs ADD COLUMN total_keywords INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        pass # Column likely exists

    # Results Table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS results (
            id {pk_auto},
            run_id INTEGER,
            keyword {text_type},
            page {text_type},
            rank {text_type},
            landing_page {text_type},
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE
        )
    """)

    # Migration for landing_page
    try:
        cursor.execute(f"ALTER TABLE results ADD COLUMN landing_page {text_type}")
        conn.commit()
    except Exception:
        pass

    # Migration for sort_order
    try:
        cursor.execute(f"ALTER TABLE results ADD COLUMN sort_order INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        pass

    # User Profiles Table
    # Added credits columns. 
    # total_credits: Limit (e.g., 1000)
    # used_credits: Consumed (e.g., 0)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS user_profiles (
            email VARCHAR(255) PRIMARY KEY,
            full_name {text_type},
            phone {text_type},
            country_code {text_type},
            profile_image {text_type},
            is_verified BOOLEAN DEFAULT 0,
            total_credits INTEGER DEFAULT 1000,
            used_credits INTEGER DEFAULT 0
        )
    """)

    # Attempt migration for credits if columns don't exist
    try:
        cursor.execute(f"ALTER TABLE user_profiles ADD COLUMN total_credits INTEGER DEFAULT 1000")
        conn.commit()
    except Exception:
        pass 
    try:
        cursor.execute(f"ALTER TABLE user_profiles ADD COLUMN used_credits INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        pass

    # Migration for country_code
    try:
        cursor.execute(f"ALTER TABLE user_profiles ADD COLUMN country_code {text_type}")
        conn.commit()
    except Exception:
        pass

    # Notifications Table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS notifications (
            id {pk_auto},
            user_email {text_type},
            message {text_type},
            is_read BOOLEAN DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_runs_user ON runs (user_email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_run ON results (run_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications (user_email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_keyword ON results (keyword)")

    conn.commit()
    conn.close()
    print(f"{'MySQL' if is_mysql else 'SQLite'} Database initialized successfully.")

# Mock mysql.connector.Error compatible exception for easier porting
class DatabaseError(Exception):
    pass

def add_credits(email, amount):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE user_profiles SET total_credits = total_credits + %s WHERE email = %s", (amount, email))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding credits: {e}")
            if conn: conn.close()
            return False
    return False
