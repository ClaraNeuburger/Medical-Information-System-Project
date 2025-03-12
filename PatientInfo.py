import tkinter as tk
from tkinter import ttk

class PatientInfo(ttk.Frame):
    def __init__(self, parent, label, texte, frame_width=1000):
        super().__init__(parent)
        # Label pour afficher le nom du patient
        self.label_text = tk.Label(self, text=label)
        self.label_text.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Créer un cadre blanc avec une largeur fixe
        self.frame_frame = tk.Frame(self, bg="white", width=frame_width)
        self.frame_frame.grid(row=0, column=1, padx=10, pady=10)

        self.frame_label = ttk.Label(self.frame_frame, text=texte)
        self.frame_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
       