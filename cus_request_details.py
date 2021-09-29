from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import sqlite3
from datetime import *

# Need to take the data from item page
d1 = date(2022, 5, 3) #Warranty end date
data = ["1001", "Blue", "Battery", "Light1", d1, "Submitted and Waiting for payment","The light does not turn on", date(2021, 9, 22), 40]

class Request_Details(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request Details", font=('Aerial 15 bold'))
        title.grid(row=0, column=1, pady =20)

        itemID = Label(self, text=data[0])
        itemID.grid(row=1, column=1)
        itemID_label = Label(self, text="Item ID: ", font=('Aerial 9 bold'))
        itemID_label.grid(row=1, column=0)

        model_label = Label(self, text="Model: ", font=('Aerial 9 bold'))
        model_label.grid(row=2, column=0)
        model = Label(self, text=data[3])
        model.grid(row=2, column=1, padx=20)

        reqDate_label = Label(self, text="Request Date: ", font=('Aerial 9 bold'))
        reqDate_label.grid(row=3, column=0)
        reqDate = Label(self, text=data[7])
        reqDate.grid(row=3, column=1, padx=20)

        paymentDate_label = Label(self, text="Payment due by: ", font=('Aerial 9 bold'))
        paymentDate_label.grid(row=4, column=0)
        paymentDate = Label(self, text=data[7] + timedelta(days=14))
        paymentDate.grid(row=4, column=1, padx=20)

        amount_label = Label(self, text="Payment Amount: ", font=('Aerial 9 bold'))
        amount_label.grid(row=5, column=0)
        amount = Label(self, text="$" + str(data[8]))
        amount.grid(row=5, column=1, padx=20)

        issue_label = Label(self, text="Issue: ", font=('Aerial 9 bold'))
        issue_label.grid(row=6, column=0)
        issue = Label(self, text=data[6])
        issue.grid(row=6, column=1, padx=20)

        cancel_btn = Button(self, text="Cancel Request", command= lambda: self.cancelRequest())
        cancel_btn.grid(row=9, column=0, pady = 20)

        return_btn = Button(self, text="Return to Past Payments", command= lambda: self.returnRequest()) # go o past payments
        return_btn.grid(row=9, column=1, pady = 20)

        pay_btn = Button(self, text="Click for Payment", command= lambda: self.payRequest())
        pay_btn.grid(row=9, column=2, pady = 20)

    def cancelRequest(self):
        self.master.switch_frame(Cancel_Request_Page)
        # Remove the relation in the Request Database

    def payRequest(self):
        self.master.switch_frame(Pay_Request_Page)
        # Modify the existing relation to change the request status
        return
    def returnRequest(self):
        #self.master.switch_frame(xxx)
        return


class Cancel_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request has been cancelled.", font=('Aerial 15 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: master.switch_frame(Request_Details)) ##Go back to the item page
        submit_btn.grid(row=11, column=400, columnspan=2)

class Pay_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request has been paid. We will be proceeding your request", font=('Aerial 15 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: master.switch_frame(Request_Details)) ##Go back to the item page
        submit_btn.grid(row=11, column=400, columnspan=2)

        
