from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import sqlite3
from datetime import *
from cus_request_details import Request_Details


# Need to take the data from item page
d1 = date(2022, 5, 3) #Warranty end date
data = ["1001", "Blue", "Battery", "Light1", d1]

class Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request Page", font=('Aerial 15 bold'))
        title.grid(row=0, column=1, pady =20)
    
        toggle = LabelFrame(self, borderwidth = 0)
        toggle.grid(row=0, column=1, padx=10)

        itemID = Label(self, text=data[0])
        itemID.grid(row=2, column=1)
        itemID_label = Label(self, text="Item ID: ", font=('Aerial 9 bold'))
        itemID_label.grid(row=2, column=0)

        colour_label = Label(self, text="Colour: ", font=('Aerial 9 bold'))
        colour_label.grid(row=3, column=0)
        colour = Label(self, text=data[1])
        colour.grid(row=3, column=1, padx=20)

        power_label = Label(self, text="Power Supply: ", font=('Aerial 9 bold'))
        power_label.grid(row=5, column=0)
        power = Label(self, text=data[2])
        power.grid(row=5, column=1, padx=20)

        model_label = Label(self, text="Model: ", font=('Aerial 9 bold'))
        model_label.grid(row=6, column=0)
        model = Label(self, text=data[3])
        model.grid(row=6, column=1, padx=20)

        warranty_label = Label(self, text="Warranty: ", font=('Aerial 9 bold'))
        warranty_label.grid(row=7, column=0)
        warranty = Label(self, text=self.getValidity(data[4]))
        warranty.grid(row=7, column=1, padx=20)

        issue = Text(self, width = 40,height=3)
        issue.grid(row=8, column=1, padx=20)
        issue_label = Label(self, text="What is the issue of the item?", font=('Aerial 9 bold'))
        issue_label.grid(row=8)

        # Creating a new relation for Request Database
        reqData = data.copy()


        submit_btn = Button(self, text="Submit Request", command= lambda: self.submitRequest(reqData,issue))
        submit_btn.grid(row=9, column=2, columnspan=2)

    def getValidity(self,end_date):
        today = date.today()
        if end_date >= today:
            return "Valid"
        else:
            return "Invalid"

    def submitRequest(self,reqData,issue):
        # Add the request status depending on the warranty status
        if self.getValidity(data[4]) == "Valid":
            reqData.append("Submitted")
        elif self.getValidity(data[4]) == "Invalid":
            reqData.append("Submitted and Waiting for payment")
        # Add the issue into the data
        reqData.append(issue.get("1.0",'end-1c'))
        # Add the request date
        reqData.append(date.today())
        print(reqData)
        self.master.switch_frame(Request_Details)
        #Push into the database of request table


class Request_Submitted_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request submitted.\n We will be processing your request shortly.", font=('Aerial 15 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: master.switch_frame(Request_Page)) ##Go back to the item page
        submit_btn.grid(row=11, column=400, columnspan=2)

        
