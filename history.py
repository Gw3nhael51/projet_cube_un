import sqlite3
from pathlib import Path 

DB_folder = Path(__file__).parent/"database"
DB_PATH = DB_folder / 'game.db'

def show_history(limit = 10):
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
  
if __name__ == '__main__':
   show_history()