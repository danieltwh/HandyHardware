from tkinter import *
from typing import Match
from PIL import ImageTk, Image
import sqlite3

# “N/A”: customer has not submitted a request for this item. 
# “Submitted”: customer who does not have a service fee has submitted a request successfully to the Administrator. 
# “Submitted and Waiting for payment” customer who has service fee has submitted a request but has not yet paid for this service. 
# “In progress”: this request is being processed. 
# “Approved”: this request has been approved by the Administrator when the service fee is paid successfully.
# “Canceled”: customer has canceled or the service fee has not been paid within the time period.


# main frame: shows all the items that the user has previously bought 
#   has a search and filter textbox/dropdown menu for the items 
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

class Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        new_request_btn = Button(self, text="Make a new request", command=lambda: master.switch_frame(Request_Submission_Page))


        request_details_btn = Button(self, text="Request details", command=lambda: master.switch_frame(Request_Details_Page))


        # returns to the catalogue page  
        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Request_Page))


        # dropdown menu for filtering by service status 
        clicked = StringVar()
        clicked.set('NA')

        dropdown_label = Label(self, text="Request status")

        dropdown = OptionMenu(self, clicked, 'NA', 'SUBMITTED', 'WAITING FOR PAYMENT', 'IN PROGRESS', 'APPROVED', 'CANCELLED')

        # shows items according to filter specified 
        def show():

            conn = sqlite3.connect('items.db')

            c = conn.cursor()

            c.execute('''
                SELECT * FROM items
                WHERE ServiceStatus = ?
            ''', [''])

            for record in c.fetchall():
                print(record)

            conn.commit()
            conn.close()

        # button to filter by service status
        filter_btn = Button(self, text="FILTER", command = show)


# submit new request for items 
class Request_Submission_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        # returns to the request page  
        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Request_Page))

# viewing the request details for items that already have a request 
class Request_Details_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        # returns to the request page  
        back_btn = Button(self, text="Back", command=lambda: master.switch_frame(Request_Page))
