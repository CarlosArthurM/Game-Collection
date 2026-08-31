from database.connection import create_connection

def get_all_lists():
    with create_connection() as con:
        return con.execute("SELECT * FROM list_type").fetchall()

def add_list(name):
    with create_connection() as con:
        con.execute("INSERT INTO list_type(name) VALUES (?)",(name,))

def remove_list(list_id):
    with create_connection() as con:
        con.execute("DELETE FROM list_type WHERE id = ?", (list_id,))