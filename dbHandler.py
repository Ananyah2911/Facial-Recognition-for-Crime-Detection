# dbHandler.py (SQLite version)
import sqlite3

# Database file name
DB_PATH = "criminals.db"

def init_db():
    """Creates the table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS criminals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            father_name TEXT,
            gender TEXT,
            dob TEXT,
            crimes_done TEXT
        )
    """)
    conn.commit()
    conn.close()

def insertData(entry_data):
    """Insert a criminal record and return the inserted ID"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = """INSERT INTO criminals (name, father_name, gender, dob, crimes_done)
             VALUES (?, ?, ?, ?, ?)"""
    values = (
        entry_data["Name"],
        entry_data["Father's Name"],
        entry_data["Gender"],
        entry_data["DOB(yyyy-mm-dd)"],
        entry_data["Crimes Done"]
    )
    c.execute(sql, values)
    conn.commit()
    rowid = c.lastrowid
    conn.close()
    return rowid

def retrieveData(name):
    """Retrieve a record by name"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = "SELECT * FROM criminals WHERE name = ?"
    c.execute(sql, (name,))
    row = c.fetchone()
    conn.close()

    if row:
        crim_data = {
            "Name": row[1],
            "Father's Name": row[2],
            "Gender": row[3],
            "DOB(yyyy-mm-dd)": row[4],
            "Crimes Done": row[5]
        }
        return (row[0], crim_data)
    else:
        return (None, None)

# Automatically initialize database on import
init_db()
