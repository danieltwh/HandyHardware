from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3

from ScrollableFrame import ScrollableFrame

# database connection 
conn = sqlite3.connect('items.db')
global c
c = conn.cursor()

c.execute(
    '''
    SELECT * 
    FROM items
    LIMIT 30
    '''
    )

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Past_Purchases)

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



class Past_Purchases(ScrollableFrame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data
        

        tk.Label(self.frame, text="Product", anchor="w").grid(
            row=1, column=0, sticky="ew", padx=10)

        tk.Label(self.frame, text="Model", anchor="w").grid(
            row=1, column=1, sticky="ew", padx=10)

        tk.Label(self.frame, text="Colour", anchor="w").grid(
            row=1, column=2, sticky="ew", padx=10)

        tk.Label(self.frame, text="Power Supply", anchor="w").grid(
            row=1, column=3, sticky="ew", padx=10)

        tk.Label(self.frame, text="Production Year", anchor="w").grid(
            row=1, column=4, sticky="ew", padx=10)

        tk.Label(self.frame, text="Factory", anchor="w").grid(
            row=1, column=5, sticky="ew", padx=10)

        tk.Label(self.frame, text="Service Status", anchor="w").grid(
            row=1, column=6, sticky="ew", padx=10)

        global clicked
        clicked = StringVar()
        clicked.set('NONE')
        OptionMenu(self.frame, clicked, 'Battery', 'USB','NA', 'SUBMITTED', 'WAITING FOR PAYMENT', 'IN PROGRESS', 'APPROVED', 'CANCELLED', 'NONE').grid(
            row=0, column=6, sticky="ew", padx=10
        )

        row = 2

        bg = ["#ffffff", "#d9e1f2"]

        highlight = {
            "Red": "#f8696b",
            "Green": "#63be7b",
            "Yellow": "#ffeb84"
        }

        for (ItemID, category, colour, factory, powerSupply, PurchaseStatus, ProductionYear, Model, ServiceStatus) in c.fetchall():
            
            product_label = tk.Label(self.frame, text=str(
                category), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            model_label = tk.Label(self.frame, text=str(
                Model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            colour_label = tk.Label(self.frame, text=str(
                colour), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            powerSupply_label = tk.Label(self.frame, text=str(
                powerSupply), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            productionYear_label = tk.Label(self.frame, text=str(
                ProductionYear), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            factory_label = tk.Label(self.frame, text=str(
                factory), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
                        
            serviceStatus_label = tk.Label(self.frame, text=str(
                ServiceStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])


            product_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            colour_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            powerSupply_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            productionYear_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            factory_label.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            serviceStatus_label.grid(row=row, column=6, sticky="ew", pady=2.5, ipady=5)

            requestButton = tk.Button(self.frame, text='Request details')
            requestButton.grid(row=row, column=7, sticky="ew", pady=2.5, ipady=5)

            row += 1
        
        self.launch()

        
if __name__ == "__main__":
    main()
