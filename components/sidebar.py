import customtkinter as ctk
from .button_sidebar import ButtonSideBar

class SideBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=200, corner_radius=10)
        self.pack_propagate(False)

        self.btn_logout = ctk.CTkButton(self, text="Logout", fg_color="#2b2b2b", hover_color="#C70000", height=50, corner_radius=10, command=self.logout)
        self.btn_logout.pack(side="bottom", fill="x", pady=5)

        self.btn_explore = ButtonSideBar(self, text="Search a Game")
        self.btn_explore.pack(padx=5, pady=5, fill="x")

        self.btn_list = ButtonSideBar(self, text="My Lists")
        self.btn_list.pack(padx=5, pady=5, fill="x")
        
        self.btn_config = ButtonSideBar(self, text="Config")
        self.btn_config.pack(padx=5, pady=5, fill="x")

    
    def logout(self):
        self.winfo_toplevel().destroy()

