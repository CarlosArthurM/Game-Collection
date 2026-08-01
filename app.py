import customtkinter as ctk
from pages.home import Home
from pages.search_page import SearchPage
from components.sidebar import SideBar

ctk.set_appearance_mode("Dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1120x720")
        self.resizable(False, False)
        self.title("Game Collection")

        self.sidebar = SideBar(self)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.home = Home(self)
        self.search_page = SearchPage(self)
        self.pages = [self.home, self.search_page]

        self.sidebar.btn_explore.configure(command=lambda: self.redirect_page(self.search_page))
        self.sidebar.btn_list.configure(command=lambda: self.redirect_page(...))
        self.sidebar.btn_config.configure(command=lambda: self.redirect_page(...))

        self.redirect_page(self.home)

    def redirect_page(self, page):
        for p in self.pages:
            p.pack_forget()
        page.pack(fill="both", expand=True, padx=(0,10), pady=10)

app = App()
app.mainloop()
