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

def rename_list(list_id, new_name):
    with create_connection() as con:
        con.execute("UPDATE list_type SET name = ? WHERE id = ?",(new_name, list_id))