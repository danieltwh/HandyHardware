from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import sqlite3
from datetime import *
from cus_request_details import Request_Details

# For SQL query
from sqlalchemy import create_engine
from pymysql.constants import CLIENT
import pandas as pd
from config import USERNAME, MYSQL_PASSWORD

# Need to take the data from item page
d1 = date(2022, 5, 3) #Warranty end date
data = ["1001", "Blue", "Battery", "Light1", d1]
db = create_engine(f"mysql+pymysql://{USERNAME}:{MYSQL_PASSWORD}@127.0.0.1:3306/ECOMMERCE", 
        connect_args = {"client_flag": CLIENT.MULTI_STATEMENTS}
    )

class Request_Page(Frame):
    #add currPaymentId ltr
    def __init__(self,curr_paymentId, master):
        Frame.__init__(self, master)
        self.master = master

        print(curr_paymentId)

        data2 = pd.read_sql_query(f"""
        SELECT pay.paymentID, pay.itemID, c.customerID, 
        p.model, p.warrantyMonths, i.powerSupply, i.colour,p.price
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
        curr_price) = list(data2.to_records(index=False))[0]
        

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
        warranty = Label(self, text=self.getValidity(data[4])) #Need to edit this
        warranty.grid(row=7, column=1, padx=20)

        issue = Text(self, width = 40,height=3)
        issue.grid(row=8, column=1, padx=20)
        issue_label = Label(self, text="What is the issue of the item?", font=('Aerial 9 bold'))
        issue_label.grid(row=8)

        # Creating a new relation for Request Database
        reqData = data.copy()


        submit_btn = Button(self, text="Submit Request", command= lambda: self.submitRequest(data2,issue.get("1.0",'end-1c')))
        submit_btn.grid(row=9, column=2, columnspan=2)

    def getValidity(self,end_date):
        today = date.today()
        if end_date >= today:
            return "Valid"
        else:
            return "Invalid"

    def submitRequest(self,data2,issue):
        # Add the request status depending on the warranty status
        reqstatus = ""
        if self.getValidity(data[4]) == "Valid":
            reqstatus = 'Submitted'
        elif self.getValidity(data[4]) == "Invalid":
            reqstatus = 'Submitted and Waiting for payment'
    
        #self.master.switch_frame(Request_Details)
        (paymentId, curr_itemId, curr_customerId, 
        curr_model,curr_warrantyMonths,curr_powerSupply,
        curr_colour,curr_price) = list(data2.to_records(index=False))[0]
        #DECLARE @totalNoOfReq int
        #SELECT @totalNoOfReq=count(1) from Requests
        
        #INSERT INTO ServiceFees(requestID, amount, creationDate, settlementDate)VALUES
        #({3}, {40 + 0.2*curr_price},{date.today()},{date.today()}) 
        #;
        print(issue)
        print(reqstatus)

        #Push into the database of request table
        with db.begin() as conn:
            savepoint = conn.begin_nested()
            try:
                # Create a request and service row (NEED CHANGE SETTLE MENT DATE)     
                query = "INSERT INTO Requests(requestID, itemID, administratorID, requestStatus, requestDetails) VALUES (%s,%s,%s,'%s','%s')" % (31, curr_itemId, 'NULL', reqstatus,issue)
                conn.execute(query)
                # conn.execute(f"""
                # INSERT INTO Requests(requestID, itemID, administratorID, requestStatus, requestDetails) VALUES
                # (28,{curr_itemId},NULL, 'Submitted', 'Item broke in half');
                # """)
                print("Added a request row")

                ## NOT DONE Check Warranty
                query2 = "ServiceFees(requestID, amount, creationDate, settlementDate)VALUES (%s,%s,%s,%s)" % (31, 50, '2021-03-01','2021-03-15')
                conn.execute(f"""
                INSERT INTO ServiceFees(requestID, amount, creationDate, settlementDate)VALUES
                (31, 50, '2021-03-01','2021-03-15')
                ;
                """)
                print("Added a service row")

                # Create a service row
                # conn.execute(f"""
                # INSERT INTO ServiceFees(requestID, amount, creationDate, settlementDate)VALUES
                # ({requestId}, "In Progress")
                # ;
                # """)
                
                # Commit changes to database
                savepoint.commit()

            except:
                # If fail, rollback the changes
                savepoint.rollback()
                print("Failed to submit request & servicefee")
        



class Request_Submitted_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request submitted.\n We will be processing your request shortly.", font=('Aerial 15 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: master.switch_frame(Request_Page)) ##Go back to the item page
        submit_btn.grid(row=11, column=400, columnspan=2)

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Request_Page)

    def switch_frame(self, frame_class):
        new_frame = frame_class(1,self.master)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

def main():
    app = App()
    app.geometry("800x800")
    app.mainloop()

if __name__ == "__main__":
    main()
        
