# db_connect.py
import sqlite3
from database.create_db import DB_PATH

sqliteConnection = sqlite3.connect(DB_PATH)
# Se connecter à la base de données et créer un cursor dans le bon chemin
c = sqliteConnection.cursor()

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        print("DB connectée ✔️")
        return conn, cursor
    except sqlite3.Error as error:
        print("Erreur de connexion à la base :", error)
        return None, None

if __name__ == '__main__':
    get_connection()