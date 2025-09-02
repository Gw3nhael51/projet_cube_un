# connexion à la base de données db_connect.py

import sqlite3
from database.create_db import DB_PATH # import de la var DB_PATH depuis create_db.py

sqliteConnection = sqlite3.connect(DB_PATH)
# Se connecter à la base de données et créer un cursor dans le bon chemin
c = sqliteConnection.cursor()

def get_connection():
    try:
        con = sqlite3.connect(DB_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()
        print("DB connectée ✔️")
        return con, cur

    except sqlite3.Error as error:
        print('Erreur -', error)