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

        self.f_name_error_label = Label(self, text= "")
        self.l_name_error_label = Label(self, text= "")
        self.username_error_label = Label(self, text= "")
        self.gender_error_label = Label(self, text= "")
        self.email_error_label = Label(self, text= "")
        self.phone_error_label = Label(self, text= "")
        self.address_error_label = Label(self, text="")
        self.password_error_label = Label(self, text= "")
        
        welcome_label = Label(self, text = "Welcome!")
        welcome_label.grid(row=0, column=0, columnspan=2)

        # Creatinag Text Boxes
        self.f_name = Entry(self, width = 30)
        self.f_name.grid(row=1, column=1, padx=20, pady=(10, 0))

        self.l_name = Entry(self, width = 30)
        self.l_name .grid(row=3, column=1, padx=20)

        self.username = Entry(self, width=30)
        self.username .grid(row=5, column=1, padx=20)

        GENDER = [
            ("Male", "MALE"),
            ("Female", "FEMALE"),
            ("Others", "OTHERS")
        ]

        self.gender = StringVar()
        self.gender.set("null")

        gender_frame = LabelFrame(self, borderwidth = 0)
        gender_frame.grid(row=7, column=1, padx=20)

        for text, sex in GENDER:
            Radiobutton(gender_frame, text=text, variable=self.gender, value=sex).pack(side=LEFT, anchor=W)

        self.email = Entry(self, width = 30)
        self.email.grid(row=9, column=1, padx=20)

        self.phone = Entry(self, width = 30)
        self.phone.grid(row=11, column=1, padx=20)

        self.address = Entry(self, width = 30)
        self.address.grid(row=13, column=1, padx=20)

        self.password = Entry(self, width = 30, show="*")
        self.password.grid(row=15, column=1, padx=20)


        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=1, column=0, pady=(10, 2.5))

        l_name_label = Label(self, text="Last Name")
        l_name_label.grid(row=3, column=0, pady=(2.5,2.5))

        username_label = Label(self, text="Username")
        username_label.grid(row=5, column=0, pady=(2.5,2.5))

        gender_label = Label(self, text="Gender")
        gender_label.grid(row=7, column=0, pady=(2.5,2.5))

        email_label = Label(self, text="Email Address")
        email_label.grid(row=9, column=0, pady=(2.5,2.5))

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=11, column=0, pady=(2.5,2.5))

        address_label = Label(self, text="Address")
        address_label.grid(row=13, column=0, pady=(2.5,2.5))

        password_label = Label(self, text="Password")
        password_label.grid(row=15, column=0, pady=(2.5,2.5))

        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Login_Page))
        back_btn.grid(row=17, column=0, padx=(10,0), sticky="W", pady=(10,2.5))
        
        confirm_btn = Button(self, text="Confirm", command=lambda: self.customer_signup())
        confirm_btn.grid(row=17, column=1, padx=(0, 10), sticky="E", pady=(10,2.5))


        # self.pack(side="top", fill="both", expand=True)

    def customer_signup(self):
        
        f_name = self.f_name.get()
        l_name = self.l_name.get()
        username = self.username.get()
        gender = self.gender.get()
        email = self.email.get()
        phone = self.phone.get()
        address = self.address.get()
        password = self.password.get()

        print(f_name, l_name, username, gender, email, phone, address, password)

        # Reset the error messages
        self.f_name_error_label.destroy()
        self.l_name_error_label.destroy()
        self.username_error_label.destroy()
        self.gender_error_label.destroy()
        self.email_error_label.destroy()
        self.phone_error_label.destroy()
        self.address_error_label.destroy()
        self.password_error_label.destroy()

        self.f_name_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.l_name_error_label = Label(self, text= "",  fg="red", anchor="w", width = 30)
        self.username_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.gender_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.email_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.phone_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.address_error_label = Label(self, text="", fg="red", anchor="w", width = 30)
        self.password_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)

        f_name_error = ""
        l_name_error = ""
        username_error = ""
        gender_error = ""
        email_error = ""
        phone_error = ""
        address_error = ""
        password_error = ""
        

        # General Regex
        whitespace = re.compile(r"\s+")
        all_numbers = re.compile(r"\D")
        sg_number = re.compile(r"^[896]\d{7}$")
        address_checker = re.compile(r"^\s|\s$")


        # Checking First Name
        if len(whitespace.findall(f_name)) > 0:
            # Whitespaces found in customerId
            f_name_error = "Whitespaces not allowed"
        elif f_name == "":
            # Required
            f_name_error = "Required"

        # Checking Last Name
        if len(whitespace.findall(l_name)) > 0:
            # Whitespaces found in customerId
            l_name_error = "Whitespaces not allowed"
        elif l_name == "":
            # Required
            l_name_error = "Required"

        # Checking Username
        if len(whitespace.findall(username)) > 0:
            # Whitespaces found in customerId
            username_error = "Whitespaces not allowed"
        elif username == "":
            # Required
            username_error = "Required"
        else:
            try:
                conn = db.connect()
                result = conn.execute(f"""
                    SELECT *
                    FROM Customers
                    WHERE customerID = "{username}"; 
                """)
                conn.close()
                if len(result.all()) != 0:
                    username_error = "Username taken"
            except:
                username_error = "Username check failed. Try again."
        
        # Checking Gender
        if gender == "null":
            # Required
            gender_error = "Required"
        
        # Checking Email
        if len(whitespace.findall(email)) > 0:
            # Whitespaces found in customerId
            email_error = "Whitespaces not allowed"
        elif email == "":
            # Required
            email_error = "Required"
        elif not self.email_validator(email):
            email_error = "Invalid email"
        
        # Checking Phone 
        if len(whitespace.findall(phone)) > 0:
            # Whitespaces found in customerId
            phone_error = "Whitespaces not allowed"
        elif phone == "":
            # Required
            phone_error = "Required"
        elif len(all_numbers.findall(phone)) >0 :
            # Invalid Phone
            phone_error = "Invalid phone number"
        elif len(phone) < 8:
            # Too short
            phone_error = "Too short...(SG number only)"
        elif len(phone) > 8:
            # Too long
            phone_error = "Max 8 digits"
        elif len(sg_number.findall(phone)) != 1:
            # SG phone number
            phone_error = "SG number only"
        
        # Checking Address
        # if len(whitespace.findall(address)) > 0:
        #     # Whitespaces found in customerId
        #     address_error = "Whitespaces not allowed"
        if address == "":
            # Required
            address_error = "Required"
        elif len(address_checker.findall(address)) != 0:
            # Required
            address_error = "Cannot start/end with whitespace(s)"
        
        # Checking Password
        if len(whitespace.findall(password)) > 0:
            # Whitespaces found in customerId
            password_error = "Whitespaces not allowed"
        elif password == "":
            # Required
            password_error = "Required"
        elif len(password) < 8:
            # Required
            password_error = "Too short... Minimum 8 characters"
        elif len(password) > 30:
            # Required
            password_error = "Too long... Maximum 30 characters"
        
        
        # Displaying Errors
        if f_name_error != "":
            self.f_name_error_label["text"] = f_name_error
            self.f_name_error_label.grid(row=2, column=1, columnspan=1, sticky="EW", padx=20)
        if l_name_error != "":
            self.l_name_error_label["text"] = l_name_error
            self.l_name_error_label.grid(row=4, column=1, columnspan=1, sticky="EW", padx=20)
        if username_error != "":
            self.username_error_label["text"] = username_error
            self.username_error_label.grid(row=6, column=1, columnspan=1, sticky="EW", padx=20)
        if gender_error != "":
            self.gender_error_label["text"] = gender_error
            self.gender_error_label.grid(row=8, column=1, columnspan=1, sticky="EW", padx=20)
        if email_error != "":
            self.email_error_label["text"] = email_error
            self.email_error_label.grid(row=10, column=1, columnspan=1, sticky="EW", padx=20)
        if phone_error != "":
            self.phone_error_label["text"] = phone_error
            self.phone_error_label.grid(row=12, column=1, columnspan=1, sticky="EW", padx=20)
        if address_error != "":
            self.address_error_label["text"] = address_error
            self.address_error_label.grid(row=14, column=1, columnspan=1, sticky="EW", padx=20)
        if password_error != "":
            self.password_error_label["text"] = password_error
            self.password_error_label.grid(row=16, column=1, columnspan=1, sticky="EW", padx=20)

        # Creating Customer User
        if f_name_error == "" and l_name_error == "" and username_error == "" \
            and gender_error == "" and email_error == "" and phone_error == "" and address_error == ""\
            and password_error == "":
            try:
                conn = db.connect()
                result = conn.execute(f"""
                    INSERT INTO Customers(customerID, customerName, gender, email, phoneNumber, address, customerPassword) VALUES
                    ('{username}', "{f_name + " " + l_name}", "{gender.upper()}", "{email}", "{phone}",
                    "{address}", "{password}");
                """)
                conn.close()
                self.master.load_login_page()
            except:
                print("error")

        print("Check & signup customer")
        
    
    def email_validator(self, email):
        validator = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}")
        if validator.fullmatch(email):
            return True
        else:
            return False


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
        self.username.grid(row=2, column=1, padx=20, pady=(10,2.5))

        self.password = Entry(self, width = 30, show="*")
        self.password.grid(row=4, column=1, padx=20, pady=(2.5,2.5))


        # Creating Text Box Labels

        self.customerId_error_label = Label(self, text= "")
        self.password_error_label = Label(self, text= "")
        self.error_label = Label(self, text= "")
        
        username_label = Label(self, text="Username")
        username_label.grid(row=2, column=0, sticky="EW", pady=(10,2.5))


        password_label = Label(self, text="Password")
        password_label.grid(row=4, column=0, sticky="EW", pady=(2.5,2.5))

        signup_btn = Button(self, text="Sign Up", command= lambda: master.switch_frame(Signup_Page))
        signup_btn.grid(row=6, column=0, columnspan=1, pady=(5,5))

        login_btn = Button(self, text="Login", command= lambda: self.attempt_login())
        login_btn.grid(row=6, column=1, columnspan=2, pady=(5,5))

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
                    self.master.login(customerId)
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
        
        self.f_name_error_label = Label(self, text= "")
        self.l_name_error_label = Label(self, text= "")
        self.username_error_label = Label(self, text= "")
        self.gender_error_label = Label(self, text= "")
  
        self.phone_error_label = Label(self, text= "")

        self.password_error_label = Label(self, text= "")
        
        welcome_label = Label(self, text = "Welcome!")
        welcome_label.grid(row=0, column=0, columnspan=2)

        # Creatinag Text Boxes
        self.f_name = Entry(self, width = 30)
        self.f_name.grid(row=1, column=1, padx=20, pady=(10, 0))

        self.l_name = Entry(self, width = 30)
        self.l_name .grid(row=3, column=1, padx=20)

        self.username = Entry(self, width=30)
        self.username .grid(row=5, column=1, padx=20)

        GENDER = [
            ("Male", "MALE"),
            ("Female", "FEMALE"),
            ("Others", "OTHERS")
        ]

        self.gender = StringVar()
        self.gender.set("null")

        gender_frame = LabelFrame(self, borderwidth = 0)
        gender_frame.grid(row=7, column=1, padx=20)

        for text, sex in GENDER:
            Radiobutton(gender_frame, text=text, variable=self.gender, value=sex).pack(side=LEFT, anchor=W)

        self.phone = Entry(self, width = 30)
        self.phone.grid(row=11, column=1, padx=20)

        self.password = Entry(self, width = 30, show="*")
        self.password.grid(row=15, column=1, padx=20)


        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=1, column=0, pady=(10, 2.5))

        l_name_label = Label(self, text="Last Name")
        l_name_label.grid(row=3, column=0, pady=(2.5,2.5))

        username_label = Label(self, text="Username")
        username_label.grid(row=5, column=0, pady=(2.5,2.5))

        gender_label = Label(self, text="Gender")
        gender_label.grid(row=7, column=0, pady=(2.5,2.5))

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=11, column=0, pady=(2.5,2.5))


        password_label = Label(self, text="Password")
        password_label.grid(row=15, column=0, pady=(2.5,2.5))

        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Login_Page))
        back_btn.grid(row=17, column=0, padx=(10,0), sticky="W", pady=(10,2.5))
        
        confirm_btn = Button(self, text="Confirm", command=lambda: self.admin_signup())
        confirm_btn.grid(row=17, column=1, padx=(0, 10), sticky="E", pady=(10,2.5))


        # self.pack(side="top", fill="both", expand=True)

    def admin_signup(self):
        
        f_name = self.f_name.get()
        l_name = self.l_name.get()
        username = self.username.get()
        gender = self.gender.get()
        phone = self.phone.get()
        password = self.password.get()

        print(f_name, l_name, username, gender, phone, password)

        # Reset the error messages
        self.f_name_error_label.destroy()
        self.l_name_error_label.destroy()
        self.username_error_label.destroy()
        self.gender_error_label.destroy()

        self.phone_error_label.destroy()

        self.password_error_label.destroy()

        self.f_name_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.l_name_error_label = Label(self, text= "",  fg="red", anchor="w", width = 30)
        self.username_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.gender_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)

        self.phone_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)

        self.password_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)

        f_name_error = ""
        l_name_error = ""
        username_error = ""
        gender_error = ""

        phone_error = ""

        password_error = ""
        

        # General Regex
        whitespace = re.compile(r"\s+")
        all_numbers = re.compile(r"\D")
        sg_number = re.compile(r"^[896]\d{7}$")
        address_checker = re.compile(r"^\s|\s$")


        # Checking First Name
        if len(whitespace.findall(f_name)) > 0:
            # Whitespaces found in adminId
            f_name_error = "Whitespaces not allowed"
        elif f_name == "":
            # Required
            f_name_error = "Required"

        # Checking Last Name
        if len(whitespace.findall(l_name)) > 0:
            # Whitespaces found in adminId
            l_name_error = "Whitespaces not allowed"
        elif l_name == "":
            # Required
            l_name_error = "Required"

        # Checking Username
        if len(whitespace.findall(username)) > 0:
            # Whitespaces found in adminId
            username_error = "Whitespaces not allowed"
        elif username == "":
            # Required
            username_error = "Required"
        else:
            try:
                conn = db.connect()
                result = conn.execute(f"""
                    SELECT *
                    FROM Administrators
                    WHERE administratorID = "{username}"; 
                """)
                conn.close()
                if len(result.all()) != 0:
                    username_error = "Username taken"
            except:
                username_error = "Username check failed. Try again."
        
        # Checking Gender
        if gender == "null":
            # Required
            gender_error = "Required"
        
        # Checking Phone 
        if len(whitespace.findall(phone)) > 0:
            # Whitespaces found in adminId
            phone_error = "Whitespaces not allowed"
        elif phone == "":
            # Required
            phone_error = "Required"
        elif len(all_numbers.findall(phone)) >0 :
            # Invalid Phone
            phone_error = "Invalid phone number"
        elif len(phone) < 8:
            # Too short
            phone_error = "Too short...(SG number only)"
        elif len(phone) > 8:
            # Too long
            phone_error = "Max 8 digits"
        elif len(sg_number.findall(phone)) != 1:
            # SG phone number
            phone_error = "SG number only"
        
        # Checking Password
        if len(whitespace.findall(password)) > 0:
            # Whitespaces found in adminId
            password_error = "Whitespaces not allowed"
        elif password == "":
            # Required
            password_error = "Required"
        elif len(password) < 8:
            # Required
            password_error = "Too short... Minimum 8 characters"
        elif len(password) > 30:
            # Required
            password_error = "Too long... Maximum 30 characters"
        
        
        # Displaying Errors
        if f_name_error != "":
            self.f_name_error_label["text"] = f_name_error
            self.f_name_error_label.grid(row=2, column=1, columnspan=1, sticky="EW", padx=20)
        if l_name_error != "":
            self.l_name_error_label["text"] = l_name_error
            self.l_name_error_label.grid(row=4, column=1, columnspan=1, sticky="EW", padx=20)
        if username_error != "":
            self.username_error_label["text"] = username_error
            self.username_error_label.grid(row=6, column=1, columnspan=1, sticky="EW", padx=20)
        if gender_error != "":
            self.gender_error_label["text"] = gender_error
            self.gender_error_label.grid(row=8, column=1, columnspan=1, sticky="EW", padx=20)
    
        if phone_error != "":
            self.phone_error_label["text"] = phone_error
            self.phone_error_label.grid(row=12, column=1, columnspan=1, sticky="EW", padx=20)
      
        if password_error != "":
            self.password_error_label["text"] = password_error
            self.password_error_label.grid(row=16, column=1, columnspan=1, sticky="EW", padx=20)

        # Creating admin User
        if f_name_error == "" and l_name_error == "" and username_error == "" \
            and gender_error == "" and phone_error == "" \
            and password_error == "":
            try:
                conn = db.connect()
                result = conn.execute(f"""
                    INSERT INTO Administrators(administratorID, administratorName, gender, phoneNumber, administratorPassword) VALUES
                    ('{username}', "{f_name + " " + l_name}", "{gender.upper()}",  "{phone}",
                    "{password}");
                """)
                conn.close()
                self.master.load_login_page()
            except:
                print("error")

        print("Check & signup admin")
        
    
    def email_validator(self, email):
        validator = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}")
        if validator.fullmatch(email):
            return True
        else:
            return False





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
       
        self.username = Entry(self, width = 30)
        self.username.grid(row=2, column=1, padx=20, pady=(10,2.5))

        self.password = Entry(self, width = 30, show="*")
        self.password.grid(row=4, column=1, padx=20, pady=(2.5,2.5))


        # Creating Text Box Labels
        self.adminId_error_label = Label(self, text= "")
        self.password_error_label = Label(self, text= "")
        self.error_label = Label(self, text= "")
        
        username_label = Label(self, text="Username")
        username_label.grid(row=2, column=0, sticky="EW", pady=(10,2.5))


        password_label = Label(self, text="Password")
        password_label.grid(row=4, column=0, sticky="EW", pady=(2.5,2.5))

        signup_btn = Button(self, text="Sign Up", command= lambda: master.switch_frame(Admin_Signup_Page))
        signup_btn.grid(row=6, column=0, columnspan=1, pady=(5,5))

        login_btn = Button(self, text="Login", command= lambda: self.attempt_login())
        login_btn.grid(row=6, column=1, columnspan=2, pady=(5,5))

    def attempt_login(self):
        adminId = self.username.get()
        password = self.password.get()

        # Reset the error message
        self.adminId_error_label.destroy()
        self.password_error_label.destroy()
        self.error_label.destroy()
        self.adminId_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.password_error_label = Label(self, text= "", fg="red", anchor="w", width = 30)
        self.error_label = Label(self, text= "", fg="red", anchor="w", width = 30)

        # General Regex
        whitespace = re.compile(r"\s+")

        adminId_Error = ""
        password_Error = ""

        # Checking adminId
        if len(whitespace.findall(adminId)) > 0:
            # Whitespaces found in adminId
            adminId_Error = "Whitespaces not allowed"
        elif adminId == "":
            adminId_Error = "Required"

        
        # Checking adminId
        if len(whitespace.findall(password)) > 0:
            # Whitespaces found in customerId
            password_Error = "Whitespaces not allowed"
        elif password == "":
            password_Error = "Required"


        # Displaying adminId Error
        if adminId_Error != "":
            self.adminId_error_label["text"] = adminId_Error
            self.adminId_error_label.grid(row=3, column=1, columnspan=1, sticky="EW", padx=20)
        
        # Displaying password Error
        if password_Error != "":
            self.password_error_label["text"] = password_Error
            self.password_error_label.grid(row=5, column=1, columnspan=1, sticky="EW", padx=20)


        # After the checks, we proceed to login
        if adminId_Error == "" and password_Error == "":
            print(adminId, password)

            conn = db.connect()
            result = conn.execute(f"""
                    SELECT administratorPassword
                    FROM Administrators
                    WHERE administratorID = "{adminId}"
                    ;
            """)
            retrieved_password = result.fetchall()

            if len(retrieved_password) == 0:
                self.adminId_error_label["text"] = "User does not exist"
                self.adminId_error_label.grid(row=3, column=1, columnspan=1, sticky="EW", padx=20)
            else:
                retrieved_password = retrieved_password[0][0]
                
                if retrieved_password == password:
                    print("success")
                    self.master.admin_login(adminId)
                else:
                    # self.error_label["text"] = "I"
                    # self.error_label.grid(row=5, column=1, columnspan=1, sticky="EW", padx=20)

                    self.password_error_label["text"] = "Incorrect password"
                    self.password_error_label.grid(row=5, column=1, columnspan=1, sticky="EW", padx=20)