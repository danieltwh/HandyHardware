from datetime import *
from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3
from dateutil.relativedelta import relativedelta

from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import math

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
class Request_Table(ScrollableFrame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(width=800, height=800, *args, **kwargs)


        customerId = str(self.master.master.customerId)

        self.data = pd.read_sql_query(f"""
            select i.itemID, p.model, i.colour, i.powerSupply, i.productionYear,
            i.factory, r.requestStatus, p.warrantyMonths, r.requestID, pay.paymentID,
            r.requestDetails, r.requestID
            FROM Requests r 
            LEFT JOIN Payments pay USING (itemID)
            LEFT JOIN Items i USING(itemID)
            LEFT JOIN Products p ON i.productID = p.productID
            WHERE r.itemID IN (SELECT itemID FROM Payments WHERE customerID = "{customerId}") 
            limit 100;
        """, db)


        # labels 
        tk.Label(self.frame, text="RequestID", anchor="w").grid(row=1, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="ItemID", anchor="w").grid(row=1, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(row=1, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Colour", anchor="w").grid(row=1, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Power Supply", anchor="w").grid(row=1, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Production Year", anchor="w").grid(row=1, column=5, sticky="ew", padx=10)
        tk.Label(self.frame, text="Factory", anchor="w").grid(row=1, column=6, sticky="ew", padx=10)
        tk.Label(self.frame, text="Request Status", anchor="w").grid(row=1, column=7, sticky="ew", padx=10)
        tk.Label(self.frame, text="Request Details", anchor="w").grid(row=1, column=8, sticky="ew", padx=10)

        row = 2

        bg = ["#ffffff", "#d9e1f2"]
            

        # populating the table row by row
        for entry in data.itertuples():
            
            # print(entry)
            requestId = entry.requestID
            itemId = entry.itemID
            model = entry.model
            colour = entry.colour
            powerSupply = entry.powerSupply
            productionYear = entry.productionYear
            factory = entry.factory
            requestDetails = entry.requestDetails

            if entry.requestStatus == None or math.isnan(entry.requestID):
                requestStatus = 'No request made'
            else:
                allRequests = pd.read_sql_query(f"""
                select * from ServiceFees
                where requestID = {entry.requestID}
                ;
                """, db)

                try: 
                    time_diff = date.today() - allRequests['creationDate'][0]

                    if time_diff.days > 10 and entry.requestStatus == 'Submitted and Waiting for payment':  

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

            requestId_label = tk.Label(self.frame, text=str(requestId), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            itemId_label = tk.Label(self.frame, text=str(itemId), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            colour_label = tk.Label(self.frame, text=str(colour), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            powerSupply_label = tk.Label(self.frame, text=str(powerSupply), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            productionYear_label = tk.Label(self.frame, text=str(productionYear), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            factory_label = tk.Label(self.frame, text=str(factory), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])   
            requestStatus_label = tk.Label(self.frame, text=str(requestStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            requestDetails_label = tk.Label(self.frame, text=str(requestDetails), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            requestId_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            itemId_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            colour_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            powerSupply_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            productionYear_label.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            factory_label.grid(row=row, column=6, sticky="ew", pady=2.5, ipady=5)
            requestStatus_label.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)    
            requestDetails_label.grid(row=row, column=8, sticky="ew", pady=2.5, ipady=5)

            # different button according to what is the request status 
            paymentID = entry.paymentID
            itemID = entry.itemID

            
            row += 1
        
        self.launch()
        
# header only 
class Request_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        global clicked
        clicked = tk.StringVar()
        clicked.set("None")

        # dropdown filter
        optionMenu = OptionMenu(self, clicked, 
        "Filter by: Submitted", 
        "Filter by: Submitted and Waiting for payment", 
        "Filter by: In progress", 
        "Filter by: Approved", 
        "Filter by: Cancelled", 
        "Filter by: Completed", 
        "Filter by: No request made", 
        "Filter by: No filter", 
        command=lambda clicked = clicked: master.filter_status(clicked))
        optionMenu.config(width=30)
        optionMenu.grid(row=0, column=6, sticky="ew", padx=10)

        #tk.Label(self.frame, text="Past Request Page", anchor="w").grid(row=0, column=2, sticky="ew", padx=20)
        title = tk.Label(self, text="Past Request Page", font=('Aerial 14 bold'))
        title.grid(row=0, column=8, pady =20)

# main frame consisting of table and header 
class Request_Table_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.header = Request_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)

        customerId = str(self.master.customerId)

        self.data = pd.read_sql_query(f"""
            select i.itemID, p.model, i.colour, i.powerSupply, i.productionYear,
            i.factory, r.requestStatus, p.warrantyMonths, r.requestID, pay.paymentID,
            r.requestDetails, r.requestID
            FROM Requests r 
            LEFT JOIN Payments pay USING (itemID)
            LEFT JOIN Items i USING(itemID)
            LEFT JOIN Products p ON i.productID = p.productID
            WHERE r.itemID IN (SELECT itemID FROM Payments WHERE customerID = "{customerId}") 
            limit 100;
        """, db)


        self.table = Request_Table(self.data, self)
        self.header.pack(side="top", fill="x", expand=False)
        self.table.pack(side="top", fill="both", expand=True)



    def show_header():
        header = Request_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        header.pack(side="top", fill="x", expand=False)

    # filtering is performed here 
    def filter_status(self, curr_view):
        
        self.table.destroy()

        customerId = str(self.master.customerId)

        self.data = pd.read_sql_query(f"""
            select i.itemID, p.model, i.colour, i.powerSupply, i.productionYear,
            i.factory, r.requestStatus, p.warrantyMonths, r.requestID, pay.paymentID,
            r.requestDetails, r.requestID
            FROM Requests r 
            LEFT JOIN Payments pay USING (itemID)
            LEFT JOIN Items i USING(itemID)
            LEFT JOIN Products p ON i.productID = p.productID
            WHERE r.itemID IN (SELECT itemID FROM Payments WHERE customerID = "{customerId}") 
            limit 100;
        """, db)

        curr_data = self.data.copy()

        
        if clicked.get() == 'Filter by: No request made':
            curr_data = curr_data[curr_data['requestStatus'].isnull()]
        
        elif clicked.get() == 'Filter by: No filter':
            curr_data = curr_data

        else:
            curr_data = curr_data[curr_data['requestStatus'] == clicked.get()[11:]]

        self.table = Request_Table(curr_data, self)
        self.table.pack(side="top", fill="both", expand=True)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)
        
