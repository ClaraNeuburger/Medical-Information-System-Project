import tkinter as tk
import sqlite3
from tkinter import messagebox
from Doc_interface import open_interface_window_doctor

def fetch_physicians():
    conn = sqlite3.connect('db_MIS.db')  
    cursor = conn.cursor()

    cursor.execute("SELECT id_doctor, id_person, first_name, last_name, login FROM doctor INNER JOIN person ON doctor.id_person = person.id")
    physicians = cursor.fetchall()

    conn.close()
    return physicians

def on_physician_select(event):
    selected_index = physician_listbox.curselection()
    if selected_index:
        selected_physician = physicians[selected_index[0]]
        login = selected_physician[4]  
        confirm_button.config(state=tk.NORMAL)  

def confirm_physician():
    selected_index = physician_listbox.curselection()
    if selected_index:
        selected_physician = physicians[selected_index[0]]
        login = selected_physician[4]  
        
        open_interface_window_doctor(login)

physicians = fetch_physicians()


root = tk.Tk()
root.title("Choose yout physician profile")

physician_listbox = tk.Listbox(root, width=40)
physician_listbox.pack(padx=10, pady=10)

for physician in physicians:
    physician_listbox.insert(tk.END, f"{physician[2]} {physician[3]}")  # First name at index 2, last name at index 3

physician_listbox.bind("<<ListboxSelect>>", on_physician_select)


confirm_button = tk.Button(root, text="Confirm", command=confirm_physician, state=tk.DISABLED)
confirm_button.pack(pady=10)


root.mainloop()
