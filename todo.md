# ✅ ToDoList – Projet Jeu de Combat
## Statut: Terminé

## 🔐 Authentification
- [X] Créer un fichier `auth.py` avec mot de passe requis
- [X] Lancer le jeu via `main.py` après vérification

## 🎮 Lancement du jeu
- [X] Demander les pseudos des deux joueurs
- [X] Verifier le format des pseudos
- [X] Vérifier si les pseudos existent dans la base SQLite
- [X] Enregistrer les pseudos manquants

## 🗃️ Base de Données
- [X] Créer une base SQLite pour les tables :
  - [X] `joueurs`
  - [X] `créatures`
  - [X] `historique`
  - [X] Concevoir le MCD (Modèle Conceptuel de Données)

## 🧠 Logique de jeu
- [X] Afficher un message de bienvenue aux joueurs
- [X] Afficher les règles du jeu et demander confirmation
- [X] Demander d'accepter les règles du jeu
- [X] Récupérer les créatures et leurs stats depuis la DB
- [X] Afficher la liste des créatures disponibles
- [X] Empêcher le joueur 2 de choisir la même créature que le joueur 1
- [X] Demander le choix de créature pour chaque joueur

## ⚔️ Combat Tour par Tour
- [X] Créer une boucle de combat
- [X] Implémenter les 3 actions :
  - Attaquer
  - Capacité spéciale
  - Passer son tour (sauf tour1)
- [X] Calculer les dégâts : `Attaque - Défense (min 1)`
- [X] Afficher les PV restants après chaque tour
- [X] Déterminer la fin de partie (PV = 0)
- [X] Afficher le gagnant avec le résumé du combat
- [X] Enregistrer l’historique du combat

## 🧪 Tests & Fiabilité
- [X] Vérifier que toutes les fonctionnalités fonctionnent sans érreur(s)

## 📐 Diagrammes UML
- [X] Cas d’utilisation (choix créature, attaque, capacité spéciale)
- [X] Séquence (tour de combat)

## 🖼️ Maquettes d’écran
- [X] Écran de sélection des créatures
- [X] Écran de combat (PV + options)

## 📄 Spécifications Techniques
- [X] Décrire la formule de calcul des dégâts
- [X] Décrire la gestion des capacités spéciales
- [X] Décrire les règles de fin de partie

## 🗣️ Soutenance
- [X] Préparer une présentation de 15 minutes
- [X] Présenter le fonctionnement de la base de données
- [X] Démonstration du jeu en console