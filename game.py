import random
import sqlite3
import time

# Connexion acceptée, lancement du jeu

# Formule d'une attaque
    # attack_player1 = damage_creature_player1 - defense_creature_player2
    # attack_player2 = damage_creature_player2 - defense_creature_player1

# Formule d'attaque spéciale

# Fonction de vérification des pseudos

def pseudo_verify():
    while True:
        # demander au joueur 1 son pseudo
        pseudo1 = input("Quel est le pseudo du joueur 1? ").lower().replace(" ", "")

        # Verifier le format du pseudo
        if not pseudo1.isalpha():
            print("❌ Le format de pseudo du joueur 1 n'est pas correct")
            continue

        # --------------------------------

        # demander au joueur 2 son pseudo
        pseudo2 = input("Quel est le pseudo du joueur 2? ").lower().replace(" ", "")

        # Verifier le format du pseudo
        if not pseudo2.isalpha():
            print("❌ Le format de pseudo du joueur 2 n'est pas correct")
            continue

        print("Le format des pseudos est correct.")
        return pseudo1, pseudo2

# Appel à la fonction
player1, player2 = pseudo_verify()

# Message de bienvenue aux deux joueurs
print(f"Bienvenue {player1} et {player2}")
time.sleep(2) # Attendre 2 secondes

# Afficher les règles
print("🐉 RÈGLES DU JEU — Combat de Créatures\n")
time.sleep(1)

print("🎯 Objectif\n"
      "Affrontez votre adversaire dans un duel stratégique où chaque joueur incarne une créature aux pouvoirs uniques.\n"
      "Le but ? Réduire les points de vie (PV) de la créature ennemie à zéro pour remporter la victoire.\n")
time.sleep(12)

print("🧙‍♂️ Mise en place\n"
      "1. Chaque joueur choisit une créature parmi celles proposées.\n"
      "2. Les créatures ont des caractéristiques propres :\n"
      "   - Points de vie (PV)\n"
      "   - Attaque\n"
      "   - Défense\n"
      "   - Capacité spéciale\n")
time.sleep(12)

print("🔁 Déroulement du jeu\n"
      "Le jeu se joue en tour par tour. À chaque tour, le joueur actif choisit une action parmi trois :\n"
      "   - Attaquer : inflige des dégâts à l’adversaire (Attaque - Défense adverse, minimum 1 dégât).\n"
      "   - Utiliser sa capacité spéciale : soin, boost, rage, etc.\n"
      "   - Passer son tour : aucune action n’est effectuée.\n")
time.sleep(12)

print("⚔️ Exemple d’actions\n"
      "Le Dragon utilise son Souffle de feu pour infliger des dégâts massifs.\n"
      "La Licorne se soigne grâce à sa Magie régénératrice.\n"
      "Le Troll entre en Rage, augmentant temporairement son attaque.\n")
time.sleep(12)

print("🏁 Fin de partie\n"
      "La partie se termine dès qu’une créature atteint 0 PV.\n"
      "Le joueur dont la créature est encore en vie est déclaré vainqueur.\n")
time.sleep(12)

print("📟 Interface console\n"
      "Le jeu se joue via une interface en ligne de commande :\n"
      "   - Sélection des créatures\n"
      "   - Affichage des statistiques\n"
      "   - Résumé des actions après chaque tour\n"
      "   - Visibilité de l'historique de parties avec /history\n")
time.sleep(12)

# Accepter les règles ?
# Récupérer dans la DB les créatures et les stats de chaque créature
# Afficher la liste des créatures disponibles et les stats, rendre indisponible
# le choix du premier joueur au joueur 2
# Demander choix_creature joueur1
# Demander choix_creature joueur2
# Définir la variable tour à 0
tour = 0

# La partie peut commencer.
# Afficher --- Début du combat ---
print("---⚔️ Début du combat ⚔️---")
# Afficher le choix des créatures avec leur stats
# Player1 : Nom - PV - Puissance d'attaque - Défense - Capacité Spéciale
print(f"{player1}\n" 
#Afficher VS
      "VS\n" 
# Afficher Player2 : Nom - PV - Puissance d'attaque - Défense - Capacité Spéciale
      f"{player2}\n")

#  while player1.pv > 0 and player2.pv > 0:
    # try:
        # Affiche les PV creature_player1
        # Demander l'attaque du Joueur 1:  attaquer, capacité spéciale, passer son tour.

        # Affiche les PV creature_player2
        # Demander l'attaque du joueur 2:  attaquer, capacité spéciale, passer son tour.

        # afficher le résumé des 2 attaques
        # continuer
    # except ValueError:
        # print("❌ Choisissez une attaque valide")


# Description:
# time.sleep(x) = délai de x secondes