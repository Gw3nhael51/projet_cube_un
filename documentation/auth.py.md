# 🔐 Documentation Technique : Module `auth.py`

## **1. Description Générale**

Ce module gère l'**authentification utilisateur** avant le lancement du jeu. Il sert de **point d'entrée principal** et peut être exécuté dans le script principal (`main.py`).

---

## **2. Fonctionnalités Clés**

| Fonctionnalité                        | Description                                                                        |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| **Message de bienvenue personnalisé** | Affiche le nom d'utilisateur système (`os.getlogin()`).                            |
| **Saisie sécurisée du mot de passe**  | Utilise `getpass.getpass()` pour masquer la saisie.                                |
| **Vérification du mot de passe**      | Compare la saisie avec la valeur définie (`'123456'`).                             |
| **Boucle de réessai**                 | Demande en boucle le mot de passe en cas d'échec.                                  |
| **Lancement du jeu**                  | Exécute --> <a href="game.py.md">`game.py`</a> après une authentification réussie. |

---

## **3. Dépendances**

| Module    | Utilisation                                              |
| --------- | -------------------------------------------------------- |
| `os`      | Récupère le nom d'utilisateur et lance `game.py`.        |
| `getpass` | Masque la saisie du mot de passe automatiquement.        |
| `time`    | Ajoute un délai avant le lancement du jeu (en secondes). |

---

## **4. Fonction `verification()`**

```python
def verification():
```

### **Logique**

1. **Boucle infinie** (`while True`) :
   - Affiche un message personnalisé avec `os.getlogin()`.
   - Demande le mot de passe via `getpass.getpass()`.
   - **Si le mot de passe est correct** :
     - Affiche un message de lancement.
     - Pause de 3 secondes (`time.sleep(3)`).
     - Lance `game.py` (`os.system("python game.py")`).
   - **Sinon** :
     - Affiche une erreur et relance la demande.

### **Flux de contrôle**

```mermaid

    A[Début] --> B[Afficher "Bonjour {pseudo}"]
    B --> C[Demander mot de passe]
    C --> D{Mot de passe correct ?}
    D -->|Oui| E[Lancer game.py]
    D -->|Non| F[Afficher "Mot de passe incorrect"]
    F --> C
```

---

## **5. Gestion du Mot de Passe**

### **Choix Actuel**

- Le mot de passe (`'123456'`) est **codé en dur** dans le script solution temporaire autorisée .

### **Évolutions Prévues**

- **Stockage sécurisé** : Migration vers une base de données (BDD) ou un fichier de configuration externe pour une version future.

---

## **6. Point d'Entrée**

```python
if __name__ == '__main__':
    verification()
```

- Exécute `verification()` si le script est lancé directement.

---

## **7. Auteur et Version**

- **Auteur** : Gwenhael
- **Date** : 23 Août 2025
- **Version** : 1.0 (version initiale avec mot de passe temporaire).

---
