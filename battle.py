# battle.py — moteur de combat
# Oui, c’est du tour par tour..
import sqlite3
from database.create_db import DB_PATH

# ===================== DB utils =====================

def get_creature_by_id(cid: int):
    # Je vais chercher la créature en DB. Si elle n’existe pas, c’est pas moi, c’est la DB.
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM creatures WHERE id_creature = ?", (cid,))
    row = cur.fetchone()
    con.close()
    return dict(row) if row else None

def get_creature_by_name(name: str):
    # Même délire, mais par nom (utile car game.py passe la créature sans id ni atk)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM creatures WHERE name_creature = ?", (name,))
    row = cur.fetchone()
    con.close()
    return dict(row) if row else None

def _as_int(x, default=0):
    try:
        return int(x)
    except (TypeError, ValueError):
        return default

def fighter_from_db(row: dict):
    # Je convertis la ligne SQL en “fighter” prêt à se battre (et à souffrir).
    return {
        "id": row["id_creature"],
        "name": row["name_creature"],
        "hp": _as_int(row["hp_initial"], 1),
        "hp_max": _as_int(row["hp_initial"], 1),
        "atk": _as_int(row["attack_value"], 0),
        "def": _as_int(row["defense_value"], 0),
        "spec_name": (row["spec_attack_name"] or "").strip(),
        "spec_val": _as_int(row["spec_attack_value"], 0),
        "spec_used": False,   # spéciale = joker unique. Après, c’est fini les cadeaux.
        "atk_mod": 0,         # petit bonus d’ATK si besoin (selon spé)
        "shield_val": 0,      # bouclier ponctuel (merci “Parade Héroïque”)

        # états sur la durée
        "atk_mod_turns": 0,         # Rage
        "enemy_atk_down": 0,        # Malédiction
        "enemy_atk_down_turns": 0,
        "burn_turns": 0,            # Souffle de feu
        "burn_val": 0,
        "malus_from_enemy": 0,      # ATK malus appliqué par l’ennemi (pour le calcul direct)
    }

def fighter_from_selection(selection: dict):
    name = selection.get("name_creature")
    row = get_creature_by_name(name)
    if not row:
        return {
            "id": -1,
            "name": name or "Inconnu",
            "hp": _as_int(selection.get("hp_initial"), 1),
            "hp_max": _as_int(selection.get("hp_initial"), 1),
            "atk": 0,  # faute de mieux
            "def": _as_int(selection.get("defense_value"), 0),
            "spec_name": (selection.get("spec_attack_name") or "").strip(),
            "spec_val": _as_int(selection.get("spec_attack_value"), 0),
            "spec_used": False,
            "atk_mod": 0,
            "shield_val": 0,
            "atk_mod_turns": 0,
            "enemy_atk_down": 0,
            "enemy_atk_down_turns": 0,
            "burn_turns": 0,
            "burn_val": 0,
            "malus_from_enemy": 0,
        }
    return fighter_from_db(row)

#  Combat core

def calc_damage(attacker, defender):
    # Formule de base : (ATK + bonus) - DEF, minimum 1.
    # On ne fait pas 0 dmg ici : même un coup de fouet mouille… fait 1.
    atk_effective = attacker["atk"] + attacker["atk_mod"]
    # Malédiction baisse l’ATK de la cible : c’est rangé dans malus_from_enemy
    if attacker.get("malus_from_enemy", 0):
        atk_effective = max(0, atk_effective - attacker["malus_from_enemy"])

    dmg = atk_effective - defender["def"]
    dmg = dmg if dmg > 0 else 1

    # Si le défenseur a un shield : on sabre dedans, et on le consomme.
    if defender["shield_val"] > 0:
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


    if "Soin" in n:            # Licorne : chill vibes ✨ (“Soin magique”)
        att["hp"] = min(att["hp_max"], att["hp"] + max(1, v))
        return f"{att['name']} lance {n} (+{max(1,v)} PV). On respire, on hydrate. PV={att['hp']}"

    if "Parade" in n:          # Guerrier noir : “Nope.” au prochain coup (“Parade Héroïque”)
        att["shield_val"] = 999
        return f"{att['name']} prépare {n} (le prochain coup ? On l’appelle ‘rien du tout’)."

    if "Charge" in n:          # Centaure : tape très fort, mais ça pique aussi (“Charge rapide”)
        base_atk = att["atk"]
        if att.get("malus_from_enemy", 0):
            base_atk = max(0, base_atk - att["malus_from_enemy"])
        dmg = max(1, base_atk * 2)
        deff["hp"] -= dmg
        att["hp"] -= 3
        return f"{att['name']} fait {n} → {dmg} dégâts ! (et -3 PV en contre-coup, faut pas abuser non plus)"

    if "Tir précis" in n:      # Elfe : ignore DEF
        pure = max(1, v)
        deff["hp"] -= pure
        return f"{att['name']} balance {n} → {pure} dégâts garantis (DEF ignorée, ça fait mal à l’ego)."

    if "Rage" in n:            # Troll : Double l’attaque pendant un tour
        att["atk_mod"] += att["atk"]  # +100% de l’ATK de base
        att["atk_mod_turns"] = 1
        return f"{att['name']} entre en {n} : ATK x2 pour ce tour. On serre les dents."

    if "Malédiction" in n:     # Sorcière : -3 ATK à l’adversaire pendant 2 tours
        malus = max(1, v)
        deff["malus_from_enemy"] = malus
        deff["enemy_atk_down"] = malus
        deff["enemy_atk_down_turns"] = 2
        return f"{att['name']} jette {n} : ATK de {deff['name']} -{malus} pendant 2 tours. Ça pique la fierté."

    if "Souffle de feu" in n:  # Dragon : brûlure (DoT) + gros dégâts initiaux
        dot = max(1, v // 10)  # ex: 30 → 3 par tour
        deff["burn_turns"] = 3
        deff["burn_val"] = dot
        init = max(1, v)
        deff["hp"] -= init
        return f"{att['name']} crache {n} → {init} dégâts initiaux, {dot}/tour pendant 3 tours. BBQ time."

    if "Appel de la meute" in n:  # Loup-garou : dégâts multipliés par 3
        base = att["atk"]
        if att.get("malus_from_enemy", 0):
            base = max(0, base - att["malus_from_enemy"])
        mult = max(1, v)  # v=3 en BDD → x3
        dmg = max(1, base * mult)
        deff["hp"] -= dmg
        return f"{att['name']} lance {n} → {dmg} dégâts sauvages. La meute ne rigole pas."

    # Épée de l’Enfer / autres : dégâts bruts. Simple, efficace, barbare.
    raw = max(1, v)
    deff["hp"] -= raw
    return f"{att['name']} utilise {n} → {raw} dégâts bruts. Le classique qui régale."

def end_of_turn_effects(actor, target):
    logs = []

    # Burn (DoT) appliqué sur la cible si actif
    if target.get("burn_turns", 0) > 0:
        target["hp"] -= max(1, target.get("burn_val", 1))
        target["burn_turns"] -= 1
        logs.append(f"{target['name']} subit la brûlure ({target.get('burn_val',1)} dmg). PV={max(0,target['hp'])}")

    # Rage expire (bonus ATK)
    if actor.get("atk_mod_turns", 0) > 0:
        actor["atk_mod_turns"] -= 1
        if actor["atk_mod_turns"] == 0:
            actor["atk_mod"] -= actor["atk"]
            logs.append(f"{actor['name']} se calme : fin de Rage (ATK redevient {actor['atk']}).")

    # Malédiction : on décrémente la durée sur la cible (qui porte le malus)
    if target.get("enemy_atk_down_turns", 0) > 0:
        target["enemy_atk_down_turns"] -= 1
        if target["enemy_atk_down_turns"] == 0:
            target["malus_from_enemy"] = 0
            logs.append(f"{target['name']} se libère de la Malédiction.")

    return " | ".join(logs) if logs else None

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

    # compteur de tours pour gérer "passer le tour" à partir du T2
    turn_idx = 1

    while f1["hp"] > 0 and f2["hp"] > 0:
        allow_pass = (turn_idx > 1)
        allow_special = (not attacker["spec_used"])

        # on demande l'action à l'humain (ou plus tard un bot)
        action = choose_action(owners[0], attacker, allow_pass, allow_special)

        if action == 1:
            msg = do_attack(attacker, deff)
        elif action == 2:
            msg = do_special(attacker, deff)
        else:
            msg = f"{owners[0]} passe son tour. (Stratégie mentale ou petite pause ? On respecte.)"

        print(msg)

        # Check fin immédiate
        if deff["hp"] <= 0 or attacker["hp"] <= 0:
            break

        # Effets de fin de tour (DoT, expiration buffs/debuffs)
        tail = end_of_turn_effects(attacker, deff)
        if tail:
            print(tail)

        # Re-check après effets
        if deff["hp"] <= 0 or attacker["hp"] <= 0:
            break

        # On inverse les rôles comme dans une bonne prod : couplet 1 → couplet 2
        attacker, deff = deff, attacker
        owners = (owners[1], owners[0])
        turn_idx += 1

    # Résultats : annonce officielle façon speaker
    if f1["hp"] <= 0 and f2["hp"] <= 0:
        print("\n💥 Double K.O. ! Match nul. Les deux aux urgences, personne n’a farmé d’XP.")
        return 0
    if f2["hp"] <= 0:
        print(f"\n🏆 Victoire de {p1_name} avec {f1['name']} ! (Propre.)")
        return 1
    print(f"\n🏆 Victoire de {p2_name} avec {f2['name']} ! (Respect.)")
    return 2
