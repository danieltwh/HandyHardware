from tkinter import *
from typing import Match
from PIL import ImageTk, Image
import sqlite3

########### Customer item page ###########
class customerItem_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        
        def show():
            conn = sqlite3.connect('products.db')

            c = conn.cursor()

            c.execute('''
                SELECT * FROM products
            ''', [''])

            for product in c.fetchall():
                print(product)
            
            conn.commit()
            conn.close()
        
        filter_btn = Button(self, text="FILTER", command = show)