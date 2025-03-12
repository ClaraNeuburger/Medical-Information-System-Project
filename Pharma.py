import tkinter as tk
from PatientInfo import PatientInfo
from Table import Table
from tkinter import ttk
from tkinter import messagebox
from HL7_msg import get_command_info
from MIS_stock import Medicine
import sqlite3

class PharmacyApp(tk.Frame):
    def __init__(self, root, prescriptions):
        super().__init__(root)
        self.root = root
        self.root.title("Pharmacy Management System")


        self.count = 1
        self.patients=[]
        self.drugs=[]
        self.commands_data = {}
        self.commands_drug = {}
        for prescription in prescriptions:
            patient_info, drug_info = prescription
            self.patients.append(patient_info)
            self.drugs.append(drug_info)

        # Créer les onglets
        self.tabControl = ttk.Notebook(self.root)
        self.tab_orders = ttk.Frame(self.tabControl)
        self.tab_history = ttk.Frame(self.tabControl)
        self.tab_stock = ttk.Frame(self.tabControl)

        # Ajouter les onglets à l'onglet
        self.tabControl.add(self.tab_orders, text="Orders")
        self.tabControl.add(self.tab_history, text= "History")
        self.tabControl.add(self.tab_stock, text="Stocks management")

        self.medicine = Medicine()

        # Configurer les onglets
        self.configure_orders_tab()
        self.configure_history()
        self.configure_stock_tab()

        # Pack l'onglet
        self.tabControl.pack(expand=1, fill="both")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_resize(self, event):
        # Ajuste la largeur du canvas pour remplir le cadre
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw'), width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def configure_history(self): 
        # Créer le canvas et la barre de défilement
        self.canvas_hist = tk.Canvas(self.tab_history)
        self.canvas_hist.grid(row=0, column=0, sticky="nsew")
        self.scroll_y = ttk.Scrollbar(self.tab_history, orient='vertical', command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky='ns')

        # Configuration du canvas
        self.canvas_hist.configure(yscrollcommand=self.scroll_y.set)

        # Créer un cadre pour contenir les éléments de l'historique
        self.history_frame = tk.Frame(self.canvas_hist)
        self.canvas_hist.create_window((0, 0), window=self.history_frame, anchor='nw')

        # S'assurer que le canvas se redimensionne correctement
        self.history_frame.bind("<Configure>", self.on_frame_configure_hist)
        #self.tab_history.bind("<Configure>", self.on_frame_resize_hist)

        # Appliquer des styles pour une apparence esthétique
        self.history_frame.configure(bg="white", highlightbackground="gray", highlightthickness=1)

    def on_frame_configure_hist(self, event):
        # Ajuster la hauteur du canvas lorsque le cadre de l'historique est redimensionné
        self.canvas_hist.configure(scrollregion=self.canvas_hist.bbox("all"))

    '''def on_frame_resize_hist(self, event):
        # Ajuster la largeur du cadre de l'historique pour correspondre à celle du canvas
        self.canvas_hist.itemconfig(width=event.width)'''





    def configure_orders_tab(self):
        # Cadre des commandes
        self.frame_commands = ttk.Frame(self.tab_orders)
        self.frame_commands.pack(side="left", fill="y")

        # Liste des onglets de commandes
        self.tabControl_commands = ttk.Notebook(self.frame_commands, width=120)
        self.tabControl_commands.pack(side="left", fill="y")

        # Onglet "A traiter"
        self.tab_to_process = ttk.Frame(self.tabControl_commands)
        self.tabControl_commands.add(self.tab_to_process, text="To process")
        self.listbox_to_process = tk.Listbox(self.tab_to_process, width=200)
        self.listbox_to_process.pack(fill="both", expand=True)

        self.command_list(self.patients, self.drugs)

        # Associer la sélection de commande à la fonction on_command_click
        self.listbox_to_process.bind("<<ListboxSelect>>", self.on_command_click)

        self.frame_command_details = ttk.Frame(self.tab_orders)
        self.frame_command_details.pack(side="left", fill="both", expand=True)

        # Cadre supp
        self.frame_supp = tk.LabelFrame(self.frame_command_details, text="")
        self.frame_supp.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.label_supp = ttk.Label(self.frame_supp, text="")
        self.label_supp.grid(padx=20, pady=20)

        # Cadre pour les informations du patient
        self.frame_patient_information = tk.LabelFrame(self.frame_supp, text="Patient information")
        self.frame_patient_information.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.label_patient_info = ttk.Label(self.frame_patient_information, text="")
        self.label_patient_info.grid(padx=20, pady=20)

        # Cadre pour les informations de l'hospitalisation
        self.frame_hospitalization_information = tk.LabelFrame(self.frame_supp, text="Hospitalization information")
        self.frame_hospitalization_information.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.label_hospitalization_info = ttk.Label(self.frame_hospitalization_information, text="")
        self.label_hospitalization_info.grid(padx=20, pady=20)

        # Cadre pour les informations de la commande
        self.frame_command_info = tk.LabelFrame(self.frame_command_details, text="Order information")
        self.frame_command_info.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.label_command_info = ttk.Label(self.frame_command_info, text="")
        self.label_command_info.grid(padx=20, pady=20)

        # Création du Canvas pour envelopper le contenu du frame_command_info
        self.canvas = tk.Canvas(self.frame_command_info)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll_x = ttk.Scrollbar(self.frame_command_info, orient='horizontal', command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky='ew')

        # Configuration du canvas
        self.canvas.configure(xscrollcommand=self.scroll_x.set)
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # S'assurer que le canvas se redimensionne correctement
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.frame_command_info.bind("<Configure>", self.on_frame_resize)

        # Configurer le poids des lignes et des colonnes pour l'extension
        self.frame_command_info.grid_rowconfigure(0, weight=1)
        self.frame_command_info.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)

        self.LastNamePatient = PatientInfo(self.frame_patient_information, "Last Name : ", "")
        self.LastNamePatient.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.FirstNamePatient = PatientInfo(self.frame_patient_information, "First Name : ", "")
        self.FirstNamePatient.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.IDPatient = PatientInfo(self.frame_patient_information, "Patient ID : ", "")
        self.IDPatient.grid(row=0, column=0)

        self.Sex = PatientInfo(self.frame_patient_information, "Sex : ", "")
        self.Sex.grid(row=0, column=3, padx=10, pady=10)

        self.Adress = PatientInfo(self.frame_patient_information, "Adress : ", "")
        self.Adress.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.PhoneNumber = PatientInfo(self.frame_patient_information, "Phone number: ", "")
        self.PhoneNumber.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.email = PatientInfo(self.frame_patient_information, "Birthdate: ", "")
        self.email.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.SSN = PatientInfo(self.frame_patient_information, "Social Security Number: ", "")
        self.SSN.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.Religion = PatientInfo(self.frame_patient_information, "Religion : ", "")
        self.Religion.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.Nationality = PatientInfo(self.frame_patient_information, "Nationality: ", "")
        self.Nationality.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        self.Allergy = PatientInfo(self.frame_patient_information, "Allergy: ", "")
        self.Allergy.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        # configuration frame hospitalization information 
        self.HospitalizationStatus = PatientInfo(self.frame_hospitalization_information, "Status : ", "")
        self.HospitalizationStatus.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.Floor = PatientInfo(self.frame_hospitalization_information, "Floor : ", "")
        self.Floor.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.Room = PatientInfo(self.frame_hospitalization_information, "Room : ", "")
        self.Room.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.Bed = PatientInfo(self.frame_hospitalization_information, "Bed : ", "")
        self.Bed.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        self.Service = PatientInfo(self.frame_hospitalization_information, "Service : ", "")
        self.Service.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.Source = PatientInfo(self.frame_hospitalization_information, "Source : ", "")
        self.Source.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.DoctorName = PatientInfo(self.frame_hospitalization_information, "Doctor name : ", "")
        self.DoctorName.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    
    def command_list(self, patients, drug):
        """Insert a command into the "To Process" tab"""
        for i in range(len(patients)):
            patient_info=patients[i]
            drug_info=drug[i]
            command_id = "Commande " + str(self.count)
            command_display = f"{patient_info['last_name']} - {drug_info['date']}"
            
            # Ajout de la commande dans la Listbox
            self.listbox_to_process.insert(tk.END, command_display)
            
            # Association de l'identifiant de commande avec les données de la commande
            self.commands_data[command_id] = patient_info
            self.commands_drug[command_id] = drug_info
            self.count += 1

    
    def update_patient_info(self, patient_data):
        self.LastNamePatient.frame_label.config(text=patient_data["last_name"])
        self.FirstNamePatient.frame_label.config(text=patient_data["first_name"])
        self.IDPatient.frame_label.config(text=patient_data["id"])
        self.Sex.frame_label.config(text=patient_data["sex"])
        self.Adress.frame_label.config(text=patient_data["address"])
        self.PhoneNumber.frame_label.config(text=patient_data["phone_number"])
        self.email.frame_label.config(text=patient_data["birthdate"])
        self.SSN.frame_label.config(text=patient_data["ssn"])
        self.Religion.frame_label.config(text=patient_data["religion"])
        self.Nationality.frame_label.config(text=patient_data["nationality"])
        self.Allergy.frame_label.config(text=patient_data["allergy"])

        self.HospitalizationStatus.frame_label.config(text=patient_data["status"])
        self.Floor.frame_label.config(text=patient_data["floor"])
        self.Room.frame_label.config(text=patient_data["room"])
        self.Bed.frame_label.config(text=patient_data["bed"])
        self.Service.frame_label.config(text=patient_data["service"])
        self.Source.frame_label.config(text=patient_data["source"])
        self.DoctorName.frame_label.config(text=patient_data["doctor_name"])

    def update_drug_info(self, drug_info):
        list = [["ID", "Order date", "Min amount", "Max amount", "Units", "Admin instruction", 
                 "Dispense amount", "Dispenses unit", "Frequency", "Expiration date", "check"],
                [drug_info["medicine"], drug_info["date"], drug_info["minimum_amount"], drug_info["maximum_amount"], 
                 drug_info["units"], drug_info["instruction"], drug_info["dispense_amount"], drug_info["dispense_units"], drug_info["frequency"], ""]]
        Rownumber = len(list)
        self.MedicineTabel = Table(self.inner_frame, list,self.send_command, Rownumber)
        

    def on_command_click(self, event):
         
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]+1
            self.patient_info=self.commands_data["Commande "+str(index)]
            self.drug_info=self.commands_drug["Commande "+str(index)]
            self.update_patient_info(self.patient_info)
            self.update_drug_info(self.drug_info)
          
    def send_command(self):

        message = "Command validated successfully."
        messagebox.showinfo("Validation", message)
        

        # Ajouter une entrée dans l'onglet historique
        command_name = self.patient_info["last_name"] 
        command_date = self.drug_info["date"]  
        history_entry = tk.Label(self.history_frame, text=(command_name,command_date))
        history_entry.pack()
        self.clear_command()
        self.clear_table()
        self.medicine.check_stock_and_order(self.drug_info["medicine"])
        self.configure_stock_tab()
    
    def clear_command(self): 
        # Obtenir la commande sélectionnée
        selection = self.listbox_to_process.curselection()
        if selection:
            index = selection[0]
            command = self.listbox_to_process.get(index)
            # Supprimer l'entrée de la listbox
            self.listbox_to_process.delete(index)
            # Supprimer les données associées
            if command in self.commands_data:
                del self.commands_data[command]
            if command in self.commands_drug:
                del self.commands_drug[command]
            # Effacer les informations affichées
            self.update_patient_info({
                "last_name": "",
                "first_name": "",
                "id": "",
                "sex": "",
                "address": "",
                "phone_number": "",
                "birthdate": "",
                "ssn": "",
                "religion": "",
                "nationality": "",
                "status": "",
                "floor": "",
                "room": "",
                "bed": "",
                "service": "",
                "source": "",
                "doctor_name": "",
                "allergy": ""
            })
            self.update_drug_info({
                "medicine": "",
                "date": "",
                "minimum_amount": "",
                "maximum_amount":"",
                "units":"",
                "instruction":"",
                "dispense_amount":"",
                "dispense_units":"",
                "frequency":""
            })
    
    def clear_table(self):
        if hasattr(self, 'MedicineTabel'):
            for widget in self.MedicineTabel.root.winfo_children():
                widget.destroy()
            del self.MedicineTabel
        
    def configure_stock_tab(self):

        if hasattr(self, 'stock_frame'):
            for widget in self.stock_frame.winfo_children():
                widget.destroy()
        else:
            self.stock_frame = tk.Frame(self.tab_stock)
            self.stock_frame.pack(side="left", fill="both", expand=True)

        if hasattr(self, 'order_frame'):
            for widget in self.order_frame.winfo_children():
                widget.destroy()
        else:
            self.order_frame = tk.Frame(self.tab_stock)
            self.order_frame.pack(side="right", fill="both", expand=True)

        self.stock_frame = tk.Frame(self.tab_stock)
        self.stock_frame.pack(side="left", fill="both", expand=True)

        self.order_frame = tk.Frame(self.tab_stock)
        self.order_frame.pack(side="right", fill="both", expand=True)

        # Create stock
        self.stock_label = tk.Label(self.stock_frame, text="Stock Information", font=("Helvetica", 16))
        self.stock_label.pack(pady=10)

        # Display stock information in a listbox
        self.stock_listbox = tk.Listbox(self.stock_frame, width=30, height=15)
        self.stock_listbox.pack(pady=10)

        # Populate the stock listbox with data from the database
        self.populate_stock_listbox()

        #create order
        self.order_label = tk.Label(self.order_frame, text="Order Information", font=("Helvetica", 16))
        self.order_label.pack(pady=10)

        # Display order information in a listbox
        self.order_listbox = tk.Listbox(self.order_frame, width=40, height=15)
        self.order_listbox.pack(pady=10)

        self.populate_order_listbox()

        self.check_order_button = tk.Button(self.stock_frame, text="Check and Order", command=self.check_and_order)
        self.check_order_button.pack(pady=10)

    def populate_order_listbox(self):
        try:
            selection_query = "SELECT ref_order, name_medicament, order_quantity, status_order FROM stock_order"
            self.medicine.cursor.execute(selection_query)
            order_data = self.medicine.cursor.fetchall()
            for order in order_data:
                order_info = f"Order ID: {order[0]} - {order[1]} - Quantity: {order[2]} - Status: {order[3]}"
                self.order_listbox.insert(tk.END, order_info)
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
    
    def populate_stock_listbox(self):
        try:
            selection_query = "SELECT name_medicament, available_stock FROM stock_medicament"
            self.medicine.cursor.execute(selection_query)
            stock_data = self.medicine.cursor.fetchall()
            for item in stock_data:
                self.stock_listbox.insert(tk.END, f"{item[0]} - Available: {item[1]}")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
    
    def check_and_order(self):
        # Get the selected medication name from the stock listbox
        selected_index = self.stock_listbox.curselection()
        if selected_index:
            selected_medication = self.stock_listbox.get(selected_index[0])

            # Extract the medication name from the selected item
            medication_name = selected_medication.split(" - ")[0]

            # Check stock and place order using Medicine class method
            self.medicine.check_stock_and_order(medication_name)

        else:
            messagebox.showinfo("Selection", "Please select a medication from the list.")


if __name__ == "__main__":
    conn = sqlite3.connect('db_MIS.db')
    cur = conn.cursor()
    cur.execute("SELECT message FROM rde")
    prescriptions=cur.fetchall()
    conn.close()
    all_prescriptions = []
    i=1
    for item in prescriptions:
        patient_info, drug_info = get_command_info(i)
        all_prescriptions.append((patient_info, drug_info))
        i=i+1
    root = tk.Tk()
    app = PharmacyApp(root, all_prescriptions)
    root.mainloop()
