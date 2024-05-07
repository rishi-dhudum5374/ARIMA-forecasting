from tkinter import Tk, Label, Entry, Button, ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import pandas as pd

class PharmacyInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x900")
        self.initialize_entries()
        self.initialize_labels()
        self.initialize_buttons()
        self.initialize_treeview()
        self.bind_events()
        self.show()

    def initialize_entries(self):
        self.entries = {}
        entry_positions = [(140, 40), (140, 70), (140, 100), (140, 130),
                           (140, 160), (140, 190), (140, 220), (140, 250), (140, 280),
                           (140, 310), (140, 340)]
        entry_names = ['name_of_drug', 'brand_name', 'name_of_company', 'dose',
                       'dosage_form', 'mfg_date', 'exp_date', 'batch_number', 'Price',
                       'Stock_in', 'Stock_out']
        for i, name in enumerate(entry_names):
            entry = Entry(self.root)
            entry.place(x=entry_positions[i][0], y=entry_positions[i][1])
            self.entries[name] = entry

        # Initialize the ID field
        self.entries['ID'] = Entry(self.root)
        self.entries['ID'].place(x=140, y=10)
        initial_id = self.get_next_id()
        if initial_id is not None:
            self.entries['ID'].insert(0, initial_id)

        # Initialize date entry fields
        self.mfg_date_entry = DateEntry(self.root, date_pattern='dd/MM/yyyy')
        self.mfg_date_entry.place(x=140, y=190)

        self.exp_date_entry = DateEntry(self.root, date_pattern='dd/MM/yyyy')
        self.exp_date_entry.place(x=140, y=220)

    def initialize_labels(self):
        label_positions = [(10, 40), (10, 70), (10, 100), (10, 130),
                           (10, 160), (10, 190), (10, 220), (10, 250), (10, 280),
                           (10, 310), (10, 340)]
        label_names = ['name_of_drug', 'brand_name', 'name_of_company', 'dose',
                       'dosage_form', 'mfg_date', 'exp_date', 'batch_number', 'Price',
                       'Stock_in', 'Stock_out']
        for i, name in enumerate(label_names):
            Label(self.root, text=name).place(x=label_positions[i][0], y=label_positions[i][1])

    def initialize_buttons(self):
        btn_add = Button(self.root, text="Add", command=self.Add, height=2, font=("None", 10, "bold"), width=10,
                        fg='white', bg='blue')
        btn_add.place(x=500, y=300)
        btn_update = Button(self.root, text="Update", command=self.update, height=2, font=("None", 10, "bold"), width=10,
                        fg='white', bg='blue')
        btn_update.place(x=600, y=300)
        btn_delete = Button(self.root, text="Delete", command=self.delete, height=2, font=("None", 10, "bold"), width=10,
                        fg='white', bg='blue')
        btn_delete.place(x=700, y=300)
        btn_export = Button(self.root, text="Export", command=self.export_to_excel, height=2, font=("None", 10, "bold"), width=10,
                        fg='white', bg='blue')
        btn_export.place(x=800, y=300)

    def initialize_treeview(self):
        self.cols = ('ID', 'name_of_drug', 'brand_name', 'name_of_company', 'dose', 'dosage_form', 'mfg_date',
                     'exp_date', 'batch_number', 'Price', 'Stock_count', 'Stock_in', 'Stock_out')
        self.listBox = ttk.Treeview(self.root, columns=self.cols, show='headings')

        for col in self.cols:
            self.listBox.heading(col, text=col)
            self.listBox.grid(row=1, column=0, columnspan=1)
            self.listBox.column(col, anchor='w', width=100)

        self.listBox.place(x=5, y=450)
        self.listBox.bind("<Double-1>", self.on_double_click)

    def bind_events(self):
        for name, entry in self.entries.items():
            entry.bind('<Return>', lambda event, name=name: self.focus_next_entry(event, name))
            entry.bind('<Up>', lambda event, name=name: self.move_cursor(event, name, -1))
            entry.bind('<Down>', lambda event, name=name: self.move_cursor(event, name, 1))

    def get_next_id(self):
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy_inventory")
        mycursor = mysqldb.cursor()

        try:
            # Retrieve the last used ID from the database
            mycursor.execute("SELECT MAX(id) FROM inventory")
            last_id = mycursor.fetchone()[0]

            # Set the initial ID if no records are present
            if last_id is None:
                next_id = 1500
            else:
                # Generate the next available ID
                next_id = last_id + 1

            return next_id

        except Exception as e:
            print(e)
            return None
        finally:
            mysqldb.close()

    def Add(self):
        try:
            next_id = self.get_next_id()

            # Automatically populate the ID entry
            self.entries['ID'].delete(0, 'end')
            self.entries['ID'].insert(0, next_id)

            # Rest of the entry data
            entry_data = [self.entries[name].get() for name in ['name_of_drug', 'brand_name', 'name_of_company',
                                                                'dose', 'dosage_form', 'batch_number', 'Price',
                                                                'Stock_in', 'Stock_out']]

            # Insert the new record into the database
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy_inventory")
            mycursor = mysqldb.cursor()
            sql = ("INSERT INTO inventory (id, name_of_drug, brand_name, name_of_company, dose, dosage_form, mfg_date, "
                   "exp_date, batch_number, price, stock_count, stock_in, stock_out) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            stock_count = int(self.entries['Stock_in'].get()) - int(self.entries['Stock_out'].get())
            val = tuple([next_id] + entry_data[:5] + [self.mfg_date_entry.get_date(), self.exp_date_entry.get_date()] +
                        entry_data[5:] + [stock_count])
            mycursor.execute(sql, val)
            mysqldb.commit()
            messagebox.showinfo("Information", "Data inserted successfully...")

            # Clear other entry fields
            for entry in self.entries.values():
                entry.delete(0, 'end')

            # Set focus to the next entry
            self.entries['name_of_drug'].focus_set()

            # Clear the Treeview
            self.listBox.delete(*self.listBox.get_children())

            # Show updated data
            self.show()

        except Exception as e:
            print(e)
        finally:
            mysqldb.close()

    def update(self):
        # Get the ID of the record to update
        id = self.entries['ID'].get()

        # Get the current data from the entry fields
        entry_data = [self.entries[name].get() for name in ['name_of_drug', 'brand_name', 'name_of_company',
                                                            'dose', 'dosage_form', 'batch_number', 'Price',
                                                            'Stock_in', 'Stock_out']]

        # Update the record in the database
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy_inventory")
        mycursor = mysqldb.cursor()

        try:
            sql = ("UPDATE inventory SET name_of_drug = %s, brand_name = %s, name_of_company = %s, dose = %s, "
                   "dosage_form = %s, mfg_date = %s, exp_date = %s, batch_number = %s, price = %s, stock_count = %s, "
                   "stock_in = %s, stock_out = %s WHERE id = %s")
            stock_count = int(self.entries['Stock_in'].get()) - int(self.entries['Stock_out'].get())
            val = entry_data[:7] + [self.mfg_date_entry.get_date(), self.exp_date_entry.get_date()] + entry_data[7:] + [stock_count, id]
            mycursor.execute(sql, val)
            mysqldb.commit()
            messagebox.showinfo("Information", "Record Updated successfully...")

            # Clear entry fields
            for entry in self.entries.values():
                entry.delete(0, 'end')

            self.entries['ID'].focus_set()

            # Clear the Treeview
            self.listBox.delete(*self.listBox.get_children())

            # Show updated data
            self.show()

        except Exception as e:
            print(e)
            mysqldb.rollback()
        finally:
            mysqldb.close()

    def delete(self):
        id = self.entries['ID'].get()
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy_inventory")
        mycursor = mysqldb.cursor()

        try:
            sql = "DELETE FROM inventory WHERE id = %s"
            mycursor.execute(sql, (id,))
            mysqldb.commit()
            messagebox.showinfo("Information", "Record Deleted successfully...")

            # Clear entry fields
            for entry in self.entries.values():
                entry.delete(0, 'end')

            self.entries['ID'].focus_set()

            # Clear the Treeview
            self.listBox.delete(*self.listBox.get_children())

            # Show updated data
            self.show()

        except Exception as e:
            print(e)
            mysqldb.rollback()
        finally:
            mysqldb.close()

    def show(self):
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy_inventory")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT id, name_of_drug, brand_name, name_of_company, dose, dosage_form, "
                         "mfg_date, exp_date, batch_number, price, stock_count, stock_in, stock_out FROM inventory")
        records = mycursor.fetchall()

        for record in records:
            self.listBox.insert("", "end", values=record)

        mysqldb.close()

    def on_double_click(self, event):
        item = self.listBox.selection()[0]
        data = self.listBox.item(item, "values")
        self.entries['ID'].delete(0, 'end')
        self.entries['ID'].insert(0, data[0])
        for i, name in enumerate(['name_of_drug', 'brand_name', 'name_of_company', 'dose',
                                  'dosage_form', 'mfg_date', 'exp_date', 'batch_number',
                                  'Price', 'Stock_in', 'Stock_out']):
            self.entries[name].delete(0, 'end')
            self.entries[name].insert(0, data[i + 1])

            # Set initial value for manufacturing date and expiry date
            if name == 'mfg_date':
                self.mfg_date_entry.set_date(data[i + 1])
            elif name == 'exp_date':
                self.exp_date_entry.set_date(data[i + 1])

    def focus_next_entry(self, event, name):
        next_entry = None
        entry_names = list(self.entries.keys())
        current_index = entry_names.index(name)
        if current_index < len(entry_names) - 1:
            next_entry_name = entry_names[current_index + 1]
            next_entry = self.entries[next_entry_name]
        elif current_index == len(entry_names) - 1:
            next_entry = self.entries['ID']
        if next_entry:
            next_entry.focus_set()

    def move_cursor(self, event, name, direction):
        entry_names = list(self.entries.keys())
        current_index = entry_names.index(name)
        new_index = current_index + direction
        if 0 <= new_index < len(entry_names):
            new_entry_name = entry_names[new_index]
            self.entries[new_entry_name].focus_set()

    def export_to_excel(self):
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy_inventory")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT id, name_of_drug, brand_name, name_of_company, dose, dosage_form, "
                         "mfg_date, exp_date, batch_number, price, stock_count, stock_in, stock_out FROM inventory")
        records = mycursor.fetchall()

        df = pd.DataFrame(records, columns=['ID', 'Name of Drug', 'Brand Name', 'Company Name', 'Dose',
                                            'Dosage Form', 'MFG Date', 'EXP Date', 'Batch Number', 'Price',
                                            'Stock Count', 'Stock In', 'Stock Out'])
        df.to_excel("pharmacy_inventory.xlsx", index=False)

        messagebox.showinfo("Information", "Data exported to 'pharmacy_inventory.xlsx'")

        mysqldb.close()

if __name__ == "__main__":
    root = Tk()
    app = PharmacyInventoryApp(root)
    root.mainloop()
