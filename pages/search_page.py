import threading
import customtkinter as ctk
from components.game_card import GameCard
from components.search_field import SearchField
import requests
from config import ACCESS_TOKEN, CLIENT_ID, BASE_URL
from utils.utils import destroy_widgets


class SearchPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=10)
        self.COLUNAS = 3

        self.search_field = SearchField(self)
        self.search_field.bind("<Return>", lambda e: self.search_game())
        self.search_field.pack(pady=5)

        self.frame_result = ctk.CTkScrollableFrame(self)
        self.frame_result.pack(padx=5, pady=5, fill="both", expand=True)

        self._show_placeholder()

    def search_game(self):
        name = self.search_field.get()

        if not name:
            return

        self.search_field.configure(state="disabled")

        thread = threading.Thread(target=self._search_thread, args=(name,), daemon=True)
        thread.start()


    def _search_thread(self, name):
        response = requests.post(
            f"{BASE_URL}/games",
            headers={
                "Client-ID": CLIENT_ID,
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            },
            data=f'''search "{name}";fields name,cover.url,rating,parent_game,game_type.type,platforms.name,platforms.platform_logo.url;where game_type = (0,8,9); limit 40;'''
        )

        if not self._is_valid_response(response):
            self.after(0, lambda: self._show_error("No results found..."))
            self.after(0, lambda: self.search_field.configure(state="normal"))
            return

        result = self._format_response(response.json())
        self.after(0, lambda : self._show_result(result))
        self.after(0, lambda : self.search_field.configure(state="normal"))


    def _is_valid_response(self,response) -> bool:
        return response.status_code == 200 and response.json() != []


    def _show_error(self,message: str):
        destroy_widgets(self.frame_result)
        ctk.CTkLabel(self.frame_result, text=message, font=("Arial", 20, "bold"), text_color="#FF0000").pack(pady=300)
        self.after(0, lambda : self.search_field.configure(state="normal"))


    def _format_response(self,games)-> list:
        result = [
            {
                "igdb_ID": game["id"],
                "name": game["name"],
                "cover": game.get("cover", {}).get("url", "").replace("t_thumb", "t_cover_big"),
                "rating": round(game.get("rating", 0) / 20, 1),
                "platforms": [
                    {
                        "name": p["name"],
                        "logo": p.get("platform_logo", {}).get("url", "").replace("t_thumb", "t_logo_med")
                    }
                    for p in game.get("platforms", [])
                ]
            }
            for game in games
        ]
        return result

    def _show_placeholder(self):
        ctk.CTkLabel(self.frame_result, text="look for something...", font=("Arial", 20, "bold")).pack(pady=300)

    def _show_result(self, result):
        destroy_widgets(self.frame_result)

        for i, game in enumerate(result):
            card = GameCard(self.frame_result, game, self.show_game_details)
            card.grid(row= i // self.COLUNAS, column = i % self.COLUNAS, padx=8, pady=8, sticky="nsew")

    def show_game_details(self, game):
        ...