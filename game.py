# game.py
from database.db_connect import *
from rules.rules import rules

# Connexion acceptée, lancement du jeu

# Fonction formule d'une attaque normale
    # attack_player1 = damage_creature_player1 - defense_creature_player2
    # attack_player2 = damage_creature_player2 - defense_creature_player1

# Fonction formule d'attaque spéciale
    # special_attack_player1 = damage_creature_player1 - defense_creature_player2 - PV > attaque normale
    # special_attack_player2 = damage_creature_player2 - defense_creature_player1 - PV > attaque normale

    # mais sil y a régénération
        # special_attack_player1, special_attack_player2  =  PV actuel du joueur + PV du coup spécial <= PV max

# Fonction passer son tour
    # si tour = 0 , ne pas afficher l'option
    # sinon attack_player = 0

# Fonction de vérification des pseudos

def pseudo_verify():
    while True:
        get_connection()
        # demander au joueur 1 son pseudo
        pseudo1 = input("Quel est le pseudo du joueur 1? ").lower().replace(" ", "")

        # Verifier le format du pseudo
        if not pseudo1.isalpha():
            print("❌ Le format de pseudo du joueur 1 n'est pas correct")
            continue

        # Verifier si le pseudo existe:
        c.execute("SELECT * FROM players WHERE name_player = ?", (pseudo1,))
        c.fetchall()

        # si SELECT * FROM players WHERE name_player = ?", (pseudo1,) = sort un resultat
            # alors pseudo existe
        # recupérer id_player

        # sinon pseudo non existant
            # enregistrer DB " INSERT INTO players (name_player) VALUES (pseudo1) "





        # --------------------------------

        # demander au joueur 2 son pseudo
        pseudo2 = input("Quel est le pseudo du joueur 2? ").lower().replace(" ", "")

        # Verifier le format du pseudo
        if not pseudo2.isalpha():
            print("❌ Le format de pseudo du joueur 2 n'est pas correct")
            continue

        print("Le format des pseudos est correct.")
        return pseudo1, pseudo2

if __name__ == '__main__':
    player1, player2 = pseudo_verify()
    print(f"Bienvenue {player1} & {player2}")
    rules()

    # Appel à la fonction

    # Récupérer dans la DB les créatures et les stats de chaque créature

    # Afficher la liste des créatures disponibles et les stats, rendre indisponible
    # le choix des joueurs
    # Demander choix_creature joueur1
    # Demander choix_creature joueur2
    # Définir la variable tour à zéro
    tour = 0

    # La partie peut commencer.
    # Afficher --- Début du combat ---
    print("---⚔️ Début du combat ⚔️---")
    # Afficher le choix des créatures avec leur stats
    # Player1 : Nom - PV - Puissance d'attaque - Défense - Capacité Spéciale
    print(f"{player1}\n"
          # Afficher VS
          "VS\n"
          # Afficher Player2 : Nom - PV - Puissance d'attaque - Défense - Capacité Spéciale
          f"{player2}\n")

    #  while player1.pv > 0 and player2.pv > 0:
    # try:
    # Affiche les PV creature_player1
    # Demander l'attaque du Joueur 1:  attaquer, capacité spéciale, passer son tour.
    # afficher le résumé

    # Affiche les PV creature_player2
    # Demander l'attaque du joueur 2:  attaquer, capacité spéciale, passer son tour.
    # afficher le résumé

    # afficher le résumé
    # continuer
    # except ValueError :
    # print("❌ Choisissez une attaque valide")

    # Fermer le cursor
    c.close()

    # Description:
    # time.sleep(x) = délai de x secondes