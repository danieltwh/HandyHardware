import tkinter  as tk 
from tkinter import *
from typing import Match
from PIL import ImageTk, Image
import sqlite3
my_conn = sqlite3.connect('item.db')

########### Customer item page ###########
class customerItem_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        e=Label(self,width=10,text='item',borderwidth=2, relief='ridge',anchor='w',bg='yellow')
        e.grid(row=0,column=0)
        e=Label(self,width=10,text='quantity',borderwidth=2, relief='ridge',anchor='w',bg='yellow')
        e.grid(row=0,column=1)
        e=Label(self,width=10,text='price',borderwidth=2, relief='ridge',anchor='w',bg='yellow')
        e.grid(row=0,column=2)

        i=1

        r_set=my_conn.execute("SELECT * FROM items")
        for items in r_set: 
            for j in range(len(items)):
                e = Entry(self, width=10, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, items[j])
            i=i+1
        