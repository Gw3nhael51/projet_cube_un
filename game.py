# game.py
from database.db_connect import *
from rules.rules import rules

# -------------------Voir dans battle.py-------------------------

# Connexion acceptée, lancement du jeu

# Fonction formule d'une attaque normale
#   attack_player1 = damage_creature_player1 - defense_creature_player2
#   attack_player2 = damage_creature_player2 - defense_creature_player1

# Fonction formule d'attaque spéciale
#   special_attack_player1 = damage_creature_player1 - defense_creature_player2 - PV > attaque normale
#   special_attack_player2 = damage_creature_player2 - defense_creature_player1 - PV > attaque normale
#   mais s'il y a régénération :
#       special_attack_player1, special_attack_player2 = PV_actuel_du_joueur + PV_du_coup_spécial <= PV_max

# Fonction passer son tour
#   si tour = 0 , ne pas afficher l'option
#   sinon attack_player = 0

# ---------------------------------------------------------
# Fonction utilitaire : get_or_create_player

def get_or_create_player(numero_joueur):

    # Demande un pseudo, vérifie le format, cherche dans la DB, crée si besoin.
    # Retourne (id_player, pseudo).

    while True:
        pseudo = input(f"Quel est le pseudo du joueur {numero_joueur}? ").lower().replace(" ", "")

        # Vérifier le format du pseudo
        if not pseudo.isalpha():
            print(f"❌ Le format de pseudo du joueur {numero_joueur} n'est pas correct")
            continue

        # Vérifier si le pseudo existe
        c.execute("SELECT id_player FROM players WHERE name_player = ?", (pseudo,))
        row = c.fetchone() # sert à récupérer le prochain résultat d’une requête SQL exécuté

        # si SELECT sort un résultat ALORS pseudo existe DONC récupérer id_player
        if row:
            print("Votre pseudo existe")
            id_player = row[0]
            return id_player, pseudo

        # Si le pseudo n'existe pas alors l'ajouter
        print("Votre pseudo n'existe pas dans la base.")
        print("Création du pseudo")
        c.execute("INSERT OR IGNORE INTO players (name_player) VALUES (?)", (pseudo,))
        conn.commit()  # commit sur la connexion
        print("Pseudo enregistré ✔️")

        # récupérer id_player créé
        c.execute("SELECT id_player FROM players WHERE name_player = ?", (pseudo,))
        id_player = c.fetchone()[0]
        return id_player, pseudo


# ---------------------------------------------------------
# Fonction de vérification des pseudos (factorisée)

def pseudo_verify():

    # Demande et valide les pseudos des deux joueurs, crée les entrées si besoin.
    # Retourne une liste de deux dico: [{'id': , 'name': ...}, ...]

    global conn, c
    conn, c = get_connection()

    joueurs = []
    # demander au joueur 1 son pseudo puis au joueur 2 (même logique)
    for numero_joueur in [1, 2]:
        id_player, pseudo = get_or_create_player(numero_joueur)
        joueurs.append({'id': id_player, 'name': pseudo})

    print("Le format des pseudos est correct.")
    return joueurs

# ---------------------------------------------------------
# Point d'entrée principal

def main():
    # Récupération/validation des pseudos
    joueurs = pseudo_verify()
    player1, player2 = joueurs[0]['name'], joueurs[1]['name']

    print(f"Bienvenue {player1} & {player2}")
    rules()

    # -----------------------------------------------------
    # Récupérer dans la DB les créatures et les stats de chaque créature

    # Afficher la liste des créatures disponibles et les stats, rendre indisponible
    # le choix des joueurs
    # Demander choix_creature joueur1
    # Demander choix_creature joueur2

    # Définir la variable tour à zéro
    tour = 0

    # -----------------------------------------------------
    # La partie peut commencer.

    print("\n ---⚔️ Début du combat ⚔️---")
    # Afficher le choix des créatures avec leur stats
    # Player1 : Nom - PV - Puissance d'attaque - Défense - Capacité Spéciale
    print(f"{player1}\n"
          "VS\n"
          f"{player2}\n")

    # -----------------------------------------------------
    # Boucle de combat voir code battle.py

    # while creature_player1.pv > 0 and creature_player2.pv > 0:
    #     try:
    #         # Affiche les PV creature_player1
    #         # Demander l'attaque du Joueur 1: attaquer, capacité spéciale, passer son tour.
    #         # - attaquer: utiliser la formule d'attaque normale
    #         # - capacité spéciale: utiliser la formule d'attaque spéciale + contraintes PV/régénération
    #         # - passer son tour: si tour > 0, attack_player = 0; sinon ne pas afficher l'option
    #         # afficher le résumé du tour du joueur 1
    #
    #         # Affiche les PV creature_player2
    #         # Demander l'attaque du Joueur 2:s attaquer, capacité spéciale, passer son tour.
    #         # afficher le résumé du tour du joueur 2
    #
    #         # Incrémenter le compteur de tour
    #         # tour += 1
    #
    #     except ValueError:
    #         print("❌ Choisissez une attaque valide")

    # -----------------------------------------------------
    # Fin de partie: fermer proprement la DB

    c.close()
    conn.close()

# ---------------------------------------------------------
# Exécution

if __name__ == '__main__':
    main()

# Description:
# time.sleep(x) = délai de x secondes

# Pourquoi utiliser fetchone() ?#
# Parce que la requête SELECT id_player ... WHERE name_player = ? ne doit renvoyer qu’une seule ligne.
# Ça évite de charger inutilement une liste avec fetchall()