# connexion à la base de données

import sqlite3
from create_db import DB_PATH # import de la var DB_PATH depuis create_db.py

sqliteConnection = sqlite3.connect(DB_PATH)

def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    return con

def database_connexion():
    try:
        # Se connecter à la base de données et créer un cursor dans le bon chemin
        c = sqliteConnection.cursor()
        print('DB connectée ✔️ \n')

        # Faire la requête SQL
        query = "SELECT * FROM creatures"
        c.execute(query)

        creatures = c.fetchall()

        print("Liste des créatures: ")
        for creature in creatures:
            print(f"- {creature[1]}")

        print("\n Liste des PV: ")
        for hp in creatures:
            print(f"- {hp[2]}")

        # Fermer le cursor
        c.close()

    except sqlite3.Error as error:
        print('Error occurred -', error)

database_connexion()