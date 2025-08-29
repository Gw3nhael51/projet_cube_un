# ✅ ToDoList – Projet Jeu de Combat 

## 🔐 Authentification
- [X] Créer un fichier `auth.py` avec mot de passe requis
- [X] Lancer le jeu via `main.py` après vérification

## 🎮 Lancement du jeu
- [X] Demander les pseudos des deux joueurs
- [X] Verifier le format des pseudos
- [] Vérifier si les pseudos existent dans la base SQLite
- [] Enregistrer les pseudos manquants

## 🗃️ Base de Données
- [] Créer une base SQLite pour les tables :
  - [X] `joueurs`
  - [X] `créatures`
  - [X] `historique`
  - [X] Concevoir le MCD (Modèle Conceptuel de Données)

## 🧠 Logique de jeu
- [X] Afficher un message de bienvenue aux joueurs
- [X] Afficher les règles du jeu et demander confirmation
- [] Récupérer les créatures et leurs stats depuis la DB
- [] Afficher la liste des créatures disponibles
- [] Empêcher le joueur 2 de choisir la même créature que le joueur 1
- [] Demander le choix de créature pour chaque joueur

## ⚔️ Combat Tour par Tour
- [X] Créer une boucle de combat
- [] Implémenter les 3 actions :
  - Attaquer
  - Capacité spéciale
  - Passer son tour (sauf tour1)
- [] Calculer les dégâts : `Attaque - Défense (min 1)`
- [] Afficher les PV restants après chaque tour
- [] Déterminer la fin de partie (PV = 0)
- [] Afficher le gagnant avec le résumé du combat
- [] Enregistrer l’historique du combat

## 🧪 Tests & Fiabilité
- [] Vérifier que toutes les fonctionnalités fonctionnent sans érreur(s)

## 📐 Diagrammes UML
- [X] Cas d’utilisation (choix créature, attaque, capacité spéciale)
- [X] Séquence (tour de combat)

## 🖼️ Maquettes d’écran
- [X] Écran de sélection des créatures
- [X] Écran de combat (PV + options)

## 📄 Spécifications Techniques
- [] Décrire la formule de calcul des dégâts
- [] Décrire la gestion des capacités spéciales
- [] Décrire les règles de fin de partie

## 🗣️ Soutenance
- [] Préparer une présentation de 15 minutes
- [] Démonstration du jeu en console
- [] Présenter le fonctionnement de la base de données