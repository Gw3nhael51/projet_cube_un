# init_db.py
import sqlite3
from pathlib import Path

# On définit où sera créée la base de données (dans le même dossier que ce fichier)
DB_PATH = Path(__file__).with_name("game.db")

def main():
    # Connexion à SQLite (si le fichier n’existe pas, il sera créé automatiquement)
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON") # IMPORTANT! PRAGMA foreign_keys = ON doit être exécutée à chaque nouvelle connexion.
    cur = con.cursor()

    # Création des tables (schéma DB)

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS creatures (
            id_creature INTEGER PRIMARY KEY AUTOINCREMENT,
            name_creature TEXT UNIQUE,
            hp_initial TEXT, 
            attack_value INTEGER,
            defense_value INTEGER,
            spec_attack_name TEXT,
            spec_attack_value TEXT,
            spec_attack_descr TEXT
        );

        CREATE TABLE IF NOT EXISTS players (
            id_player INTEGER PRIMARY KEY AUTOINCREMENT,
            name_player TEXT,
            id_creature INTEGER,
            FOREIGN KEY (id_creature) REFERENCES creatures(id_creature)
        );

        CREATE TABLE IF NOT EXISTS history (
            id_battle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_player_winner INTEGER,
            id_creature INTEGER,
            FOREIGN KEY (id_player_winner) REFERENCES players(id_player),
            FOREIGN KEY (id_creature) REFERENCES creatures(id_creature)
        );
    """)

    # Liste des créatures jouables
    creatures = [
        # (name_creature, hp_initial, attack_value, defense_value, spec_attack_name, spec_attack_value, spec_attack_descr)
        ("Démon", "45", 10, 5, "Épée de l'Enfer", "20", "Inflige des dégâts massifs"),
        ("Troll", "60", 6, 6, "Rage", "15", "Double l'attaque pendant un tour"),
        ("Sorcière", "?", "?", "?", "?", "?", "?"),
        ("Licorne", "40", 8, 8, "Soin magique", "25", "Restaure des PV"),
        ("Centaure", "?", "?", "?", "?", "?", "?"),
        ("Guts", "?", "?", "?", "?", "?", "?"),
        ("Dragon", "50", 10, 5, "Souffle de feu", "30", "Brûle l'ennemi"),
        ("Loup-garou", "?", "?", "?", "?", "?", "?"),
        ("Elfe", "?", "?", "?", "?", "?", "?")
    ]

    cur.executemany("""
        INSERT OR IGNORE INTO creatures (name_creature, hp_initial, attack_value, defense_value, spec_attack_name, spec_attack_value, spec_attack_descr)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, creatures)

    # On valide les changements (commit) et on ferme la connexion
    con.commit()
    con.close()
    print(" Database created successfully.")

if __name__ == "__main__":
    main()

#Special_attacks :
# Catalogue des attaques spéciales.
# Exemple : "souffle_de_feu" est de type "damage" avec une valeur de 3.

#Creatures :
#Chaque créature a une attaque spéciale associée via spec_attack_name.
#Exemple : "Dragon" a spec_attack_name = "souffle_de_feu".

# History :
# Sert de journal pour voir les combats précedents.
# Exemple : après une partie, on insère "Joueur 1 vs Joueur 2, gagnant Joueur 1 avec x tours".