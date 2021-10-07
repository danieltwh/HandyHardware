from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3
import pymongo

# For SQL query
from sqlalchemy import create_engine
from pymysql.constants import CLIENT
import pandas as pd

# For mongodb query
from pymongo import MongoClient

#get data from mongodb
client = MongoClient()
db = client.Assignment
products = db.products
items = db.items
data = products.find({})

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Customer_Shopping_Catalogue_Page)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)


def main():
    app = App()
    app.geometry("1200x800")
    app.mainloop()

class Catalogue_Table(tk.LabelFrame):
    def __init__(self, data, *args, **kwargs):
        tk.LabelFrame.__init__(self, width=800, height=800, *args, **kwargs)



        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Categories", anchor="w").grid(row=0, column=0, sticky="ew", padx=10)
        tk.Label(self, text="Model", anchor="w").grid(row=0, column=1, sticky="ew", padx=10)
        tk.Label(self, text="Price", anchor="w").grid(row=0, column=2, sticky="ew", padx=10)
        tk.Label(self, text="Warranty", anchor="w").grid(row=0, column=3, sticky="ew", padx=10)
        tk.Label(self, text="Number of Item Available", anchor="w").grid(row=0, column=4, sticky="ew", padx=10)

        

        row = 1
        for dic in data:
            categories_label = tk.Label(self, text=str(dic["Category"]), anchor="w", borderwidth=2, relief="groove", padx=10)
            model_label = tk.Label(self, text=str(dic["Model"]), anchor="w", borderwidth=2, relief="groove", padx=10)
            price_label = tk.Label(self, text=str(dic["Price"]), anchor="w", borderwidth=2, relief="groove", padx=10)
            warranty_label = tk.Label(self, text=str(dic["Warranty"]), anchor="w", borderwidth=2, relief="groove", padx=10)             
            numberOfItemsAvailable_label = tk.Label(self, text=str(items.count_documents({"Model": dic["Model"]})), anchor="w", borderwidth=2, relief="groove", padx=10)


            categories_label.grid(row=row, column=0, sticky="ew")
            model_label.grid(row=row, column=1, sticky="ew")
            price_label.grid(row=row, column=2, sticky="ew", )
            warranty_label.grid(row=row, column=3, sticky="ew")
            warranty_label.grid_columnconfigure(0, weight=5)
            numberOfItemsAvailable_label.grid(row=row, column=4, sticky="ew")
            numberOfItemsAvailable_label.grid_columnconfigure(0, weight=5)


            if numberOfItemsAvailable_label != "0":
                action_button = tk.Button(self, text="Add", command=lambda row = row: self.add(row))
                action_button.grid(row=row, column=5, sticky="ew")

            row += 1
    
    def minus(self, numberOfItemsAvailable):
        print("Inventory reduce by 1")

    # def add(self, row):
    #     global data
    #     global cart
    #     newData = data.copy()
    #     cart.append(newData[row - 1][:-1])



# class Cart_Table(tk.LabelFrame):
#     def __init__(self, data, *args, **kwargs):
#         tk.LabelFrame.__init__(self, *args, **kwargs)

#         self.data = data

#         self.grid_columnconfigure(1, weight=1)
#         tk.Label(self, text="Categories", anchor="w").grid(row=0, column=0, sticky="ew", padx=10)
#         tk.Label(self, text="Model", anchor="w").grid(row=0, column=1, sticky="ew", padx=10)
#         tk.Label(self, text="Price", anchor="w").grid(row=0, column=2, sticky="ew", padx=10)
#         tk.Label(self, text="Warranty", anchor="w").grid(row=0, column=3, sticky="ew", padx=10)

        

#         row = 1
#         for (categories, model, price, warranty) in data:
#             categories_label = tk.Label(self, text=str(categories), anchor="w", borderwidth=2, relief="groove", padx=10)
#             model_label = tk.Label(self, text=str(model), anchor="w", borderwidth=2, relief="groove", padx=10)
#             price_label = tk.Label(self, text=str(price), anchor="w", borderwidth=2, relief="groove", padx=10)
#             warranty_label = tk.Label(self, text=str(warranty), anchor="w", borderwidth=2, relief="groove", padx=10)             


#             categories_label.grid(row=row, column=0, sticky="ew")
#             model_label.grid(row=row, column=1, sticky="ew")
#             price_label.grid(row=row, column=2, sticky="ew", )
#             warranty_label.grid(row=row, column=3, sticky="ew")
#             warranty_label.grid_columnconfigure(0, weight=5)

#             print(row)
#             action_button = tk.Button(self, text="Remove", command=lambda row = row: self.remove(row))
#             action_button.grid(row=row, column=5, sticky="ew")

#             row += 1
        
#     def remove(self, row):
#         global cart
#         cart.pop(row - 1)


class Customer_Shopping_Catalogue_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master


        tab1 = tk.Button(self, text="Shopping Catalogue", command= lambda: master.refresh("All"))
        tab1.grid(row=0, column=0, padx=(10, 5))

        #tab3 = tk.Button(self, text="Cart", command= lambda: master.goCart("Cart"))
        #tab2.pack(side="left", fill="both")
        #tab3.grid(row=0, column=1, padx=5)
        global clicked
        clicked1 = tk.StringVar()
        clicked1.set("All Categories")
        clicked2 = tk.StringVar()
        clicked2.set("All Models")
        clicked3 = tk.StringVar()
        clicked3.set("All Price")
        clicked4 = tk.StringVar()
        clicked4.set("All Color")
        clicked5 = tk.StringVar()
        clicked5.set("All Factory")
        clicked6 = tk.StringVar()
        clicked6.set("All Production year")

        # dropdown filter
        tab2 = OptionMenu(self, clicked1, "All Categories", "lights", "locks", 
        command=lambda clicked = clicked1: master.filter_status(clicked1)).grid(row=0, column=1, sticky="ew", padx=5)

        tab3 = OptionMenu(self, clicked2, "All Models", "Light1", "Light2", "SmartHome1", "locks1", "locks2", "locks3",
        command=lambda clicked = clicked2: master.filter_status(clicked2)).grid(row=0, column=2, sticky="ew", padx=5)
    
        tab4 = OptionMenu(self, clicked3, "All Price", "$50", "$60", "$70", "$100", "$120", "$l25", "$200",
        command=lambda clicked = clicked3: master.filter_status(clicked3)).grid(row=0, column=3, sticky="ew", padx=5)

        tab5 = OptionMenu(self, clicked4, "All Color", "White", "Blue", "Yellow", "Green", "Black",
        command=lambda clicked = clicked4: master.filter_status(clicked4)).grid(row=0, column=4, sticky="ew", padx=5)

        tab6 = OptionMenu(self, clicked5, "All Factory", "Malaysia", "China", "Philippines", 
        command=lambda clicked = clicked5: master.filter_status(clicked5)).grid(row=0, column=5, sticky="ew", padx=5)
    
        tab7 = OptionMenu(self, clicked6, "All Production Year", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
        command=lambda clicked = clicked6: master.filter_status(clicked6)).grid(row=0, column=6, sticky="ew", padx=5)


class Customer_Shopping_Catalogue_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.header = Customer_Shopping_Catalogue_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)

        global data
        #global cart
        self.Catalogue_Table = Catalogue_Table(data, self)
        #self.Cart_Table = Cart_Table(cart, self)

        self.header.pack(side="top", fill="x", expand=False)
        self.Catalogue_Table.pack(side="top", fill="both", expand=True)

        # self.header.pack(side="top", fill="x", expand=False)
        # self.Cart_Table.pack(side="top", fill="both", expand=True)

        self.filter = {
            "All" : lambda row: row
        }

    def show_header():
        header = Customer_Shopping_Catalogue_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        header.pack(side="top", fill="x", expand=False)

    
    def refresh(self, curr_view):

        self.Catalogue_Table.destroy()

        curr_data = products.find({})
        #curr_data = filter(self.filter.get(curr_view), curr_data)

        self.Catalogue_Table = Catalogue_Table(curr_data, self)
        self.Catalogue_Table.pack(side="top", fill="both", expand=True)
    
    
    # def goCart(self, curr_view):

    #     self.Catalogue_Table.destroy()

    #     global cart
    #     curr_data = cart.copy()

    #     self.Catalogue_Table = Cart_Table(curr_data, self)
    #     self.Catalogue_Table.pack(side="top", fill="both", expand=True)
    def filter_status(self, curr_view):
        
        self.table.destroy()

        global data
        curr_data = data.copy()

        if clicked.get() == 'lights':
            curr_data = curr_data
        
        elif clicked.get() == 'locks':
            curr_data = curr_data


        self.table = Catalogue_Table(curr_data, self)
        self.table.pack(side="top", fill="both", expand=True)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)




if __name__ == "__main__":
    main()  
