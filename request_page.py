from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import sqlite3

# Need to take the data from item page

class Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request Page", font=('Aerial 15 bold'))
        title.grid(row=0, column=200, pady =20)
        
        toggle = LabelFrame(self, borderwidth = 0)
        toggle.grid(row=0, column=1, padx=10)

        itemID = Label(self, text="1001")
        itemID.grid(row=2, column=1)
        itemID_label = Label(self, text="Item ID: ")
        itemID_label.grid(row=2, column=0)

        colour_label = Label(self, text="Colour: ")
        colour_label.grid(row=3, column=0)
        colour = Label(self, text="Blue")
        colour.grid(row=3, column=1, padx=20)

        factory_label = Label(self, text="Factory: ")
        factory_label.grid(row=4, column=0)
        factory = Label(self, text="Malaysia")
        factory.grid(row=4, column=1, padx=20)

        power_label = Label(self, text="Power Supply: ")
        power_label.grid(row=5, column=0)
        power = Label(self, text="Battery")
        power.grid(row=5, column=1, padx=20)

        model_label = Label(self, text="Model: ")
        model_label.grid(row=6, column=0)
        model = Label(self, text="Light1")
        model.grid(row=6, column=1, padx=20)

        warranty_label = Label(self, text="Warranty: ")
        warranty_label.grid(row=7, column=0)
        warranty = Label(self, text="Valid")
        warranty.grid(row=7, column=1, padx=20)

        comment = Entry(self, width = 30)
        comment.grid(row=10, column=1, padx=20)
        comment_label = Label(self, text="Comments:")
        comment_label.grid(row=10, column=0)

        submit_btn = Button(self, text="Submit Request", command= lambda: master.switch_frame(Request_Submitted_Page))
        submit_btn.grid(row=11, column=400, columnspan=2)

class Request_Submitted_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        title = Label(self, text="Request submitted.\n We will be processing your request shortly.", font=('Aerial 15 bold'))
        title.grid(row=0, column=400, pady =60)

        submit_btn = Button(self, text="Proceed to Past Payments", command= lambda: master.switch_frame(Request_Page)) ##Go back to the item page
        submit_btn.grid(row=11, column=400, columnspan=2)

        
