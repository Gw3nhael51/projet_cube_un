import time
import getpass
import os

def verification():
    while True:
        pseudo = os.getlogin().upper()
        pwd = getpass.getpass(prompt=f'{pseudo} entrez votre code PIN...: ')

        if pwd == '123456': # enregistrer le mdp dans la DB
            print("Lancement du jeu...")
            time.sleep(3)
            print("ouverture du Jeu")
            print("Bienvenue...")
            os.system("python game.py") # lance le jeu
            break
        else:
            print("Mot de passe incorrect 😔")
            continue

if __name__ == '__main__':
    verification()

# 🔐 Authentification
    #- [x] Créer un fichier `auth.py` avec mot de passe requis
    #- [x] Lancer le jeu via `main.py` après vérification