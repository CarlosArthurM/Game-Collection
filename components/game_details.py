import threading
import customtkinter as ctk
import requests
from PIL import Image
from io import BytesIO
from config import BASE_URL, CLIENT_ID, ACCESS_TOKEN
from deep_translator import GoogleTranslator

class GameDetails(ctk.CTkFrame):
    def __init__(self, parent, game,on_back):
        super().__init__(parent)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Frame left
        self.frame_left = ctk.CTkFrame(self, width=250, fg_color="#1A1A2E")
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_left.grid_propagate(False)

        self.cover_label = ctk.CTkLabel(self.frame_left, text="Loading...", width=230, height=320)
        self.cover_label.pack(padx=10, pady=(10, 5))

        ctk.CTkButton(self.frame_left, text="+ Add to list",fg_color="#50007E", hover_color="#370057").pack(padx=10, pady=5, fill="x")

        # Frame right
        self.frame_right = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=10)
        self.frame_right.columnconfigure(0, weight=1)

        # name
        self.frame_name = ctk.CTkFrame(self.frame_right, fg_color="#1A1A2E", corner_radius=8)
        self.frame_name.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(self.frame_name, text="NAME", font=("Arial", 10), text_color="#7777AA").pack(anchor="w", padx=12, pady=(8,0))
        self.label_name = ctk.CTkLabel(self.frame_name, text="...", font=("Arial", 18, "bold"))
        self.label_name.pack(anchor="w", padx=12, pady=(2,8))

        # rating
        self.frame_rating = ctk.CTkFrame(self.frame_right, fg_color="#1A1A2E", corner_radius=8)
        self.frame_rating.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(self.frame_rating, text="RATING", font=("Arial", 10), text_color="#7777AA").pack(anchor="w", padx=12, pady=(8,0))
        self.label_rating = ctk.CTkLabel(self.frame_rating, text="...", font=("Arial", 15))
        self.label_rating.pack(anchor="w", padx=12, pady=(2,8))

        # platforms
        self.frame_platforms = ctk.CTkFrame(self.frame_right, fg_color="#1A1A2E", corner_radius=8)
        self.frame_platforms.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(self.frame_platforms, text="PLATFORMS", font=("Arial", 10), text_color="#7777AA").pack(anchor="w", padx=12, pady=(8,0))
        self.label_platforms = ctk.CTkLabel(self.frame_platforms, text="...", font=("Arial", 13), wraplength=400, justify="left")
        self.label_platforms.pack(anchor="w", padx=12, pady=(2,8))

        # genres
        self.frame_genres = ctk.CTkFrame(self.frame_right, fg_color="#1A1A2E", corner_radius=8)
        self.frame_genres.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(self.frame_genres, text="GENRES", font=("Arial", 10), text_color="#7777AA").pack(anchor="w", padx=12, pady=(8,0))
        self.label_genres = ctk.CTkLabel(self.frame_genres, text="...", font=("Arial", 13), wraplength=400, justify="left")
        self.label_genres.pack(anchor="w", padx=12, pady=(2,8))

        # summary
        self.frame_summary = ctk.CTkScrollableFrame(self.frame_right, fg_color="#1A1A2E", corner_radius=8)
        self.frame_summary.pack(fill="both", expand=True)
        ctk.CTkLabel(self.frame_summary, text="SUMMARY", font=("Arial", 10), text_color="#7777AA").pack(anchor="w", padx=12, pady=(8,0))
        self.label_summary = ctk.CTkLabel(self.frame_summary, text="...", font=("Arial", 12), wraplength=500, justify="left")
        self.label_summary.pack(anchor="n", padx=12, pady=(2))

        self.on_back = on_back

        self.btn_back = ctk.CTkButton(self, text="← Back", command=self._back, fg_color="#50007E", hover_color="#370057")
        self.btn_back.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10))

        # loading dates
        threading.Thread(target=self._search_thread, args=(game["igdb_ID"],), daemon=True).start()

        if game.get("cover"):
            threading.Thread(target=self._load_cover, args=(game["cover"],), daemon=True).start()


    def _back(self):
        self.pack_forget()
        self.on_back()

    def _translate(self, text: str) -> str:
        try:
            return GoogleTranslator(source="en", target="pt").translate(text)
        except Exception:
            return text

    def _search_thread(self, id_game):
        response = requests.post(
            f"{BASE_URL}/games",
            headers={
                "Client-ID": CLIENT_ID,
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            },
            data=f'fields name,cover.url,rating,platforms.name,genres.name,summary; where id = {id_game};'
        )

        if not self._is_valid_response(response):
            return

        game = response.json()[0]

        if game.get("summary"):
            game["summary"] = self._translate(game["summary"])

        self.after(0, lambda: self._show_result(game))

    def _show_result(self, game):
        self.label_name.configure(text=game.get("name", "—"))
        self.label_rating.configure(text=f"⭐ {round(game.get('rating', 0) / 20, 1)}")
        self.label_platforms.configure(text=", ".join([p["name"] for p in game.get("platforms", [])]))
        self.label_genres.configure(text=", ".join([g["name"] for g in game.get("genres", [])]))
        self.label_summary.configure(text=game.get("summary", "No summary available."))


    def _load_cover(self, url):
        try:
            response = requests.get(f"https:{url}")
            img = Image.open(BytesIO(response.content)).resize((230, 320))
            ctk_img = ctk.CTkImage(img, size=(230, 320))
            self.after(0, lambda: self.cover_label.configure(image=ctk_img, text=""))
        except Exception:
            self.after(0, lambda: self.cover_label.configure(text="No cover"))


    def _is_valid_response(self, response) -> bool:
        return response.status_code == 200 and bool(response.json())