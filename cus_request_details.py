from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import sqlite3
from datetime import *
from past_purchases import Past_Purchase_Page

# For SQL query
from sqlalchemy import create_engine
from pymysql.constants import CLIENT
import pandas as pd
from config import USERNAME, MYSQL_PASSWORD

db = create_engine(f"mysql+pymysql://{USERNAME}:{MYSQL_PASSWORD}@127.0.0.1:3306/ECOMMERCE", 
        connect_args = {"client_flag": CLIENT.MULTI_STATEMENTS}
    )

# Need to take the data from item page
d1 = date(2022, 5, 3) #Warranty end date
data = ["1001", "Blue", "Battery", "Light1", d1, "Submitted and Waiting for payment","The light does not turn on", date(2021, 9, 22), 40]

class Request_Details(Frame):
    def __init__(self, curr_requestId, master):
        Frame.__init__(self, master)
        self.master = master

        print("reqID: " + str(curr_requestId))

        data2 = pd.read_sql_query(f"""
        SELECT r.itemID, p.model,
        r.requestDetails, pay.purchaseDate, 
        sf.creationDate,sf.settlementDate,sf.amount
        FROM Requests r 
        LEFT JOIN Payments pay USING (itemID)
        LEFT JOIN Items i USING(itemID)
        LEFT JOIN ServiceFees sf USING(requestID)
        LEFT JOIN Products p ON i.productID = p.productID
        WHERE r.requestID = {curr_requestId}
        ;
        """, db)

        (curr_itemId, curr_model, curr_requestDetails,
        curr_purchaseDate, curr_creationDate, curr_settlementDate,
        curr_amount) = list(data2.to_records(index=False))[0]
        

        title = Label(self, text="Request Details", font=('Helvetica 14 bold'))
        title.grid(row=0, column=1, pady =20)

        itemID = Label(self, text=curr_itemId)
        itemID.grid(row=1, column=1)
        itemID_label = Label(self, text="Item ID: ", font=('Helvetica 12 bold'))
        itemID_label.grid(row=1, column=0)

        model_label = Label(self, text="Model: ", font=('Helvetica 12 bold'))
        model_label.grid(row=2, column=0)
        model = Label(self, text=curr_model)
        model.grid(row=2, column=1, padx=20)

        reqDate_label = Label(self, text="Request Date: ", font=('Helvetica 12 bold'))
        reqDate_label.grid(row=3, column=0)
        reqDate = Label(self, text=curr_creationDate)
        reqDate.grid(row=3, column=1, padx=20)

        paymentDate_label = Label(self, text="Payment due by: ", font=('Helvetica 12 bold'))
        paymentDate_label.grid(row=4, column=0)
        paymentDate = Label(self, text=curr_settlementDate)
        paymentDate.grid(row=4, column=1, padx=20)

        amount_label = Label(self, text="Payment Amount: ", font=('Helvetica 12 bold'))
        amount_label.grid(row=5, column=0)
        amount = Label(self, text="$" + str(curr_amount))
        amount.grid(row=5, column=1, padx=20)

        issue_label = Label(self, text="Issue: ", font=('Helvetica 12 bold'))
        issue_label.grid(row=6, column=0)
        issue = Label(self, text=curr_requestDetails)
        issue.grid(row=6, column=1, padx=20)

        cancel_btn = Button(self, text="Cancel Request", command= lambda: self.cancelRequest(curr_requestId))
        cancel_btn.grid(row=9, column=0, pady = 20)

        pay_btn = Button(self, text="Click for Payment", command= lambda: self.payRequest(curr_requestId))
        pay_btn.grid(row=9, column=2, pady = 20)

        ## If $0, they cannot return to past_purchases page
        if curr_amount > 0:
            return_btn = Button(self, text="Return to Past Payments", command= lambda: self.returnRequest()) # go o past payments
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
                
                # Commit changes to database
                savepoint.commit()

                print("The request is cancelled")
            except:

                # If fail, rollback the changes
                savepoint.rollback()
                print("Failed to cancel request")


        self.master.switch_frame(Cancel_Request_Page)

    
    def payRequest(self, requestId):
        with db.begin() as conn:
            savepoint = conn.begin_nested()
            print(requestId)
            try:
                # Update the request status to In progress
                query = f"""
                UPDATE Requests r
                SET r.requestStatus = 'In progress'
                WHERE r.requestID = {requestId}
                ;
                """
                conn.execute(query)

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

        title = Label(self, text="Request has been cancelled.", font=('Helvetica 14 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: master.switch_frame(Request_Details)) ##Go back to the item page
        submit_btn.grid(row=11, column=400, columnspan=2)

class Pay_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request has been paid. We will be proceeding your request", font=('Helvetica 14 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: self.master.switch_frame(Past_Purchase_Page)) ##Go back to the item page
        submit_btn.grid(row=11, column=400, columnspan=2)

        
