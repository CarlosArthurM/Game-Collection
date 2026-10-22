<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=1A1A2E,50007E&height=180&section=header&text=Game+Collection&fontSize=54&fontColor=FFFFFF&fontAlignY=36&animation=fadeIn" alt="Game Collection" />

  <h1>🎮 Game Collection</h1>

  <p>A desktop application to search, organize and track your personal game collection.</p>

  <img src="https://img.shields.io/badge/Status-In%20development-50007E?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/CustomTkinter-UI-50007E?style=flat-square" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/IGDB-API-9146FF?style=flat-square" alt="IGDB API" />

  <br /><br />

  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#setup">Setup</a> •
  <a href="#environment">Environment</a>
</div>

---

## About

**Game Collection** is a desktop application built with Python and CustomTkinter that allows gamers to organize and track their game collections. It integrates with the **IGDB API** to fetch real game data and uses **SQLite** as a local database to persist user collections.

## Features

- Search games by title using the IGDB database
- Filter results by platform (PC, PlayStation, Xbox, Nintendo)
- Paginated search results
- View detailed game information: cover, rating, platforms, genres and summary
- Create custom lists to organize your games
- Add games to multiple lists (N:N relationship)
- Remove games from lists

## Architecture

```text
┌──────────────────────────────────────┐
│  UI Layer (CustomTkinter)            │
│  pages/ + components/                │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│  Data Layer                          │
│  database/ (SQLite + IGDB API)       │
└──────────────────────────────────────┘
```

### Project Structure

```text
Game-Collection/
├── components/
│   ├── button_sidebar.py       # reusable sidebar button
│   ├── filter_search_field.py  # platform filter combobox
│   ├── game_card.py            # search result card
│   ├── game_details.py         # game detail view
│   ├── list_selector_dialog.py # list selection popup
│   ├── search_field.py         # search input
│   └── sidebar.py              # navigation sidebar
├── database/
│   ├── connection.py           # SQLite connection and table creation
│   ├── game_list.py            # game_list table CRUD
│   ├── games.py                # game table CRUD
│   └── lists.py                # list_type table CRUD
├── pages/
│   ├── home.py                 # home page
│   ├── list_page.py            # user lists page
│   └── search_page.py          # game search page
├── utils/
│   └── utils.py                # shared utilities
├── app.py                      # application entry point
├── config.py                   # constants and environment variables
├── token_manager.py            # IGDB token management
├── requirements.txt
└── .env                        # API credentials (not versioned)
```

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Python 3.14, CustomTkinter |
| Database | SQLite |
| Game Data | IGDB API (via Twitch OAuth) |
| Image Processing | Pillow |

## Setup

```bash
git clone https://github.com/CarlosArthurM/Game-Collection.git
cd Game-Collection
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
```

## Environment

Create a `.env` file at the project root with your IGDB credentials:

```text
CLIENT_ID=your_twitch_client_id
ACCESS_TOKEN=your_igdb_access_token
```

To get your credentials:
1. Create an application at [dev.twitch.tv](https://dev.twitch.tv)
2. Get your `Client ID` and `Client Secret`
3. Generate your access token by running `token_manager.py`

After setting up the `.env`, run the application:

```bash
python app.py
```

## Author

Developed by [Carlos Arthur](https://github.com/CarlosArthurM).

<div align="center">
  <a href="https://www.linkedin.com/in/carlos-arthur-mendes-bispo-1294042ab/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://github.com/CarlosArthurM">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=1A1A2E,50007E&height=120&section=footer" alt="" />