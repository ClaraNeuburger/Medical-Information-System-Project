import sqlite3

##################################################################################################################
# this is function that adds a list of medicine and incompatibilities to the tables 
##################################################################################################################


conn = sqlite3.connect('db_MIS.db')
cur = conn.cursor()


def insertion_medicaments(name, medicament_class, code, give_min_amount, give_max_amount, give_units, admin_instruction=None, dispense_amount=None, dispense_units=None, frequency=None, notes=None):
    data_med = (name, medicament_class)
    insert_query_med = "INSERT INTO medicament (name, medicament_class) VALUES (?, ?)"
    existing_data_med = cur.execute("SELECT * FROM medicament WHERE name = ? AND medicament_class = ?", data_med).fetchone()
    if not existing_data_med:
        cur.execute(insert_query_med, data_med)
        
        
        prescription_data = (name, code, give_min_amount, give_max_amount, give_units, admin_instruction, dispense_amount, dispense_units, frequency, notes)
        insert_query_prescription = "INSERT INTO MedicineDetails (medicament, code,  give_min_amout, give_max_amout, give_units, admin_instruction, dispense_amount, dispense_units, frequency, notes) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(insert_query_prescription, prescription_data)
        
        print("Medication added successfully.")
    else:
        print("Medication already present in the medicament table.")





def insertion_class_med(description_class_med):
    insert_query_class = "INSERT INTO class_medicament (description) VALUES ( ?)"
    existing_data_class = cur.execute("SELECT * FROM class_medicament where  descriptions = ? ", (description_class_med)).fetchone()
    if not existing_data_class : 
        #data is not present execute the inquery
        cur.execute(insert_query_class, (description_class_med))
    else : 
        print("Class already present in the table person")

def insertion_incompatibilities(class1, class2, description=None):
    data_inc = (class1, class2)
    insert_query_inc = "INSERT INTO Incompatibilities (concerned_class_medicament1, concerned_class_medicament2, description) VALUES (?, ?, ?)"
    existing_data_inc = cur.execute("SELECT * FROM Incompatibilities WHERE concerned_class_medicament1 = ? AND concerned_class_medicament2 = ?", (data_inc[0], data_inc[1])).fetchone()
    if not existing_data_inc:
        # Data is not present, execute the query
        cur.execute(insert_query_inc, (data_inc[0], data_inc[1], description))
    else:
        print("Incompatibility already present in the table Incompatibilities")

    if description is not None:
        cur.execute("UPDATE Incompatibilities SET description = ? WHERE concerned_class_medicament1 = ? AND concerned_class_medicament2 = ?", (description, data_inc[0], data_inc[1]))

#insertion_medicaments("Paracetamol", "Analgesic")
#insertion_medicaments("Ibuprofen", "Anti-inflammatory")

#insertion_incompatibilities("Analgesic", "Anti-inflammatory", description="Avoid concurrent use due to increased risk of adverse effects.")


""" insertion_incompatibilities("Analgesic", "Anti-inflammatory", "Avoid concurrent use due to increased risk of adverse effects.")
insertion_incompatibilities("Analgesic", "Antihypertensive", "May reduce the efficacy of antihypertensive medications.")
insertion_incompatibilities("Antihyperlipidemic", "Antidiabetic", "May increase blood sugar levels.")
insertion_incompatibilities("Antibiotic", "Antihypertensive", "May lead to low blood pressure.")
insertion_incompatibilities("Antibiotic", "Proton Pump Inhibitor", "May reduce the efficacy of proton pump inhibitors.")
 """


#name, medicament_class, code, give_min_amount, give_max_amount, give_units, admin_instruction=None, dispense_amount=None, dispense_units=None, frequency=None, notes=None):
 

# Fill the database
""" insertion_medicaments("Ibuprofen", "Analgesic", 2, 200, 400, "mg", admin_instruction="Take with food", dispense_amount=30, dispense_units="tablets", frequency="Every 4-6 hours as needed", notes="For pain and inflammation")
insertion_medicaments("Amoxicillin", "Antibiotic", 3, 250, 500, "mg", admin_instruction="Take with plenty of water", dispense_amount=14, dispense_units="capsules", frequency="Twice daily", notes="For bacterial infections")
insertion_medicaments("Lisinopril", "Antihypertensive", 4, 2.5, 10, "mg", admin_instruction="Take with or without food", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For high blood pressure")
insertion_medicaments("Simvastatin", "Antihyperlipidemic", 5, 10, 40, "mg", admin_instruction="Take in the evening", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For high cholesterol")
insertion_medicaments("Omeprazole", "Proton Pump Inhibitor", 6, 20, None, "mg", admin_instruction="Take before breakfast", dispense_amount=28, dispense_units="capsules", frequency="Once daily", notes="For acid reflux")
insertion_medicaments("Metformin", "Antidiabetic", 7, 500, 1000, "mg", admin_instruction="Take with meals", dispense_amount=60, dispense_units="tablets", frequency="Twice daily", notes="For type 2 diabetes")
insertion_medicaments("Albuterol", "Bronchodilator", 8, 90, 180, "mcg", admin_instruction="Inhale as needed for asthma symptoms", dispense_amount=1, dispense_units="inhaler", frequency="As needed", notes="For asthma relief")
insertion_medicaments("Warfarin", "Anticoagulant", 9, 1, 5, "mg", admin_instruction="Take at the same time each day", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For blood clot prevention")
insertion_medicaments("Atorvastatin", "Antihyperlipidemic", 10, 10, 80, "mg", admin_instruction="Take at bedtime", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For high cholesterol")
insertion_medicaments("Citalopram", "Antidepressant", 11, 10, 40, "mg", admin_instruction="Take in the morning or evening", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For depression")
insertion_medicaments("Dexamethasone", "Corticosteroid", 12, 0.5, 8, "mg", admin_instruction="Take with food", dispense_amount=20, dispense_units="tablets", frequency="Once daily", notes="For inflammation and autoimmune conditions")
insertion_medicaments("Lorazepam", "Anxiolytic", 13, 0.5, 2, "mg", admin_instruction="Take as directed for anxiety", dispense_amount=20, dispense_units="tablets", frequency="As needed for anxiety", notes="For short-term relief of anxiety symptoms")
insertion_medicaments("Diphenhydramine", "Antihistamine", 14, 25, 50, "mg", admin_instruction="Take before bedtime", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For allergies and sleep aid")
insertion_medicaments("Metoprolol", "Beta Blocker", 15, 25, 100, "mg", admin_instruction="Take with or without food", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For hypertension and angina")
insertion_medicaments("Ranitidine", "H2 Antagonist", 16, 75, 150, "mg", admin_instruction="Take before meals or at bedtime", dispense_amount=30, dispense_units="tablets", frequency="Twice daily", notes="For acid reflux and ulcers")
insertion_medicaments("Hydrochlorothiazide", "Diuretic", 17, 12.5, 25, "mg", admin_instruction="Take in the morning with food", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For hypertension and edema")
insertion_medicaments("Clonazepam", "Antiepileptic", 18, 0.5, 2, "mg", admin_instruction="Take as directed for seizures", dispense_amount=30, dispense_units="tablets", frequency="Twice daily", notes="For epilepsy")
insertion_medicaments("Venlafaxine", "Antidepressant", 19, 37.5, 225, "mg", admin_instruction="Take with food", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For depression and anxiety disorders")
insertion_medicaments("Amitriptyline", "Tricyclic Antidepressant", 20, 10, 150, "mg", admin_instruction="Take at bedtime", dispense_amount=30, dispense_units="tablets", frequency="Once daily", notes="For depression and neuropathic pain")
insertion_medicaments("Gabapentin", "Anticonvulsant", 21, 100, 800, "mg", admin_instruction="Take with food", dispense_amount=30, dispense_units="capsules", frequency="Three times daily", notes="For epilepsy and neuropathic pain")
 """
def print_all_medicaments():
    # Connect to the database
    conn = sqlite3.connect('db_MIS.db')  # Replace 'db_MIS.db' with the name of your SQLite database file
    cur = conn.cursor()

    # Execute SELECT query to fetch all medicaments
    cur.execute("SELECT * FROM medicament")

    # Fetch all medicaments
    medicaments = cur.fetchall()

    # Print each medicament's information
    print("Medicaments:")
    for medicament in medicaments:
        print(medicament)

    # Close cursor and connection
    cur.close()
    conn.close()

# Call the function to print all medicaments
print_all_medicaments()


def clear_tables():
    
    conn = sqlite3.connect('db_MIS.db') 
    cur = conn.cursor()

    tables = ["medicament"]

    try: 
        for table in tables:
            cur.execute(f"DELETE FROM {table}")
            conn.commit()
        
        print("All tables cleared successfully.")
    except Exception as e:
        print(f"Error clearing tables: {e}")



cur.close()
conn.commit()
