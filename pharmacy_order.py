import tkinter as tk
from tkinter import messagebox
import sqlite3
#from drug_info import drug_window
#from drug_info import save_variables
import HL7_msg
import random
import string
import os


##################################################################################################################
# This is the order window where you place your medicine order to the pharmacy

# The physician has to choose one of the patients and search for the needed medicine. When both are selected, 
# the medicine details appear an the physician can modifie it as wished

# Before sending an order, make sure to execute in a split terminal the HL7_recieve function that will recieve the order
# When the order is sent, the prescription is added to the prescription table and a .txt is created in the Prescriptions
# folder with the information of the prescription
##################################################################################################################

conn = sqlite3.connect("db_MIS.db")  # Connect to the db_MIS.db database
cur = conn.cursor()
rde_server = HL7_msg.HL7Server('localhost', 2575, HL7_msg.handle_rde_message)

def pharma_order(login):

    def display_patient_info(info_text, name_listbox):
        selected_index = name_listbox.curselection()
        if selected_index:
            selected_name = name_listbox.get(selected_index)
            selected_first_name, selected_last_name = selected_name.split()
            
            cur.execute("""
                SELECT patient.*, person.*
                FROM patient
                INNER JOIN person ON patient.id_person = person.id
                WHERE person.first_name=? AND person.last_name=?
            """, (selected_first_name, selected_last_name))
            patient_info = cur.fetchone()
            

            cur.execute("""SELECT * FROM person WHERE first_name=? AND last_name=?""", (selected_first_name, selected_last_name))
            person_info = cur.fetchone()
            
            if person_info:
                id = person_info[0]
                first_name = person_info[1]
                middle_name = person_info[2]
                last_name = person_info[3]
                date_of_birth = person_info[6]
                birth_place = person_info[5]
                sex = person_info[4]
                email = person_info[7]
                Phone_home = person_info[8]
                Phone_business = person_info[9]
                primary_langage = person_info[10]
                nationality = person_info[11]
                national_number = person_info[12]    

            if patient_info:
                # Fetch pathology and allergy IDs
                pathology_id = patient_info[9]
                allergy1_id = patient_info[7]
                allergy2_id = patient_info[8]
            
                cur.execute("SELECT name FROM pathologies WHERE id_pathology=?", (pathology_id,))
                pathology_name = cur.fetchone()[0] if pathology_id else "None"

                cur.execute("SELECT name FROM allergies WHERE id=?", (allergy1_id,))
                allergy1_name = cur.fetchone()[0] if allergy1_id else "None"

                cur.execute("SELECT name FROM allergies WHERE id=?", (allergy2_id,))
                allergy2_name = cur.fetchone()[0] if allergy2_id else "None"

                info_text.config(state=tk.NORMAL)
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, f"First name: {first_name}\n")
                info_text.insert(tk.END, f"Middle name: {middle_name}\n")
                info_text.insert(tk.END, f"Last name: {last_name}\n")
                info_text.insert(tk.END, f"Date of birth: {date_of_birth}\n")
                info_text.insert(tk.END, f"Birth place: {birth_place}\n")
                info_text.insert(tk.END, f"Sex: {sex}\n")
                info_text.insert(tk.END, f"Patient ID: {patient_info[0]}\n")
                info_text.insert(tk.END, f"Person ID: {patient_info[1]}\n")
                info_text.insert(tk.END, f"Doctor's name: {patient_info[2]}\n")
                info_text.insert(tk.END, f"Patient Class: {patient_info[3]}\n")
                info_text.insert(tk.END, f"Chamber: {patient_info[4]}\n")
                info_text.insert(tk.END, f"Bed: {patient_info[5]}\n")
                info_text.insert(tk.END, f"Patient Source: {patient_info[6]}\n")
                info_text.insert(tk.END, f"Allergy 1: {allergy1_name}\n")
                info_text.insert(tk.END, f"Allergy 2: {allergy2_name}\n")
                info_text.insert(tk.END, f"Current Pathologies: {pathology_name}\n")
                info_text.insert(tk.END, f"Past Pathologies: {patient_info[10]}\n")
                info_text.insert(tk.END, f"Date of Entry: {patient_info[11]}\n")
                info_text.insert(tk.END, f"Date of Exit: {patient_info[12]}\n")
                info_text.insert(tk.END, f"Service ID: {patient_info[13]}\n")
                info_text.insert(tk.END, f"Social Security Number: {patient_info[14]}\n")
                info_text.insert(tk.END, f"Marital Status: {patient_info[15]}\n")
                info_text.insert(tk.END, f"Religion: {patient_info[16]}\n")
                info_text.insert(tk.END, f"Email: {email}\n")
                info_text.insert(tk.END, f"Phone Home: {Phone_home}\n")
                info_text.insert(tk.END, f"Phone Buisness: {Phone_business}\n")
                info_text.insert(tk.END, f"Primary language: {primary_langage}\n")
                info_text.insert(tk.END, f"Nationality: {nationality}\n")
                info_text.insert(tk.END, f"National number: {national_number}\n")

                info_text.config(state=tk.DISABLED)
                

    def display_patient_names(name_listbox, login):

        cur.execute("SELECT id_doctor FROM doctor WHERE login=?", (login,))
        doctor_id = cur.fetchone()[0]

        cur.execute("""
            SELECT p.first_name, p.last_name
            FROM patient AS pt
            INNER JOIN person AS p ON pt.id_person = p.id
            WHERE pt.id_doctor = ?
        """, (doctor_id,))
        

        patient_names = cur.fetchall()
       
        for patient_name in patient_names:
            full_name = f"{patient_name[0]} {patient_name[1]}"
            name_listbox.insert(tk.END, full_name)

    def on_patient_select(event):
        selected_index = name_listbox.curselection()
        if selected_index:
            selected_patient = name_listbox.get(selected_index)
            display_patient_info(info_text, name_listbox)


            


    def choose_patient():
        selected_index = name_listbox.curselection()
        if selected_index:
            selected_name = name_listbox.get(selected_index)
            selected_first_name, selected_last_name = selected_name.split()

            cur.execute("SELECT * FROM patient INNER JOIN person ON patient.id_person = person.id WHERE person.first_name=? AND person.last_name=?", (selected_first_name, selected_last_name))
            patient_info = cur.fetchone()
            
            global id_patient
            global doctor
            global patient_class
            global chamber
            global bed
            global patient_source
            global allergie1
            global allergie2
            global curent_pathologies
            global past_pathologies
            global date_entry
            global date_out
            global service
            global SS_number
            global marital_status
            global religion
            global id
            global first_name
            global middle_name
            global last_name
            global date_of_birth
            global birth_place
            global sex
            global email
            global Phone_business
            global Phone_home
            global primary_langage
            global nationality
            global national_number

            if patient_info:
                id_patient = patient_info[0]
                doctor = patient_info[2]
                patient_class = patient_info[3]
                chamber = patient_info[4]
                bed = patient_info[5]
                patient_source = patient_info[6]
                allergie1 =  patient_info[7]
                print(type(allergie1))
                allergie2  =  patient_info[8]
                curent_pathologies =  patient_info[9]
                past_pathologies  =  patient_info[10]
                date_entry  =  patient_info[11]
                date_out  =  patient_info[12]
                service  =  patient_info[13]
                SS_number =  patient_info[14]
                marital_status  =  patient_info[15]
                religion  =  patient_info[16]
     
                
            cur.execute("""SELECT * FROM person WHERE first_name=? AND last_name=?""", (selected_first_name, selected_last_name))
            person_info = cur.fetchone()
            if person_info:
                id = person_info[0]
                first_name = person_info[1]
                middle_name = person_info[2]
                last_name = person_info[3]
                date_of_birth = person_info[6]
                birth_place = person_info[5]
                sex = person_info[4]
                email = person_info[7]
                Phone_home = person_info[8]
                Phone_business = person_info[9]
                primary_langage = person_info[10]
                nationality = person_info[11]
                national_number = person_info[12]    

                return id, first_name,middle_name,last_name,date_of_birth,birth_place,sex, email,Phone_home,Phone_business,primary_langage,national_number,nationality, id_patient, doctor, patient_class, chamber, bed, patient_source, allergie1, allergie2, curent_pathologies, past_pathologies, date_entry, date_out,service,SS_number, marital_status, religion
                
            else:
                messagebox.showerror("Error", "Please select a patient.")

    
    def get_medicament_id(medicament_name):
        cur.execute("SELECT id_medicament FROM medicament WHERE name=?", (medicament_name,))
        medicament_id = cur.fetchone()
        if medicament_id:
            return medicament_id[0]
        else:
            print("Medicament not found")
            return None
        
    def insert_prescription(id_prescription, id_concerned_patient, id_doctor, medicament, give_min_amount, give_max_amount, give_units, admin_instruction,dispense_amount, dispense_unit, frequency, notes):
        
        try:
            cur.execute("SELECT id_prescription FROM prescription WHERE id_prescription=?", (id_prescription,))
            existing_prescription = cur.fetchone()
            
            if existing_prescription:
                print("Prescription already exists with ID:", id_prescription)
                return

            medicament_id = get_medicament_id(medicament)
            print(medicament_id)
            cur.execute("""
                INSERT INTO prescription (id_prescription, id_concerned_patient, id_doctor, medicament, give_min_amout, give_max_amout, give_units, admin_instruction, dispense_amount, dispense_units, frequency, notes)
                VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_prescription, id_concerned_patient, id_doctor, medicament_id, give_min_amount, give_max_amount, give_units, admin_instruction, dispense_amount, dispense_unit, frequency, notes))
            conn.commit()
            print("Data inserted successfully")
        except sqlite3.Error as e:
            print("Error inserting data:", e)

        
    def generate_random_string(length=20):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))


    def write_prescription_to_txt(file_name,  id_prescription, id_concerned_patient, id_doctor, medicament, give_min_amount, give_max_amount, give_units, admin_instruction, dispense_amount, dispense_units, frequency, notes):
        folder_path = 'Prescriptions'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name + '.txt')
        try:
            with open(file_path, 'a') as file:
                file.write("Prescription ID: {}\n".format(id_prescription))
                file.write("Patient ID: {}\n".format(id_concerned_patient))
                file.write("Doctor ID: {}\n".format(id_doctor))
                file.write("Medicament: {}\n".format(medicament))
                file.write("Give Min Amount: {}\n".format(give_min_amount))
                if give_max_amount is not None:
                    file.write("Give Max Amount: {}\n".format(give_max_amount))
                file.write("Give Units: {}\n".format(give_units))
                if admin_instruction:
                    file.write("Admin Instruction: {}\n".format(admin_instruction))
                if dispense_amount is not None:
                    file.write("Dispense Amount: {}\n".format(dispense_amount))
                if dispense_units:
                    file.write("Dispense Units: {}\n".format(dispense_units))
                if frequency:
                    file.write("Frequency: {}\n".format(frequency))
                if notes:
                    file.write("Notes: {}\n".format(notes))
                file.write("\n")
            print("Prescription data written to", file_path)
        except Exception as e:
            print("Error writing prescription data to file:", e)

    def prepare_message(): 
        global id_patient
        global doctor
        global patient_class
        global chamber
        global bed
        global patient_source
        global allergie1
        global allergie2
        global curent_pathologies
        global past_pathologies
        global date_entry
        global date_out
        global service
        global SS_number
        global marital_status
        global religion
        global id
        global first_name
        global middle_name
        global last_name
        global date_of_birth
        global birth_place
        global sex
        global email
        global Phone_business
        global Phone_home
        global primary_langage
        global nationality
        global national_number
        global medicament
        full_name = ''.join([first_name, last_name])
        urgency_value = urgency_var.get()
        substitution_value = substitution_var.get()
        if (urgency_value == True): 
            urgent = "A"
        else: 
            urgent = "R"

        code = code_entry.get()
        minAmount = min_amount_entry.get()
        maxAmount = max_amount_entry.get()
        Units = units_entry.get()
        Admin_instru = admin_instruction_entry.get()
        dispense_amount = dispense_amount_entry.get()
        dispense_unit = dispense_units_entry.get()
        frequency = frequency_entry.get()
        notes = prescription_notes_entry.get()
        deadline = deadline_entry.get()
        id_prescription = generate_random_string()
        id_doctor = '123456'
        cur.execute("SELECT name FROM allergies WHERE id=?", (allergie1,))
        allergie1_name = cur.fetchone()[0] if allergie1 else "None"
        #id, first_name, middle_name, last_name, date_of_birth, birth_place, sex, email, Phone_home, Phone_business, primary_langage, national_number, nationality, id_patient, doctor, patient_class, chamber, bed, patient_source, allergie1, allergie2, curent_pathologies, past_pathologies, date_entry, date_out, service, SS_number, marital_status, religion = patient_info
        HL7_msg.send_rde_message(rde_server,first_name, last_name,date_of_birth,sex,Phone_home, Phone_business, primary_langage, marital_status,religion,SS_number,birth_place,nationality,doctor,service, date_entry, date_out, bed, chamber, code, minAmount, maxAmount, Units, Admin_instru, dispense_amount, dispense_unit, frequency, notes, urgent, deadline, allergie1, allergie1_name, medicament)
        insert_prescription(id_prescription, id_patient, id_doctor, medicament, minAmount, maxAmount, Units, Admin_instru,dispense_amount, dispense_unit, frequency, notes)
        write_prescription_to_txt(full_name, id_prescription, id_patient, id_doctor, medicament, minAmount, maxAmount, Units, Admin_instru, dispense_amount, dispense_unit, frequency, notes)
    
    
    def search_medicine():
        search_term = search_entry.get()
        cur.execute("SELECT * FROM medicament WHERE name LIKE ?", ('%' + search_term + '%',))
        medicines = cur.fetchall()
        medicine_listbox.delete(0, tk.END)
        for medicine in medicines:
            medicine_listbox.insert(tk.END, medicine[1])

    def display_medicine_info():
        selected_index = medicine_listbox.curselection()
        if selected_index:
            selected_medicine = medicine_listbox.get(selected_index)
            cur.execute("SELECT * FROM medicament WHERE name=?", (selected_medicine,))
            medicine_info = cur.fetchone()
            if medicine_info:
                medicine_details_text.config(state=tk.NORMAL)
                medicine_details_text.delete(1.0, tk.END)
                medicine_details_text.insert(tk.END, f"Name: {medicine_info[1]}\n")
                medicine_details_text.insert(tk.END, f"Class: {medicine_info[2]}\n")
                medicine_details_text.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "Medicine not found in database.")


    def select_medecine(): 
        selected_index = medicine_listbox.curselection()
        if selected_index:
            selected_medicine = medicine_listbox.get(selected_index)
            cur.execute("SELECT * FROM MedicineDetails WHERE medicament=?", (selected_medicine,))
            medicine_details = cur.fetchone()
            return medicine_details
        
    def load_details_medecine(): 
        global medicament
        detail_medicine = select_medecine()
        medicament, code, give_min_amount, give_max_amount, give_units, admin_instruction, dispense_amount, dispense_units, frequency, notes = detail_medicine
         
        code_entry.delete(0, tk.END)  # Clear the current content
        code_entry.insert(0, code)  # Insert the dynamic value

        min_amount_entry.delete(0, tk.END) 
        min_amount_entry.insert(0, give_min_amount)

        max_amount_entry.delete(0, tk.END) 
        max_amount_entry.insert(0, give_max_amount)

        units_entry.delete(0, tk.END) 
        units_entry.insert(0, give_units)

        admin_instruction_entry.delete(0, tk.END) 
        admin_instruction_entry.insert(0, admin_instruction)

        dispense_amount_entry.delete(0, tk.END) 
        dispense_amount_entry.insert(0, dispense_amount)

        dispense_units_entry.delete(0, tk.END) 
        dispense_units_entry.insert(0, dispense_units)

        prescription_notes_entry.delete(0, tk.END) 
        prescription_notes_entry.insert(0, notes)

        frequency_entry.delete(0, tk.END) 
        frequency_entry.insert(0, frequency)
        

    ###########################################################################
    #   INTERFACE 
    ###########################################################################    
    
    pharma_window = tk.Toplevel()
    pharma_window.title("Pharmacy Order")

    patient_frame = tk.Frame(pharma_window)
    patient_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    tk.Label(patient_frame, text="Select Patient:").pack()

    name_listbox = tk.Listbox(pharma_window, width=20, height=10)
    name_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(pharma_window, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar.config(command=name_listbox.yview)
    name_listbox.config(yscrollcommand=scrollbar.set)

    name_listbox.bind("<<ListboxSelect>>", on_patient_select)

    info_text = tk.Text(pharma_window, width=40, height=10)
    info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    info_text.config(state=tk.DISABLED)

    display_patient_names(name_listbox,login)

    search_frame = tk.Frame(pharma_window)
    search_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

    search_label = tk.Label(search_frame, text="Search Medicine:")
    search_label.pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=(5, 0))

    search_button = tk.Button(search_frame, text="Search", command=search_medicine)
    search_button.pack(side=tk.LEFT, padx=(5, 0))

    select_button = tk.Button(search_frame, text="Select Medicine", command=load_details_medecine)
    select_button.pack(side=tk.LEFT, padx=(10, 0))

    select_button = tk.Button(search_frame, text="Select Patient", command=choose_patient)
    select_button.pack(side=tk.LEFT, padx=(15, 0))

    medicine_listbox = tk.Listbox(pharma_window, width=40, height=10)
    medicine_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    
    medicine_details_text = tk.Text(pharma_window, width=40, height=10)
    medicine_details_text.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    medicine_details_text.config(state=tk.DISABLED)

    medicine_listbox.bind("<<ListboxSelect>>", lambda event: display_medicine_info())    

    order_frame = tk.Frame(pharma_window)
    order_frame.pack(side=tk.TOP, padx=10, pady=(10, 0), fill=tk.X)

    order_details_frame = tk.Frame(order_frame)
    order_details_frame.pack(side=tk.TOP, padx=10, pady=(0, 10), fill=tk.X)

    tk.Label(order_details_frame, text="Code:").grid(row=0, column=0)
    code_entry = tk.Entry(order_details_frame, width=30)
    code_entry.insert(0,"")
    code_entry.grid(row=0, column=1)

    tk.Label(order_details_frame, text="MinAmount:").grid(row=1, column=0)
    min_amount_entry = tk.Entry(order_details_frame, width=30)
    min_amount_entry.insert(0,"")
    min_amount_entry.grid(row=1, column=1)

    tk.Label(order_details_frame, text="MaxAmount:").grid(row=2, column=0)
    max_amount_entry = tk.Entry(order_details_frame, width=30)
    max_amount_entry.insert(0,"")
    max_amount_entry.grid(row=2, column=1)

    tk.Label(order_details_frame, text="Units:").grid(row=3, column=0)
    units_entry = tk.Entry(order_details_frame, width=30)
    units_entry.insert(0,"")
    units_entry.grid(row=3, column=1)

    tk.Label(order_details_frame, text="Administration Instruction:").grid(row=4, column=0)
    admin_instruction_entry = tk.Entry(order_details_frame, width=30)
    admin_instruction_entry.insert(0,"")
    admin_instruction_entry.grid(row=4, column=1)

    tk.Label(order_details_frame, text="Dispense Amount:").grid(row=5, column=0)
    dispense_amount_entry = tk.Entry(order_details_frame, width=30)
    dispense_amount_entry.insert(0,"")
    dispense_amount_entry.grid(row=5, column=1)

    tk.Label(order_details_frame, text="Dispense Units:").grid(row=6, column=0)
    dispense_units_entry = tk.Entry(order_details_frame, width=30)
    dispense_units_entry.insert(0,"")
    dispense_units_entry.grid(row=6, column=1)


    tk.Label(order_details_frame, text="Frequency:").grid(row=7, column=0)
    frequency_entry = tk.Entry(order_details_frame, width=30)
    frequency_entry.insert(0,"")
    frequency_entry.grid(row=7, column=1)

    tk.Label(order_details_frame, text="Notes:").grid(row=8, column=0)
    prescription_notes_entry = tk.Entry(order_details_frame, width=30)
    prescription_notes_entry.insert(0,"")
    prescription_notes_entry.grid(row=8, column=1)

    tk.Label(order_details_frame, text="Deadline (days):").grid(row=9, column=0)
    deadline_entry = tk.Entry(order_details_frame, width=30)
    deadline_entry.insert(0,"")
    deadline_entry.grid(row=9, column=1)


    urgency_var = tk.BooleanVar()
    urgency_check = tk.Checkbutton(order_frame, text="Urgent", variable=urgency_var)
    urgency_check.pack(side=tk.TOP, padx=(0, 10), anchor="w")
    
    substitution_var = tk.BooleanVar()
    substitution_check = tk.Checkbutton(order_frame, text="Allow Substitutions", variable=substitution_var)
    substitution_check.pack(side=tk.TOP, padx=(0, 10), anchor="w")

    add_order_button = tk.Button(order_frame, text="Add Order", command=prepare_message, bg="blue")
    add_order_button.pack(side=tk.TOP, fill="x", pady=10, padx=(0, 10))

  

    pharma_window.mainloop()

    
 


#pharma_order()
