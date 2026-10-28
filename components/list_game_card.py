import customtkinter as ctk
from components.game_card import GameCard


class ListGameCard(GameCard):
    def __init__(self, parent, game, show_game_details, on_remove):
        super().__init__(parent, game, show_game_details)
        self.columnconfigure(0, weight=1)
        ctk.CTkButton(
            self,
            text="Remove",
            font=("Arial", 12),
            fg_color="#CA0000",
            hover_color="#A50000",
            command=lambda: on_remove(game)
        ).grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")