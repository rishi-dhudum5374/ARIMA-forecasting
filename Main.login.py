# from tkinter import *
# from tkinter import ttk
#
# def main():
#     app = Tk()
#     ob = Loginpage(app)
#     app.mainloop()
#
# class Loginpage:
#     def __init__(self, win):
#         self.win = win
#         self.win.geometry("1350x750")
#         self.win.title("Pharma Management System | Login")
#
#         self.title_lbl = Label(self.win,text="Pharma Management System", bg="purple",fg="yellow",
#                                bd=8,relief=SUNKEN,font=("Arial",26,"bold"))
#         self.title_lbl.pack(side= "top",fill= X)
#
#         self.login_lbl = Label(self.win, text="Login", bg="red", fg="indigo", bd=8, relief=SUNKEN,
#                                font=("Arial", 26, "bold"))
#         self.login_lbl.pack(side="top", fill=X)
#
#         self.main_frame = Frame(self.win,bg="#FFEFDB",bd=10,relief="ridge")
#         self.main_frame.place(x=315 ,y=160,width=720,height=480)
#
#         self.login_as_frame = LabelFrame(self.main_frame,text="Login As", bg="#00FFFF", bd=8, relief="ridge",font=("Arial",20),pady=20)
#         self.login_as_frame.pack(side="top", fill=BOTH)
#
#         self.entry_frame = LabelFrame(self.main_frame,text="Enter Credential", bg="#00FFFF", bd=8, relief="ridge",font=("Arial",20))
#         self.entry_frame.pack(side="top", fill=BOTH)
#
#         #===============Text variables============#
#
#         username = StringVar()
#         password = StringVar()
#
#         #=========================================#
#
#         self.login_as_emp = Button(self.login_as_frame,text="Employee",bd=8,width=15,font=("Arial",15))
#         self.login_as_emp.grid(row=0,column=1,padx=12)
#
#         self.dum1_lbl = Label(self.login_as_frame, text="", bg="lightgrey")
#         self.dum1_lbl.grid(row=0, column=0, padx=12)
#
#         self.login_as_adm = Button(self.login_as_frame, text="Admin", bd=8, width=15, font=("Arial", 15))
#         self.login_as_adm.grid(row=0, column=2, padx=12)
#
#         self.username_lbl = Label(self.entry_frame, text="Username : ", font=('Arial',15),bg="lightgrey")
#         self.username_lbl.grid(row=1,column=0,padx=2,pady=2)
#
#         self.username_ent = Entry(self.entry_frame,border=9,textvariable=username,font=("Arial",14))
#         self.username_ent.grid(row=1,column=1,padx=2,pady=2)
#
#         self.password_lbl = Label(self.entry_frame, text="Password : ", font=('Arial', 15), bg="lightgrey")
#         self.password_lbl.grid(row=2, column=0, padx=2, pady=2)
#
#         self.password_ent = Entry(self.entry_frame, border=9, textvariable=password, font=("Arial", 14))
#         self.password_ent.grid(row=2, column=1, padx=2, pady=2)
#
#         self.false_frame1 = Frame(self.entry_frame,bd=0,bg='lightgrey')
#
#         self.button_frame = LabelFrame(self.main_frame,text="Option", bg="lightgrey",bd=8,relief=RIDGE,font=("Arial",18))
#         self.button_frame.pack(side=TOP,fill=BOTH)
#
#         self.dum1_lbl = Label(self.button_frame,text="",bg="lightgrey")
#         self.dum1_lbl.grid(row=0,column=1,padx=12)
#
#         #================Function================#
#
#         def submit_func():
#             if username.get() == "" or password.get() == "":
#                 print("Error")
#
#
#         def reset_func():
#             username.set("")
#             password.set("")
#
#         def exit_func():
#             # Add message box here
#             self.win.destroy()
#
#         #=============== Buttons ================#
#
#         self.submit_btn = Button(self.button_frame,text="Submit",bd=8,command=submit_func,font=("Arial",15),width=15)
#         self.submit_btn.grid(row=1,column=2,padx=8,pady=6)
#
#         self.reset_btn = Button(self.button_frame,text="Reset",bd=8,command=reset_func,font=("Arial",15),width=15)
#         self.reset_btn.grid(row=1,column=3,padx=8,pady=6)
#
#         self.exit_btn = Button(self.button_frame, text="Exit", bd=8, command=exit_func, font=("Arial", 15), width=15)
#         self.exit_btn.grid(row=1, column=4, padx=8, pady=6)
#
#
#
#
#         #=======================================#
#
# if __name__=="__main__":
#     main()
#


from tkinter import *
from tkinter import messagebox
import os

class Loginpage:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1350x750")
        self.win.title("Pharma Management System | Login")
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title_lbl = Label(self.win, text="Pharma Management System", bg="purple", fg="yellow",
                               bd=8, relief=SUNKEN, font=("Arial", 26, "bold"))
        self.title_lbl.pack(side="top", fill=X)

        self.login_lbl = Label(self.win, text="Login", bg="red", fg="indigo", bd=8, relief=SUNKEN,
                               font=("Arial", 26, "bold"))
        self.login_lbl.pack(side="top", fill=X)

        self.main_frame = Frame(self.win, bg="#FFEFDB", bd=10, relief="ridge")
        self.main_frame.place(x=315, y=160, width=720, height=480)

        self.login_as_frame = LabelFrame(self.main_frame, text="Login As", bg="#00FFFF", bd=8, relief="ridge",
                                         font=("Arial", 20), pady=20)
        self.login_as_frame.pack(side="top", fill=BOTH)

        self.entry_frame = LabelFrame(self.main_frame, text="Enter Credential", bg="#00FFFF", bd=8, relief="ridge",
                                      font=("Arial", 20))
        self.entry_frame.pack(side="top", fill=BOTH)

        # ===============Text variables============#
        self.username = StringVar()
        self.password = StringVar()
        # =========================================#

        self.login_as_emp = Button(self.login_as_frame, text="Employee", bd=8, width=15, font=("Arial", 15),
                                   command=self.employee_login)
        self.login_as_emp.grid(row=0, column=1, padx=12)

        self.dum1_lbl = Label(self.login_as_frame, text="", bg="lightgrey")
        self.dum1_lbl.grid(row=0, column=0, padx=12)

        self.login_as_adm = Button(self.login_as_frame, text="Admin", bd=8, width=15, font=("Arial", 15),
                                   command=self.admin_login)
        self.login_as_adm.grid(row=0, column=2, padx=12)

        self.username_lbl = Label(self.entry_frame, text="Username : ", font=('Arial', 15), bg="lightgrey")
        self.username_lbl.grid(row=1, column=0, padx=2, pady=2)

        self.username_ent = Entry(self.entry_frame, border=9, textvariable=self.username, font=("Arial", 14))
        self.username_ent.grid(row=1, column=1, padx=2, pady=2)

        self.password_lbl = Label(self.entry_frame, text="Password : ", font=('Arial', 15), bg="lightgrey")
        self.password_lbl.grid(row=2, column=0, padx=2, pady=2)

        self.password_ent = Entry(self.entry_frame, border=9, textvariable=self.password, font=("Arial", 14),
                                  show="*")
        self.password_ent.grid(row=2, column=1, padx=2, pady=2)

        self.false_frame1 = Frame(self.entry_frame, bd=0, bg='lightgrey')

        self.button_frame = LabelFrame(self.main_frame, text="Option", bg="lightgrey", bd=8, relief=RIDGE,
                                       font=("Arial", 18))
        self.button_frame.pack(side=TOP, fill=BOTH)

        self.dum1_lbl = Label(self.button_frame, text="", bg="lightgrey")
        self.dum1_lbl.grid(row=0, column=1, padx=12)

        # ================ Buttons ================#
        self.submit_btn = Button(self.button_frame, text="Submit", bd=8, command=self.submit_func,
                                 font=("Arial", 15), width=15)
        self.submit_btn.grid(row=1, column=2, padx=8, pady=6)

        self.reset_btn = Button(self.button_frame, text="Reset", bd=8, command=self.reset_func,
                                font=("Arial", 15), width=15)
        self.reset_btn.grid(row=1, column=3, padx=8, pady=6)

        self.exit_btn = Button(self.button_frame, text="Exit", bd=8, command=self.exit_func,
                               font=("Arial", 15), width=15)
        self.exit_btn.grid(row=1, column=4, padx=8, pady=6)

    def submit_func(self):
        username = self.username.get()
        password = self.password.get()

        if username == "emp0001" and password == "1234":
            self.open_employee_window()
        elif username == "Admin001" and password == "Admin01":
            self.open_admin_window()
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")

    def reset_func(self):
        self.username.set("")
        self.password.set("")

    def exit_func(self):
        self.win.destroy()

    def on_closing(self):
        self.win.deiconify()  # Restore the login window
        self.reset_func()  # Clear the credentials

    def open_employee_window(self):
        # self.win.withdraw()  # Hide the login window
        os.system('python main.py')

    def open_admin_window(self):
        self.win.withdraw()  # Hide the login window
        admin_window = Toplevel(self.win)
        admin_window.title("Admin Window")
        admin_window.geometry("1350x750")
        Label(admin_window, text="Welcome, Admin!", font=("Arial", 20)).pack(pady=20)
        Button(admin_window, text="Entry", command=self.open_entry_window, height=2, font=("None", 10, "bold"), width=10,
                        fg='white', bg='blue').pack(pady=5)
        Button(admin_window, text="ARIMA", command=self.open_arima_window, height=2, font=("None", 10, "bold"), width=10,
                        fg='white', bg='blue').pack(pady=5)
        Button(admin_window, text="Logout", command=self.logout_admin, height=2, font=("None", 10, "bold"), width=10,
                        fg='white', bg='red').pack(pady=10)

    def logout_admin(self):
        self.win.deiconify()  # Restore the login window
        self.reset_func()  # Clear the credentials

    def open_entry_window(self):
        os.system('python main.py')

    def open_arima_window(self):
        os.system('python "ARIMA 2.py"')

    def employee_login(self):
        self.username.set("")
        self.password.set("")

    def admin_login(self):
        self.username.set("")
        self.password.set("")


def main():
    app = Tk()
    ob = Loginpage(app)
    app.mainloop()


if __name__ == "__main__":
    main()

