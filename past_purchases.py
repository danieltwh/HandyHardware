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

db = create_engine(f"mysql+pymysql://{USERNAME}:{MYSQL_PASSWORD}@127.0.0.1:3306/ECOMMERCE", 
        connect_args = {"client_flag": CLIENT.MULTI_STATEMENTS}
    )

# Import custom Scrollable Frame
from ScrollableFrame import ScrollableFrame

# table of items only
class Past_Purchases_Table(ScrollableFrame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(width=800, height=800, *args, **kwargs)


        customerId = str(self.master.master.customerId)

        with_request = pd.read_sql_query(f"""
        SELECT * FROM Items i
        LEFT JOIN Payments c USING (itemID)
        LEFT JOIN Requests r USING(itemID)
        LEFT JOIN Products p USING(productID)
        WHERE requestID = (
        SELECT max(requestID)
            FROM Items i2
        LEFT JOIN Payments c2 USING (itemID)
        LEFT JOIN Requests r2 USING(itemID)
            WHERE i2.itemID = i.itemID
            GROUP BY i2.itemID
        ) and c.customerID = "{customerId}"
        {ORDER_BY_REQUEST_STATUS};
        """, db)

        no_request = pd.read_sql_query(f"""
            select i.itemID, p.model, i.colour, i.powerSupply,
            i.productionYear, i.factory, r.requestStatus, p.warrantyMonths,
            r.requestID, pay.paymentID, p.price
            from items i 
            inner join products p on i.productID = p.productID
            left join requests r on i.itemID = r.itemID
            left join payments pay on i.itemID = pay.itemID
            where i.itemID in (select itemID from payments where customerID = "{customerId}") and r.requestStatus is null
            {ORDER_BY_REQUEST_STATUS}
            limit 100;
        """, db)

        self.data = pd.concat([with_request, no_request], axis=0)

        # labels 
        tk.Label(self.frame, text="ItemID", anchor="w").grid(row=1, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(row=1, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Colour", anchor="w").grid(row=1, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Power Supply", anchor="w").grid(row=1, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Production Year", anchor="w").grid(row=1, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Factory", anchor="w").grid(row=1, column=5, sticky="ew", padx=10)
        tk.Label(self.frame, text="Amount Paid", anchor="w").grid(row=1, column=6, sticky="ew", padx=10)
        tk.Label(self.frame, text="Request Status", anchor="w").grid(row=1, column=7, sticky="ew", padx=10)

        row = 2

        bg = ["#ffffff", "#d9e1f2"]
            

        # populating the table row by row
        for entry in data.itertuples():
            
            # print(entry)
            itemId = entry.itemID
            model = entry.model
            colour = entry.colour
            powerSupply = entry.powerSupply
            productionYear = entry.productionYear
            factory = entry.factory
            amountPaid = entry.price

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

            itemID_label = tk.Label(self.frame, text=str(itemId), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            colour_label = tk.Label(self.frame, text=str(colour), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            powerSupply_label = tk.Label(self.frame, text=str(powerSupply), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            productionYear_label = tk.Label(self.frame, text=str(productionYear), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            factory_label = tk.Label(self.frame, text=str(factory), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])   
            amountPaid_label = tk.Label(self.frame, text="$" + "{:.2f}".format(amountPaid), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            requestStatus_label = tk.Label(self.frame, text=str(requestStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            
            itemID_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            colour_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            powerSupply_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            productionYear_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            factory_label.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            amountPaid_label.grid(row=row, column=6, sticky="ew", pady=2.5, ipady=5)
            requestStatus_label.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)    

            # different button according to what is the request status 
            paymentID = entry.paymentID

            if requestStatus in ['Completed', 'Cancelled', 'No request made']:
                requestButton = tk.Button(self.frame, text="Make new request", command = lambda paymentID = paymentID: self.master.master.id_switch_frame(paymentID, Request_Page))  
            else:
                requestButton = tk.Button(self.frame, text="Request details", command = lambda itemId = itemId: self.master.master.id_switch_frame(itemId, Request_Details))  
            requestButton.grid(row=row, column=8, sticky="ew", pady=2.5, ipady=5)

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
        optionMenu = OptionMenu(self, clicked, "Submitted", "Submitted and Waiting for payment", "In progress", "Approved", "Cancelled", "Completed", "No request made", "No filter", 
        command=lambda clicked = clicked: master.filter_status(clicked))
        optionMenu.config(width=30)
        optionMenu.grid(row=0, column=6, sticky="ew", padx=10)
        
        title = tk.Label(self, text="Past Purchases Page", font=('Aerial 14 bold'))
        title.grid(row=0, column=8, pady =20)
# main frame consisting of table and header 
class Past_Purchase_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.header = Past_Purchase_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)

        customerId = str(self.master.customerId)

        with_request = pd.read_sql_query(f"""
        SELECT * FROM Items i
        LEFT JOIN Payments c USING (itemID)
        LEFT JOIN Requests r USING(itemID)
        LEFT JOIN Products p USING(productID)
        WHERE requestID = (
        SELECT max(requestID)
            FROM Items i2
        LEFT JOIN Payments c2 USING (itemID)
        LEFT JOIN Requests r2 USING(itemID)
            WHERE i2.itemID = i.itemID
            GROUP BY i2.itemID
        ) and c.customerID = "{customerId}"
        {ORDER_BY_REQUEST_STATUS};
        """, db)

        no_request = pd.read_sql_query(f"""
            select i.itemID, p.model, i.colour, i.powerSupply,
            i.productionYear, i.factory, r.requestStatus,
            p.warrantyMonths, r.requestID, pay.paymentID, p.price
            from items i 
            inner join products p on i.productID = p.productID
            left join requests r on i.itemID = r.itemID
            left join payments pay on i.itemID = pay.itemID
            where i.itemID in (select itemID from payments where customerID = "{customerId}") and r.requestStatus is null
            {ORDER_BY_REQUEST_STATUS}
            limit 100;
        """, db)

        self.data = pd.concat([with_request, no_request], axis=0)


        self.table = Past_Purchases_Table(self.data, self)
        self.header.pack(side="top", fill="x", expand=False)
        self.table.pack(side="top", fill="both", expand=True)



    def show_header():
        header = Past_Purchase_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        header.pack(side="top", fill="x", expand=False)

    # filtering is performed here 
    def filter_status(self, curr_view):
        
        self.table.destroy()

        customerId = str(self.master.customerId)

        with_request = pd.read_sql_query(f"""
        SELECT * FROM Items i
        LEFT JOIN Payments c USING (itemID)
        LEFT JOIN Requests r USING(itemID)
        LEFT JOIN Products p USING(productID)
        WHERE requestID = (
        SELECT max(requestID)
            FROM Items i2
        LEFT JOIN Payments c2 USING (itemID)
        LEFT JOIN Requests r2 USING(itemID)
            WHERE i2.itemID = i.itemID
            GROUP BY i2.itemID
        ) and c.customerID = "{customerId}"
        {ORDER_BY_REQUEST_STATUS};
        """, db)

        no_request = pd.read_sql_query(f"""
            select i.itemID, p.model, i.colour, i.powerSupply,
            i.productionYear, i.factory, r.requestStatus,
            p.warrantyMonths, r.requestID, pay.paymentID, p.price
            from items i 
            inner join products p on i.productID = p.productID
            left join requests r on i.itemID = r.itemID
            left join payments pay on i.itemID = pay.itemID
            where i.itemID in (select itemID from payments where customerID = "{customerId}") and r.requestStatus is null
            {ORDER_BY_REQUEST_STATUS}
            limit 100;
        """, db)

        self.data = pd.concat([with_request, no_request], axis=0)

        curr_data = self.data.copy()

        if clicked.get() == 'No request made':
            curr_data = curr_data[curr_data['requestStatus'].isnull()]
        
        elif clicked.get() == 'No filter':
            curr_data = curr_data

        else:
            curr_data = curr_data[curr_data['requestStatus'] == clicked.get()]

        self.table = Past_Purchases_Table(curr_data, self)
        self.table.pack(side="top", fill="both", expand=True)

        

# --------------------------------------------------------------------- #

class Request_Page(Frame):
    #add currPaymentId ltr
    def __init__(self,curr_paymentId, master):
        Frame.__init__(self, master)
        self.master = master

        curr_adminId = self.master.adminId
        print(curr_adminId)

        print(curr_paymentId)

        data2 = pd.read_sql_query(f"""
        SELECT pay.paymentID, pay.itemID, c.customerID, 
        p.model, p.warrantyMonths, i.powerSupply, i.colour,
        p.cost, pay.purchaseDate
        FROM Payments pay 
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN Products p ON i.productID = p.productID
        LEFT JOIN Customers c ON pay.customerID = c.customerID
        WHERE pay.paymentID = {curr_paymentId}
        ;
        """, db)

        print(data2)
        (paymentId, curr_itemId, curr_customerId, curr_model,
        curr_warrantyMonths,curr_powerSupply,curr_colour,
        curr_cost, curr_purchaseDate) = list(data2.to_records(index=False))[0]
        print(curr_adminId)

        title = Label(self, text="Request Page", font=('Aerial 15 bold'))
        title.grid(row=0, column=1, pady =20)
    
        toggle = LabelFrame(self, borderwidth = 0)
        toggle.grid(row=0, column=1, padx=10)

        itemID = Label(self, text=curr_itemId)
        itemID.grid(row=2, column=1)
        itemID_label = Label(self, text="Item ID: ", font=('Aerial 9 bold'))
        itemID_label.grid(row=2, column=0)

        colour_label = Label(self, text="Colour: ", font=('Aerial 9 bold'))
        colour_label.grid(row=3, column=0)
        colour = Label(self, text=curr_colour)
        colour.grid(row=3, column=1, padx=20)

        power_label = Label(self, text="Power Supply: ", font=('Aerial 9 bold'))
        power_label.grid(row=5, column=0)
        power = Label(self, text=curr_powerSupply)
        power.grid(row=5, column=1, padx=20)

        model_label = Label(self, text="Model: ", font=('Aerial 9 bold'))
        model_label.grid(row=6, column=0)
        model = Label(self, text=curr_model)
        model.grid(row=6, column=1, padx=20)

        warranty_label = Label(self, text="Warranty: ", font=('Aerial 9 bold'))
        warranty_label.grid(row=7, column=0)
        end_warranty_date = curr_purchaseDate + relativedelta(months=+int(curr_warrantyMonths))
        warrantyStatus = self.getValidity(end_warranty_date)
        if warrantyStatus == "Invalid":
            warranty = Label(self, text=warrantyStatus, fg='#f00') 
            warranty.grid(row=7, column=1, padx=20)
        elif warrantyStatus == "Valid":
            warranty = Label(self, text=warrantyStatus, fg='green') 
            warranty.grid(row=7, column=1, padx=20)

        issue = Text(self, width = 40,height=3)
        issue.grid(row=8, column=1, padx=20)
        issue_label = Label(self, text="What is the issue of the item?", font=('Aerial 9 bold'))
        issue_label.grid(row=8)


        submit_btn = Button(self, text="Submit Request", command= lambda: self.submitRequest(data2,issue.get("1.0",'end-1c')))
        submit_btn.grid(row=9, column=2, columnspan=2)

    #Check todays date with the warranty end date
    def getValidity(self,end_date):
        today = date.today()
        if end_date >= today:
            return "Valid"
        else:
            return "Invalid"

    def submitRequest(self,data2,issue):
        # Get the data into variables
        (paymentId, curr_itemId, curr_customerId, 
        curr_model,curr_warrantyMonths,curr_powerSupply,
        curr_colour,curr_cost,curr_purchaseDate) = list(data2.to_records(index=False))[0]
        curr_adminId = self.master.adminId
        print("curr_adminId: " + str(curr_adminId))

        # Checking for the warranty status
        warranty_status = False
        end_warranty_date = curr_purchaseDate + relativedelta(months=+int(curr_warrantyMonths))
        if self.getValidity(end_warranty_date) == "Valid":
            reqstatus = 'Submitted'
            warranty_status = True
        elif self.getValidity(end_warranty_date) == "Invalid":
            reqstatus = 'Submitted and Waiting for payment'
            warranty_status = False

        print("Purchase Date: " + str(curr_purchaseDate))
        print("End Warranty Date: " + str(end_warranty_date))
        print("Issue: " + issue)
        print("Warranty status: " + str(warranty_status))

        #Push into the database of request table
        with db.begin() as conn:
            savepoint = conn.begin_nested()
            try:
                
                query = """
                SELECT COUNT(*) INTO @r_count FROM Requests;
                INSERT INTO Requests(requestID, itemID, administratorID, requestStatus, requestDetails) VALUES
                (@r_count + 1,%s,NULL,'%s',"%s");""" % (curr_itemId, reqstatus, str(issue))

                conn.execute(query)
                print("Added a request row")

                # To find the settlement Date (10 days away)
                now = date.today()
                dateStr = now.strftime("%Y-%m-%d")
                end_date = datetime.now() + timedelta(days = 10)
                end_dateStr = end_date.strftime("%Y-%m-%d")
                
                # 0 Service Fee if it is still in warranty
                if warranty_status:   
                    query2 = f"""
                    SELECT COUNT(*) INTO @r_count FROM Requests;
                    INSERT INTO ServiceFees(requestID, amount, creationDate, settlementDate) VALUES
                    (@r_count, {0}, '%s', '%s')
                    ;""" % (dateStr, dateStr)
                    conn.execute(query2)
                else:
                    query2 = f"""
                    SELECT COUNT(*) INTO @r_count FROM Requests;
                    INSERT INTO ServiceFees(requestID, amount, creationDate, settlementDate) VALUES
                    (@r_count, 40 + {curr_cost} * 0.2, '%s', NULL)
                    ;""" % (dateStr)
                    conn.execute(query2)

                print("Added a ServiceFee row")

                query3 = f"""
                SELECT COUNT(*) INTO @r_count FROM Requests;
                INSERT INTO Services(requestID, serviceStatus)VALUES
                (@r_count, "Waiting for approval")
                ;
                """
                conn.execute(query3)
                print("Added a Service row")

                
                # Commit changes to database
                savepoint.commit()

                # output = conn.execute("SELECT COUNT(*) FROM Requests")
                # requestID = output.fetchall()[0][0]
                
            except:
                # If fail, rollback the changes
                savepoint.rollback()
                print("Failed to submit request & servicefee")
        
        self.master.id_switch_frame(curr_itemId, Request_Details)


class Request_Details(Frame):
    def __init__(self, curr_itemId, master):
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
        WHERE (r.itemID = {curr_itemId} AND 
            r.requestID = (
                SELECT max(r2.requestID)
                    FROM Items i2
                LEFT JOIN Payments c2 USING (itemID)
                LEFT JOIN Requests r2 USING(itemID)
                    WHERE i2.itemID = i.itemID
                    GROUP BY i2.itemID)
            )
        ;
        """, db)

        (curr_itemId, curr_requestId, curr_model, curr_requestDetails,
        curr_purchaseDate, curr_creationDate, curr_settlementDate,
        curr_amount, curr_requestStatus) = list(data2.to_records(index=False))[0]
        print(curr_requestStatus)

        title = Label(self, text="Request Details", font=('Aerial 15 bold'))
        title.grid(row=0, column=1, pady =20)

        itemID = Label(self, text=curr_itemId)
        itemID.grid(row=1, column=1)
        itemID_label = Label(self, text="Item ID: ", font=('Aerial 9 bold'))
        itemID_label.grid(row=1, column=0)

        model_label = Label(self, text="Model: ", font=('Aerial 9 bold'))
        model_label.grid(row=2, column=0)
        model = Label(self, text=curr_model)
        model.grid(row=2, column=1, padx=20)

        reqDate_label = Label(self, text="Request Date: ", font=('Aerial 9 bold'))
        reqDate_label.grid(row=3, column=0)
        reqDate = Label(self, text=curr_creationDate)
        reqDate.grid(row=3, column=1, padx=20)

        # Calculating the end date after 10 days
        end_date = curr_creationDate + timedelta(days = 10)
        end_dateStr = end_date.strftime("%Y-%m-%d")

        paymentDate_label = Label(self, text="Payment due by: ", font=('Aerial 9 bold'))
        paymentDate_label.grid(row=4, column=0)
        paymentDate = Label(self, text=end_dateStr)
        paymentDate.grid(row=4, column=1, padx=20)

        if int(curr_amount) == 0:
            amount_label = Label(self, text="Payment Amount: ", font=('Aerial 9 bold'))
            amount_label.grid(row=5, column=0)
            amount = Label(self, text="$" + "{:.2f}".format(curr_amount) + " (No Payment Required)")
            amount.grid(row=5, column=1, padx=20)
        else:
            amount_label = Label(self, text="Payment Amount: ", font=('Aerial 9 bold'))
            amount_label.grid(row=5, column=0)
            amount = Label(self, text="$" + "{:.2f}".format(curr_amount))
            amount.grid(row=5, column=1, padx=20)

        issue_label = Label(self, text="Issue: ", font=('Aerial 9 bold'))
        issue_label.grid(row=6, column=0)
        issue = Label(self, text=curr_requestDetails)
        issue.grid(row=6, column=1, padx=20)

        if curr_requestStatus in ['Submitted', 'Submitted and Waiting for payment']:

            cancel_btn = Button(self, text="Cancel Request", command= lambda: self.cancelRequest(curr_requestId))
            cancel_btn.grid(row=9, column=0, pady = 20)

            return_btn = Button(self, text="Return to Past Payments", command= lambda: self.returnRequest()) # go to past payments
            return_btn.grid(row=9, column=1, pady = 20)

            ## If $0, they cannot return to past_purchases page
            if int(curr_amount) > 0:
                pay_btn = Button(self, text="Click for Payment", command= lambda: self.payRequest(curr_requestId,curr_amount))
                pay_btn.grid(row=9, column=2, pady = 20)
                
         
        elif curr_requestStatus in ['In progress', 'Approved']:
            cancel_btn = Button(self, text="Cancel Request", command= lambda: self.cancelRequest(curr_requestId))
            cancel_btn.grid(row=9, column=0, pady = 20)
            
            return_btn = Button(self, text="Return to Past Payments", command= lambda: self.returnRequest()) # go to past payments
            return_btn.grid(row=9, column=1, pady = 20)
        
        elif curr_requestStatus in ['Cancelled', 'Completed']:
            return_btn = Button(self, text="Return to Past Payments", command= lambda: self.returnRequest()) # go to past payments
            return_btn.grid(row=9, column=1, pady = 20)


    def cancelRequest(self,requestId):
        with db.begin() as conn:
            savepoint = conn.begin_nested()
            print(requestId)
            try:
                # Update the request status to Cancelled
                query = f"""
                UPDATE Requests r
                SET r.requestStatus = 'Cancelled'
                WHERE r.requestID = {requestId}
                ;
                """
                conn.execute(query)

                conn.execute(f"""
                UPDATE Services
                SET serviceStatus = 'Completed'
                where requestID = {requestId}
                ;
                """)
                
                # Commit changes to database
                savepoint.commit()
                print("The request is cancelled")
            except:

                # If fail, rollback the changes
                savepoint.rollback()
                print("Failed to cancel request")


        self.master.switch_frame(Cancel_Request_Page)

    
    def payRequest(self, requestId, curr_amount):
        with db.begin() as conn:
            savepoint = conn.begin_nested()
            
            today = date.today()

            try:
                
                # Update the request status to In progress
                query = f"""
                UPDATE Requests r
                SET r.requestStatus = 'In progress'
                WHERE (r.requestID = {requestId} AND r.requestStatus != 'Cancelled')
                ;
                """
                conn.execute(query)
                print("Update Request to In progress")

                # Update the ServiceFee's settlement date
                query2 = f"""
                UPDATE ServiceFees sf
                SET sf.settlementDate = '{today}'
                WHERE (sf.requestID = {requestId})
                ;
                """
                conn.execute(query2)
                print("Update the ServiceFee's settlement Date to today")

                # Commit changes to database
                savepoint.commit()
                print("The request has been paid")
            except:
                # If fail, rollback the changes
                savepoint.rollback()
                print("Failed to pay the request")

        self.master.switch_frame(Pay_Request_Page)
        
    # Return to TY Page    
    def returnRequest(self):
        self.master.switch_frame(Past_Purchase_Page)
        return


class Cancel_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request has been cancelled.", font=('Aerial 15 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: self.master.switch_frame(Past_Purchase_Page)) 
        submit_btn.grid(row=11, column=400, columnspan=2)

class Pay_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request has been paid. We will be proceeding your request", font=('Aerial 15 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: self.master.switch_frame(Past_Purchase_Page))
        submit_btn.grid(row=11, column=400, columnspan=2)