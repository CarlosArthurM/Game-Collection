import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
import threading

class GameCard(ctk.CTkFrame):
    def __init__(self, parent, game, show_game_details):
        super().__init__(parent, corner_radius=10)
        self.columnconfigure(0, weight=1)

        self.cover_label = ctk.CTkLabel(self, text="Loading...", width=200, height=120)
        self.cover_label.grid(row=0, column=0, padx=10, pady=(10,5))

        ctk.CTkLabel(self, text=game["name"], font=("Arial", 13, "bold"), wraplength=180).grid(row=1, column=0, padx=10, pady=(5,2))

        platforms = ", ".join([p["name"] for p in game.get("platforms", [])])
        ctk.CTkLabel(self, text=platforms, font=("Arial", 10), text_color="#7777AA", wraplength=200, justify="left").grid(row=2, column=0, padx=12, pady=(0, 6), sticky="w")

        ctk.CTkButton(self, text="see more...", font=("Arial", 12), fg_color="#50007E", hover_color="#370057", command= lambda : show_game_details(game)).grid(row=4, column=0, padx=10, pady=(5,10), sticky="ew")

        self._get_game_cover(game)

    def _get_game_cover(self,game):
        if game.get("cover"):
            threading.Thread(
                target=self._load_cover,
                args=(game["cover"],),
                daemon=True
            ).start()

    def _load_cover(self, url):
        try:
            response = requests.get(f"https:{url}")
            img = Image.open(BytesIO(response.content)).resize((250, 200))
            ctk_img = ctk.CTkImage(img, size=(250, 200))
            self.after(0, lambda : self.cover_label.configure(image=ctk_img, text=""))
        except Exception:
            self.after(0, lambda : self.cover_label.configure(text="without a cover"))