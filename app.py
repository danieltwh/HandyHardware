from tkinter import *
from tkinter import ttk
from typing import Match
from PIL import ImageTk, Image
import sqlite3



##### IMPORT PAGES #####
from login import Admin_Login_Page, Admin_Signup_Page, Login_Page, Signup_Page
from request_page import Request_Page
from admin_request import Admin_Request_Page
from cus_request_details import Request_Details
from customerItem import Customer_Shopping_Catalogue_Page
from past_purchases import Past_Purchase_Page
from ResetDB import RESET_DB

PAGES = {
    "login": Login_Page, 
    "customer_shopping_catalogue": Customer_Shopping_Catalogue_Page,
    "customer_past_purchases": Past_Purchase_Page,
    "admin_request": Admin_Request_Page,
}

##########################

class SideBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=400, height=800)
        self.master = master

        catalogue_btn = Button(self, text="Shop", padx=10, highlightbackground="#ffffff", 
            command=lambda: master.switch_frame(PAGES.get("customer_shopping_catalogue")))
        catalogue_btn.grid(row=1, column=0, padx=(5, 10), sticky="EW", pady=(10, 5))

        past_purchases_btn = Button(self, text="Past Purchases / Make Request", wraplength=130,
            command=lambda: master.switch_frame(PAGES.get("customer_past_purchases")))
        past_purchases_btn.grid(row=2, column=0, padx=(5, 10), sticky="EW", pady=(5, 5))

        # ttk.Style().configure("red/black.TButton", foreground="black", background="red")

        logout_btn = Button(self, text="Logout", padx=10,  
            command=lambda: master.logout())
        logout_btn.grid(row=3, column=0, padx=(5, 10), sticky="EW", pady=(5, 5))

class AdminSideBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=400, height=800)
        self.master = master

        catalogue_btn = Button(self, text="Items", padx=10, highlightbackground="#ffffff", 
            command=lambda: master.switch_frame(PAGES.get("customer_shopping_catalogue")))
        catalogue_btn.grid(row=1, column=0, padx=(5, 10), sticky="EW", pady=(10, 5))

        past_purchases_btn = Button(self, text="Manage Request", wraplength=130,
            command=lambda: master.switch_frame(PAGES.get("admin_request")))
        past_purchases_btn.grid(row=2, column=0, padx=(5, 10), sticky="EW", pady=(5, 5))

        # ttk.Style().configure("red/black.TButton", foreground="black", background="red")

        logout_btn = Button(self, text="Logout", padx=10,  
            command=lambda: master.logout())
        logout_btn.grid(row=3, column=0, padx=(5, 10), sticky="EW", pady=(5, 5))

        DB_reset_btn = Button(self, text = "Reset DB", padx=10,
            command=lambda: self.resetDB())
        DB_reset_btn.grid(row=4, column=0, padx=(5, 10), sticky="EW", pady=(5, 5))

    
    def resetDB(self):
        RESET_DB()
        self.master.switch_frame(PAGES.get("customer_shopping_catalogue"))
        
        


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self._sideBar= None
        
        # self.mount_sidebar()
        # self.switch_frame(Request_Details)
        
        self.load_login_page();

        

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

        if frame_class in [Login_Page, Signup_Page, Admin_Login_Page, Admin_Signup_Page]:
            self._frame.pack(fill="both", expand=True, padx=350, pady=250)
        else:
            self._frame.pack(side="right", fill="both", expand=True, anchor = "nw", padx=(10, 0))
            # self._frame.grid(row=0, column=1, )

    ### FOR CUSTOMERS ###
    def mount_sidebar(self):
        self._sideBar = SideBar(self)
        self._sideBar.config(bg="#495867")
        self._sideBar.pack(side="left", fill="y")

    def unmount_sidebar(self):
        self._sideBar.destroy()
    
    def load_login_page(self):
        new_frame = PAGES.get("login")(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True, padx=350, pady=250)
    
    def logout(self):
        self.unmount_sidebar()
        self.load_login_page()

    def login(self):
        self.mount_sidebar()
        self.switch_frame(PAGES.get("customer_shopping_catalogue"))


    ### FOR ADMINS ###   
    def mount_admin_sidebar(self):
        self._sideBar = AdminSideBar(self)
        self._sideBar.config(bg="#495867")
        self._sideBar.pack(side="left", fill="y")

    def admin_login(self):
        self.mount_admin_sidebar()
        self.switch_frame(PAGES.get("admin_request"))



def main():
    # root = Tk()
    # root.title("OSHE")
    # # root.iconbitmap('coffee.ico')
    # root.geometry("800x800")
    # # app = Signup_Page(root)
    # # app = Login_Page(root)
    # root.mainloop()

    app = App()
    app.geometry("1200x800")
    app.mainloop()

if __name__ == "__main__":
    main()