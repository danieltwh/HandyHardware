from sys import platform
from tkinter import *
import tkinter as tk
from typing import Match
from PIL import ImageTk, Image
import sqlite3

from ScrollableFrame import ScrollableFrame


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

    # def print_hello(self):
    #     print("Hello")
    #     self.after(2000, self.print_hello)


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
    # app.after(2000, app.print_hello)
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
    ("009", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("010", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "Approved"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("015", "Ethel", "Lock1", "Issue", "Canceled"),
    ("016", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("019", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "Approved"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("024", "Ethel", "Lock1", "Issue", "Canceled"),
    ("025", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("028", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "Approved"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("033", "Ethel", "Lock1", "Issue", "Canceled"),
    ("034", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("001", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "Approved"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("006", "Ethel", "Lock1", "Issue", "Canceled"),
    ("007", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("010", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "Approved"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("015", "Ethel", "Lock1", "Issue", "Canceled"),
    ("016", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("019", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "Approved"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("024", "Ethel", "Lock1", "Issue", "Canceled"),
    ("025", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment"),
    ("028", "John", "Light1", "Issue", "Submitted and Waiting for payment"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "Approved"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("033", "Ethel", "Lock1", "Issue", "Canceled"),
    ("034", "Fabian", "Lock2", "Issue", "Submitted and Waiting for payment"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Submitted and Waiting for payment")
]


service = [
    ("001", "John", "Light1", "Issue", "Waiting for approval"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "In progress"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("006", "Ethel", "Lock1", "Issue", "Completed"),
    ("007", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("010", "John", "Light1", "Issue", "Waiting for approval"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "In progress"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("015", "Ethel", "Lock1", "Issue", "Completed"),
    ("016", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("019", "John", "Light1", "Issue", "Waiting for approval"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "In progress"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("024", "Ethel", "Lock1", "Issue", "Completed"),
    ("025", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("028", "John", "Light1", "Issue", "Waiting for approval"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "In progress"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("033", "Ethel", "Lock1", "Issue", "Completed"),
    ("034", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("001", "John", "Light1", "Issue", "Waiting for approval"),
    ("002", "Ash", "Light2", "Issue", "Submitted"),
    ("003", "Bob", "Light3", "Issue", "In progress"),
    ("004", "Carly", "Lock1", "Issue", "In progress"),
    ("005", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("006", "Ethel", "Lock1", "Issue", "Completed"),
    ("007", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("008", "Giselle", "Light1", "Issue", "Submitted"),
    ("009", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("010", "John", "Light1", "Issue", "Waiting for approval"),
    ("011", "Ash", "Light2", "Issue", "Submitted"),
    ("012", "Bob", "Light3", "Issue", "In progress"),
    ("013", "Carly", "Lock1", "Issue", "In progress"),
    ("014", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("015", "Ethel", "Lock1", "Issue", "Completed"),
    ("016", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("017", "Giselle", "Light1", "Issue", "Submitted"),
    ("018", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("019", "John", "Light1", "Issue", "Waiting for approval"),
    ("020", "Ash", "Light2", "Issue", "Submitted"),
    ("021", "Bob", "Light3", "Issue", "In progress"),
    ("022", "Carly", "Lock1", "Issue", "In progress"),
    ("023", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("024", "Ethel", "Lock1", "Issue", "Completed"),
    ("025", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("026", "Giselle", "Light1", "Issue", "Submitted"),
    ("027", "Haaland", "Light3", "Issue", "Waiting for approval"),
    ("028", "John", "Light1", "Issue", "Waiting for approval"),
    ("029", "Ash", "Light2", "Issue", "Submitted"),
    ("030", "Bob", "Light3", "Issue", "In progress"),
    ("031", "Carly", "Lock1", "Issue", "In progress"),
    ("032", "Dash", "Lock2", "Issue", "Waiting for approval"),
    ("033", "Ethel", "Lock1", "Issue", "Completed"),
    ("034", "Fabian", "Lock2", "Issue", "Waiting for approval"),
    ("035", "Giselle", "Light1", "Issue", "Submitted"),
    ("036", "Haaland", "Light3", "Issue", "Waiting for approval")
]




class Request_Table(ScrollableFrame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # data = [
        #     # Nr. Name  Active
        #     [1,   "ST", True],
        #     [2,   "SO", False],
        #     [3,   "SX", True],
        #     ]

        self.data = data


        # self.vscrollbar = AutoScrollbar(self)
        # self.vscrollbar.grid(row=0, column=1, sticky=N+S)

        # self.canvas = Canvas(self, yscrollcommand=self.vscrollbar.set)
        # self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        # self.vscrollbar.config(command=self.canvas.yview)

        # # make the canvas expandable
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # self.frame = Frame(self.canvas)
        # self.frame.rowconfigure(1, weight=1)
        # self.frame.columnconfigure(1, weight=1)

        # self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # self.canvas.create_window(0, 0, anchor=NW, window=self.frame)
        # self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # self.grid_columnconfigure(1, weight=1)
        tk.Label(self.frame, text="Request ID", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="Name", anchor="w").grid(
            row=0, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(
            row=0, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Issue", anchor="w").grid(
            row=0, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Request Status", anchor="w").grid(
            row=0, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Action", anchor="w").grid(
            row=0, column=5, sticky="ew", padx=10)

        row = 1

        bg = ["#ffffff", "#d9e1f2"]

        highlight = {
            "Red": "#f8696b",
            "Green": "#63be7b",
            "Yellow": "#ffeb84"
        }

        for (requestId, name, model, issue, requestStatus) in data:
            
            requestId_label = tk.Label(self.frame, text=str(
                requestId), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            name_label = tk.Label(self.frame, text=str(
                name), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(
                model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            issue_label = tk.Label(self.frame, text=str(
                issue), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            requestStatus_label = tk.Label(self.frame, text=str(
                requestStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            # active_cb = tk.Checkbutton(self.frame, onvalue=True, offvalue=False)
            # active = True
            # if active:
            #     active_cb.select()
            # else:
            #     active_cb.deselect()

            requestId_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            name_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid_columnconfigure(0, weight=5)
            requestStatus_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            requestStatus_label.grid_columnconfigure(0, weight=5, )
            # active_cb.grid(row=row, column=4, sticky="ew")

            if requestStatus == "In progress":
                action_button = tk.Button(
                    self.frame, text="Approve", command=lambda requestId=requestId: self.approve(requestId))
                action_button.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)
            elif requestStatus == "Approved":
                action_button = tk.Button(
                    self.frame, text="Service", command=lambda requestId=requestId: self.service(requestId))
                action_button.grid(row=row, column=5, sticky="ew", pady=2.5, ipady=5)

            row += 1
        
        self.launch()
        
    #     self.canvas.create_window(0, 0, anchor=NW, window=self.frame)
    #     self.frame.update_idletasks()
    #     self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # def _on_mousewheel(self, event):
    #     if platform == "darwin":
    #         self.canvas.yview_scroll(-event.delta, "units")        
    #     elif platform == "win32":
    #         self.canvas.yview_scroll(-1 * (event.delta/120), "units") 

    def approve(self, requestId):
        print("Show approving page for ", requestId)

    def service(self, requestId):
        print("Show service page for ", requestId)


class Service_Table(ScrollableFrame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data

        tk.Label(self.frame, text="Service ID", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=10)
        tk.Label(self.frame, text="Name", anchor="w").grid(
            row=0, column=1, sticky="ew", padx=10)
        tk.Label(self.frame, text="Model", anchor="w").grid(
            row=0, column=2, sticky="ew", padx=10)
        tk.Label(self.frame, text="Issue", anchor="w").grid(
            row=0, column=3, sticky="ew", padx=10)
        tk.Label(self.frame, text="Service Status", anchor="w").grid(
            row=0, column=4, sticky="ew", padx=10)
        tk.Label(self.frame, text="Action", anchor="w").grid(
            row=0, column=5, sticky="ew", padx=10)

        row = 1

        bg = ["#ffffff", "#d9e1f2"]

        for (serviceId, name, model, issue, serviceStatus) in data:
            serviceId_label = tk.Label(self.frame, text=str(
                serviceId), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            name_label = tk.Label(self.frame, text=str(
                name), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            model_label = tk.Label(self.frame, text=str(
                model), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            issue_label = tk.Label(self.frame, text=str(
                issue), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])
            serviceStatus_label = tk.Label(self.frame, text=str(
                serviceStatus), anchor="w", borderwidth=2, relief="groove", padx=10, bg=bg[row%2])

            # active_cb = tk.Checkbutton(self.frame, onvalue=True, offvalue=False)
            # active = True
            # if active:
            #     active_cb.select()
            # else:
            #     active_cb.deselect()

            serviceId_label.grid(row=row, column=0, sticky="ew", pady=2.5, ipady=5)
            name_label.grid(row=row, column=1, sticky="ew", pady=2.5, ipady=5)
            model_label.grid(row=row, column=2, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid(row=row, column=3, sticky="ew", pady=2.5, ipady=5)
            issue_label.grid_columnconfigure(0, weight=5)
            serviceStatus_label.grid(row=row, column=4, sticky="ew", pady=2.5, ipady=5)
            serviceStatus_label.grid_columnconfigure(0, weight=5)
            # active_cb.grid(row=row, column=4, sticky="ew")

            if serviceStatus == "In progress":
                action_button = tk.Button(
                    self.frame, text="View", command=lambda serviceId=serviceId: self.view(serviceId))
                action_button.grid(row=row, column=5, sticky="ew")
            elif serviceStatus == "Completed":
                action_button = tk.Button(
                    self.frame, text="View", command=lambda serviceId=serviceId: self.view_completed(serviceId))
                action_button.grid(row=row, column=5, sticky="ew")
            else:
                action_button = tk.Button(
                    self.frame, text="View", command=lambda serviceId=serviceId: self.view(serviceId))
                action_button.grid(row=row, column=5, sticky="ew")

            row += 1
        
        self.launch()
        
    def view(self, serviceId):
        # print("Show service page for ", serviceId)
        self.master.show_service_details(serviceId)

    def view_completed(self, serviceId):
        # print("Show completed service page for ", serviceId)
        self.master.show_completed_service_details(serviceId)



class Service_Info_Page(Frame):
    def __init__(self, curr_serviceId, master):
        Frame.__init__(self, master)
        self.master = master

        data = list(filter(lambda row: row[0] == curr_serviceId, service))[0]
        print(data)
        
        # Creatinag Text Boxes
        f_name = Entry(self, width = 30)
        f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
        f_name.insert(0, data[1])

        # l_name = Entry(self, width = 30)
        # l_name .grid(row=1, column=1, padx=20)

        # GENDER = [
        #     ("Male", "M"),
        #     ("Female", "F"),
        #     ("Others", "Others")
        # ]

        # gender = StringVar()
        # gender.set("null")

        # gender_frame = LabelFrame(self, borderwidth = 0)
        # gender_frame.grid(row=2, column=1, padx=20)

        # for text, sex in GENDER:
        #     Radiobutton(gender_frame, text=text, variable=gender, value=sex).pack(side=LEFT, anchor=W)

        email = Entry(self, width = 30)
        email.grid(row=3, column=1, padx=20)

        phone = Entry(self, width = 30)
        phone.grid(row=4, column=1, padx=20)

        address = Entry(self, width = 30)
        address.grid(row=5, column=1, padx=20)

        model = Entry(self, width = 30)
        model.grid(row=6, column=1, padx=20)
        model.insert(0, data[2])


        SERVICE_STATUS = [
            "In progress",
            "Completed"
        ]

        curr_serviceStatus = StringVar()
        curr_serviceStatus.set(data[4])

        serviceStatus = OptionMenu(self, curr_serviceStatus, *SERVICE_STATUS)
        serviceStatus.config(width=28)
        serviceStatus.grid(row=7, column=1, padx=20)

        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 0))

        # l_name_label = Label(self, text="Last Name")
        # l_name_label.grid(row=1, column=0)

        # gender_label = Label(self, text="Gender")
        # gender_label.grid(row=2, column=0)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0)

        model_label = Label(self, text="Model")
        model_label.grid(row=6, column=0)

        serviceStatus_label = Label(self, text="Service Status")
        serviceStatus_label.grid(row=7, column=0)

        back_btn = Button(self, text="Back", command=lambda: master.show_service("All"))
        back_btn.grid(row=8, column=0, padx=(10,0), sticky="W")
        
        complete_btn = Button(self, text="Confirm")
        complete_btn.grid(row=8, column=1, padx=(0, 10), sticky="E")


class Completed_Service_Info_Page(Frame):
    def __init__(self, curr_serviceId, master):
        Frame.__init__(self, master)
        self.master = master

        data = list(filter(lambda row: row[0] == curr_serviceId, service))[0]
        print(data)
        
        # Creatinag Text Boxes
        f_name = tk.Label(self, text=data[1], anchor="w", borderwidth=1, relief="solid", padx=10, width=30)
        f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

        # l_name = Entry(self, width = 30)
        # l_name .grid(row=1, column=1, padx=20)

        # GENDER = [
        #     ("Male", "M"),
        #     ("Female", "F"),
        #     ("Others", "Others")
        # ]

        # gender = StringVar()
        # gender.set("null")

        # gender_frame = LabelFrame(self, borderwidth = 0)
        # gender_frame.grid(row=2, column=1, padx=20)

        # for text, sex in GENDER:
        #     Radiobutton(gender_frame, text=text, variable=gender, value=sex).pack(side=LEFT, anchor=W)

        email = tk.Label(self, text="", anchor="w", borderwidth=1, relief="solid", padx=10, width=30)
        email.grid(row=3, column=1, padx=20)

        phone = tk.Label(self, text="", anchor="w", borderwidth=1, relief="solid", padx=10, width=30)
        phone.grid(row=4, column=1, padx=20)

        address = tk.Label(self, text="", anchor="w", borderwidth=1, relief="solid", padx=10, width=30)
        address.grid(row=5, column=1, padx=20)

        model = tk.Label(self, text=data[2], anchor="w", borderwidth=1, relief="solid", padx=10, width=30)
        model.grid(row=6, column=1, padx=20)


        # SERVICE_STATUS = [
        #     "In progress",
        #     "Completed"
        # ]

        # curr_serviceStatus = StringVar()
        # curr_serviceStatus.set(data[4])

        serviceStatus = tk.Label(self, text="Completed", borderwidth=1, relief="solid", padx=10, width=30, anchor=CENTER)
        serviceStatus.grid(row=7, column=1, padx=30)

        # Creating Text Box Labels
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=0, column=0, pady=(10, 0))

        # l_name_label = Label(self, text="Last Name")
        # l_name_label.grid(row=1, column=0)

        # gender_label = Label(self, text="Gender")
        # gender_label.grid(row=2, column=0)

        email_label = Label(self, text="Email Address")
        email_label.grid(row=3, column=0)

        phone_label = Label(self, text="Phone Number")
        phone_label.grid(row=4, column=0)

        address_label = Label(self, text="Address")
        address_label.grid(row=5, column=0)

        model_label = Label(self, text="Model")
        model_label.grid(row=6, column=0)

        serviceStatus_label = Label(self, text="Service Status")
        serviceStatus_label.grid(row=7, column=0)

        back_btn = Button(self, text="Back", command=lambda: master.show_service("All"))
        back_btn.grid(row=8, column=0, padx=(10,0), sticky="W")
        
        # complete_btn = Button(self, text="Confirm")
        # complete_btn.grid(row=8, column=1, padx=(0, 10), sticky="E")




class Admin_Request_Page_Header(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        self.master = master

        tab1 = tk.Button(self, text="All Request",
                         command=lambda: master.show_request("All"))
        tab1.grid(row=0, column=0, padx=(10, 5))

        tab2 = tk.Button(self, text="Pending Approval",
                         command=lambda: master.show_request("Pending Approval"))
        # tab2.pack(side="left", fill="both")
        tab2.grid(row=0, column=1, padx=5)

        tab3 = tk.Button(self, text="Pending Service",
                         command=lambda: master.show_request("Pending Service"))
        # tab2.pack(side="left", fill="both")
        tab3.grid(row=0, column=2, padx=5)

        tab3 = tk.Button(self, text="Service Jobs",
                         command=lambda: master.show_service("All"))
        tab3.grid(row=0, column=3, padx=5)


class Admin_Request_Page(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.header = Admin_Request_Page_Header(
            self, borderwidth=0, highlightthickness=0, pady=10)

        global data
        self.table = Request_Table(data, self)

        self.header.pack(side="top", fill="x", expand=False)
        self.table.pack(side="top", fill="both", expand=True)

        self.request_filter = {
            "All": lambda row: row,
            "Pending Approval": lambda row: row[4] == "In progress",
            "Pending Service": lambda row: row[4] == "Approved"
        }

        self.service_filter = {

        }

    def show_header():
        self.header = Admin_Request_Page_Header(
            self, borderwidth=0, highlightthickness=0, pady=10)
        self.header.pack(side="top", fill="x", expand=False)

    def show_request(self, curr_view):

        self.table.destroy()

        global data
        curr_data = data.copy()
        curr_data = filter(self.request_filter.get(curr_view), curr_data)

        self.table = Request_Table(curr_data, self)
        self.table.pack(side="top", fill="both", expand=True)


    def show_service(self, curr_view):

        self.table.destroy()

        global service
        curr_data = service.copy()
        # curr_data = filter(self.filter.get(curr_view), curr_data)

        self.table = Service_Table(curr_data, self)
        self.table.pack(side="top", fill="both", expand=True)
    
    
    def show_service_details(self, serviceId):
        self.table.destroy()
        
        self.table = Service_Info_Page(serviceId, self)
        self.table.pack(side="top", fill="both", expand=True)

    
    def show_completed_service_details(self, serviceId):
        self.table.destroy()
        
        self.table = Completed_Service_Info_Page(serviceId, self)
        self.table.pack(side="top", fill="both", expand=True)


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

    



if __name__ == "__main__":
    main()
