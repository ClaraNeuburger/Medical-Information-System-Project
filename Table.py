import tkinter as tk
import tkinter.messagebox as messagebox

class Table:
    
    def __init__(self, root, lst,send_command_callback, Rownumber, ColumnNumber=11):
        self.check_vars = []
        self.checkbuttons = []
        self.labels = []
        self.entries = []
        self.cells = []
        self.root = root
        self.Rownumber = Rownumber
        self.send_command_callback = send_command_callback

       
        for i in range(Rownumber):
            row_vars = []
            row_checkbuttons = []
            row_labels = []
            row_entries = []
            row_cells = []

            for j in range(ColumnNumber):
                if i == 0:
                    e = tk.Label(root, text=lst[i][j] if j < len(lst[i]) else "", width=18, borderwidth=1, relief="solid")
                    e.grid(row=i, column=j)
                elif j == ColumnNumber - 1:
                    var = tk.BooleanVar()
                    e = tk.Checkbutton(root, variable=var)
                    row_vars.append(var)
                    row_checkbuttons.append(e)
                    row_cells.append((e, var))  # Store the Checkbutton and its variable as a tuple
                    e.grid(row=i, column=j)
                elif j == ColumnNumber - 2:
                    e = tk.Entry(root, width=5)
                    row_entries.append(e)
                    row_cells.append(e)
                    e.grid(row=i, column=j)
                else:
                    e = tk.Label(root, text=lst[i][j] if i < len(lst) and j < len(lst[i]) else "", width=18, borderwidth=0.5)
                    row_labels.append(e)
                    row_cells.append(e)
                    e.grid(row=i, column=j)

            if i != 0:
                self.check_vars.append(row_vars)
                self.checkbuttons.append(row_checkbuttons)
                self.labels.append(row_labels)
                self.entries.append(row_entries)
                self.cells.append(row_cells)
        self.save_button = tk.Button(root, text="Save", command=self.save)
        self.save_button.grid(row=Rownumber+1, column=10)
        
    def get_root(self):
        return self.root

    def get_row_number(self):
        return self.Rownumber  

    root=get_root
    Rownumber=get_row_number  
    
    def check_all_checked(self):
        for row in self.check_vars:
            if not all(var.get() for var in row):
                return False
        return True

    def update_send_button_visibility(self):
        print("ok")
        
        self.send_button = tk.Button(self.root, text="Send", command=self.send_command)
        self.send_button.grid(row=self.Rownumber+1, column=len(self.cells[0]) - 2)
        
        

        

    def update_row(self, row_idx, data):
        if 1 <= row_idx < len(self.cells) + 1:  # ensure row_idx is within the valid range
            for col_idx, value in enumerate(data):
                cell = self.cells[row_idx - 1][col_idx]
                if isinstance(cell, tk.Label):
                    cell.config(text=value)
                elif isinstance(cell, tk.Entry):
                    cell.delete(0, tk.END)
                    cell.insert(0, value)
                elif isinstance(cell, tuple) and isinstance(cell[0], tk.Checkbutton):
                    _, var = cell
                    var.set(value)

    def save(self):
        
        all_checked = all(all(var.get() for var in row) for row in self.check_vars)
        print(all_checked)
            
        if all_checked:
                    
            self.update_send_button_visibility()
    
    def send_command(self):
        if self.send_command_callback:
            self.send_command_callback()
    
    
        


            




# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Table Example")

    # Sample data for the table header
    lst = [["Medicament ID", "Order date", "Min amount", "Max amount", "Units", "Admin instruction", 
            "Dispense amount", "Dispenses unit", "Frequency", "Expiration date", "check"]]
    
    # Number of rows
    Rownumber = 4
    
    # Create a Table instance
    table = Table(root, lst, Rownumber)

    # Sample data to insert into the first row (row index 1)
    data = ["ID001", "2024-05-24", "10", "50", "units", "instructions", "5", "units", "daily", "2025-05-24", True]
    table.update_row(1, data)

    

    root.mainloop()


