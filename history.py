import sqlite3
from database.db_connect import get_connection, DB_PATH
from datetime import datetime

get_connection()


def show_history(limit=10):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    cur.execute("""
      SELECT h.id_battle,
             h.date,
             p.name_player,
             c.name_creature
      FROM history h
      JOIN players p ON p.id_player = h.id_player_winner
      JOIN creatures c ON c.id_creature=h.id_creature
      ORDER BY h.id_battle DESC
      LIMIT ?
              """, (limit,))
    rows = cur.fetchall()

    print(f"\n ---Historique de combats ---\n")
    if not rows:
        print("(aucun combat enregistré)")
    else:
        for row in rows:
            print(f"#{row[0]} | {row[1]} | Vainqueur: {row[2]} | Créature: {row[3]}")

    conn.close()


def new_history(player_name, creature_id):
    """Enregistre une nouvelle bataille avec le nom du joueur gagnant"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    try:
        # Récupérer ID du joueur depuis le nom
        cur.execute("SELECT id_player FROM players WHERE name_player = ?", (player_name,))
        player_row = cur.fetchone()

        if not player_row:
            print(f"⚠️ Joueur {player_name} non trouvé, création en cours...")
            # Créer le joueur s'il n'existe pas
            cur.execute("INSERT INTO players (name_player) VALUES (?)", (player_name,))
            conn.commit()
            # Récupérer le nouvel ID
            cur.execute("SELECT id_player FROM players WHERE name_player = ?", (player_name,))
            player_row = cur.fetchone()

        id_player_winner = player_row[0]

        # Vérifie que la créature existe
        cur.execute("SELECT id_creature FROM creatures WHERE id_creature = ?", (creature_id,))
        creature_row = cur.fetchone()

        if not creature_row:
            print(f"❌ Erreur: Créature ID {creature_id} n'existe pas")
            conn.close()
            return False

        #Insérer dans l'historique avec la date de la fin de combat
        cur.execute("""
        INSERT INTO history (id_player_winner, id_creature, date)
        VALUES (?, ?, ?)
                """, (id_player_winner, creature_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        conn.commit()
        print(f"✅ Bataille enregistrée: {player_name} (ID:{id_player_winner}) avec créature ID {creature_id}")

    except sqlite3.Error as e:
        print(f"❌ Erreur base de données: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

    return True


if __name__ == '__main__':
    show_history()