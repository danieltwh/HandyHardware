import tkinter  as tk 
from tkinter import *
from typing import Match
from PIL import ImageTk, Image
import sqlite3
from login import Login_Page
from customerItem import customerItem_Page
from customer_request import Request_Page


#print(TkVersion)

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Request_Page)

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

if __name__ == "__main__":
    main()