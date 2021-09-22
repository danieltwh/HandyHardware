from tkinter import *
from typing import Match
import sqlite3

# “N/A”: customer has not submitted a request for this item. 
# “Submitted”: customer who does not have a service fee has submitted a request successfully to the Administrator. 
# “Submitted and Waiting for payment” customer who has service fee has submitted a request but has not yet paid for this service. 
# “In progress”: this request is being processed. 
# “Approved”: this request has been approved by the Administrator when the service fee is paid successfully.
# “Canceled”: customer has canceled or the service fee has not been paid within the time period.


# main frame: shows all the items that the user has previously bought 
#   has a filter textbox/dropdown menu for the items 
#   for each item, show its request status, as well as a button at the side 

# items with past requests:
#   the button will be named 'make a new request'
#   this button will redirect to a new frame, where they can input details about the request 
#   after submitting the new request, update the request status, and notify the administrator 

# items with past requests: 
#   the button will be named 'request details'
#   this button will redirect to a new frame, where they can view the details regarding the request / cancel the request / make payment 
#   after cancellation or payment, update the request status

# customer's interaction with admins 
#   when the admin modifies the request, must reflect in the customer side as well
#   vice versa for customer 

class Past_Purchase_Page(Frame):
    def __init__(self, master):

        LabelFrame.__init__(self, master)
        self.master = master

        # dropdown menu for filtering items by service status 
        global clicked
        clicked = StringVar()
        clicked.set('NONE')

        dropdown_label = Label(self, text="Filter by:")
        dropdown_label.pack()

        dropdown = OptionMenu(self, clicked, 'Battery', 'USB','NA', 'SUBMITTED', 'WAITING FOR PAYMENT', 'IN PROGRESS', 'APPROVED', 'CANCELLED', 'NONE', command=self.filter)
        dropdown.pack()

        # wrapper frame
        items_frame = LabelFrame(self)

        # canvas 
        canvas = Canvas(items_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # scrollbar 
        scrollbar = Scrollbar(items_frame, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # configuring canvas 
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # canvas frame 
        global canvas_frame
        canvas_frame = Frame(canvas)
        canvas.create_window((0,0), window=canvas_frame, anchor='nw')

        # canvas frame
        items_frame.pack(fill=BOTH, expand=YES)

        # database connection 
        conn = sqlite3.connect('items.db')
        global c
        c = conn.cursor()

        c.execute(
            '''
            SELECT Model, PowerSupply 
            FROM items

            '''
            )

        self.show_items()


            

        # returns to the catalogue page  
        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Past_Purchase_Page))
        back_btn.pack()

        conn.commit()



    def filter(self, event):

        # destroying the old frame entries 
        for widgets in canvas_frame.winfo_children():
             widgets.destroy()

        # should be Model, Price, Warranty, ServiceStatus instead of powersupply 

        if clicked.get() == 'NONE':  # show all items without filter
            c.execute(
                '''
                SELECT Model, PowerSupply 
                FROM items
                '''
                )
        else :  # show the items with specified filter 
            c.execute(
                '''
                SELECT Model, PowerSupply 
                FROM items
                WHERE PowerSupply = ? 
                ''', 
                [clicked.get()]
                )

        self.show_items()
    
    def show_items(self):

        for record in c.fetchall():
            temp_frame = Frame(canvas_frame)
            txt = Text(temp_frame, height=1)
            txt.insert('1.0', record)
            txt.pack(side=LEFT)
            Button(temp_frame, text='Request details').pack(side=LEFT)
            temp_frame.pack()

    #     for record in c.fetchall():
    #         individual_item_frame = Frame(canvas_frame)
    #         individual_item_frame.pack()

    #         txt = Text(individual_item_frame, height=1)
    #         txt.insert('1.0',record)
    #         txt.pack(side = LEFT)

    #         if there are no requests for the item, redirect to new page to make a new request (marvin side)
    #         new_request_btn = Button(individual_item_frame, text="Make a new request")
    #         new_request_btn.pack(side = LEFT)

    #         if there are requests for the item, redirect to new page to view the request details (marvin side)
    #         request_details_btn = Button(individual_item_frame, text="Request details")
    #         request_details_btn.pack(side = LEFT)