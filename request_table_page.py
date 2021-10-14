from datetime import *
from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3
from dateutil.relativedelta import relativedelta
import tkinter.font as tkFont

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
            ;
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

                                conn.execute(f"""
                                UPDATE services
                                SET serviceStatus = "Completed"
                                where requestID = {entry.requestID}
                                ;
                                """)
                                
                                savepoint.commit()
                            except:
                                savepoint.rollback()

                    else:
                        requestStatus = entry.requestStatus
                except: 
                    requestStatus = entry.requestStatus 
            
            if requestDetails and len(requestDetails) > 25:
                requestDetails = requestDetails[:22]
                requestDetails += "..."

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

            requestButton = tk.Button(self.frame, text="View Details", command = lambda requestId = requestId: self.master.master.id_switch_frame(requestId, Request_Details2))
            requestButton.grid(row=row, column=9, sticky="ew", pady=2.5, ipady=5)
            
            row += 1
        
        self.launch()
        
# header only 
class Request_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        global clicked
        clicked = tk.StringVar()
        clicked.set("Filter by: No filter")

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
        optionMenu.grid(row=1, column=0, sticky="ew", padx=10)

        title = tk.Label(self, text="Past Request Page", font=tkFont.Font(size=20), width = 20)
        title.grid(row=0, column=0, padx=(10, 5))

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
            ;
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
            ;
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

class Request_Details2(Frame):
    def __init__(self, curr_requestId, master):
        Frame.__init__(self, master)
        self.master = master


        data2 = pd.read_sql_query(f"""
        SELECT r.itemID, r.requestID, p.model,
        r.requestDetails, pay.purchaseDate, 
        sf.creationDate,sf.settlementDate,
        sf.amount, r.requestStatus
        FROM Requests r 
        LEFT JOIN Payments pay USING (itemID)
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN ServiceFees sf ON r.requestID = sf.requestID
        LEFT JOIN Products p ON i.productID = p.productID
        WHERE (r.requestId = {curr_requestId})
        ;
        """, db)

        (curr_itemId, curr_requestId, curr_model, curr_requestDetails,
        curr_purchaseDate, curr_creationDate, curr_settlementDate,
        curr_amount, curr_requestStatus) = list(data2.to_records(index=False))[0]

        title = Label(self, text="Request Details", font=('Helvetica 20 bold'))
        title.grid(row=0, column=1, pady =20)

        requestID = Label(self, text=str(curr_requestId))
        requestID.grid(row=1, column=1)
        requestID_label = Label(self, text="Request ID: ", font=('Helvetica 12 bold'))
        requestID_label.grid(row=1, column=0)

        itemID = Label(self, text=curr_itemId)
        itemID.grid(row=2, column=1)
        itemID_label = Label(self, text="Item ID: ", font=('Helvetica 12 bold'))
        itemID_label.grid(row=2, column=0)

        model_label = Label(self, text="Model: ", font=('Helvetica 12 bold'))
        model_label.grid(row=3, column=0)
        model = Label(self, text=curr_model)
        model.grid(row=3, column=1, padx=20)

        reqDate_label = Label(self, text="Request Date: ", font=('Helvetica 12 bold'))
        reqDate_label.grid(row=4, column=0)
        reqDate = Label(self, text=curr_creationDate)
        reqDate.grid(row=4, column=1, padx=20)

        if int(curr_amount) == 0:
            amount_label = Label(self, text="Payment Amount: ", font=('Helvetica 12 bold'))
            amount_label.grid(row=5, column=0)
            amount = Label(self, text="$" + "{:.2f}".format(curr_amount) + " (No Payment Required)")
            amount.grid(row=5, column=1, padx=20)
        else:
            amount_label = Label(self, text="Payment Amount: ", font=('Helvetica 12 bold'))
            amount_label.grid(row=5, column=0)
            amount = Label(self, text="$" + "{:.2f}".format(curr_amount))
            amount.grid(row=5, column=1, padx=20)

        reqStatus_label = Label(self, text="Request Status: ", font=('Helvetica 12 bold'))
        reqStatus_label.grid(row=6, column=0)
        reqStatus = Label(self, text=curr_requestStatus)
        reqStatus.grid(row=6, column=1, padx=20)

        issue_label = Label(self, text="Issue: ", font=('Helvetica 12 bold'))
        issue_label.grid(row=7, column=0)
        issue = Label(self, text=curr_requestDetails, wraplength=250, justify = 'left')
        issue.grid(row=7, column=1, padx=20)


        return_btn = Button(self, text="Return to Past Requests", command= lambda: self.master.switch_frame(Request_Table_Page)) # go to past payments
        return_btn.grid(row=9, column=0, pady = 15)

            
        
