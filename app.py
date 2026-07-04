import customtkinter as ctk
from pages.home import Home

ctk.set_appearance_mode("Dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.resizable(False, False)
        self.title("Game Collection")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.home = Home(self)
        self.home.grid(row=0, column=1, sticky="nsew")

        self.paginas = [self.home]

app = App()
app.mainloop()