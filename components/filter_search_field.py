import customtkinter as ctk

class FilterCombox(ctk.CTkComboBox):
    def __init__(self, parent):
        super().__init__(parent, values=["PC","PlayStation","Xbox","Nintendo"], corner_radius=10, state="readonly", width=150)
        self.set("Select a platform")