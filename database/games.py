from database.connection import create_connection

def insert_game(igdb_id, name, cover_url):
    with create_connection() as con:
        con.execute(
            "INSERT INTO game (game_id, name, cover_url) VALUES (?, ?, ?)",
            (igdb_id, name, cover_url)
        )
        return con.execute("SELECT last_insert_rowid()").fetchone()[0]

def get_game_by_igdb_id(igdb_id):
    with create_connection() as con:
        return con.execute("SELECT * FROM game WHERE game_id = ?", (igdb_id,)).fetchone()