import sqlite3

DB_NAME = "database.db"

def init_db():
    """Create the database tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,  -- 'driver' or 'authority'
        license_image TEXT,  -- Stores filename
        position TEXT  -- Municipality/Corporation/Panchayath (For Authorities)
    );

    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image TEXT,  -- Stores image filename
        description TEXT,
        latitude REAL,
        longitude REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS danger_zones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database Initialized!")
