import sqlite3
from sqlite3 import Error

_conn = None

def create_connection():
    global _conn

    if _conn is not None:
        try:
            return _conn
        except sqlite3.Error as err:
            raise err

    try:
        _conn = sqlite3.connect("database.db")
    except sqlite3.Error as err:
        raise err

    return _conn


def close_connection():
    global _conn

    if _conn is not None:
        _conn.close()


def create_tables():
    try:

        sql_create_table_list_type = """
            CREATE TABLE IF NOT EXISTS list_type (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        
        """

        sql_create_table_list = """
            CREATE TABLE IF NOT EXISTS game_list (
                fk_game INTEGER NOT NULL,
                fk_list INTEGER NOT NULL,
                FOREIGN KEY (fk_game) REFERENCES game(game_id),
                FOREIGN KEY (fk_list) REFERENCES list_type(id),
                PRIMARY KEY (fk_game, fk_list)
            )
        """

        sql_create_table_game = """
        CREATE TABLE IF NOT EXISTS game(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            name TEXT NOT NULL, 
            cover_url TEXT
        )
        """

        con = create_connection()

        cursor = con.cursor()

        cursor.execute(sql_create_table_game)
        cursor.execute(sql_create_table_list_type)
        cursor.execute(sql_create_table_list)
        con.commit()


    except Error as er:
        raise er


create_tables()