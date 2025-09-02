# battle.py — moteur de combat
# Oui, c'est du tour par tour..
import sqlite3
from database.create_db import DB_PATH

def safe_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0  # ou une valeur par défaut


# DB utils
def get_creature_by_id(cid: int):
    # Je vais chercher la créature en DB. Si elle n'existe pas, c'est pas moi, c'est la DB.
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM creatures WHERE id_creature = ?", (cid,))
    row = cur.fetchone()
    con.close()
    return dict(row) if row else None

def fighter_from_db(row):
    return {
        "id": row.get("id_creature", None),
        "name": row.get("name_creature", "Inconnu"),
        "hp": int(row.get("hp_initial", 100)),
        "hp_max": int(row.get("hp_initial", 100)),
        "hp_initial": int(row.get("hp_initial", 100)),  # AJOUTÉ
        "atk": int(row.get("attack_value", 5)),         # AJOUTÉ
        "def": int(row.get("defense_value", 10)),
        "special": row.get("spec_attack_name", None),
        "spec_name": row.get("spec_attack_name", None), # AJOUTÉ
        "spec_value": int(row.get("spec_attack_value", 0)),
        "spec_descr": row.get("spec_attack_descr", ""),
        "spec_used": False,
        "atk_mod": 1.0,
        "shield_val": 0
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
    # La spéciale c'est comme un cheat code… mais on te le laisse qu'une fois.
    if att["spec_used"]:
        return "Capacité spéciale déjà utilisée. Il fallait cliquer plus tôt 😅"
    att["spec_used"] = True

    n, v = att["spec_name"], att["spec_value"]

    if "Soin" in n:            # Licorne : chill vibes ✨
        att["hp"] = min(att["hp_max"], att["hp"] + v)
        return f"{att['name']} lance {n} (+{v} PV). On respire, on hydrate. PV={att['hp']}"

    if "Parade" in n:          # Guerrier noir : "Nope." au prochain coup
        att["shield_val"] = 999
        return f"{att['name']} prépare {n} (le prochain coup ? On l'appelle 'rien du tout')."

    if "Charge" in n:          # Centaure : tape très fort, mais ça pique aussi
        dmg = att["atk"] * 2
        deff["hp"] -= dmg
        att["hp"] -= 3
        return f"{att['name']} fait {n} → {dmg} dégâts ! (et -3 PV en contre-coup, faut pas abuser non plus)"

    if "Tir précis" in n:      # Elfe : ignore DEF, comme si l'autre n'avait jamais levé les bras
        deff["hp"] -= v
        return f"{att['name']} balance {n} → {v} dégâts garantis (DEF ignorée, ça fait mal à l'ego)."

    # Par défaut : dégâts bruts (Démon, Dragon, etc.). Simple, efficace, barbare.
    raw = max(1, v)
    deff["hp"] -= raw
    return f"{att['name']} utilise {n} → {raw} dégâts bruts. Le classique qui régale."


def choose_action(player_name, fighter, allow_pass: bool, allow_special: bool):
    # Menu dynamique : on n'affiche que ce qui est autorisé
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
    turn_idx = 0  # Compteur de tours
    attacker, deff = f1, f2
    owners = (p1_name, p2_name)

    # Initialisation des PV actuels
    f1["hp"] = f1["hp_initial"]
    f2["hp"] = f2["hp_initial"]

    print("\n=== ⚔️ Début du combat ! Que le meilleur spammeur gagne. ⚔️ ===")

    while f1["hp"] > 0 and f2["hp"] > 0:
        print(f"\n🎯 Tour {turn_idx + 1}")
        allow_pass = (turn_idx > 1)
        allow_special = (not attacker["spec_used"])

        # Choix de l'action
        action = choose_action(owners[0], attacker, allow_pass, allow_special)

        # Exécution de l'action
        if action == 1:
            msg = do_attack(attacker, deff)
        elif action == 2:
            msg = do_special(attacker, deff)
        else:
            msg = f"{owners[0]} passe son tour. (Stratégie mentale ou petite pause ? On respecte.)"

        print(msg)

        # Vérification de fin de combat
        if deff["hp"] <= 0 or attacker["hp"] <= 0:
            break

        # Inversion des rôles
        attacker, deff = deff, attacker
        owners = (owners[1], owners[0])
        turn_idx += 1

    # Résultat final
    if f1["hp"] <= 0 and f2["hp"] <= 0:
        print("\n💥 Double K.O. ! Match nul. Les deux aux urgences, personne n'a farmé d'XP.")
        return 0
    elif f2["hp"] <= 0:
        print(f"\n🏆 Victoire de {p1_name} avec {f1['name']} ! (Propre.)")
        # Enregistrer la victoire dans l'historique
        try:
            from history import new_history
            new_history(p1_name, f1["id"])
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde historique: {e}")
        return 1
    else:
        print(f"\n🏆 Victoire de {p2_name} avec {f2['name']} ! (Respect.)")
        # Enregistrer la victoire dans l'historique
        try:
            from history import new_history
            new_history(p2_name, f2["id"])
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde historique: {e}")
        return 2


if __name__ == '__main__':
    battle_loop(p1_name="Jean", p2_name="Jacques", f1=fighter_from_db(get_creature_by_id(1)), f2=fighter_from_db(get_creature_by_id(2)))