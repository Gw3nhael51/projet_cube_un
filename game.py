# game.py
from database.db_connect import *
from rules.rules import rules
from battle import *
from history import show_history
# -------------------Voir dans battle.py-------------------------

# Connexion acceptée, lancement du jeu

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
    # Retourne une liste de deux dictionnaires : [{'id' :, 'name' : ...}, ...]

    global conn, c
    conn, c = get_connection()

    joueurs = []
    # demander au joueur 1 son pseudo puis au joueur 2 (même logique)
    for numero_joueur in [1, 2]:
        id_player, pseudo = get_or_create_player(numero_joueur)
        joueurs.append({'id': id_player, 'name': pseudo})

    print("Le format des pseudos est correct.")
    return joueurs

def choose_creature(joueur_nom, creatures_disponibles):
    print(f"\n--- {joueur_nom} --- \nchoisissez votre créature :")

    for i, creature in enumerate(creatures_disponibles):
        print(f"{i} - {creature['name_creature']} | PV: {creature['hp_initial']} "
              f"| Défense: {creature['defense_value']} "
              f"| Spéciale: {creature['spec_attack_name']} ({creature['spec_attack_value']})")

    while True:
        try:
            choice = int(input("Entrez le numéro de votre créature : "))
            if 0 <= choice < len(creatures_disponibles):
                return creatures_disponibles.pop(choice)
            else:
                print("❌ Numéro invalide.")
        except ValueError:
            print("❌ Veuillez entrer un nombre.")


# ---------------------------------------------------------
# Point d'entrée principal

def main():
    # Récupération/validation des pseudos
    joueurs = pseudo_verify()
    player1, player2 = joueurs[0]['name'], joueurs[1]['name']

    print(f"Bienvenue {player1} & {player2} \n")
    rules()

    # -----------------------------------------------------

    raw_creatures = c.execute(
        "SELECT name_creature, hp_initial, defense_value, spec_attack_name, spec_attack_value, spec_attack_descr FROM creatures").fetchall()

    available_creatures = [
        {
            'name_creature':        row[0],
            'hp_initial':           row[1],
            'defense_value':        row[2],
            'spec_attack_name':     row[3],
            'spec_attack_value':    row[4],
            'spec_attack_descr':    row[5]
        }

        for row in raw_creatures
    ]

    creature_player1 = choose_creature(player1, available_creatures)
    # print(f"Liste après choix de {player1} : {[c['name_creature'] for c in available_creatures]}")

    creature_player2 = choose_creature(player2, available_creatures)
    # print(f"Liste après choix de {player2} : {[c['name_creature'] for c in available_creatures]}")

    fight = [
        f"{player1}: a choisi {creature_player1['name_creature']} voici ses stats: PV: {creature_player1['hp_initial']}, Défense: {creature_player1['defense_value']}, Spéciale: {creature_player1['spec_attack_name']} - {creature_player1['spec_attack_descr']}",
        f"{player2}: a choisi {creature_player2['name_creature']} voici ses stats: PV: {creature_player2['hp_initial']}, Défense: {creature_player2['defense_value']}, Spéciale: {creature_player2['spec_attack_name']} - {creature_player2['spec_attack_descr']}"
    ]

    # Définir la variable tour à zéro
    tour = 0

    # -----------------------------------------------------
    # La partie peut commencer.

    print("\n ---⚔️ Début du combat ⚔️---")
    # Afficher le choix des créatures avec leur stats
    # Player1 : Nom - PV - Puissance d'attaque - Défense - Capacité Spéciale
    print(f"{fight[0]}\n🆚\n{fight[1]}\n")

    # -----------------------------------------------------
    # Boucle de combat voir code battle.py


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