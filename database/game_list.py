from database.connection import create_connection

def get_games_by_list(list_id):
    with create_connection() as con:
        return con.execute(
            """SELECT g.id, g.name, g.cover_url 
                FROM game g 
                INNER JOIN game_list gl 
                ON gl.fk_game = g.id 
                WHERE gl.fk_list = ?
             """,(list_id,)).fetchall()

def add_game_to_list(list_id, game_id):
    with create_connection() as con:
        con.execute("INSERT INTO game_list(fk_game, fk_list) VALUES (?, ?)",(game_id,list_id))

def remove_game_from_list(list_id,game_id):
    with create_connection() as con:
        con.execute("DELETE FROM game_list WHERE fk_game = ? AND fk_list = ?", (game_id, list_id))