import customtkinter as ctk
from database.lists import get_all_lists
from config import COLUMNS


class ListPage(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent, segmented_button_selected_color="#50007E", segmented_button_selected_hover_color="#3A005C", segmented_button_unselected_hover_color="#2A0040", corner_radius=10)
        self.render()

    def render(self):
        for tab in self._tab_dict.copy():
            self.delete(tab)

        lists = get_all_lists()

        if not lists:
            self.add("No lists yet")

        for list_id, list_name in lists:
            self.add(list_name)

            frame = ctk.CTkScrollableFrame(self.tab(list_name))
            frame.pack(fill="both", expand=True, padx=5, pady=5)

            for c in range(COLUMNS):
                frame.columnconfigure(c, weight=1)

