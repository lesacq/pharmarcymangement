import os
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- Database Connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pms"
)
cursor = db.cursor()

# --- Main Application Class ---
class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("900x650")

        self.db = db
        self.cursor = cursor
        self.total_sales = 0.0

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=('Arial', 10))
        style.configure("TButton", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

        self.tab_control = ttk.Notebook(root)
        self.tab_inventory = ttk.Frame(self.tab_control)
        self.tab_sales = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_inventory, text="Inventory")
        self.tab_control.add(self.tab_sales, text="Sales")
        self.tab_control.pack(expand=1, fill='both')

        self.create_inventory_tab()
        self.create_sales_tab()
        self.load_inventory()

    # --- Inventory Tab UI ---
    def create_inventory_tab(self):
        frame = self.tab_inventory

        ttk.Label(frame, text=" L.A PHARMACEUTICALS ", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Medicine Name").grid(row=1, column=0, padx=5, pady=5, sticky='W')
        ttk.Label(frame, text="Quantity").grid(row=2, column=0, padx=5, pady=5, sticky='W')
        ttk.Label(frame, text="Expiration Date (YYYY-MM-DD)").grid(row=3, column=0, padx=5, pady=5, sticky='W')
        ttk.Label(frame, text="Price (GHS)").grid(row=4, column=0, padx=5, pady=5, sticky='W')

        self.entry_name = ttk.Entry(frame)
        self.entry_quantity = ttk.Entry(frame)
        self.entry_exp_date = ttk.Entry(frame)
        self.entry_price = ttk.Entry(frame)

        self.entry_name.grid(row=1, column=1, padx=5, pady=5)
        self.entry_quantity.grid(row=2, column=1, padx=5, pady=5)
        self.entry_exp_date.grid(row=3, column=1, padx=5, pady=5)
        self.entry_price.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Medicine", command=self.add_medicine).grid(row=5, column=1, pady=10)

        self.tree_inventory = ttk.Treeview(frame, columns=('ID', 'Name', 'Qty', 'Expiry', 'Price(GHS)'), show='headings')
        self.tree_inventory.column("ID", width=30, anchor='center')
        self.tree_inventory.column("Name", width=150)
        self.tree_inventory.column("Qty", width=50, anchor='center')
        self.tree_inventory.column("Expiry", width=100)
        self.tree_inventory.column("Price(GHS)", width=70)

        for col in self.tree_inventory['columns']:
            self.tree_inventory.heading(col, text=col)

        self.tree_inventory.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    # --- Add Medicine to DB ---
    def add_medicine(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        exp_date = self.entry_exp_date.get()
        price = self.entry_price.get()

        if not name or not quantity or not exp_date or not price:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            datetime.strptime(exp_date, "%Y-%m-%d")

            sql = "INSERT INTO inventory (name, quantity, expiration_date, price) VALUES (%s, %s, %s, %s)"
            val = (name, quantity, exp_date, price)
            self.cursor.execute(sql, val)
            self.db.commit()
            self.load_inventory()

            self.entry_name.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)
            self.entry_exp_date.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)

            messagebox.showinfo("Success", "Medicine added successfully.")
        except ValueError:
            messagebox.showerror("Input Error", "Check that quantity is an integer, price is a number, and date is in YYYY-MM-DD format.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- Load Inventory ---
    def load_inventory(self):
        for row in self.tree_inventory.get_children():
            self.tree_inventory.delete(row)
        self.cursor.execute("SELECT * FROM inventory")
        for row in self.cursor.fetchall():
            self.tree_inventory.insert('', tk.END, values=row)

    # --- Sales Tab UI ---
    def create_sales_tab(self):
        frame = self.tab_sales

        ttk.Label(frame, text="New Sale", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Medicine Name").grid(row=1, column=0, padx=5, pady=5, sticky='W')
        ttk.Label(frame, text="Quantity").grid(row=2, column=0, padx=5, pady=5, sticky='W')

        self.sale_name = ttk.Entry(frame)
        self.sale_quantity = ttk.Entry(frame)

        self.sale_name.grid(row=1, column=1, padx=5, pady=5)
        self.sale_quantity.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Process Sale", command=self.process_sale).grid(row=3, column=1, pady=10)

        ttk.Label(frame, text="Sales Receipt", font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=2)

        self.sales_output = tk.Text(frame, height=15, width=70, state='normal')
        self.sales_output.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.total_label = ttk.Label(frame, text="Total Sales: GHS 0.00", font=('Arial', 10, 'bold'))
        self.total_label.grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Button(frame, text="Clear Receipt", command=self.clear_receipt).grid(row=7, column=0, pady=5)
        ttk.Button(frame, text="Save Receipt", command=self.save_receipt).grid(row=7, column=1, pady=5)

    # --- Process Sale ---
    def process_sale(self):
        name = self.sale_name.get()
        quantity = self.sale_quantity.get()

        if not name or not quantity:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be an integer.")
            return

        cursor.execute("SELECT quantity, price FROM inventory WHERE name=%s", (name,))
        item = cursor.fetchone()

        if item:
            stock_qty, price = item
            if quantity > stock_qty:
                messagebox.showwarning("Stock Error", "Not enough stock.")
            else:
                total = quantity * price
                self.cursor.execute("UPDATE inventory SET quantity = quantity - %s WHERE name = %s", (quantity, name))
                self.cursor.execute("INSERT INTO sales (medicine_name, quantity, total_price, sale_time) VALUES (%s, %s, %s, %s)",
                               (name, quantity, total, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.db.commit()
                self.load_inventory()

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.sales_output.insert(tk.END, f"{timestamp} - Sold {quantity} x {name} @ GHS{price:.2f} = GHS{total:.2f}\n")
                self.total_sales += total
                self.total_label.config(text=f"Total Sales: GHS {self.total_sales:.2f}")

                self.sale_name.delete(0, tk.END)
                self.sale_quantity.delete(0, tk.END)
        else:
            messagebox.showerror("Not Found", "Medicine not found in inventory.")

    # --- Clear Receipt ---
    def clear_receipt(self):
        self.sales_output.delete(1.0, tk.END)
        self.total_sales = 0.0
        self.total_label.config(text="Total Sales: GHS 0.00")
        
    import os  # Make sure this is at the top of your file

    def save_receipt(self):
        receipt_text = self.sales_output.get("1.0", tk.END).strip()
        if not receipt_text:
            messagebox.showwarning("Save Error", "No receipt content to save.")
            return

        # Create 'receipts' folder in current directory if it doesn't exist
        receipts_folder = os.path.join(os.getcwd(), "receipts")
        os.makedirs(receipts_folder, exist_ok=True)

        # Generate file path with timestamp
        filename = f"receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        file_path = os.path.join(receipts_folder, filename)

        try:
            with open(file_path, "w") as file:
                file.write(receipt_text)
            messagebox.showinfo("Success", f"Receipt saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save receipt:\n{str(e)}")


   
        

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()
