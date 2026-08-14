import threading
import customtkinter as ctk
from components.game_card import GameCard
from components.filter_search_field import FilterCombox
from components.search_field import SearchField
import requests
from config import ACCESS_TOKEN, CLIENT_ID, BASE_URL
from utils.utils import destroy_widgets
from components.game_details import GameDetails

COLUMNS = 3

class SearchPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=10)

        self.create_frame_top()

        self.frame_result = ctk.CTkScrollableFrame(self)
        self.frame_result.pack(padx=5, pady=5, fill="both", expand=True)

        self.create_frame_down()

        self._show_placeholder()

    def create_frame_top(self):
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack()

        self.search_field = SearchField(self.frame_top)
        self.search_field.bind("<Return>", lambda e: self.search_game())
        self.search_field.grid(row=0, column=0, padx=10)

        self.combox_filter = FilterCombox(self.frame_top)
        self.combox_filter.grid(row=0, column=1, padx=10)

    def create_frame_down(self):
        self.frame_pagination = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_prev = ctk.CTkButton(self.frame_pagination, text="← Prev", fg_color="#50007E", hover_color="#370057", command=self._prev_page)
        self.btn_prev.pack(side="left", padx=5)

        self.btn_next = ctk.CTkButton(self.frame_pagination, text="Next →", fg_color="#50007E", hover_color="#370057", command=self._next_page)
        self.btn_next.pack(side="left", padx=5)


    def _get_platform_id(self, platform: str) -> str | None:
        match platform:
            case "PC":
                return "(6)"
            case "PlayStation":
                return "(7,8,9,48, 167)"
            case "Xbox":
                return "(11,12,49,169)"
            case "Nintendo":
                return "(130,5,41,21,4,24,20,37)"
            case _:
                return None

    def search_game(self):
        name = self.search_field.get()
        platform = self.combox_filter.get()

        if not name:
            return

        self.current_page = 0
        self.current_name = name
        self.current_platform = platform

        self.search_field.configure(state="disabled")

        thread = threading.Thread(target=self._search_thread, args=(name,platform, 0), daemon=True)
        thread.start()

    def _search_thread(self, name: str, platform: str, page: int):
        offset = page * 40
        platform_id = self._get_platform_id(platform)
        platform_filter = f"& platforms = {platform_id}" if platform_id else ""

        response = requests.post(
            f"{BASE_URL}/games",
            headers={
                "Client-ID": CLIENT_ID,
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            },
            data=f''' search "{name}"; fields name,cover.url,rating,parent_game,game_type.type,platforms.name,platforms.platform_logo.url; where game_type = (0,8,9) {platform_filter}; limit 40; offset {offset}; '''
        )

        if not self._is_valid_response(response):
            self.after(0, lambda: self._show_error("No results found..."))
            self.after(0, lambda: self.search_field.configure(state="normal"))
            return

        result = self._format_response(response.json())
        self.after(0, lambda : self._show_result(result))
        self.after(0, lambda : self.search_field.configure(state="normal"))


    def _is_valid_response(self,response) -> bool:
        return response.status_code == 200 and bool(response.json())


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
            card.grid(row=i // COLUMNS, column=i % COLUMNS, padx=8, pady=8, sticky="nsew")

        self.frame_pagination.pack(pady=(0, 10))

        self.btn_prev.configure(state="disabled" if self.current_page == 0 else "normal")

    def show_game_details(self, game):
        self.frame_top.pack_forget()
        self.frame_result.pack_forget()
        self.frame_pagination.pack_forget()

        self.game_details = GameDetails(self, game, on_back=self.back_to_search)
        self.game_details.pack(fill="both", expand=True, padx=10, pady=10)

    def back_to_search(self):
        self.frame_top.pack()
        self.frame_result.pack(padx=5, pady=5, fill="both", expand=True)
        self.frame_pagination.pack(pady=(0, 10))

    def _next_page(self):
        self.current_page += 1
        threading.Thread(target=self._search_thread, args=(self.current_name, self.current_platform, self.current_page),daemon=True).start()

    def _prev_page(self):
        self.current_page -= 1
        threading.Thread(target=self._search_thread, args=(self.current_name, self.current_platform, self.current_page),daemon=True).start()

