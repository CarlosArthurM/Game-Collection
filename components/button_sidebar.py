import customtkinter as ctk

class ButtonSideBar(ctk.CTkButton):
    def __init__(self, parent, text):
        super().__init__(parent, text=text, fg_color="transparent", hover_color="#50007E", corner_radius=10, height=40)

