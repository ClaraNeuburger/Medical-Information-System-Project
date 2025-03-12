import sqlite3

def delete_and_create_rde_table():
    # Connect to the SQLite database
    conn = sqlite3.connect("db_MIS.db")
    cur = conn.cursor()
    
    # Drop the existing rde table if it exists
    cur.execute('DROP TABLE IF EXISTS rde')
    cur.execute('DROP TABLE IF EXISTS rds')
    print("Dropped existing rde table.")
    
    # Create the new rde_messages table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rde (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message TEXT
        )
    ''')
    print("Created new rde_messages table.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Call this function to delete the existing table and create the new one
delete_and_create_rde_table()
