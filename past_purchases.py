# data = [
#     ("1001", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted"), 
#     ("1003", "Lights", "Yellow", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted and Waiting for payment"), 
#     ("1004", "Lights", "Green", "Malaysia", "Battery", "Sold", "2014", "Light1", "In progress"), 
#     ("1005", "Lights", "Black", "Malaysia", "Battery", "Sold", "2014", "Light1", "Approved"), 
#     ("1006", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Canceled"), 
#     ("1007", "Lights", "Blue", "Malaysia", "Battery", "Sold", "2014", "Light1", "Completed"),
#     ("1008", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted"), 
#     ("1009", "Lights", "Yellow", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted and Waiting for payment"), 
#     ("1010", "Lights", "Green", "Malaysia", "Battery", "Sold", "2014", "Light1", "In progress"), 
#     ("1011", "Lights", "Black", "Malaysia", "Battery", "Sold", "2014", "Light1", "Approved"), 
#     ("1012", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Canceled"), 
#     ("1013", "Lights", "Blue", "Malaysia", "Battery", "Sold", "2014", "Light1", "Completed"),
#     ("1008", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted"), 
#     ("1009", "Lights", "Yellow", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted and Waiting for payment"), 
#     ("1010", "Lights", "Green", "Malaysia", "Battery", "Sold", "2014", "Light1", "In progress"), 
#     ("1011", "Lights", "Black", "Malaysia", "Battery", "Sold", "2014", "Light1", "Approved"), 
#     ("1012", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Canceled"), 
#     ("1013", "Lights", "Blue", "Malaysia", "Battery", "Sold", "2014", "Light1", "Completed")
#     ]

from datetime import datetime
from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3
from datetime import date

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

# table of items only
class Past_Purchases_Table(ScrollableFrame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(width=800, height=800, *args, **kwargs)

        # unknown column error to fix 
        customerId = str(self.master.master.customerId)

        self.data = pd.read_sql_query(f"""
        select i.itemID, p.model, i.colour, i.powerSupply, i.productionYear, i.factory, r.requestStatus, p.warrantyMonths, r.requestID
        from items i 
        inner join products p on i.productID = p.productID
        left join requests r on i.itemID = r.itemID
        where i.itemID in (select itemID from payments where customerID = "JohnSmith123")
        limit 100
        ;
        """, db)

        # labels 
        tk.Label(self.frame, text="Product", anchor="w").grid(row=1, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(row=1, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Colour", anchor="w").grid(row=1, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Power Supply", anchor="w").grid(row=1, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Production Year", anchor="w").grid(row=1, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Factory", anchor="w").grid(row=1, column=5, sticky="ew", padx=10)
        tk.Label(self.frame, text="Request Status", anchor="w").grid(row=1, column=6, sticky="ew", padx=10)

        row = 2

        bg = ["#ffffff", "#d9e1f2"]
            

        # populating the table row by row
        for entry in data.itertuples():

            category = entry.itemID
            model = entry.model
            colour = entry.colour
            powerSupply = entry.powerSupply
            productionYear = entry.productionYear
            factory = entry.factory

            if entry.requestStatus == None:
                requestStatus = 'No request made'
            else:
                allRequests = pd.read_sql_query(f"""
                select * from ServiceFees
                where requestID = {entry.requestID}
                ;
                """, db)

                try: 
                    time_diff = date.today() - allRequests['creationDate'][0]

                    if time_diff.days > 10 :  

                        requestStatus = "Cancelled"
                        
                        with db.begin() as conn:
                            try:
                                savepoint = conn.begin_nested()
                                conn.execute(f"""
                                UPDATE Requests
                                SET requestStatus = "Cancelled"
                                WHERE requestID = {entry.requestID}
                                ;
                                """)
                                savepoint.commit()
                            except:
                                savepoint.rollback()

                    else:
                        requestStatus = entry.requestStatus
                except: 
                    requestStatus = entry.requestStatus 

            product_label = tk.Label(self.frame, text=str(category), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            colour_label = tk.Label(self.frame, text=str(colour), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            powerSupply_label = tk.Label(self.frame, text=str(powerSupply), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            productionYear_label = tk.Label(self.frame, text=str(productionYear), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            factory_label = tk.Label(self.frame, text=str(factory), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])   
            requestStatus_label = tk.Label(self.frame, text=str(requestStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            
            product_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            colour_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            powerSupply_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            productionYear_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            factory_label.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            requestStatus_label.grid(row=row, column=6, sticky="ew", pady=2.5, ipady=5)    

            # different button according to what is the request status 
            if requestStatus in ['Completed', 'Cancelled', 'No request made']:
                requestButton = tk.Button(self.frame, text="Make new request")  
                # command=lambda requestId = requestId: self.master.show_approval_details(requestId)
            else:
                requestButton = tk.Button(self.frame, text="Request details")  
            requestButton.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)

            row += 1
        
        self.launch()
        
# header only 
class Past_Purchase_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        global clicked
        clicked = tk.StringVar()
        clicked.set("None")

        # dropdown filter
        OptionMenu(self, clicked, "Submitted", "Approved", "Submitted and Waiting for payment", "In progress", "Cancelled", "Completed", "No request made", "No filter", 
        command=lambda clicked = clicked: master.filter_status(clicked)).grid(row=0, column=6, sticky="ew", padx=10)

# main frame consisting of table and header 
class Past_Purchase_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.header = Past_Purchase_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)

        customerId = str(self.master.customerId)
        self.data = pd.read_sql_query(f"""
        select i.itemID, p.model, i.colour, i.powerSupply, i.productionYear, i.factory, r.requestStatus, p.warrantyMonths, r.requestID
        from items i 
        inner join products p on i.productID = p.productID
        left join requests r on i.itemID = r.itemID
        where i.itemID in (select itemID from payments where customerID = "JohnSmith123")
        limit 100
        ;
        """, db)


        self.table = Past_Purchases_Table(self.data, self)
        self.header.pack(side="top", fill="x", expand=False)
        self.table.pack(side="top", fill="both", expand=True)



    def show_header():
        header = Past_Purchase_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        header.pack(side="top", fill="x", expand=False)

    # filtering is performed here 
    def filter_status(self, curr_view):
        
        self.table.destroy()

        customerId = str(self.master.master.customerId)
        self.data = pd.read_sql_query(f"""
        select i.itemID, p.model, i.colour, i.powerSupply, i.productionYear, i.factory, r.requestStatus, p.warrantyMonths, r.requestID
        from items i 
        inner join products p on i.productID = p.productID
        left join requests r on i.itemID = r.itemID
        where i.itemID in (select itemID from payments where customerID = "JohnSmith123")
        limit 100
        ;
        """, db)
        curr_data = self.data.copy()

        if clicked.get() == 'No request made':
            curr_data = curr_data[curr_data['requestStatus'].isnull()]
        
        elif clicked.get() == 'No filter':
            curr_data = curr_data

        else:
            curr_data = curr_data[curr_data['requestStatus'] == clicked.get()]

        self.table = Past_Purchases_Table(curr_data, self)
        self.table.pack(side="top", fill="both", expand=True)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    class App(Tk):
        def __init__(self):
            Tk.__init__(self)
            self._frame = None
            self.switch_frame(Past_Purchase_Page)

        def switch_frame(self, frame_class):
            new_frame = frame_class(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack(side="top", fill="both", expand=True)

    def main():

        app = App()
        app.geometry("1200x800")
        app.mainloop()
    main()
