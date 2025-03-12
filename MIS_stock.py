import time
import sqlite3
from tkinter import messagebox

class Medicine: 
    def __init__(self, db_name="db_MIS.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def check_stock_and_order(self, medicament_name):
        try:
            # Get medicament info from the database
            selection_query = "SELECT * FROM stock_medicament WHERE name_medicament = ?"
            self.cursor.execute(selection_query, (medicament_name,))
            medicament_info = self.cursor.fetchone()

            if medicament_info:
                available_stock = medicament_info[3]
                dormant_stock = medicament_info[2]

                if available_stock < dormant_stock:
                    # Place an order
                    self.place_order(medicament_name, medicament_info[5])
                    messagebox.showinfo(f"Low stock alert: {medicament_name} is below the threshold level of {dormant_stock} units. An order has been placed.")
                else:
                    self.update_stock_after_prescription(medicament_name)
            else:
                messagebox.showinfo("Stock Information", f"Medicament {medicament_name} not found in the database.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def place_order(self, medicament_name, order_quantity):
        try:
            # Generate a unique reference for the order
            ref_order = f"{medicament_name}_{int(time.time())}"
            
            # Insert the order into the database
            insert_query = "INSERT INTO stock_order (ref_order, name_medicament, order_quantity, status_order) VALUES (?, ?, ?, ?)"
            self.cursor.execute(insert_query, (ref_order, medicament_name, order_quantity, "in progress"))
            self.conn.commit()

            messagebox.showinfo("Order Placed", f"Order placed for {order_quantity} boxes of {medicament_name}. Reference order: {ref_order}")

        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def update_stock_after_delivery(self, medicament_name):
        try:
            # Get the reference of the last order placed for the medicament
            order_query = "SELECT ref_order FROM stock_order WHERE name_medicament = ? ORDER BY id_stock_order DESC LIMIT 1"
            self.cursor.execute(order_query, (medicament_name,))
            last_order_ref = self.cursor.fetchone()

            if last_order_ref:
                # Check if the status of the last order is "delivered"
                status_query = "SELECT status_order FROM stock_order WHERE ref_order = ?"
                self.cursor.execute(status_query, (last_order_ref[0],))
                status = self.cursor.fetchone()[0]

                if status == "delivered":
                    # Get the order quantity of the last order
                    quantity_query = "SELECT order_quantity FROM stock_order WHERE ref_order = ?"
                    self.cursor.execute(quantity_query, (last_order_ref[0],))
                    order_quantity = self.cursor.fetchone()[0]

                    # Update the available stock in the stock_medicament table
                    update_query = "UPDATE stock_medicament SET available_stock = available_stock + ? WHERE name_medicament = ?"
                    self.cursor.execute(update_query, (order_quantity, medicament_name))
                    self.conn.commit()

                    messagebox.showinfo("Stock Updated", f"Available stock for {medicament_name} updated after delivery of order: {last_order_ref[0]}")

                else:
                    messagebox.showinfo("Stock Information", f"Last order for {medicament_name} is not delivered yet.")

            else:
                messagebox.showinfo("Stock Information", f"No orders found for {medicament_name}.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))


    def update_stock_after_prescription(self, medicament_name):
        try:
            # Get the reference of the last order placed for the medicament
            order_query = "SELECT ref_order FROM stock_order WHERE name_medicament = ? ORDER BY id_stock_order DESC LIMIT 1"
            self.cursor.execute(order_query, (medicament_name,))
            last_order_ref = self.cursor.fetchone()

            if last_order_ref:
                # Check if the status of the last order is "delivered"
                status_query = "SELECT status_order FROM stock_order WHERE ref_order = ?"
                self.cursor.execute(status_query, (last_order_ref[0],))
                status = self.cursor.fetchone()[0]

                if status == "delivered":
                    order_quantity = 1

                    # Update the available stock in the stock_medicament table
                    update_query = "UPDATE stock_medicament SET available_stock = available_stock - ? WHERE name_medicament = ?"
                    self.cursor.execute(update_query, (order_quantity, medicament_name))
                    self.conn.commit()

                    messagebox.showinfo("Stock Updated", f"Available stock for {medicament_name} updated after delivery of order: {last_order_ref[0]}")

                

            else:
                messagebox.showinfo("Stock Information", f"No orders found for {medicament_name}.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

