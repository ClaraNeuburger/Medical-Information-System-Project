import sqlite3
##################################################################################################################
# This function is here to load the database
# It's a bit messy but you can find the INSERT functions, DELETE and PRINT as well
# If you simply want to load the database, juste uncomment 'fill_all_tables()' which is at the very end of the code
##################################################################################################################

#Connect to or create a SQLite database
conn = sqlite3.connect('db_MIS.db')
cur = conn.cursor()

def insert_person(first_name, last_name,sex, date_of_birth, primary_language, nationalnb, middle_name=None, birth_place=None, email=None, phoneH=None, phoneB=None, nationality=None):    #insertion into the person's table
    data_person = (first_name, last_name, date_of_birth, sex, primary_language, nationalnb)
    insert_query_person = "INSERT INTO person (first_name, last_name, date_of_birth, sex, primary_langage, national_number) VALUES ( ?, ?, ?, ?, ?, ?)"
    existing_data_person = cur.execute("SELECT * FROM person where  first_name = ? AND last_name = ? AND date_of_birth = ? AND sex = ?", (data_person[0], data_person[1], data_person[2], data_person[3])).fetchone()
    if not existing_data_person : 
        #data is not present execute the inquery
        cur.execute(insert_query_person, data_person)
    else : 
        print("Person already present in the table person")
        id_person_inserted = cur.execute("SELECT id FROM person WHERE first_name = ? AND last_name = ? AND date_of_birth = ? AND sex = ?", (data_person[0], data_person[1], data_person[2], data_person[3])).fetchone()
        return(id_person_inserted[0])

    #first we got get the person's id
    id_person_inserted = cur.execute("SELECT id FROM person where  first_name = ? AND last_name = ? AND date_of_birth = ? AND sex = ?", (data_person[0], data_person[1], data_person[2], data_person[3])).fetchone()

    #then we add the possible added data:
    if middle_name != None : cur.execute("UPDATE person SET middle_name = ? WHERE id = ?", ( middle_name, id_person_inserted[0]))
    if birth_place != None : cur.execute("UPDATE person SET birth_place = ? WHERE id = ?", (birth_place, id_person_inserted[0]))
    if email != None : cur.execute("UPDATE person SET email = ? WHERE id = ?", (email, id_person_inserted[0]))
    if phoneH != None : cur.execute("UPDATE person SET phone_home = ? WHERE id = ?", (phoneH, id_person_inserted[0]))
    if phoneB != None : cur.execute("UPDATE person SET phone_business = ? WHERE id = ?", (phoneB, id_person_inserted[0]))
    if nationality != None : cur.execute("UPDATE person SET nationality = ? WHERE id = ?", (nationality, id_person_inserted[0]))
    
    return(id_person_inserted[0])


def insertion_patient(first_name, last_name,sex, date_of_birth, primary_language, nationalnb, id_doctor, patient_class, current_pathologie, service, SSnb, middle_name=None, birth_place=None, email=None, phoneH=None, phoneB=None, nationality=None, chamber=None, bed=None, patient_source=None, allergie1=None, allergie2=None, past_pathologies=None, date_entry=None, marital_status=None, religion=None):    #insertion into the patient's table
    # Insert or get person id
    id_person_inserted = insert_person(first_name, last_name, date_of_birth, sex, primary_language, nationalnb, middle_name, birth_place, email, phoneH, phoneB, nationality)


    data_patient = (id_person_inserted, id_doctor,patient_class, current_pathologie, service, SSnb)
    insert_query_patient = "INSERT INTO patient (id_person, id_doctor,patient_class, curent_pathologies, service, SS_number) VALUES ( ?, ?, ?, ?, ?, ?)"
    
    existing_data_patient = cur.execute("SELECT * FROM patient where id_person = ? AND id_doctor = ? AND patient_class = ? AND curent_pathologies = ? AND service = ?", (data_patient[0], data_patient[1], data_patient[2], data_patient[3], data_patient[4])).fetchone()
    if not existing_data_patient : 
        #data is not present execute the inquery
        cur.execute(insert_query_patient, data_patient)
    else : return(print("Patient already present in the table patient"))

    #then we add the possible added data:
    if chamber != None : cur.execute("UPDATE patient SET chamber = ? WHERE id_person = ?", ( chamber, id_person_inserted))
    if bed != None : cur.execute("UPDATE patient SET bed = ? WHERE id_person = ?", (bed, id_person_inserted))
    if patient_source != None : cur.execute("UPDATE patient SET patient_source = ? WHERE id_person = ?", (patient_source, id_person_inserted))
    if allergie1 != None : cur.execute("UPDATE patient SET allergie1 = ? WHERE id_person = ?", (allergie1, id_person_inserted))
    if allergie2 != None : cur.execute("UPDATE patient SET allergie2 = ? WHERE id_person = ?", (allergie2, id_person_inserted))
    if past_pathologies != None : cur.execute("UPDATE patient SET past_pathologies = ? WHERE id_person = ?", (past_pathologies, id_person_inserted))
    if date_entry != None : cur.execute("UPDATE patient SET date_entry = ? WHERE id_person = ?", ( date_entry, id_person_inserted))
    if marital_status != None : cur.execute("UPDATE patient SET marital_status = ? WHERE id_person = ?", ( marital_status, id_person_inserted))
    if religion != None : cur.execute("UPDATE patient SET religion = ? WHERE id_person = ?", ( religion, id_person_inserted))

    # Shoowing that the data is well added
    selection_join_query = """SELECT per.id, per.first_name, per.last_name, per.date_of_birth, pa.id_patient
                    FROM person per
                    INNER JOIN patient pa 
                    ON per.id = pa.id_person
                    WHERE per.id = ?
                    """
    added_data = cur.execute(selection_join_query,(id_person_inserted, )).fetchone()
    print ("The data has been added : ", added_data )

def insertion_doctor(first_name, last_name,sex, date_of_birth, primary_language, nationalnb, service, statut, login, password,  middle_name=None, birth_place=None, email=None, phoneH=None, phoneB=None, nationality=None ):    #insertion into the doctor's table
    #if the person is already present, it will get the id and if not it will create it
    id_person_inserted = insert_person(first_name, last_name, date_of_birth, sex, primary_language, nationalnb, middle_name, birth_place, email, phoneH, phoneB, nationality)
    
    #insertion into the patient's table
    #then we insert it into the patient's table
    data_doctor = (id_person_inserted, service, statut, login, password)
    insert_query_patient = "INSERT INTO doctor (id_person, service, statut, login, password) VALUES ( ?, ?, ?, ?, ?)"
    existing_data_patient = cur.execute("SELECT * FROM doctor where  id_person = ? AND service = ? AND statut = ? AND login = ? AND password = ?", (data_doctor[0], data_doctor[1], data_doctor[2], data_doctor[3], data_doctor[4])).fetchone()
    if not existing_data_patient : 
        #data is not present execute the inquery
        cur.execute(insert_query_patient, data_doctor)
    else : return(print("Doctor already present in the table patient"))

    # Showing that the data is well added
    selection_join_query = """SELECT per.id, per.first_name, per.last_name, per.date_of_birth, do.id_doctor
                    FROM person per
                    INNER JOIN doctor do 
                    ON per.id = do.id_person
                    WHERE per.id = ?
                    """
    added_data = cur.execute(selection_join_query,(id_person_inserted, )).fetchone()
    print ("The data has been added : ", added_data )


def insert_hospital_service(name):
    try:
        cur.execute("""
            INSERT INTO service (name)
            VALUES (?)
        """, (name,))
        conn.commit()

        print("Hospital service '{}' inserted successfully".format(name))

    except sqlite3.Error as e:
        print("Error inserting hospital service:", e)

##################################################################################################################
# Services insertion 
##################################################################################################################

""" insert_hospital_service("Cardiology")
insert_hospital_service("Pediatrics")
insert_hospital_service("Neurology")
insert_hospital_service("Oncology")
insert_hospital_service("Orthopedics")
insert_hospital_service("Dermatology")
insert_hospital_service("Gastroenterology")
insert_hospital_service("Urology")
insert_hospital_service("Ophthalmology")
insert_hospital_service("Radiology")
insert_hospital_service("Hematology")
insert_hospital_service("Endocrinology")
insert_hospital_service("Pulmonology")
insert_hospital_service("Nephrology")
insert_hospital_service("Otolaryngology") """

##################################################################################################################
# Doctor insertion 
##################################################################################################################
""" insertion_doctor("Jack", "Johnson","M", "1980-12-12","English","123456789", "1","I","Jack.Johnson@ulb.be","1234")
insertion_doctor("Emily", "Smith", "F", "1985-05-25", "Spanish", "987654321", "2", "E", "emily.smith@example.com", "5678")
insertion_doctor("Michael", "Brown", "M", "1976-09-15", "French", "555123456", "3", "P", "michael.brown@example.com", "9012")
insertion_doctor("Sophia", "Lee", "F", "1990-02-08", "Mandarin", "111222333", "4", "P", "sophia.lee@example.com", "3456")
 """

##################################################################################################################
# Patient insertion 
##################################################################################################################


""" insertion_patient("Emily", "Smith", "F", "1990-07-20", "English", 987654321, 2, 2, 3, "I", 123456789, 
                   middle_name="Grace", birth_place="London", email="emily.smith@example.com", nationality="British", 
                   phoneH="111-222-333", phoneB="444-555-666", chamber=15, bed=3, patient_source="Clinic", 
                   allergie1='2003', allergie2=None, past_pathologies=6, date_entry='2024-05-15', 
                   marital_status='Single', religion='None')

insertion_patient("Sophia", "Brown", "F", "1982-09-10", "English", 555555555, 1, 1, 4, "E", 777777777,
                   middle_name="Rose", birth_place="Manchester", email="sophia.brown@example.com", nationality="British", 
                   phoneH="111-111-111", phoneB="222-222-222", chamber=10, bed=1, patient_source="Emergency", 
                   allergie1='2002', allergie2='2005', past_pathologies=None, date_entry='2024-05-18', 
                   marital_status='Divorced', religion='Christian')

insertion_patient("Daniel", "Johnson", "M", "1975-04-03", "English", 666666666, 1, 2, 1, "O", 888888888,
                   middle_name="Robert", birth_place="Birmingham", email="daniel.johnson@example.com", nationality="British", 
                   phoneH="333-333-333", phoneB="444-444-444", chamber=7, bed=4, patient_source="Referral", 
                   allergie1='2004', allergie2='2006', past_pathologies=None, date_entry='2024-05-20', 
                   marital_status='Married', religion='None')

insertion_patient("Emma", "Wilson", "F", "1995-12-28", "English", 999999999, 4, 3, 2, "P", 222222222,
                   middle_name="Louise", birth_place="Liverpool", email="emma.wilson@example.com", nationality="British", 
                   phoneH="555-555-555", phoneB="666-666-666", chamber=20, bed=3, patient_source="Walk-in", 
                   allergie1='2007', allergie2=None, past_pathologies=1, date_entry='2024-05-22', 
                   marital_status='Single', religion='None')


insertion_patient("Josie", "Blacket", "F", "1995-12-28", "English", 124996998, 4, 3, 2, "E", 56148113579,
                   middle_name="Louise", birth_place="Liverpool", email="emma.wilson@example.com", nationality="British", 
                   phoneH="555-555-555", phoneB="666-666-666", chamber=20, bed=3, patient_source="Walk-in", 
                   allergie1='2009', allergie2=None, past_pathologies=1, date_entry='2024-05-22', 
                   marital_status='Single', religion='None')


insertion_patient("Étienne", "Dupont", "M", "1987-06-25", "French", 111222333, 1, 2, 3, "P", 111111111, 
                   middle_name="Jean", birth_place="Paris", email="etienne.dupont@example.com", nationality="French", 
                   phoneH="111-111-111", phoneB="222-222-222", chamber=10, bed=1, patient_source="Referral", 
                   allergie1=None, allergie2=None, past_pathologies=2, date_entry='2024-05-20', 
                   marital_status='Married', religion='Catholic')

insertion_patient("Camille", "Lefèvre", "F", "1992-09-10", "French", 444555666, 2, 3, 4, "I", 222333444, 
                   middle_name="Louise", birth_place="Lyon", email="camille.lefevre@example.com", nationality="French", 
                   phoneH="333-333-333", phoneB="444-444-444", chamber=15, bed=2, patient_source="Walk-in", 
                   allergie1='Pollen', allergie2=None, past_pathologies=3, date_entry='2024-05-21', 
                   marital_status='Single', religion='None')

insertion_patient("Antoine", "Martin", "M", "1995-04-15", "French", 777888999, 4, 2, 1, "P", 333444555, 
                   middle_name="Pierre", birth_place="Marseille", email="antoine.martin@example.com", nationality="French", 
                   phoneH="555-555-555", phoneB="666-666-666", chamber=20, bed=3, patient_source="Emergency", 
                   allergie1='Dust', allergie2='Peanuts', past_pathologies=1, date_entry='2024-05-22', 
                   marital_status='Single', religion='None') """

##################################################################################################################
# Allergies and pathologies insertion 
##################################################################################################################

def fill_add_data():
    allergies_data = [
        ("Peanuts",'2001'),
        ("Penicillin",'2002'),
        ("Shellfish",'2003'),
        ("Eggs",'2004'),
        ("Soy",'2005'),
        ("Milk",'2006'),
        ("Wheat",'2007'),
        ("Tree nuts",'2008'),
        ("Fish",'2009'),
        ("Sesame",'2010')
    ]

    pathologies_data = [
        ("Common cold", "A viral infection of your nose and throat (upper respiratory tract)"),
        ("Influenza", "A common viral infection that can be deadly, especially in high-risk groups"),
        ("Asthma", "A condition in which your airways narrow and swell and produce extra mucus"),
        ("Diabetes", "A group of diseases that affect how your body uses blood sugar (glucose)"),
        ("Hypertension", "High blood pressure, a common condition in which the long-term force of the blood against your artery walls is high enough that it may eventually cause health problems, such as heart disease"),
        ("Arthritis", "Inflammation of one or more of your joints"),
        ("Obesity", "A complex disease involving an excessive amount of body fat"),
        ("Migraine", "A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound"),
        ("Depression", "A mood disorder that causes a persistent feeling of sadness and loss of interest"),
        ("Anxiety", "A feeling of worry, nervousness, or unease, typically about an imminent event or something with an uncertain outcome")
    ]

    for allergy_data in allergies_data:
        cur.execute("INSERT INTO allergies (name, id) VALUES (?, ?)", allergy_data)

    for pathology_data in pathologies_data:
        cur.execute("INSERT INTO pathologies (name, description) VALUES (?, ?)", pathology_data)

    conn.commit()

fill_add_data()



##################################################################################################################
# Prints and clear table
##################################################################################################################

def clear_tables():
    tables = ["patient", "person", "doctor", "allergies", "pathologies"]

    try: 
        for table in tables:
            cur.execute(f"DELETE FROM {table}")
            conn.commit()
        
        print("All tables cleared successfully.")
    except Exception as e:
        print(f"Error clearing tables: {e}")


#clear_tables()

def print_all_patients():
    cur.execute("SELECT * FROM patient")

    patients = cur.fetchall()

    
    print("Patients:")
    for patient in patients:
        print(patient)


#print_all_patients()

def print_all_persons():

    cur.execute("SELECT * FROM person")
    persons = cur.fetchall()

    print("Persons:")
    for person in persons:
        print(person)


#print_all_persons()


def print_all_doctors():

    cur.execute("SELECT * FROM doctor")

    doctors = cur.fetchall()

    
    print("Doctor:")
    for doctor in doctors:
        print(doctor)



#print_all_doctors()


def print_patient_doctors():

    try:
        cur.execute("""
            SELECT patient.id_patient, person.first_name AS patient_first_name, person.last_name AS patient_last_name, 
                   doctor.id_doctor, doctor.first_name AS doctor_first_name, doctor.last_name AS doctor_last_name
            FROM patient
            INNER JOIN person ON patient.id_person = person.id
            INNER JOIN doctor ON patient.id_doctor = doctor.id_doctor
        """)
        
        rows = cur.fetchall()
        
        for row in rows:
            patient_id, patient_first_name, patient_last_name, doctor_id, doctor_first_name, doctor_last_name = row
            print(f"Patient ID: {patient_id}, Patient Name: {patient_first_name} {patient_last_name}, Doctor: {doctor_first_name} {doctor_last_name}")

    except sqlite3.Error as e:
        print("Error retrieving patient doctors:", e)

#print_patient_doctors()

def print_prescriptions():
 
    try:
        cur.execute("SELECT * FROM prescription")
        prescriptions = cur.fetchall()

        if prescriptions:
            print("Prescriptions:")
            for prescription in prescriptions:
                print("Prescription ID:", prescription[0])
                print("Concerned Patient ID:", prescription[1])
                print("Doctor ID:", prescription[2])
                print("Medicament ID:", prescription[3])
                print("Minimum Amount to Give:", prescription[4])
                print("Maximum Amount to Give:", prescription[5])
                print("Give Units:", prescription[6])
                print("Administration Instruction:", prescription[7])
                print("Dispense Amount:", prescription[8])
                print("Dispense Units:", prescription[9])
                print("Frequency:", prescription[10])
                print("Notes:", prescription[11])
                print()
        else:
            print("No prescriptions found.")

    except sqlite3.Error as e:
        print("Error fetching prescriptions:", e)

#print_prescriptions()


##################################################################################################################
# Fill all the tables 
##################################################################################################################

def fill_all_tables():

    fill_add_data()
    insert_hospital_service("Cardiology")
    insert_hospital_service("Pediatrics")
    insert_hospital_service("Neurology")
    insert_hospital_service("Oncology")
    insert_hospital_service("Orthopedics")
    insert_hospital_service("Dermatology")
    insert_hospital_service("Gastroenterology")
    insert_hospital_service("Urology")
    insert_hospital_service("Ophthalmology")
    insert_hospital_service("Radiology")
    insert_hospital_service("Hematology")
    insert_hospital_service("Endocrinology")
    insert_hospital_service("Pulmonology")
    insert_hospital_service("Nephrology")
    insert_hospital_service("Otolaryngology")

    insertion_patient("Emily", "Smith", "F", "1990-07-20", "English", 987654321, 2, 2, 3, "I", 123456789, 
                   middle_name="Grace", birth_place="London", email="emily.smith@example.com", nationality="British", 
                   phoneH="111-222-333", phoneB="444-555-666", chamber=15, bed=3, patient_source="Clinic", 
                   allergie1='2003', allergie2=None, past_pathologies=6, date_entry='2024-05-15', 
                   marital_status='Single', religion='None')

    insertion_patient("Sophia", "Brown", "F", "1982-09-10", "English", 555555555, 1, 1, 4, "E", 777777777,
                    middle_name="Rose", birth_place="Manchester", email="sophia.brown@example.com", nationality="British", 
                    phoneH="111-111-111", phoneB="222-222-222", chamber=10, bed=1, patient_source="Emergency", 
                    allergie1='2002', allergie2='2005', past_pathologies=None, date_entry='2024-05-18', 
                    marital_status='Divorced', religion='Christian')

    insertion_patient("Daniel", "Johnson", "M", "1975-04-03", "English", 666666666, 1, 2, 1, "O", 888888888,
                    middle_name="Robert", birth_place="Birmingham", email="daniel.johnson@example.com", nationality="British", 
                    phoneH="333-333-333", phoneB="444-444-444", chamber=7, bed=4, patient_source="Referral", 
                    allergie1='2004', allergie2='2006', past_pathologies=None, date_entry='2024-05-20', 
                    marital_status='Married', religion='None')

    insertion_patient("Emma", "Wilson", "F", "1995-12-28", "English", 999999999, 4, 3, 2, "P", 222222222,
                    middle_name="Louise", birth_place="Liverpool", email="emma.wilson@example.com", nationality="British", 
                    phoneH="555-555-555", phoneB="666-666-666", chamber=20, bed=3, patient_source="Walk-in", 
                    allergie1='2007', allergie2=None, past_pathologies=1, date_entry='2024-05-22', 
                    marital_status='Single', religion='None')


    insertion_patient("Josie", "Blacket", "F", "1995-12-28", "English", 124996998, 4, 3, 2, "E", 56148113579,
                    middle_name="Louise", birth_place="Liverpool", email="emma.wilson@example.com", nationality="British", 
                    phoneH="555-555-555", phoneB="666-666-666", chamber=20, bed=3, patient_source="Walk-in", 
                    allergie1='2009', allergie2=None, past_pathologies=1, date_entry='2024-05-22', 
                    marital_status='Single', religion='None')


    insertion_patient("Étienne", "Dupont", "M", "1987-06-25", "French", 111222333, 1, 2, 3, "P", 111111111, 
                    middle_name="Jean", birth_place="Paris", email="etienne.dupont@example.com", nationality="French", 
                    phoneH="111-111-111", phoneB="222-222-222", chamber=10, bed=1, patient_source="Referral", 
                    allergie1=None, allergie2=None, past_pathologies=2, date_entry='2024-05-20', 
                    marital_status='Married', religion='Catholic')

    insertion_patient("Camille", "Lefèvre", "F", "1992-09-10", "French", 444555666, 2, 3, 4, "I", 222333444, 
                    middle_name="Louise", birth_place="Lyon", email="camille.lefevre@example.com", nationality="French", 
                    phoneH="333-333-333", phoneB="444-444-444", chamber=15, bed=2, patient_source="Walk-in", 
                    allergie1='2008', allergie2=None, past_pathologies=3, date_entry='2024-05-21', 
                    marital_status='Single', religion='None')

    insertion_patient("Antoine", "Martin", "M", "1995-04-15", "French", 777888999, 4, 2, 1, "P", 333444555, 
                    middle_name="Pierre", birth_place="Marseille", email="antoine.martin@example.com", nationality="French", 
                    phoneH="555-555-555", phoneB="666-666-666", chamber=20, bed=3, patient_source="Emergency", 
                    allergie1='2010', allergie2='2001', past_pathologies=1, date_entry='2024-05-22', 
                    marital_status='Single', religion='None')
    
    insertion_doctor("Jack", "Johnson","M", "1980-12-12","English","123456789", "1","I","Jack.Johnson@ulb.be","1234")
    insertion_doctor("Emily", "Smith", "F", "1985-05-25", "Spanish", "987654321", "2", "E", "emily.smith@example.com", "5678")
    insertion_doctor("Michael", "Brown", "M", "1976-09-15", "French", "555123456", "3", "P", "michael.brown@example.com", "9012")
    insertion_doctor("Sophia", "Lee", "F", "1990-02-08", "Mandarin", "111222333", "4", "P", "sophia.lee@example.com", "3456")

fill_all_tables()


cur.close()
conn.commit()