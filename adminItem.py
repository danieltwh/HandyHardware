from datetime import date
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3
import pymongo
from tkinter.messagebox import askyesno, askquestion

# For SQL query
from sqlalchemy import create_engine
from pymysql.constants import CLIENT
import pandas as pd

from config import USERNAME, MYSQL_PASSWORD
db = create_engine(f"mysql+pymysql://{USERNAME}:{MYSQL_PASSWORD}@127.0.0.1:3306/ECOMMERCE", 
        connect_args = {"client_flag": CLIENT.MULTI_STATEMENTS}
    )

# For mongodb query
from pymongo import MongoClient

#get data from mongodb
client = MongoClient()
mydb = client.Assignment
products = mydb.products
items = mydb.items
data = products.find({})

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Admin_Shopping_Catalogue_Page)

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
        tk.Label(self, text="Cost ($)", anchor="w").grid(row=0, column=2, sticky="ew", padx=10)
        tk.Label(self, text="Price ($)", anchor="w").grid(row=0, column=3, sticky="ew", padx=10)
        tk.Label(self, text="Warranty (months)", anchor="w").grid(row=0, column=4, sticky="ew", padx=10)
        tk.Label(self, text="Number of Item Sold", anchor="w").grid(row=0, column=5, sticky="ew", padx=10)
        tk.Label(self, text="Number of Item Available", anchor="w").grid(row=0, column=6, sticky="ew", padx=10)
        items = mydb.items

        bg = ["#ffffff", "#d9e1f2"]
        row = 1
        for dic in data:
            categories_label = tk.Label(self, text=str(dic["Category"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self, text=str(dic["Model"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            cost_label = tk.Label(self, text=str(dic["Cost ($)"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            price_label = tk.Label(self, text=str(dic["Price ($)"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            warranty_label = tk.Label(self, text=str(dic["Warranty (months)"]), anchor="w", borderwidth=2, relief="groove", padx=10,bg=bg[row%2]) 
            numberOfItemsSold_label = tk.Label(self, text=str(items.count_documents({"Category": dic["Category"], "Model": dic["Model"], "PurchaseStatus": "Sold"})), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])             
            numberOfItemsAvailable_label = tk.Label(self, text=str(items.count_documents({"Category": dic["Category"], "Model": dic["Model"], "PurchaseStatus": "Unsold"})), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            categories_label.grid(row=row, column=0, sticky="ew")
            model_label.grid(row=row, column=1, sticky="ew")
            cost_label.grid(row=row, column=2, sticky="ew")
            price_label.grid(row=row, column=3, sticky="ew", )
            warranty_label.grid(row=row, column=4, sticky="ew")
            warranty_label.grid_columnconfigure(0, weight=5)
            numberOfItemsSold_label.grid(row=row, column=5, sticky="ew")
            numberOfItemsSold_label.grid_columnconfigure(0, weight=5)       
            numberOfItemsAvailable_label.grid(row=row, column=6, sticky="ew")
            numberOfItemsAvailable_label.grid_columnconfigure(0, weight=5)

            row += 1

class Advance_Table(tk.LabelFrame):
    def __init__(self, data, *args, **kwargs):
        tk.LabelFrame.__init__(self, width=800, height=800, *args, **kwargs)

        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Categories", anchor="w").grid(row=0, column=0, sticky="ew", padx=10)
        tk.Label(self, text="Model", anchor="w").grid(row=0, column=1, sticky="ew", padx=10)
        tk.Label(self, text="Cost ($)", anchor="w").grid(row=0, column=2, sticky="ew", padx=10)
        tk.Label(self, text="Price ($)", anchor="w").grid(row=0, column=3, sticky="ew", padx=10)
        tk.Label(self, text="Warranty (months)", anchor="w").grid(row=0, column=4, sticky="ew", padx=10)
        tk.Label(self, text="Number of Item Sold", anchor="w").grid(row=0, column=5, sticky="ew", padx=10)
        tk.Label(self, text="Number of Item Available", anchor="w").grid(row=0, column=6, sticky="ew", padx=10)
        
        items_data = data
        products_data = products.find({})

        bg = ["#ffffff", "#d9e1f2"]
        row = 1
        for dic in products_data:

            if self.master.clicked2.get() != "Filter 1: All Cost":
                if int(dic["Cost ($)"]) != int(self.master.clicked2.get()[1:]):
                    continue

            if self.master.clicked3.get() != "Filter 2: All Price":
                if int(dic["Price ($)"]) != int(self.master.clicked3.get()[1:]):
                    continue

            if self.master.clicked1.get() == "Category: Lights":
                if dic["Category"] != "Lights":
                    continue

            if self.master.clicked1.get() == "Category: Locks":
                if dic["Category"] != "Locks":
                    continue  

            if self.master.clicked1.get() == "Model: Light1":
                if dic["Model"] != "Light1":
                    continue  

            if self.master.clicked1.get() == "Model: Light2":
                if dic["Model"] != "Light2":
                    continue  
            
            if self.master.clicked1.get() == "Model: Safe1":
                if dic["Model"] != "Safe1":
                    continue  

            if self.master.clicked1.get() == "Model: Safe2":
                if dic["Model"] != "Safe2":
                    continue  
            
            if self.master.clicked1.get() == "Model: Safe3":
                if dic["Model"] != "Safe3":
                    continue  

            if self.master.clicked1.get() == "Model: SmartHome1":
                if dic["Model"] != "SmartHome1":
                    continue  

            categories_label = tk.Label(self, text=str(dic["Category"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self, text=str(dic["Model"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            cost_label = tk.Label(self, text=str(dic["Cost ($)"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            price_label = tk.Label(self, text=str(dic["Price ($)"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            warranty_label = tk.Label(self, text=str(dic["Warranty (months)"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])  
            
            count = 0
            for idic in items_data:
                if idic['PurchaseStatus'] == 'Sold':
                    if dic['Category'] == idic['Category']:
                        if dic['Model'] == idic['Model']:
                            count += 1
            numberOfItemsSold_label = tk.Label(self, text=str(count), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            count = 0
            for idic in items_data:
                if idic['PurchaseStatus'] == 'Unsold':
                    if dic['Category'] == idic['Category']:
                        if dic['Model'] == idic['Model']:
                            count += 1
            numberOfItemsAvailable_label = tk.Label(self, text=str(count), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            categories_label.grid(row=row, column=0, sticky="ew")
            model_label.grid(row=row, column=1, sticky="ew")
            cost_label.grid(row=row, column=2, sticky="ew")
            price_label.grid(row=row, column=3, sticky="ew", )
            warranty_label.grid(row=row, column=4, sticky="ew")
            warranty_label.grid_columnconfigure(0, weight=5)
            numberOfItemsSold_label.grid(row=row, column=5, sticky="ew")
            numberOfItemsSold_label.grid_columnconfigure(0, weight=5)       
            numberOfItemsAvailable_label.grid(row=row, column=6, sticky="ew")
            numberOfItemsAvailable_label.grid_columnconfigure(0, weight=5)

            row += 1

class Admin_Shopping_Catalogue_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        tab1 = tk.Button(self, text="Refresh Shopping Catalogue", command= lambda: master.refresh("All"))
        tab1.grid(row=0, column=0, padx=(10, 5))

        #tab3 = tk.Button(self, text="Cart", command= lambda: master.goCart("Cart"))
        #tab2.pack(side="left", fill="both")
        #tab3.grid(row=0, column=1, padx=5)
        # global clicked1
        # global clicked2
        # global clicked3
        # global clicked4
        # global clicked5
        # global clicked6
        # clicked1 = tk.StringVar()
        # clicked1.set("All Categories & Models")
        # clicked2 = tk.StringVar()
        # clicked2.set("Filter 1: All Cost")
        # clicked3 = tk.StringVar()
        # clicked3.set("Filter 2: All Price")
        # clicked4 = tk.StringVar()
        # clicked4.set("Filter 3: All Color")
        # clicked5 = tk.StringVar()
        # clicked5.set("Filter 4: All Factory")
        # clicked6 = tk.StringVar()
        # clicked6.set("Filter 5: All Production Year")

        self.master.clicked1.set("All Categories & Models")
        self.master.clicked2.set("Filter 1: All Cost")
        self.master.clicked3.set("Filter 2: All Price")
        self.master.clicked4.set("Filter 3: All Color")
        self.master.clicked5.set("Filter 4: All Factory")
        self.master.clicked6.set("Filter 5: All Production Year")

        # dropdown filter
        # tab2 = OptionMenu(self, clicked1, "Simple Search", "Category: Lights", "Category: Locks", "Model: Light1", "Model: Light2", "Model: SmartHome1", "Model: Safe1", "Model: Safe2", "Model: Safe3",
        # command=lambda clicked1 = clicked1: master.filter_status1(clicked1)).grid(row=0, column=1, sticky="ew", padx=5)

        tab2 = OptionMenu(self, self.master.clicked1, "All Models", "Category: Lights", "Category: Locks", "Model: Light1", "Model: Light2", "Model: SmartHome1", "Model: Safe1", "Model: Safe2", "Model: Safe3").grid(row=0, column=1, sticky="ew", padx=5)
        tab9 = tk.Button(self, text="Simple Search", command=lambda clicked1 = self.master.clicked1: master.filter_status1(self.master.clicked1)).grid(row=0, column=2, sticky="ew", padx=5) 

        tab3 = OptionMenu(self, self.master.clicked2, "Filter 1: All Cost", "$20", "$22", "$30", "$50", "$100").grid(row=2, column=0, sticky="ew", padx=5)
        tab4 = OptionMenu(self, self.master.clicked3, "Filter 2: All Price", "$50", "$60", "$70", "$100", "$120", "$125", "$200").grid(row=2, column=1, sticky="ew", padx=5)
        tab5 = OptionMenu(self, self.master.clicked4, "Filter 3: All Color", "White", "Blue", "Yellow", "Green", "Black").grid(row=2, column=2, sticky="ew", padx=5)
        tab6 = OptionMenu(self, self.master.clicked5, "Filter 4: All Factory", "Malaysia", "China", "Philippines").grid(row=2, column=3, sticky="ew", padx=5)
        tab7 = OptionMenu(self, self.master.clicked6, "Filter 5: All Production Year", "2014", "2015", "2016", "2017", "2018", "2019", "2020").grid(row=2, column=4, sticky="ew", padx=5)
        tab8 = tk.Button(self, text="Advanced Search", command= lambda: master.filter_status2(self.master.clicked2, self.master.clicked3, self.master.clicked4, self.master.clicked5, self.master.clicked6)).grid(row=2, column=5, sticky="ew", padx=5)
        tab9 = tk.Entry(self)
        tab9.grid(row=3, column=0, sticky="ew", padx=5)
        tab10 = tk.Button(self, text="Search Item ID", command=lambda: master.filter_status3(tab9.get())).grid(row=3, column=1, sticky="ew", padx=5)

class Admin_Shopping_Catalogue_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        curr_data = products.find({})
        item_curr_data = items.find({}).limit(1)

        self.clicked1 = tk.StringVar()
        self.clicked2 = tk.StringVar()
        self.clicked3 = tk.StringVar()
        self.clicked4 = tk.StringVar()
        self.clicked5 = tk.StringVar()
        self.clicked6 = tk.StringVar()  
        self.clicked7 = tk.StringVar() 

        self.header = Admin_Shopping_Catalogue_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        self.header.pack(side="top", fill="x", expand=False)

        # global data
        # self.Catalogue_Table = Catalogue_Table(data, self)

        self.Catalogue_Table = Catalogue_Table(curr_data, self)
        self.Catalogue_Table.pack(side="top", fill="both", expand=True)

        # self.header = Item_Table_Header.pack(self, borderwidth=0, highlightthickness=0, pady=10)

        # self.Item_Table_Header =  Item_Table_Header(master, self)
        # self.Item_Table_Header.pack(side="top", fill="both", expand=True)

        self.Item_Table = Item_Table(item_curr_data, self)
        self.Item_Table.pack(side="bottom", fill="both", expand=True)

       

        # self.filter = {
        #     "All" : lambda row: row
        # }

    # def show_header():
    #     header = Admin_Shopping_Catalogue_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
    #     header.pack(side="top", fill="x", expand=False)

    
    def refresh(self, curr_view):

        self.Catalogue_Table.destroy()
        self.header.destroy()

        curr_data = products.find({})
        #curr_data = filter(self.filter.get(curr_view), curr_data)

        self.header = Admin_Shopping_Catalogue_Page_Header(self, borderwidth=0, highlightthickness = 0, pady=10)
        self.header.pack(side="top", fill="x", expand=False)
        self.Catalogue_Table = Catalogue_Table(curr_data, self)
        self.Catalogue_Table.pack(side="top", fill="both", expand=True)
    

    def filter_status1(self, curr_view):
        self.clicked2.set("Filter 1: All Cost")
        self.clicked3.set("Filter 2: All Price")
        self.clicked4.set("Filter 3: All Color")
        self.clicked5.set("Filter 4: All Factory")
        self.clicked6.set("Filter 5: All Production Year")    

        self.Catalogue_Table.destroy()
        curr_data = products.find({})
        
        if self.clicked1.get() == 'Category: Lights':
            curr_data = products.find({"Category": "Lights"})    
        elif self.clicked1.get() == 'Category: Locks':
            curr_data = products.find({"Category": "Locks"})
        elif self.clicked1.get() == 'Model: Light1':
            curr_data = products.find({"Model": "Light1"})    
        elif self.clicked1.get() == 'Model: Light2':
            curr_data = products.find({"Model": "Light2"})    
        elif self.clicked1.get() == 'Model: Safe1':
            curr_data = products.find({"Model": "Safe1"})
        elif self.clicked1.get() == 'Model: Safe2':
            curr_data = products.find({"Model": "Safe2"})
        elif self.clicked1.get() == 'Model: Safe3':
            curr_data = products.find({"Model": "Safe3"})
        elif self.clicked1.get() == 'Model: SmartHome1':
            curr_data = products.find({"Model": "SmartHome1"})

        self.Catalogue_Table = Catalogue_Table(curr_data, self)
        self.Catalogue_Table.pack(side="top", fill="both", expand=True)
    
    def filter_status2(self, c2, c3, c4, c5, c6):
        
        self.Catalogue_Table.destroy()
        items_data = list(items.find({}))
        # cost_list = ["$20", "$22", "$30", "$50", "$100"]
        price_list = ["$50", "$60", "$100", "$120", "$125"]
        model_list = ["Light1", "Light2", "Safe1", "Safe2", "Safe3"]

        for dic in items_data.copy():
            # if c2.get() != "Filter 1: All Cost":
            #     if dic["Cost ($)"] != c2.get():
            #         if dic in items_data:
            #             items_data.remove(dic)
            # if c3.get() != "Filter 2: All Price":
            #     if dic["Price ($)"] != c3.get():
            #         if dic in items_data:
            #             items_data.remove(dic)

            if c4.get() != "Filter 3: All Color":
                if dic["Color"] != c4.get():
                    if dic in items_data:
                        items_data.remove(dic)
            if c5.get() != "Filter 4: All Factory":
                if dic['Factory'] != c5.get():
                    if dic in items_data:
                        items_data.remove(dic)
            if c6.get() != "Filter 5: All Production Year":
                if dic['ProductionYear'] != int(c6.get()):
                    if dic in items_data:
                        items_data.remove(dic)

            # Cost Adv Filter
            # if c2.get() == "$30":
            #     if dic['Category'] != 'Lights':
            #         if dic in items_data:
            #             items_data.remove(dic)
            #     else:
            #         if dic['Model'] != 'SmartHome1':
            #             if dic in items_data:
            #                 items_data.remove(dic)

            # if c2.get() == "$100":
            #     if dic['Category'] != 'Locks':
            #         if dic in items_data:
            #             items_data.remove(dic)
            #     else:
            #         if dic['Model'] != 'SmartHome1':
            #             if dic in items_data:
            #                 items_data.remove(dic) 


            # Price Adv Filter
            if c3.get() == "$70":
                if dic['Category'] != 'Lights':
                    if dic in items_data:
                        items_data.remove(dic)
                else:
                    if dic['Model'] != 'SmartHome1':
                        if dic in items_data:
                            items_data.remove(dic)

            if c3.get() == "$200":
                if dic['Category'] != 'Locks':
                    if dic in items_data:
                        items_data.remove(dic)
                else:
                    if dic['Model'] != 'SmartHome1':
                        if dic in items_data:
                            items_data.remove(dic)   

            # for i in range(len(cost_list)):
            #     if c2.get() == cost_list[i]:
            #         if dic['Model'] != model_list[i]:
            #             if dic in items_data:
            #                 items_data.remove(dic)
            #                 break

            if self.clicked1.get() == 'Category: Lights':
                if dic['Category'] != 'Lights':
                    if dic in items_data:
                        items_data.remove(dic)
            elif self.clicked1.get() == 'Category: Locks':
                if dic['Category'] != "Locks":
                    if dic in items_data:
                        items_data.remove(dic)
            elif self.clicked1.get() == 'Model: Light1':
                if dic['Model'] != "Light1":
                    if dic in items_data:
                        items_data.remove(dic)
            elif self.clicked1.get() == 'Model: Light2':
                if dic['Model'] != "Light2":
                    if dic in items_data:
                        items_data.remove(dic)
            elif self.clicked1.get() == 'Model: Safe1':
                if dic['Model'] != "Safe1":
                    if dic in items_data:
                        items_data.remove(dic)
            elif self.clicked1.get() == 'Model: Safe2':
                if dic['Model'] != "Safe2":
                    if dic in items_data:
                        items_data.remove(dic)
            elif self.clicked1.get() == 'Model: Safe3':
                if dic['Model'] != "Safe3":
                    if dic in items_data:
                        items_data.remove(dic)
            elif self.clicked1.get() == 'Model: SmartHome1':
                if dic['Model'] != "SmartHome1":
                    if dic in items_data:
                        items_data.remove(dic)

            for i in range(len(price_list)):
                if c3.get() == price_list[i]:
                    if dic['Model'] != model_list[i]:
                        if dic in items_data:
                            items_data.remove(dic)
                            break

        self.Catalogue_Table = Advance_Table(items_data, self)
        self.Catalogue_Table.pack(side="top", fill="both", expand=True)

    def filter_status3(self, result):
        # print(str(result))
        self.Item_Table.destroy()
        itemID = result
        item_curr_data = items.find({"ItemID": str(itemID)})
        self.Item_Table = Item_Table(item_curr_data, self)
        self.Item_Table.pack(side="bottom", fill="both", expand=True)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

# class Item_Table_Header(tk.LabelFrame):
#     def __init__(self, master, *args, **kwargs):
#         tk.LabelFrame.__init__(self, width=800, height=800, *args, **kwargs)
#         searchBar = tk.Entry(self)
#         searchBar.grid(row=0, column=0, sticky="ew", padx=5)
#         searchButton = tk.Button(self, text="Search Item ID", command=lambda: master.filter_status3(searchBar.get())).grid(row=0, column=1, sticky="ew", padx=5)


class Item_Table(tk.LabelFrame):
    def __init__(self, data, *args, **kwargs):
        tk.LabelFrame.__init__(self, width=800, height=800, *args, **kwargs)

        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Item ID", anchor="w").grid(row=0, column=0, sticky="ew", padx=10)
        tk.Label(self, text="Category", anchor="w").grid(row=0, column=1, sticky="ew", padx=10)
        tk.Label(self, text="Color", anchor="w").grid(row=0, column=2, sticky="ew", padx=10)
        tk.Label(self, text="Factory", anchor="w").grid(row=0, column=3, sticky="ew", padx=10)
        tk.Label(self, text="Power Supply", anchor="w").grid(row=0, column=4, sticky="ew", padx=10)
        tk.Label(self, text="Purchase Status", anchor="w").grid(row=0, column=5, sticky="ew", padx=10)
        tk.Label(self, text="Production Year", anchor="w").grid(row=0, column=6, sticky="ew", padx=10)
        tk.Label(self, text="Model", anchor="w").grid(row=0, column=7, sticky="ew", padx=10)
        tk.Label(self, text="Service Status", anchor="w").grid(row=0, column=8, sticky="ew", padx=10)     

        bg = ["#ffffff", "#d9e1f2"]
        row = 1
        for dic in data:
            itemID_label = tk.Label(self, text=str(dic["ItemID"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            category_label = tk.Label(self, text=str(dic["Category"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            color_label = tk.Label(self, text=str(dic["Color"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            factory_label = tk.Label(self, text=str(dic["Factory"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            powerSupply_label = tk.Label(self, text=str(dic["PowerSupply"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            purchaseStatus_label = tk.Label(self, text=str(dic["PurchaseStatus"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            productionYear_label = tk.Label(self, text=str(dic["ProductionYear"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self, text=str(dic["Model"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            serviceStatus_label = tk.Label(self, text=str(dic["ServiceStatus"]), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            itemID_label.grid(row=row, column=0, sticky="ew")
            category_label.grid(row=row, column=1, sticky="ew")
            color_label.grid(row=row, column=2, sticky="ew")
            factory_label.grid(row=row, column=3, sticky="ew")
            powerSupply_label.grid(row=row, column=4, sticky="ew")
            purchaseStatus_label.grid(row=row, column=5, sticky="ew")
            productionYear_label.grid(row=row, column=6, sticky="ew")
            model_label.grid(row=row, column=7, sticky="ew")
            serviceStatus_label.grid(row=row, column=8, sticky="ew")

            row += 1






if __name__ == "__main__":
    main()  
