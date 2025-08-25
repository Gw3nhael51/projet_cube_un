# init_db.py
import sqlite3
from pathlib import Path

# On définit où sera créée la base de données (dans le même dossier que ce fichier)
DB_PATH = Path(__file__).with_name("game.db")

def main():
    # Connexion à SQLite (si le fichier n’existe pas, il sera créé automatiquement)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    
    # Création des tables (schéma DB)

    cur.executescript("""
    -- Table des attaques spéciales
    CREATE TABLE IF NOT EXISTS special_attacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- identifiant unique auto-incrémenté
        name TEXT UNIQUE,                      -- nom de l’attaque spéciale (clé logique)
        type TEXT,                             -- type d’effet ("damage", "heal", "buff")
        value INTEGER,                         -- valeur numérique (+3 dégâts, +10 PV, etc.)
        description TEXT                       -- description affichable
    );

    -- Table des créatures
    CREATE TABLE IF NOT EXISTS creatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-incremented unique identifier
        name TEXT UNIQUE,                      -- creature's name
        hp INTEGER,                            -- basic health points
        attack INTEGER,                        -- attack power
        defense INTEGER,                       -- defense
        ability TEXT                           -- special attack name (key to special_attacks.name)
    );

    -- Table des combats joués (historique)
    CREATE TABLE IF NOT EXISTS battles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-incremented unique identifier
        started_at TEXT,                       -- date/time of the start of the game
        finished_at TEXT,                      -- date/time of the end of the game
        player1 TEXT,                          -- nom du joueur 1
        player2 TEXT,                          -- nom du joueur 2
        winner TEXT                            -- nom du gagnant
    );
    """)

    
    # Données de base (initialisation)
   

    # Liste des attaques spéciales avec leurs effets
    special_attacks = [
        # (nom, type, valeur, description)
        ("souffle_de_feu", "damage", 3, "Adds +3 damage to the attack"),
        ("soin_magique", "heal", 10, "Heals 10 PV"),
        ("rage", "buff", 3, "Increases the attack by +3")
    ]
    cur.executemany("""
        INSERT OR IGNORE INTO special_attacks (name, type, value, description)
        VALUES (?, ?, ?, ?)
    """, special_attacks)

    # Liste des créatures jouables
    creatures = [
        # (nom, hp, attaque, défense, capacité spéciale associée)
        ("Dragon", 50, 10, 5, "souffle_de_feu"),
        ("Licorne", 40, 8, 8, "soin_magique"),
        ("Troll", 60, 6, 6, "rage")
    ]
    cur.executemany("""
        INSERT OR IGNORE INTO creatures (name, hp, attack, defense, ability)
        VALUES (?, ?, ?, ?, ?)
    """, creatures)

    # On valide les changements (commit) et on ferme la connexion
    con.commit()
    con.close()
    print(" Database created successfully.")

if __name__ == "__main__":
    main()

#special_attacks :
#C’est le catalogue des attaques spéciales.
#Exemple : "souffle_de_feu" est de type "damage" avec une valeur de 3.

#creatures :
#Chaque créature a une attaque spéciale associée via ability.
#Exemple : "Dragon" a ability = "souffle_de_feu".

#battles :
#Sert de journal pour prouver en soutenance que la BD est bien utilisée.
#Exemple : après une partie, on insère "Joueur 1 vs Joueur 2, gagnant Joueur 1".