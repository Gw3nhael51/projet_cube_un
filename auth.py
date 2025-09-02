import time
import getpass
import os

def verification():
    while True:
        pseudo = os.getlogin()
        print(f"Bonjour {pseudo}")
        pwd = getpass.getpass(prompt='Quel est votre mot de passe ?')

        if pwd == '123456':
            print("Lancement du jeu...")
            time.sleep(3)
            print("ouverture du Menu")
            print("Bienvenue...")
            os.system("python3 menu.py") # lance le jeu
            break
        else:
            print("Mot de passe incorrect 😔")
            continue

if __name__ == '__main__':
    verification()

# 🔐 Authentification
    #- [x] Créer un fichier `auth.py` avec mot de passe requis
    #- [x] Lancer le jeu via `main.py` après vérification