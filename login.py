from tkinter import *
from typing import Match
from PIL import ImageTk, Image
import sqlite3
import re


# For SQL query
from sqlalchemy import create_engine
from pymysql.constants import CLIENT
import pandas as pd

from config import USERNAME, MYSQL_PASSWORD
db = create_engine(f"mysql+pymysql://{USERNAME}:{MYSQL_PASSWORD}@127.0.0.1:3306/ECOMMERCE", 
        connect_args = {"client_flag": CLIENT.MULTI_STATEMENTS}
    )



######## Customer Registration & Login ###########
class Signup_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=800, height=800)
        self.master = master
        
        # Creatinag Text Boxes
        f_name = Entry(self, width = 30)
        f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

        l_name = Entry(self, width = 30)
        l_name .grid(row=1, column=1, padx=20)

        GENDER = [
            ("Male", "M"),
            ("Female", "F"),
            ("Others", "Others")
        ]

        gender = StringVar()
        gender.set("null")

        gender_frame = LabelFrame(self, borderwidth = 0)
        gender_frame.grid(row=2, column=1, padx=20)

        for text, sex in GENDER:
            Radiobutton(gender_frame, text=text, variable=gender, value=sex).pack(side=LEFT, anchor=W)

        email = Entry(self, width = 30)
        email.grid(row=3, column=1, padx=20)

        phone = Entry(self, width = 30)
        phone.grid(row=4, column=1, padx=20)

        address = Entry(self, width = 30)
        address.grid(row=5, column=1, padx=20)

        password = Entry(self, width = 30)
        password.grid(row=6, column=1, padx=20)


        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 0))

        l_name_label = Label(self, text="Last Name")
        l_name_label.grid(row=1, column=0)

        gender_label = Label(self, text="Gender")
        gender_label.grid(row=2, column=0)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0)

        password_label = Label(self, text="Password")
        password_label.grid(row=6, column=0)

        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Login_Page))
        back_btn.grid(row=7, column=0, padx=(10,0), sticky="W")
        
        confirm_btn = Button(self, text="Confirm", command=lambda: self.customer_signup())
        confirm_btn.grid(row=7, column=1, padx=(0, 10), sticky="E")


        # self.pack(side="top", fill="both", expand=True)

    def customer_signup(self):
        print("Check & signup customer")


class Login_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=800, height=800)
        self.master = master


        title = Label(self, text="Customer Login Page")
        title.grid(row=0, column=0, columnspan=1)

        toggle = LabelFrame(self, borderwidth = 0)
        toggle.grid(row=0, column=1, padx=20)

        customer_btn = Button(toggle, text="Customer", command= lambda: master.switch_frame(Login_Page))
        customer_btn.grid(row=0, column=0, columnspan=1)

        admin_btn = Button(toggle, text="Admin", command= lambda: master.switch_frame(Admin_Login_Page))
        admin_btn.grid(row=0, column=1, columnspan=1)
       
        self.username = Entry(self, width = 30)
        self.username.grid(row=2, column=1, padx=20)

        self.password = Entry(self, width = 30)
        self.password.grid(row=4, column=1, padx=20)


        # Creating Text Box Labels

        self.customerId_error_label = Label(self, text= "")
        self.password_error_label = Label(self, text= "")
        self.error_label = Label(self, text= "")
        
        username_label = Label(self, text="Email Address")
        username_label.grid(row=2, column=0, sticky="EW")


        password_label = Label(self, text="Password")
        password_label.grid(row=4, column=0, sticky="EW")

        signup_btn = Button(self, text="Sign Up", command= lambda: master.switch_frame(Signup_Page))
        signup_btn.grid(row=6, column=0, columnspan=1)

        login_btn = Button(self, text="Login", command= lambda: self.attempt_login())
        login_btn.grid(row=6, column=1, columnspan=2)

    def attempt_login(self):
        customerId = self.username.get()
        password = self.password.get()

        # Reset the error message
        self.customerId_error_label.destroy()
        self.password_error_label.destroy()
        self.error_label.destroy()
        self.customerId_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.password_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.error_label = Label(self, text= "", fg="red", anchor="w", width = 30)

        # General Regex
        whitespace = re.compile(r"\s+")

        customerId_Error = ""
        password_Error = ""

        # Checking customerId
        if len(whitespace.findall(customerId)) > 0:
            # Whitespaces found in customerId
            customerId_Error = "Whitespaces not allowed"
        elif customerId == "":
            customerId_Error = "Required"

        
        # Checking customerId
        if len(whitespace.findall(password)) > 0:
            # Whitespaces found in customerId
            password_Error = "Whitespaces not allowed"
        elif password == "":
            password_Error = "Required"


        # Displaying customerId Error
        if customerId_Error != "":
            self.customerId_error_label["text"] = customerId_Error
            self.customerId_error_label.grid(row=3, column=1, columnspan=1, sticky="EW", padx=20)
        
        # Displaying password Error
        if password_Error != "":
            self.password_error_label["text"] = password_Error
            self.password_error_label.grid(row=5, column=1, columnspan=1, sticky="EW", padx=20)


        # After the checks, we proceed to login
        if customerId_Error == "" and password_Error == "":
            print(customerId, password)

            conn = db.connect()
            result = conn.execute(f"""
                    SELECT customerPassword
                    FROM Customers
                    WHERE customerID = "{customerId}"
                    ;
            """)
            retrieved_password = result.fetchall()

            if len(retrieved_password) == 0:
                self.customerId_error_label["text"] = "User does not exist"
                self.customerId_error_label.grid(row=3, column=1, columnspan=1, sticky="EW", padx=20)
            else:
                retrieved_password = retrieved_password[0][0]
                
                if retrieved_password == password:
                    print("success")
                    self.master.login()
                else:
                    # self.error_label["text"] = "I"
                    # self.error_label.grid(row=5, column=1, columnspan=1, sticky="EW", padx=20)

                    self.password_error_label["text"] = "Incorrect password"
                    self.password_error_label.grid(row=5, column=1, columnspan=1, sticky="EW", padx=20)




######## Admin Registration & Login ###########
class Admin_Signup_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=800, height=800)
        self.master = master
        
        # Creatinag Text Boxes
        f_name = Entry(self, width = 30)
        f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

        l_name = Entry(self, width = 30)
        l_name .grid(row=1, column=1, padx=20)

        GENDER = [
            ("Male", "M"),
            ("Female", "F"),
            ("Others", "Others")
        ]

        gender = StringVar()
        gender.set("null")

        gender_frame = LabelFrame(self, borderwidth = 0)
        gender_frame.grid(row=2, column=1, padx=20)

        for text, sex in GENDER:
            Radiobutton(gender_frame, text=text, variable=gender, value=sex).pack(side=LEFT, anchor=W)

        email = Entry(self, width = 30)
        email.grid(row=3, column=1, padx=20)

        phone = Entry(self, width = 30)
        phone.grid(row=4, column=1, padx=20)

        address = Entry(self, width = 30)
        address.grid(row=5, column=1, padx=20)

        password = Entry(self, width = 30)
        password.grid(row=6, column=1, padx=20)


        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 0))

        l_name_label = Label(self, text="Last Name")
        l_name_label.grid(row=1, column=0)

        gender_label = Label(self, text="Gender")
        gender_label.grid(row=2, column=0)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0)

        password_label = Label(self, text="Password")
        password_label.grid(row=6, column=0)

        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Login_Page))
        back_btn.grid(row=7, column=0, padx=(10,0), sticky="W")
        
        confirm_btn = Button(self, text="Confirm", command=lambda: self.admin_signup())
        confirm_btn.grid(row=7, column=1, padx=(0, 10), sticky="E")
        
        # self.pack(side="top", fill="both", expand=True)
    
    def admin_signup(self):
        print("Check & signup admin")





class Admin_Login_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=800, height=800)
        self.master = master

        title = Label(self, text="Admin Login Page")
        title.grid(row=0, column=0, columnspan=1)

        toggle = LabelFrame(self, borderwidth = 0)
        toggle.grid(row=0, column=1, padx=20)

        customer_btn = Button(toggle, text="Customer", command= lambda: master.switch_frame(Login_Page))
        customer_btn.grid(row=0, column=0, columnspan=1)

        admin_btn = Button(toggle, text="Admin", command= lambda: master.switch_frame(Admin_Login_Page))
        admin_btn.grid(row=0, column=1, columnspan=1)
       
        email = Entry(self, width = 30)
        email.grid(row=2, column=1, padx=20)

        password = Entry(self, width = 30)
        password.grid(row=3, column=1, padx=20)


        # Creating Text Box Labels
        email_label = Label(self, text="Email Address")
        email_label.grid(row=2, column=0)

        password_label = Label(self, text="Password")
        password_label.grid(row=3, column=0)

        signup_btn = Button(self, text="Sign Up", command= lambda: master.switch_frame(Admin_Signup_Page))
        signup_btn.grid(row=4, column=0, columnspan=1)

        login_btn = Button(self, text="Login", command= lambda: self.attempt_login())
        login_btn.grid(row=4, column=1, columnspan=2)

    def attempt_login(self):
        self.master.admin_login()