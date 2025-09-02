# battle.py — moteur de combat
# Oui, c’est du tour par tour..
import sqlite3
from database.create_db import DB_PATH

# DB utils
def get_creature_by_id(cid: int):
    # Je vais chercher la créature en DB. Si elle n’existe pas, c’est pas moi, c’est la DB.
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM creatures WHERE id_creature = ?", (cid,))
    row = cur.fetchone()
    con.close()
    return dict(row) if row else None

def fighter_from_db(row: dict):
    # Je convertis la ligne SQL en “fighter” prêt à se battre (et à souffrir).
    return {
        "id": row["id_creature"],
        "name": row["name_creature"],
        "hp": int(row["hp_initial"]),
        "hp_max": int(row["hp_initial"]),
        "atk": int(row["attack_value"]),
        "def": int(row["defense_value"]),
        "spec_name": row["spec_attack_name"] or "",
        "spec_val": int(row["spec_attack_value"]) if str(row["spec_attack_value"]).isdigit() else 0,
        "spec_used": False,   # spéciale = joker unique. Après, c’est fini les cadeaux.
        "atk_mod": 0,         # petit bonus d’ATK si besoin (selon spé)
        "shield_val": 0,      # bouclier ponctuel (merci “Parade Héroïque”)
    }

# === Combat core =======================================================
def calc_damage(attacker, defender):
    # Formule de base : (ATK + bonus) - DEF, minimum 1.
    # On ne fait pas 0 dmg ici : même un coup de fouet mouille… fait 1.
    dmg = (attacker["atk"] + attacker["atk_mod"]) - defender["def"]
    dmg = dmg if dmg > 0 else 1

    # Si le défenseur a un shield : on sabre dedans, et on le consomme.
    if defender["shield_val"] > 0:
        old = dmg
        dmg = max(1, dmg - defender["shield_val"])
        defender["shield_val"] = 0

    return dmg

def do_attack(att, deff):
    dmg = calc_damage(att, deff)
    deff["hp"] -= dmg
    return f"{att['name']} claque une attaque → {dmg} dégâts ! ({deff['name']} PV restants : {max(0,deff['hp'])})"

def do_special(att, deff):
    # La spéciale c’est comme un cheat code… mais on te le laisse qu’une fois.
    if att["spec_used"]:
        return "Capacité spéciale déjà utilisée. Il fallait cliquer plus tôt 😅"
    att["spec_used"] = True

    n, v = att["spec_name"], att["spec_val"]

    if "Soin" in n:            # Licorne : chill vibes ✨
        att["hp"] = min(att["hp_max"], att["hp"] + v)
        return f"{att['name']} lance {n} (+{v} PV). On respire, on hydrate. PV={att['hp']}"

    if "Parade" in n:          # Guerrier noir : “Nope.” au prochain coup
        att["shield_val"] = 999
        return f"{att['name']} prépare {n} (le prochain coup ? On l’appelle ‘rien du tout’)."

    if "Charge" in n:          # Centaure : tape très fort, mais ça pique aussi
        dmg = att["atk"] * 2
        deff["hp"] -= dmg
        att["hp"] -= 3
        return f"{att['name']} fait {n} → {dmg} dégâts ! (et -3 PV en contre-coup, faut pas abuser non plus)"

    if "Tir précis" in n:      # Elfe : ignore DEF, comme si l’autre n’avait jamais levé les bras
        deff["hp"] -= v
        return f"{att['name']} balance {n} → {v} dégâts garantis (DEF ignorée, ça fait mal à l’ego)."

    # Par défaut : dégâts bruts (Démon, Dragon, etc.). Simple, efficace, barbare.
    raw = max(1, v)
    deff["hp"] -= raw
    return f"{att['name']} utilise {n} → {raw} dégâts bruts. Le classique qui régale."


def choose_action(player_name, fighter, allow_pass: bool, allow_special: bool):
    # Menu dynamique : on n’affiche que ce qui est autorisé
    print(
        f"\n— {player_name} joue ({fighter['name']}) —  PV={fighter['hp']}/{fighter['hp_max']}  ATK={fighter['atk']}  DEF={fighter['def']}")

    options = {}
    idx = 1
    options[str(idx)] = ("Attaquer", 1)
    print(f"{idx}. Attaquer")
    idx += 1

    if allow_special:
        options[str(idx)] = ("Capacité spéciale", 2)
        print(f"{idx}. Capacité spéciale")
        idx += 1

    if allow_pass:
        options[str(idx)] = ("Passer", 3)
        print(f"{idx}. Passer (si tu veux jouer mindgame)")

    while True:
        c = input("Choix: ").strip()
        if c in options:
            return options[c][1]
        print("Choix invalide. Sélectionne un numéro affiché (promis, pas de 4 caché).")


def battle_loop(p1_name, p2_name, f1, f2):
    # Le ring est prêt : on alterne les baffes jusqu’à ce qu’il n’y ait plus de PV.
    attacker, deff = f1, f2
    owners = (p1_name, p2_name)

    print("\n=== Début du combat ! Que le meilleur spammeur gagne. ===")

    while f1["hp_initial"] > 0 and f2["hp_initial"] > 0:
        allow_pass = (turn_idx > 1)
        allow_special = (not attacker["spec_used"])

        if action == 1:
            msg = do_attack(attacker, deff)
        elif action == 2:
            msg = do_special(attacker, deff)
        else:
            msg = f"{owners[0]} passe son tour. (Stratégie mentale ou petite pause ? On respecte.)"

        print(msg)

        # Check fin
        if deff["hp_initial"] <= 0 or attacker["hp_initial"] <= 0:
            break

        # On inverse les rôles comme dans une bonne prod : couplet 1 → couplet 2
        attacker, deff = deff, attacker
        owners = (owners[1], owners[0])

    # Résultats : annonce officielle façon speaker
    if f1["hp_initial"] <= 0 and f2["hp_initial"] <= 0:
        print("\n💥 Double K.O. ! Match nul. Les deux aux urgences, personne n’a farmé d’XP.")
        return 0
    if f2["hp"] <= 0:
        print(f"\n🏆 Victoire de {p1_name} avec {f1['name']} ! (Propre.)")
        return 1
    print(f"\n🏆 Victoire de {p2_name} avec {f2['name']} ! (Respect.)")
    return 2
