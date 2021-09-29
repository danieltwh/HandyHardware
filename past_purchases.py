from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3

from ScrollableFrame import ScrollableFrame

data = [
    ("1001", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted"), 
    ("1003", "Lights", "Yellow", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted and Waiting for payment"), 
    ("1004", "Lights", "Green", "Malaysia", "Battery", "Sold", "2014", "Light1", "In progress"), 
    ("1005", "Lights", "Black", "Malaysia", "Battery", "Sold", "2014", "Light1", "Approved"), 
    ("1006", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Canceled"), 
    ("1007", "Lights", "Blue", "Malaysia", "Battery", "Sold", "2014", "Light1", "Completed"),
    ("1008", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted"), 
    ("1009", "Lights", "Yellow", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted and Waiting for payment"), 
    ("1010", "Lights", "Green", "Malaysia", "Battery", "Sold", "2014", "Light1", "In progress"), 
    ("1011", "Lights", "Black", "Malaysia", "Battery", "Sold", "2014", "Light1", "Approved"), 
    ("1012", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Canceled"), 
    ("1013", "Lights", "Blue", "Malaysia", "Battery", "Sold", "2014", "Light1", "Completed"),
    ("1008", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted"), 
    ("1009", "Lights", "Yellow", "Malaysia", "Battery", "Sold", "2014", "Light1", "Submitted and Waiting for payment"), 
    ("1010", "Lights", "Green", "Malaysia", "Battery", "Sold", "2014", "Light1", "In progress"), 
    ("1011", "Lights", "Black", "Malaysia", "Battery", "Sold", "2014", "Light1", "Approved"), 
    ("1012", "Lights", "White", "Malaysia", "Battery", "Sold", "2014", "Light1", "Canceled"), 
    ("1013", "Lights", "Blue", "Malaysia", "Battery", "Sold", "2014", "Light1", "Completed")
    ]

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Past_Purchase_Page)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

def main():

    app = App()
    app.geometry("800x800")
    app.mainloop()

# contains the table of items
class Past_Purchases_Table(ScrollableFrame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data

        # labels
        tk.Label(self.frame, text="Product", anchor="w").grid(row=1, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(row=1, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Colour", anchor="w").grid(row=1, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Power Supply", anchor="w").grid(row=1, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Production Year", anchor="w").grid(row=1, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Factory", anchor="w").grid(row=1, column=5, sticky="ew", padx=10)
        tk.Label(self.frame, text="Service Status", anchor="w").grid(row=1, column=6, sticky="ew", padx=10)

        row = 2

        bg = ["#ffffff", "#d9e1f2"]

        # populating the table row by row
        for (ItemID, category, colour, factory, powerSupply, PurchaseStatus, ProductionYear, Model, ServiceStatus) in data:

            product_label = tk.Label(self.frame, text=str(category), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(Model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            colour_label = tk.Label(self.frame, text=str(colour), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            powerSupply_label = tk.Label(self.frame, text=str(powerSupply), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            productionYear_label = tk.Label(self.frame, text=str(ProductionYear), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            factory_label = tk.Label(self.frame, text=str(factory), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])   
            serviceStatus_label = tk.Label(self.frame, text=str(ServiceStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            requestButton = tk.Button(self.frame, text="Request details")

            product_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            colour_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            powerSupply_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            productionYear_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            factory_label.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            serviceStatus_label.grid(row=row, column=6, sticky="ew", pady=2.5, ipady=5)      
            requestButton.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)

            row += 1
        
        self.launch()

# header 
class Past_Purchase_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        global clicked
        clicked = tk.StringVar()
        clicked.set("None")

        OptionMenu(self, clicked, "Submitted", "Approved", "Submitted and Waiting for payment", "In progress", "Canceled", "Completed", "None", 
        command=lambda clicked = clicked: master.filter_status(clicked)).grid(
            row=0, column=6, sticky="ew", padx=10)

# main frame consisting of table and header 
class Past_Purchase_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.header = Past_Purchase_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)

        global data

        self.table = Past_Purchases_Table(data, self)

        self.header.pack(side="top", fill="x", expand=False)
        self.table.pack(side="top", fill="both", expand=True)

        self.status_filter = {
            "None": lambda row: row,
            "Submitted": lambda row: row[8] == "Submitted",
            "Approved": lambda row: row[8] == "Approved",
            "Submitted and Waiting for payment": lambda row: row[8] == "Submitted and Waiting for payment",
            "In progress": lambda row: row[8] == "In progress",
            "Canceled": lambda row: row[8] == "Canceled",
            "Completed": lambda row: row[8] == "Completed"
        }

    def show_header():
        header = Past_Purchase_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        header.pack(side="top", fill="x", expand=False)

    def filter_status(self, curr_view):
        
        self.table.destroy()

        global data
        curr_data = data.copy()
        curr_data = filter(self.status_filter.get(curr_view), curr_data)

        self.table = Past_Purchases_Table(curr_data, self)
        self.table.pack(side="top", fill="both", expand=True)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    main()
