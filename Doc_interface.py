import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import PhotoImage
import tkinter.font as tkfont
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from pharmacy_order import pharma_order

##################################################################################################################
# This is the main window, the doctor interface (which we can still complete with additional functions)

# The window opens accordingly to the physician that you chose in choose_doctor.py
# The interface that opens is fit for this doctor: only his patients will appear 
# Depending on the status of the physician (Intern, extern or physician) she/he/they can prescribe or not
# For example emily.smith@example.com is an extern that cannot prescribe but Jack.Johnson@ulb.be can prescribe 
##################################################################################################################

conn = sqlite3.connect("db_MIS.db")  
cur = conn.cursor()

def open_interface_window_doctor(login): 
    interface_window = tk.Tk()
    interface_window.title("Welcome to our medical plateform!")

    def view_appointments():
        print("Viewing all appointments...")


    def display_patient_info(info_text, name_listbox):
        selected_index = name_listbox.curselection()
        if selected_index:
            selected_name = name_listbox.get(selected_index)
            selected_first_name, selected_last_name = selected_name.split()
            print(selected_first_name, selected_last_name)
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

        # Retrieve the names of patients under the care of the doctor
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



       
       
    ##################################################################################################################
    # Frames
    ##################################################################################################################

    review_frame = tk.Frame(interface_window, borderwidth=2, relief="groove")
    review_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    appointment_frame = tk.Frame(interface_window, borderwidth=2, relief="groove")
    appointment_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    view_appointments_frame = tk.Frame(interface_window, borderwidth=2, relief="groove")
    view_appointments_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    list_patient_frame = tk.Frame(interface_window, borderwidth=2, relief="groove")
    list_patient_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

     
    bold_font = tk.font.Font(weight='bold')
    personal_info_label = tk.Label(review_frame, text="Results review", font=bold_font)
    personal_info_label.pack()

    appointment_label = tk.Label(appointment_frame, text="Order for pharmacy", font=bold_font)
    appointment_label.pack()

    view_appointments_label = tk.Label(view_appointments_frame, text="View All Appointments", font=bold_font)
    view_appointments_label.pack()

    list_patient_label = tk.Label(list_patient_frame, text="List of patients", font=bold_font)
    list_patient_label.pack()

  

    MRI_button = tk.Button(review_frame, text="MRI results")
    MRI_button.pack()

    X_ray_button = tk.Button(review_frame, text="Xrays results")
    X_ray_button.pack()

    CT_button = tk.Button(review_frame, text="CT scan results")
    CT_button.pack()

    lab_button = tk.Button(review_frame, text="Lab results")
    lab_button.pack()

    def pharma_check(login): 
        query = "SELECT statut FROM doctor WHERE login = ?"
        cur.execute(query, (login,))
        result = cur.fetchone()
        if result:
            if result[0] == "E":
                messagebox.showerror("Error", "You do not have the authorization to prescribe. Please contact your supervisor if needed.")
            else:
                pharma_order(login)
        else:
            messagebox.showerror("Error", "Doctor with login {} not found.".format(login))


    order_pharma_button = tk.Button(appointment_frame, text="Create a new order", command=lambda: pharma_check(login))
    order_pharma_button.pack()

    view_appointments_button = tk.Button(view_appointments_frame, text="View Appointments", command=view_appointments)
    view_appointments_button.pack()



    name_listbox = tk.Listbox(list_patient_frame, width=40, height=10)
    name_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    
    scrollbar = tk.Scrollbar(list_patient_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar.config(command=name_listbox.yview)
    name_listbox.config(yscrollcommand=scrollbar.set)

    name_listbox.bind("<<ListboxSelect>>", lambda event: display_patient_info(info_text, name_listbox))

    info_text = tk.Text(list_patient_frame, width=40, height=10)
    info_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    info_text.config(state=tk.DISABLED)

    display_patient_names(name_listbox,login)

    interface_window.rowconfigure(0, weight=1)
    interface_window.rowconfigure(1, weight=1)
    interface_window.columnconfigure(0, weight=1)
    interface_window.columnconfigure(1, weight=1)

        
    interface_window.mainloop()
