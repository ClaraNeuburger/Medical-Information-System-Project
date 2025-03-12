import sqlite3

def delete_and_create_stock_medicament_table():
    # Connect to the SQLite database
    conn = sqlite3.connect("db_MIS.db")
    cur = conn.cursor()
    
    # Drop the existing rde table if it exists
    cur.execute('DROP TABLE IF EXISTS stock_medicament')
    print("Dropped existing stock_medicament table.")
    
    # Create the new stock_medicament table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stock_medicament (
            id_medicament INTEGER PRIMARY KEY AUTOINCREMENT,
            name_medicament INTEGER,
            dormant_stock INTEGER,
            available_stock INTEGER,
            delivery_time INTEGER, 
            order_quantity INTEGER    
        )
    ''')
    print("Created new stock_medicament table.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

delete_and_create_stock_medicament_table()

conn = sqlite3.connect("db_MIS.db")
cur = conn.cursor()

insert_query = "INSERT INTO stock_medicament (name_medicament, dormant_stock, available_stock, delivery_time, order_quantity) Values (?,?,?,?,?)"
medicament_to_insert = [
    ("Ibuprofen", 100, 300, 2, 1000),
    ("Amoxicillin", 100, 400, 2, 500),
    ("Lisinopril", 50, 150, 3, 1000),
    ("Simvastatin", 100, 300, 2, 1000),
    ("Omeprazole", 100, 300, 2, 1000),
    ("Metformin", 150, 500, 2, 1000),
    ("Albuterol", 50, 200, 1, 500),
    ("Warfarin", 30, 100, 2, 300),
    ("Atorvastatin", 100, 300, 2, 1000),
    ("Citalopram", 75, 250, 3, 750),
    ("Dexamethasone", 40, 120, 3, 400),
    ("Lorazepam", 20, 80, 2, 200),
    ("Diphenhydramine", 60, 180, 2, 500),
    ("Metoprolol", 80, 240, 2, 800),
    ("Ranitidine", 90, 270, 2, 900),
    ("Hydrochlorothiazide", 50, 150, 3, 500),
    ("Clonazepam", 30, 100, 3, 300),
    ("Venlafaxine", 60, 180, 3, 600),
    ("Amitriptyline", 40, 120, 3, 400),
    ("Gabapentin", 70, 210, 2, 700),
]

for medicament in medicament_to_insert:
    cur.execute(insert_query,medicament)

data_verified = cur.execute("SELECT * from stock_medicament").fetchall()
print(data_verified)

conn.commit()
conn.close()
