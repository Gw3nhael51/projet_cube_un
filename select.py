from db import list_creatures, get_creature

def print_creatures(locked_id=None):
    rows = list_creatures()
    print("\n=== Monstres disponibles ===")
    for r in rows:
        lock = (" (INDISPONIBLE)" if locked_id and r["id_creature"] == locked_id else "")
        print(f'[{r["id_creature"]}] {r["nom"]} | PV:{r["hp_max"]} ATK:{r["attaque"]} DEF:{r["defense"]} | {r["special_nom"]}{lock}')
    print()

def choose_creature(prompt="Choisis l'ID de ton Monstre: ", locked_id=None):
    while True:
        try:
            cid = int(input(prompt))
            c = get_creature(cid)
            if not c:
                print("ID inconnu. Réessaie.")
                continue
            if locked_id and cid == locked_id:
                print("Déjà pris par l'autre joueur. Choisis-en une autre.")
                continue
            return c
        except ValueError:
            print("Entre un nombre valide.")
