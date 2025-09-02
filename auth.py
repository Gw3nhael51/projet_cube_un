import os
import time
import getpass
import hashlib
from database.db_connect import get_connection
import pyfiglet
from termcolor import colored

conn, c = get_connection()

# Fonction pour hasher le mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Création de la table user_auth si elle n'existe pas
c.execute("""
CREATE TABLE IF NOT EXISTS user_auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_hash TEXT NOT NULL
)
""")

# Vérifie si un hash est déjà présent
c.execute("SELECT pin_hash FROM user_auth LIMIT 1")
row = c.fetchone()

# Si aucun hash, demande à l'utilisateur d'en créer un
if row is None:
    register_text = pyfiglet.figlet_format(" --REGISTER--", font="slant")
    print(colored(register_text, "blue"))
    print(register_text)
    print("🔐 Aucun mot de passe trouvé. Création d’un mot de passe initial.")
    pwd = getpass.getpass(prompt='🆕 Entrez un nouveau mot de passe : ')
    confirm = getpass.getpass(prompt='🔁 Confirmez le mot de passe : ')
    if pwd != confirm:
        print("❌ Les mots de passe ne correspondent pas.")
        exit()
    hashed = hash_password(pwd)
    c.execute("INSERT INTO user_auth (pin_hash) VALUES (?)", (hashed,))
    conn.commit()
    stored_hash = hashed
else:
    stored_hash = row[0]

if conn is None or c is None:
    exit("❌ Impossible de se connecter à la base de données.")

# Fonction de vérification
def verification():
    login_text = pyfiglet.figlet_format(" --Login--", font="slant")
    print(colored(login_text, "yellow"))
    while True:
        pseudo = os.getlogin()
        print(f"Bonjour {pseudo}")
        pwd = getpass.getpass(prompt="Quel est votre mot de passe ?")

        if hash_password(pwd) == stored_hash:
            print("✅ Lancement du jeu...")
            time.sleep(2)
            print("🎮 Ouverture du Menu")
            os.system("python menu.py")
            break
        else:
            print("❌ Mot de passe incorrect 😔")
            continue

if __name__ == '__main__':
    verification()