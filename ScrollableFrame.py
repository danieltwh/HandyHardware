from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3


# ScrollBar Class
class AutoScrollbar(Scrollbar):
    # A scrollbar that hides itself if it"s not needed.
    # Only works if you use the grid geometry manager!
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")


# Scrollable Frame
class ScrollableFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.vscrollbar = AutoScrollbar(self)
        self.vscrollbar.grid(row=0, column=1, sticky=N+S)

        self.canvas = Canvas(self, yscrollcommand=self.vscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        self.vscrollbar.config(command=self.canvas.yview)

        # make the canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = Frame(self.canvas)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.create_window(0, 0, anchor=NW, window=self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def launch(self):
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def yview(self, *args):
        if self.canvas.yview() == (0.0, 1.0):
            return
        self.canvas.yview(*args)


    def _on_mousewheel(self, event):
        # if platform == "darwin":
        #     self.canvas.yview_scroll(-event.delta, "units")        
        # elif platform == "win32":
        #     self.canvas.yview_scroll(-1 * (event.delta/120), "units") 

        if platform == "darwin":
            self.yview("scroll", int(-event.delta), "units")        
        elif platform == "win32":
            self.yview("scroll", int(-1 * (event.delta/120)), "units") 