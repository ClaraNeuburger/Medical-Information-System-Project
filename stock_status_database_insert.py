import sqlite3

def delete_and_create_stock_order_table():
    # Connect to the SQLite database
    conn = sqlite3.connect("db_MIS.db")
    cur = conn.cursor()
    
    # Drop the existing rde table if it exists
    cur.execute('DROP TABLE IF EXISTS stock_order')
    print("Dropped existing stock_order table.")
    
    # Create the new stock_medicament table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stock_order (
            id_stock_order INTEGER PRIMARY KEY AUTOINCREMENT,
            ref_order TEXT,
            name_medicament INTEGER, 
            order_quantity INTEGER,
            status_order TEXT    
        )
    ''')
    print("Created new stock_order table.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

delete_and_create_stock_order_table()

conn = sqlite3.connect("db_MIS.db")
cur = conn.cursor()

insert_query = "INSERT INTO stock_order (ref_order, name_medicament, order_quantity,status_order)  Values (?,?,?,?)"
stock_to_insert = [
    ('AB12CD34EF', 'Ibuprofen', 1000, 'in progress'),
    ('XY98WV76TS', 'Amoxicillin', 500, 'delivered'),
    ('GH56IJ78KL', 'Lisinopril', 1000, 'added to stock'),
    ('MN34OP12QR', 'Simvastatin', 1000, 'in progress'),
    ('ST23UV45WX', 'Omeprazole', 1000, 'delivered'),
    ('YZ67QR89OP', 'Metformin', 1000, 'added to stock'),
    ('IJ23KL45MN', 'Albuterol', 500, 'in progress'),
    ('BC67DE89FG', 'Warfarin', 300, 'delivered'),
    ('UV56WX78YZ', 'Atorvastatin', 1000, 'added to stock'),
    ('KL12MN34OP', 'Citalopram', 750, 'in progress'),
    ('WX23YZ45AB', 'Dexamethasone', 400, 'delivered'),
    ('CD45EF67GH', 'Lorazepam', 200, 'added to stock'),
    ('IJ89KL01MN', 'Diphenhydramine', 500, 'in progress'),
    ('OP34QR56ST', 'Metoprolol', 800, 'delivered'),
    ('AB67CD89EF', 'Ranitidine', 900, 'added to stock'),
    ('GH23IJ45KL', 'Hydrochlorothiazide', 500, 'in progress'),
    ('MN78OP90QR', 'Clonazepam', 300, 'delivered'),
    ('ST12UV34WX', 'Venlafaxine', 600, 'added to stock'),
    ('YZ45AB67CD', 'Amitriptyline', 400, 'in progress'),
    ('EF89GH01IJ', 'Gabapentin', 700, 'delivered')
]

for order in stock_to_insert:
    cur.execute(insert_query,order)

data_verified = cur.execute("SELECT * from stock_order").fetchall()
print(data_verified)
conn.commit()
conn.close()
