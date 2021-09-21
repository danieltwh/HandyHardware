from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Admin_Request_Page)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)



def main():
    # root = Tk()
    # root.title("OSHE")
    # # root.iconbitmap('coffee.ico')
    # root.geometry("800x800")
    # # app = Signup_Page(root)
    # # app = Login_Page(root)
    # root.mainloop()

    app = App()
    app.geometry("800x800")
    app.mainloop()

        
data = [
    ("001", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "Approved"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("006", "Ethel", "Lock1", "Issue", "Canceled"),
    ("007", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment")
]

class Request_Table(tk.LabelFrame):
    def __init__(self, data, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)
        # data = [
        #     # Nr. Name  Active
        #     [1,   "ST", True],
        #     [2,   "SO", False],
        #     [3,   "SX", True],
        #     ]

        self.data = data


        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Request ID", anchor="w").grid(row=0, column=0, sticky="ew", padx=10)
        tk.Label(self, text="Name", anchor="w").grid(row=0, column=1, sticky="ew", padx=10)
        tk.Label(self, text="Model", anchor="w").grid(row=0, column=2, sticky="ew", padx=10)
        tk.Label(self, text="Issue", anchor="w").grid(row=0, column=3, sticky="ew", padx=10)
        tk.Label(self, text="Request Status", anchor="w").grid(row=0, column=4, sticky="ew", padx=10)
        tk.Label(self, text="Action", anchor="w").grid(row=0, column=5, sticky="ew", padx=10)

        row = 1
        for (requestId, name, model, issue, requestStatus) in data:
            requestId_label = tk.Label(self, text=str(requestId), anchor="w", borderwidth=2, relief="groove", padx=10)
            name_label = tk.Label(self, text=str(name), anchor="w", borderwidth=2, relief="groove", padx=10) 
            model_label = tk.Label(self, text=str(model), anchor="w", borderwidth=2, relief="groove", padx=10)
            issue_label = tk.Label(self, text=str(issue), anchor="w", borderwidth=2, relief="groove", padx=10)
            requestStatus_label = tk.Label(self, text=str(requestStatus), anchor="w", borderwidth=2, relief="groove", padx=10)

            
            
            # active_cb = tk.Checkbutton(self, onvalue=True, offvalue=False)
            # active = True
            # if active:
            #     active_cb.select()
            # else:
            #     active_cb.deselect()

            requestId_label.grid(row=row, column=0, sticky="ew")
            name_label.grid(row=row, column=1, sticky="ew")
            model_label.grid(row=row, column=2, sticky="ew")
            issue_label.grid(row=row, column=3, sticky="ew", )
            issue_label.grid_columnconfigure(0, weight=5)
            requestStatus_label.grid(row=row, column=4, sticky="ew")
            requestStatus_label.grid_columnconfigure(0, weight=5)
            # active_cb.grid(row=row, column=4, sticky="ew")

            if requestStatus == "Submitted":
                action_button = tk.Button(self, text="Approve", command=lambda requestId = requestId: self.delete(requestId))
                action_button.grid(row=row, column=5, sticky="ew")


            row += 1

    def delete(self, requestId):
        print ("deleting...nr=", requestId)

class Admin_Request_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        

        tab1 = tk.Button(self, text="All Request", command= lambda: master.refresh("All"))
        tab1.grid(row=0, column=0, padx=(10, 5))

        tab2 = tk.Button(self, text="Pending", command= lambda: master.refresh("Pending"))
        # tab2.pack(side="left", fill="both")
        tab2.grid(row=0, column=1, padx=5)

        tab3 = tk.Button(self, text="My Jobs", command= lambda: master.refresh("My Jobs"))
        # tab2.pack(side="left", fill="both")
        tab3.grid(row=0, column=2, padx=5)

        
    


class Admin_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.header = Admin_Request_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)

        global data
        self.requestTable = Request_Table(data, self)

        self.header.pack(side="top", fill="x", expand=False)
        self.requestTable.pack(side="top", fill="both", expand=True)

        self.filter = {
            "All" : lambda row: row,
            "Pending": lambda row: row[4] == "Submitted", 
            "My Jobs": lambda row: row[4] == "Approved"
        }

    def show_header():
        header = Admin_Request_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        header.pack(side="top", fill="x", expand=False)

    
    def refresh(self, curr_view):

        self.requestTable.destroy()

        global data
        curr_data = data.copy()
        curr_data = filter(self.filter.get(curr_view), curr_data)

        self.requestTable = Request_Table(curr_data, self)
        self.requestTable.pack(side="top", fill="both", expand=True)
    
    

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)




if __name__ == "__main__":
    main()