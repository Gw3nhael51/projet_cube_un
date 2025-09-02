from game import main      # la fonction principale (démarrer une partie)
from history import show_history

def main_menu():
  
    #Menu principal :
      #1) Démarrer le jeu (appelle game.main())
      #2) Regarder l'historique (appelle history.show_history())
 
    while True:
        print("\n=== Menu principal ===")
        print("1) Démarrer le jeu")
        print("2) Regarder l'historique")

        choix = input("Votre choix: ").strip()

        if choix == "1":
            # Lancer la partie via la fonction main() dans game.py
            main()

        elif choix == "2":
    # Ici je n’utilise pas input(), j’affiche directement 10 derniers combats
         show_history(limit=20)

        else:
            print("❌ Choix invalide, réessayez.")


# Point d’entrée
if __name__ == "__main__":
    main_menu()