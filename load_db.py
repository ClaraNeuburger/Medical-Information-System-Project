import sqlite3
##################################################################################################################
# This is the first step when opening the project, load the data base 
##################################################################################################################

conn = sqlite3.connect('db_MIS.db')
cur = conn.cursor()

# Load SQL script from file
with open("db_MIS.sql", 'r') as file:
    sql_script = file.read()

cur.executescript(sql_script)
print("db_MIS is loaded")

cur.close()
conn.commit()