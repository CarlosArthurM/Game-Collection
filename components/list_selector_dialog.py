import customtkinter as ctk
from database.lists import get_all_lists


class ListSelectorDialog(ctk.CTkToplevel):
    def __init__(self, parent, game, on_confirm):
        super().__init__(parent)
        self.geometry("300x400")
        self.title("Add to list")
        self.grab_set()

        self.game = game
        self.on_confirm = on_confirm

        ctk.CTkLabel(self, text="Select a list", font=("Arial", 16, "bold")).pack(pady=20)

        lists = get_all_lists()

        if not lists:
            ctk.CTkLabel(self, text="No lists yet").pack(pady=10)
        else:
            scroll = ctk.CTkScrollableFrame(self)
            scroll.pack(padx=10, pady=10, fill="both", expand=True)

            for list_id, list_name in lists:
                ctk.CTkButton(scroll, text=list_name,fg_color="#50007E", hover_color="#370057", command=lambda lid=list_id: self._confirm(lid)).pack(padx=5, pady=5, fill="x")

        ctk.CTkButton(self, text="Cancel", fg_color="transparent", hover_color="#2A2A2A", command=self.destroy).pack(padx=20, pady=(10,20), fill="x")


    def _confirm(self, list_id):
        self.on_confirm(self.game, list_id)
        self.destroy()