from tkinter import *
from typing import Match
from PIL import ImageTk, Image
import sqlite3

########### Customer item page ###########
class customerItem_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        getProducts()

    def getProducts():
        my_conn = sqlite3.connect('products.db')
        r_set=my_conn.execute('''SELECT * from products''');
        i=0 # row value inside the loop 
        for product in r_set: 
            for j in range(len(product)):
                e = Entry(self, width=10, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, product[j])
            i=i+1