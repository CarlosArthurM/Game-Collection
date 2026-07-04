import customtkinter as ctk

class Home(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.greeting = ctk.CTkLabel(self, text="Hi, Welcome :)", font=("Arial", 20))
        self.greeting.grid(row=1, column=0)

