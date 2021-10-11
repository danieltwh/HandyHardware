from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3

# For SQL query
from sqlalchemy import create_engine
from pymysql.constants import CLIENT
import pandas as pd

from config import USERNAME, MYSQL_PASSWORD
db = create_engine(f"mysql+pymysql://{USERNAME}:{MYSQL_PASSWORD}@127.0.0.1:3306/ECOMMERCE", 
        connect_args = {"client_flag": CLIENT.MULTI_STATEMENTS}
    )

# Import custom Scrollable Frame
from ScrollableFrame import ScrollableFrame

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

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self._sideBar= None
        
        self.customerId = ""
        self.adminId = "EddMing321"
        
        # self.mount_sidebar()
        # self.switch_frame(Request_Details_page)
        
        # self.load_login_page();

        

    def switch_frame(self, frame_class):
        print(self.customerId if self.customerId else self.adminId)
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

 
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
        # self._frame.pack(fill="both", expand=True, padx=0, pady=225)
        self._frame.pack(expand=True)
    
    def logout(self):
        self.customerId = ""
        self.adminId = ""
        self.unmount_sidebar()
        self.load_login_page()

    def login(self, customerId):
        self.customerId = customerId
        self.mount_sidebar()
        self.switch_frame(PAGES.get("customer_shopping_catalogue"))


    ### FOR ADMINS ###   
    def mount_admin_sidebar(self):
        self._sideBar = AdminSideBar(self)
        self._sideBar.config(bg="#495867")
        self._sideBar.pack(side="left", fill="y")

    def admin_login(self, adminId):
        self.adminId = adminId
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
    app.switch_frame(Admin_Request_Page)
    app.mainloop()
    

####################



data = [
    ("001", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "Approved"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("006", "Ethel", "Lock1", "Issue", "Canceled"),
    ("007", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("010", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "Approved"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("015", "Ethel", "Lock1", "Issue", "Canceled"),
    ("016", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("019", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "Approved"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("024", "Ethel", "Lock1", "Issue", "Canceled"),
    ("025", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("028", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "Approved"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("033", "Ethel", "Lock1", "Issue", "Canceled"),
    ("034", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("001", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "Approved"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("006", "Ethel", "Lock1", "Issue", "Canceled"),
    ("007", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("010", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "Approved"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("015", "Ethel", "Lock1", "Issue", "Canceled"),
    ("016", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("019", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "Approved"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("024", "Ethel", "Lock1", "Issue", "Canceled"),
    ("025", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("028", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "Approved"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("033", "Ethel", "Lock1", "Issue", "Canceled"),
    ("034", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment")
]


service = [
    ("001", "John", "Light1", "Issue", "Waiting for approval"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "In progress"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("006", "Ethel", "Lock1", "Issue", "Completed"),
    ("007", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("010", "John", "Light1", "Issue", "Waiting for approval"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "In progress"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("015", "Ethel", "Lock1", "Issue", "Completed"),
    ("016", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("019", "John", "Light1", "Issue", "Waiting for approval"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "In progress"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("024", "Ethel", "Lock1", "Issue", "Completed"),
    ("025", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("028", "John", "Light1", "Issue", "Waiting for approval"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "In progress"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("033", "Ethel", "Lock1", "Issue", "Completed"),
    ("034", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("001", "John", "Light1", "Issue", "Waiting for approval"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "In progress"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("006", "Ethel", "Lock1", "Issue", "Completed"),
    ("007", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("010", "John", "Light1", "Issue", "Waiting for approval"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "In progress"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("015", "Ethel", "Lock1", "Issue", "Completed"),
    ("016", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("019", "John", "Light1", "Issue", "Waiting for approval"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "In progress"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("024", "Ethel", "Lock1", "Issue", "Completed"),
    ("025", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("028", "John", "Light1", "Issue", "Waiting for approval"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "In progress"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("033", "Ethel", "Lock1", "Issue", "Completed"),
    ("034", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Waiting for approval")
]


####### Admin Request Pages ###########


request_view = "All"
service_view = "All"

ORDER_BY_SERVICE_STATUS = """
ORDER BY 
	CASE s.serviceStatus
      WHEN 'In progress' THEN 1
      WHEN 'Waiting for approval' THEN 2
      WHEN 'Completed' THEN 3
	END, 
    CASE r.requestStatus
      WHEN 'Approved' THEN 1
      WHEN 'Completed' THEN 2
      WHEN 'Cancelled' THEN 3
	END,
    r.requestID
"""

ORDER_BY_REQUEST_STATUS = """
ORDER BY 
    CASE r.requestStatus
      WHEN 'Submitted' THEN 1
      WHEN 'In progress' THEN 2
      WHEN 'Submitted and Waiting for payment' THEN 3
	  WHEN 'Approved' THEN 4
      WHEN 'Completed' THEN 5
      WHEN 'Cancelled' THEN 6
	END,
    r.requestID
"""


class Request_Table(ScrollableFrame):
    def __init__(self, curr_view, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # data = [
        #     # Nr. Name  Active
        #     [1,   "ST", True],
        #     [2,   "SO", False],
        #     [3,   "SX", True],
        #     ]

        global request_view

        view_mapping = {
            "All": "WHERE r.requestID IS NOT NULL",
            "Pending Approval": "WHERE r.requestStatus in ('In Progress', 'Submitted')"
        }

        self.data = pd.read_sql_query(f"""
                SELECT r.requestID, c.customerID, p.model, r.requestDetails, r.requestStatus
                FROM Requests r 
                LEFT JOIN Services s USING(requestID)
                LEFT JOIN Payments c USING (itemID)
                LEFT JOIN Items i USING(itemID)
                LEFT JOIN Products p ON i.productID = p.productID
                {view_mapping.get(curr_view)}
                {ORDER_BY_REQUEST_STATUS}
                ;
                """, db)


        # self.vscrollbar = AutoScrollbar(self)
        # self.vscrollbar.grid(row=0, column=1, sticky=N+S)

        # self.canvas = Canvas(self, yscrollcommand=self.vscrollbar.set)
        # self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        # self.vscrollbar.config(command=self.canvas.yview)

        # # make the canvas expandable
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # self.frame = Frame(self.canvas)
        # self.frame.rowconfigure(1, weight=1)
        # self.frame.columnconfigure(1, weight=1)

        # self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # self.canvas.create_window(0, 0, anchor=NW, window=self.frame)
        # self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # self.grid_columnconfigure(1, weight=1)
        tk.Label(self.frame, text="Request ID", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="Name", anchor="w").grid(
            row=0, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(
            row=0, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Issue", anchor="w").grid(
            row=0, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Request Status", anchor="w").grid(
            row=0, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Action", anchor="w").grid(
            row=0, column=5, sticky="ew", padx=10)

        row = 1

        bg = ["#ffffff", "#d9e1f2"]

        highlight = {
            "Red": "#f8696b",
            "Green": "#63be7b",
            "Yellow": "#ffeb84"
        }

        for request in self.data.itertuples():
            requestId = int(request.requestID)
            name = str(request.customerID)
            model = str(request.model)
            issue = str(request.requestDetails)
            requestStatus = str(request.requestStatus)
            
            requestId_label = tk.Label(self.frame, text=str(
                requestId), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            name_label = tk.Label(self.frame, text=str(
                name), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(
                model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            issue_label = tk.Label(self.frame, text=str(
                issue), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            requestStatus_label = tk.Label(self.frame, text=str(
                requestStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            # active_cb = tk.Checkbutton(self.frame, onvalue=True, offvalue=False)
            # active = True
            # if active:
            #     active_cb.select()
            # else:
            #     active_cb.deselect()

            requestId_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            name_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid_columnconfigure(0, weight=5)
            requestStatus_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            requestStatus_label.grid_columnconfigure(0, weight=5, )
            # active_cb.grid(row=row, column=4, sticky="ew")

            if requestStatus in ["In progress", "Submitted"]:
                action_button = tk.Button(
                    self.frame, text="Approve", command=lambda requestId = requestId: self.master.show_approval_details(requestId))
                action_button.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            else:
                action_button = tk.Button(
                    self.frame, text="View", command=lambda requestId = requestId: self.master.show_request_details(requestId))
                action_button.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)

            # elif requestStatus == "Approved":
                # action_button = tk.Button(
                #     self.frame, text="Service", command=lambda requestId=requestId: self.service(requestId))
                # action_button.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)

            row += 1
        
        self.launch()
        
    #     self.canvas.create_window(0, 0, anchor=NW, window=self.frame)
    #     self.frame.update_idletasks()
    #     self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # def _on_mousewheel(self, event):
    #     if platform == "darwin":
    #         self.canvas.yview_scroll(-event.delta, "units")        
    #     elif platform == "win32":
    #         self.canvas.yview_scroll(-1 * (event.delta/120), "units") 



class Service_Table(ScrollableFrame):
    def __init__(self, curr_view, adminId, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.data = data

        view_mapping = {
            "All": "AND r.requestID IS NOT NULL",
            "Pending Service": "AND s.serviceStatus in ('In Progress')",
            "My Service Jobs": f"AND r.administratorID = \"{str(adminId)}\""
        }

        self.data = pd.read_sql_query(f"""
        SELECT r.requestID, c.customerID, p.model, r.requestDetails, r.requestStatus, s.serviceStatus, r.administratorID
        FROM Requests r 
        LEFT JOIN Services s USING(requestID)
        LEFT JOIN Payments c USING (itemID)
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN Products p ON i.productID = p.productID
        WHERE s.serviceStatus IS NOT NULL {view_mapping.get(curr_view)}
        {ORDER_BY_SERVICE_STATUS}
        ;
        """, db)

        tk.Label(self.frame, text="Service ID", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="Name", anchor="w").grid(
            row=0, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(
            row=0, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Issue", anchor="w").grid(
            row=0, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Request Status", anchor="w").grid(
            row=0, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Service Status", anchor="w").grid(
            row=0, column=5, sticky="ew", padx=10)
        tk.Label(self.frame, text="Admin In-charge", anchor="w").grid(
            row=0, column=6, sticky="ew", padx=10)
        tk.Label(self.frame, text="Action", anchor="w").grid(
            row=0, column=7, sticky="ew", padx=10)

        row = 1

        bg = ["#ffffff", "#d9e1f2"]

        for request in self.data.itertuples():

            serviceId = request.requestID
            name = request.customerID
            model = request.model
            issue = request.requestDetails
            if len(issue) > 25:
                issue = issue[:22]
                issue += "..." 

            requestStatus = request.requestStatus
            serviceStatus = request.serviceStatus
            request_admin = request.administratorID

            list_of_data = [name, request_admin]
            for item in list_of_data:
                if len(item) > 18:
                    item = item[:15]
                    item += "..." 

            serviceId_label = tk.Label(self.frame, text=str(
                serviceId), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            name_label = tk.Label(self.frame, text=str(
                name), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(
                model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            issue_label = tk.Label(self.frame, text=str(
                issue), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            requestStatus_label = tk.Label(self.frame, text=str(
                requestStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            serviceStatus_label = tk.Label(self.frame, text=str(
                serviceStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            adminId_label = tk.Label(self.frame, text=str(
            request_admin), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            # active_cb = tk.Checkbutton(self.frame, onvalue=True, offvalue=False)
            # active = True
            # if active:
            #     active_cb.select()
            # else:
            #     active_cb.deselect()

            serviceId_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            name_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid_columnconfigure(0, weight=5)
            requestStatus_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            serviceStatus_label.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            serviceStatus_label.grid_columnconfigure(0, weight=5)
            adminId_label.grid(row=row, column=6, sticky="ew", pady=2.5, ipady=5)
            # active_cb.grid(row=row, column=4, sticky="ew")

            # if serviceStatus == "In progress":
            #     action_button = tk.Button(
            #         self.frame, text="View", command=lambda serviceId=serviceId: self.view(serviceId))
            #     action_button.grid(row=row, column=6, sticky="ew", pady=2.5, ipady=5)

            if request_admin == self.master.adminId and serviceStatus == "In progress":
                action_button = tk.Button(
                    self.frame, text="Edit", command=lambda serviceId=serviceId: self.view(serviceId))
                action_button.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)
            elif serviceStatus == "Completed":
                action_button = tk.Button(
                    self.frame, text="View", command=lambda serviceId=serviceId: self.view_completed(serviceId))
                action_button.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)
            else:
                action_button = tk.Button(
                    self.frame, text="View", command=lambda serviceId=serviceId: self.view(serviceId))
                action_button.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)

            row += 1
        
        self.launch()
        
    def view(self, serviceId):
        # print("Show service page for ", serviceId)
        self.master.show_service_details(serviceId)

    def view_completed(self, serviceId):
        # print("Show completed service page for ", serviceId)
        self.master.show_completed_service_details(serviceId)



class Service_Info_Page(Frame):
    def __init__(self, curr_requestId, adminId, master):
        Frame.__init__(self, master)
        self.master = master

        # data = list(filter(lambda row: row[0] == curr_serviceId, service))[0]
        # print(data)

        data = pd.read_sql_query(f"""
        SELECT r.requestID, c.customerID, c.email, c.phoneNumber, c.address, p.model, 
        r.requestDetails, r.requestStatus, s.serviceStatus, r.administratorID
        FROM Requests r 
        LEFT JOIN Services s USING(requestID)
        LEFT JOIN Payments pay USING (itemID)
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN Products p ON i.productID = p.productID
        LEFT JOIN Customers c ON pay.customerID = c.customerID
        WHERE r.requestID = {curr_requestId}
        ;
        """, db)

        (requestId, curr_name, curr_email, curr_phone, curr_address,
        curr_model, curr_requestDetails, curr_requestStatus, curr_serviceStatus, curr_adminId) = list(data.to_records(index=False))[0]
        

        # Creatinag Text Boxes

        f_name = Label(self, padx= 5, width = 30, text=curr_name, borderwidth=2, relief="groove", justify="left", anchor="w")
        f_name.grid(row=0, column=1, padx=20, pady=(10, 2.5), ipady=5)

        email = Label(self, padx= 5,width = 30, text=curr_email, borderwidth=2, relief="groove", justify="left", anchor="w")
        email.grid(row=3, column=1, padx=20, pady=2.5, ipady=5)

        phone = Label(self, padx= 5,width = 30, text=curr_phone, borderwidth=2, relief="groove", justify="left", anchor="w")
        phone.grid(row=4, column=1, padx=20, pady=2.5, ipady=5)

        address = Label(self, padx= 5,width = 30, text=curr_address, borderwidth=2, relief="groove", justify="left", anchor="w")
        address.grid(row=5, column=1, padx=20, pady=2.5, ipady=5)

        model = Label(self, padx= 5, width = 30, text=curr_model, borderwidth=2, relief="groove", justify="left", anchor="w")
        model.grid(row=6, column=1, padx=20, pady=2.5, ipady=5)

        request_details = Label(self, padx= 5, width = 30, text=curr_requestDetails, borderwidth=2, relief="groove", justify="left", anchor="w")
        request_details.grid(row=7, column=1, padx=20, pady=2.5, ipady=5)

        requestStatus = Label(self, padx= 5, width=30, justify="center", text=curr_requestStatus, borderwidth=2, relief="groove")
        requestStatus.grid(row=8, column=1, padx=20, pady=2.5, ipady=5)

        serviceStatus = Label(self, padx= 5,width=30, justify="center", text=curr_serviceStatus, borderwidth=2, relief="groove")
        serviceStatus.grid(row=9, column=1, padx=20, pady=2.5, ipady=5)

        curr_adminId_serving = Label(self, padx= 5, width=30, justify="center", text=curr_adminId, borderwidth=2, relief="groove")
        curr_adminId_serving.grid(row=10, column=1, padx=20, pady=2.5, ipady=5)


        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 2.5), ipady=5)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0, pady=2.5, ipady=5)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0, pady=2.5, ipady=5)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0, pady=2.5, ipady=5)

        model_label = Label(self, text="Model")
        model_label.grid(row=6, column=0, pady=2.5, ipady=5)

        request_details_label = Label(self, text="Issue")
        request_details_label.grid(row=7, column=0, pady=2.5, ipady=5)

        requestStatus_label = Label(self, text="Request Status")
        requestStatus_label.grid(row=8, column=0, pady=2.5, ipady=5)

        serviceStatus_label = Label(self, text="Service Status")
        serviceStatus_label.grid(row=9, column=0, pady=2.5, ipady=5)

        curr_admin_label = Label(self, text="Admin In-charge")
        curr_admin_label.grid(row=10, column=0, pady=2.5, ipady=5)

        back_btn = Button(self, text="Back", command=lambda: master.back_to_service())
        back_btn.grid(row=11, column=0, padx=(10,0), sticky="W", pady=15)


        if curr_adminId == adminId:
            complete_btn = Button(self, text="Complete Service", command=lambda requestId = requestId: master.complete_service(requestId))
            complete_btn.grid(row=11, column=1, padx=(0, 15), sticky="E", pady=15)


class Approval_Info_Page(Frame):
    def __init__(self, curr_requestId, master):
        Frame.__init__(self, master)
        self.master = master

        print(curr_requestId)

        # data = list(filter(lambda row: row[0] == curr_serviceId, service))[0]
        # print(data)

        data = pd.read_sql_query(f"""
        SELECT r.requestID, c.customerID, c.email, c.phoneNumber, c.address, p.model, r.requestDetails, r.requestStatus
        FROM Requests r 
        LEFT JOIN Services s USING(requestID)
        LEFT JOIN Payments pay USING (itemID)
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN Products p ON i.productID = p.productID
        LEFT JOIN Customers c ON pay.customerID = c.customerID
        WHERE r.requestID = {curr_requestId}
        ;
        """, db)


        (requestId, curr_name, curr_email, curr_phone, curr_address,
        curr_model, curr_requestDetails, curr_requestStatus) = list(data.to_records(index=False))[0]
        
        # Creatinag Text Boxes
        f_name = Label(self, padx= 5, width = 30, text=curr_name, borderwidth=2, relief="groove", justify="left", anchor="w")
        f_name.grid(row=0, column=1, padx=20, pady=(10, 2.5), ipady=5)


        email = Label(self, padx= 5, width = 30, text=curr_email, borderwidth=2, relief="groove", justify="left", anchor="w")
        email.grid(row=3, column=1, padx=20, pady=2.5, ipady=5)
  

        phone = Label(self, padx= 5, width = 30, text=curr_phone, borderwidth=2, relief="groove", justify="left", anchor="w")
        phone.grid(row=4, column=1, padx=20, pady=2.5, ipady=5)
 

        address = Label(self, padx= 5, width = 30, text=curr_address, borderwidth=2, relief="groove", justify="left", anchor="w")
        address.grid(row=5, column=1, padx=20, pady=2.5, ipady=5)


        model = Label(self, padx= 5, width = 30, text=curr_model, borderwidth=2, relief="groove", justify="left", anchor="w")
        model.grid(row=6, column=1, padx=20, pady=2.5, ipady=5)

        REQUEST_STATUS = [
            "In progress",
            "Submitted"
        ]

        requestDetails = Label(self, padx= 5, width=30, justify="center", text=curr_requestDetails, borderwidth=2, relief="groove")
        requestDetails.grid(row=7, column=1, padx=20, pady=2.5, ipady=5)


        requestStatus = Label(self, padx= 5, width=30, justify="center", text=curr_requestStatus, borderwidth=2, relief="groove")
        requestStatus.grid(row=8, column=1, padx=20, pady=2.5, ipady=5)

        

        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 2.5), ipady=5)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0, pady=2.5, ipady=5)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0, pady=2.5, ipady=5)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0, pady=2.5, ipady=5)

        model_label = Label(self, text="Model")
        model_label.grid(row=6, column=0, pady=2.5, ipady=5)

        requestDetails_label = Label(self, text="Issue")
        requestDetails_label.grid(row=7, column=0, pady=2.5, ipady=5)

        requestStatus_label = Label(self, text="Request Status")
        requestStatus_label.grid(row=8, column=0, pady=2.5, ipady=5)

        back_btn = Button(self, text="Back", command=lambda: master.back_to_request())
        back_btn.grid(row=9, column=0, padx=(10,0), sticky="W", pady=15)
        
        
        complete_btn = Button(self, text="Approve", command=lambda requestId = requestId: master.approve_request(requestId))
        complete_btn.grid(row=9, column=1, padx=(0, 15), sticky="E", pady=15)

    
class Request_Info_Page(Frame):
    def __init__(self, curr_requestId, master):
        Frame.__init__(self, master)
        self.master = master

        # data = list(filter(lambda row: row[0] == curr_serviceId, service))[0]
        # print(data)

        data = pd.read_sql_query(f"""
        SELECT r.requestID, c.customerID, c.email, c.phoneNumber, c.address, p.model, r.requestDetails, r.requestStatus
        FROM Requests r 
        LEFT JOIN Services s USING(requestID)
        LEFT JOIN Payments pay USING (itemID)
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN Products p ON i.productID = p.productID
        LEFT JOIN Customers c ON pay.customerID = c.customerID
        WHERE r.requestID = {curr_requestId}
        ;
        """, db)


        (requestId, curr_name, curr_email, curr_phone, curr_address,
        curr_model, curr_requestDetails, curr_requestStatus) = list(data.to_records(index=False))[0]
        
        f_name = Label(self, padx= 5,width = 30, text=curr_name, borderwidth=2, relief="groove", justify="left", anchor="w")
        f_name.grid(row=0, column=1, padx=20, pady=(10,2.5), ipady=5)
        # f_name.insert(0, curr_name)
        # f_name.configure(state="disabled")

        email = Label(self, padx= 5,width = 30, text=curr_email, borderwidth=2, relief="groove", justify="left", anchor="w")
        email.grid(row=3, column=1, padx=20, pady=2.5, ipady=5)
        # email.insert(0, curr_email)
        # email.configure(state="disabled")

        phone = Label(self, padx= 5,width = 30, text=curr_phone, borderwidth=2, relief="groove", justify="left", anchor="w")
        phone.grid(row=4, column=1, padx=20, pady=2.5, ipady=5)
        # phone.insert(0, curr_phone)
        # phone.configure(state="disabled")

        address = Label(self, padx= 5,width = 30, text=curr_address, borderwidth=2, relief="groove", justify="left", anchor="w")
        address.grid(row=5, column=1, padx=20, pady=2.5, ipady=5)
        # address.insert(0, curr_address)
        # address.configure(state="disabled")

        model = Label(self, padx= 5,width = 30, text=curr_model, borderwidth=2, relief="groove", justify="left", anchor="w")
        model.grid(row=6, column=1, padx=20, pady=2.5, ipady=5)
        # model.insert(0, curr_model)
        # model.configure(state="disabled")

        requestDetails = Label(self, padx= 5,width = 30, text=curr_requestDetails, borderwidth=2, relief="groove", justify="left", anchor="w")
        requestDetails.grid(row=7, column=1, padx=20, pady=2.5, ipady=5)

        requestStatus = Label(self, padx= 5, width=30, justify="center", text=curr_requestStatus, borderwidth=2, relief="groove")
        requestStatus.grid(row=8, column=1, padx=20, pady=2.5, ipady=5)
        # requestStatus.insert(0, curr_requestStatus)
        # requestStatus.configure(state="disabled") 

        

        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 2.5), ipady=5)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0, pady=2.5, ipady=5)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0, pady=2.5, ipady=5)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0, pady=2.5, ipady=5)

        model_label = Label(self, text="Model")
        model_label.grid(row=6, column=0, pady=2.5, ipady=5)

        requestDetails_label = Label(self, text="Issue")
        requestDetails_label.grid(row=7, column=0, pady=2.5, ipady=5)

        requestStatus_label = Label(self, text="Request Status")
        requestStatus_label.grid(row=8, column=0, pady=2.5, ipady=5)

        back_btn = Button(self, text="Back", command=lambda: master.back_to_request())
        back_btn.grid(row=9, column=0, padx=(10,0), sticky="W", pady=15)
        


class Completed_Service_Info_Page(Frame):
    def __init__(self, curr_requestId, master):
        Frame.__init__(self, master)
        self.master = master

        # data = list(filter(lambda row: row[0] == curr_serviceId, service))[0]
        # print(data)

        data = pd.read_sql_query(f"""
        SELECT r.requestID, c.customerID, c.email, c.phoneNumber, c.address, p.model, 
        r.requestDetails, r.requestStatus, s.serviceStatus, r.administratorID
        FROM Requests r 
        LEFT JOIN Services s USING(requestID)
        LEFT JOIN Payments pay USING (itemID)
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN Products p ON i.productID = p.productID
        LEFT JOIN Customers c ON pay.customerID = c.customerID
        WHERE r.requestID = {curr_requestId}
        ;
        """, db)

        (requestId, curr_name, curr_email, curr_phone, curr_address,
        curr_model, curr_requestDetails, curr_requestStatus, curr_serviceStatus, curr_admin) = list(data.to_records(index=False))[0]
        

        # Creatinag Text Boxes
        f_name = Label(self, padx= 5, width = 30, text=curr_name, borderwidth=2, relief="groove", justify="left", anchor="w")
        f_name.grid(row=0, column=1, padx=20, pady=(10, 2.5), ipady=5)
        # f_name.insert(0, curr_name)
        # f_name.configure(state="disabled")

        email = Label(self, padx= 5,width = 30, text=curr_email, borderwidth=2, relief="groove", justify="left", anchor="w")
        email.grid(row=3, column=1, padx=20, pady=2.5, ipady=5)
        # email.insert(0, curr_email)
        # email.configure(state="disabled")

        phone = Label(self, padx= 5,width = 30, text=curr_phone, borderwidth=2, relief="groove", justify="left", anchor="w")
        phone.grid(row=4, column=1, padx=20, pady=2.5, ipady=5)
        # phone.insert(0, curr_phone)
        # phone.configure(state="disabled")

        address = Label(self, padx= 5,width = 30, text=curr_address, borderwidth=2, relief="groove", justify="left", anchor="w")
        address.grid(row=5, column=1, padx=20, pady=2.5, ipady=5)
        # address.insert(0, curr_address)
        # address.configure(state="disabled")

        model = Label(self, padx= 5, width = 30, text=curr_model, borderwidth=2, relief="groove", justify="left", anchor="w")
        model.grid(row=6, column=1, padx=20, pady=2.5, ipady=5)
        # model.insert(0, curr_model)
        # model.configure(state="disabled")

        requestDetails = Label(self, padx= 5, width = 30, text=curr_requestDetails, borderwidth=2, relief="groove", justify="left", anchor="w")
        requestDetails.grid(row=7, column=1, padx=20, pady=2.5, ipady=5)

        requestStatus = Label(self, padx= 5, width=30, justify="center", text=curr_requestStatus, borderwidth=2, relief="groove")
        requestStatus.grid(row=8, column=1, padx=20, pady=2.5, ipady=5)
        # requestStatus.insert(0, curr_requestStatus)
        # requestStatus.configure(state="disabled") 

        serviceStatus = Label(self, padx= 5, width=30, justify="center", text=curr_serviceStatus, borderwidth=2, relief="groove")
        serviceStatus.grid(row=9, column=1, padx=20, pady=2.5, ipady=5)
        # serviceStatus.insert(0, curr_serviceStatus)
        # serviceStatus.configure(state="disabled") 

        request_admin = Label(self, padx= 5, width=30, justify="center", text=curr_admin, borderwidth=2, relief="groove")
        request_admin.grid(row=10, column=1, padx=20, pady=2.5, ipady=5)



        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 2.5), ipady=5)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0, pady=2.5, ipady=5)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0, pady=2.5, ipady=5)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0, pady=2.5, ipady=5)

        model_label = Label(self, text="Model")
        model_label.grid(row=6, column=0, pady=2.5, ipady=5)

        requestDetails_label = Label(self, text="Issue")
        requestDetails_label.grid(row=7, column=0, pady=2.5, ipady=5)

        requestStatus_label = Label(self, text="Request Status")
        requestStatus_label.grid(row=8, column=0, pady=2.5, ipady=5)

        serviceStatus_label = Label(self, text="Service Status")
        serviceStatus_label.grid(row=9, column=0, pady=2.5, ipady=5)

        request_admin_label = Label(self, text="Admin In-charge")
        request_admin_label.grid(row=10, column=0, pady=2.5, ipady=5)

        back_btn = Button(self, text="Back", command=lambda: master.back_to_service())
        back_btn.grid(row=11, column=0, padx=(10,0), sticky="W", pady=15)





class Admin_Request_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        tab1 = tk.Button(self, text="All Request",
                         command=lambda: master.show_request("All"))
        tab1.grid(row=0, column=0, padx=(10, 5))

        tab2 = tk.Button(self, text="Pending Approval",
                         command=lambda: master.show_request("Pending Approval"))
        # tab2.pack(side="left", fill="both")
        tab2.grid(row=0, column=1, padx=5)

        tab3 = tk.Button(self, text="Pending Service",
                         command=lambda: master.show_service("Pending Service"))
        tab3.grid(row=0, column=2, padx=5)

        tab4 = tk.Button(self, text="My Service Jobs",
                         command=lambda: master.show_service("My Service Jobs"))
        tab4.grid(row=0, column=3, padx=5)

        tab5 = tk.Button(self, text="All Service Jobs",
                         command=lambda: master.show_service("All"))
        tab5.grid(row=0, column=4, padx=5)


class Admin_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.adminId = master.adminId

        self.header = Admin_Request_Page_Header(
            self, borderwidth=0, highlightthickness=0, pady=10)

        self.table = Request_Table("All", self)

        self.header.pack(side="top", fill="x", expand=False)
        self.table.pack(side="top", fill="both", expand=True)

        self.request_filter = {
            "All": lambda row: row,
            "Pending Approval": lambda row: row[4] == "In progress",
            "Pending Service": lambda row: row[4] == "Approved"
        }

        # self.adminId = "EddMing321"


    def show_header():
        self.header = Admin_Request_Page_Header(
            self, borderwidth=0, highlightthickness=0, pady=10)
        self.header.pack(side="top", fill="x", expand=False)

    def show_request(self, curr_view):

        self.table.destroy()

        global request_view
        request_view = curr_view

        self.table = Request_Table(curr_view, self)
        self.table.pack(side="top", fill="both", expand=True)
    
    def back_to_request(self):

        self.table.destroy()

        global request_view

        self.table = Request_Table(request_view, self)
        self.table.pack(side="top", fill="both", expand=True)


    def show_service(self, curr_view):

        self.table.destroy()

        global service_view
        service_view = curr_view

        self.table = Service_Table(curr_view, self.adminId, self)
        self.table.pack(side="top", fill="both", expand=True)
    
    def back_to_service(self):

        self.table.destroy()

        global service_view

        self.table = Service_Table(service_view, self.adminId, self)
        self.table.pack(side="top", fill="both", expand=True)

    
    def show_service_details(self, serviceId):
        self.table.destroy()
        
        self.table = Service_Info_Page(serviceId, self.adminId, self)
        self.table.pack(side="top", fill="both", expand=True)

    def show_approval_details(self, requestId):
        self.table.destroy()
        self.table = Approval_Info_Page(requestId, self)
        self.table.pack(side="top", fill="both", expand=True)

    
    def show_request_details(self, requestId):
        self.table.destroy()
        self.table = Request_Info_Page(requestId, self)
        self.table.pack(side="top", fill="both", expand=True)


    
    def show_completed_service_details(self, serviceId):
        self.table.destroy()
        
        self.table = Completed_Service_Info_Page(serviceId, self)
        self.table.pack(side="top", fill="both", expand=True)


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

    def approve_request(self, requestId):
        # print(requestId)
        # print(self.adminId)

        status = False

        # Approve request in database
        with db.begin() as conn:
            savepoint = conn.begin_nested()
            try:
                # Create a service for the request        
                conn.execute(f"""
                INSERT INTO Services(requestID, serviceStatus)VALUES
                ({requestId}, "In Progress")
                ;
                """)

                # Update the request status
                conn.execute(f"""
                UPDATE Requests
                SET requestStatus = "Approved",
                administratorID = "{self.adminId}"
                WHERE requestID = {requestId}
                ;
                """)
                
                # Commit changes to database
                savepoint.commit()

                # Update the progress status
                status = True
            except:
                # If fail, rollback the changes
                savepoint.rollback()
                print("Failed to approve request")
        
        if status:
            self.show_service("My Service Jobs")


        
    
    def complete_service(self, requestId):
        # print("Service completed for ", requestId)
        status = False

        # Approve request in database
        with db.begin() as conn:
            savepoint = conn.begin_nested()
            try:
                # Create a service for the request        
                conn.execute(f"""
                UPDATE Services
                SET serviceStatus = "Completed"
                WHERE requestID = {requestId}
                ;
                """)

                # Update the request status
                conn.execute(f"""
                UPDATE Requests
                SET requestStatus = "Completed"
                WHERE requestID = {requestId}
                ;
                """)
                
                # Commit changes to database
                savepoint.commit()

                # Update the progress status
                status = True
            except:
                # If fail, rollback the changes
                savepoint.rollback()
                print("Failed to complete service")
        
        if status:
            self.show_service("My Service Jobs")        



if __name__ == "__main__":
    main()
