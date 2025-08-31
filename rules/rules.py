import time

def rules():
    # Message de bienvenue aux deux joueurs, faire entrer pour faire afficher le message suivant

    time.sleep(2)  # Attendre 2 secondes

    # Afficher les règles
    print("🐉 RÈGLES DU JEU — Combat de Créatures\n")
    time.sleep(1)

    print("🎯 Objectif\n"
          "Affrontez votre adversaire dans un duel stratégique où chaque joueur incarne une créature aux pouvoirs uniques.\n"
          "Le but ? Réduire les points de vie (PV) de la créature ennemie à zéro pour remporter la victoire.\n")
    time.sleep(5)

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
          "   - Passer son tour : aucune action n’est effectuée, vous ne pouvez pas le passer à votre premier tour.\n")
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
          "   - Visibilité de l'historique des parties avec /history\n")
    time.sleep(12)

# Accepter les règles ?