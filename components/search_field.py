import customtkinter as ctk

class SearchField(ctk.CTkEntry):
    def __init__(self,parent):
        super().__init__(parent, corner_radius=20, width=350, font=("Arial", 14))