# battle.py
from dataclasses import dataclass

@dataclass
class Fighter:
    name: str
    hp: int
    atk: int
    df: int
    spec_name: str
    spec_val: int
    spec_used: bool = False
    burn_turns: int = 0
    atk_mod: int = 0
    guard: bool = False

    def base_damage(self, target_df: int) -> int:
        return max(1, (self.atk + self.atk_mod) - target_df)

# Fonction attaques spéciales
def apply_special(attacker: Fighter, defender: Fighter) -> str:
    s = attacker.spec_name.lower()
    msg = ""
    if "épée de l'enfer" in s:  # Démon
        msg = f"{attacker.name} active {attacker.spec_name} (+{attacker.spec_val} dmg)"
        attacker.atk_mod += attacker.spec_val
    elif "rage" in s:           # Troll
        msg = f"{attacker.name} entre en Rage (ATK x2 ce tour)"
        attacker.atk_mod += attacker.atk  # +100%
    elif "malédiction" in s:    # Sorcière
        defender.atk_mod -= attacker.spec_val
        msg = f"{defender.name} -{attacker.spec_val} ATK (2 tours)"
    elif "soin magique" in s:   # Licorne
        attacker.hp += attacker.spec_val
        msg = f"{attacker.name} se soigne de {attacker.spec_val} PV"
    elif "charge rapide" in s:  # Centaure
        attacker.atk_mod += attacker.atk  # x2 sur ce coup
        attacker.hp -= 3
        msg = f"{attacker.name} charge (dégâts x2, -3 PV)"
    elif "parade" in s:         # Guerrier noir
        attacker.guard = True
        msg = f"{attacker.name} se met en Parade (prochain coup bloqué)"
    elif "souffle de feu" in s: # Dragon
        attacker.atk_mod += attacker.spec_val
        defender.burn_turns = max(defender.burn_turns, 2)
        msg = f"{attacker.name} brûle l'ennemi (+{attacker.spec_val} dmg, brûlure)"
    elif "appel de la meute" in s:  # Loup-garou
        attacker.atk_mod += 2 * attacker.atk  # total ~ x3
        msg = f"{attacker.name} multiplie ses dégâts (x3)"
    elif "tir précis" in s:     # Elfe
        defender.df = -10**6  # ignore la DEF en forçant le calcul
        attacker.atk_mod += attacker.spec_val
        msg = f"{attacker.name} tire précisément (8 dégâts vrais)"
    attacker.spec_used = True
    return msg

# Fonction attaque normale
def attack(attacker: Fighter, defender: Fighter) -> str:
    dmg = attacker.base_damage(defender.df)
    if defender.guard:
        defender.guard = False
        dmg = 0
        text = f"{attacker.name} attaque, mais {defender.name} pare tout !"
    else:
        defender.hp -= dmg
        text = f"{attacker.name} inflige {dmg} dmg à {defender.name} (PV {defender.hp})"
    # effets de fin de coup
    if defender.burn_turns > 0:
        defender.hp -= 3
        defender.burn_turns -= 1
        text += f" | Brûlure -3 (PV {defender.hp})"
    # reset mod d'attaque temporaire
    attacker.atk_mod = 0
    return text

# Si l'une des creatures est a 0 PV
def is_ko(f: Fighter) -> bool:
    return f.hp <= 0

# Fonction formule d'une attaque normale
#   attack_player1 = damage_creature_player1 - defense_creature_player2
#   attack_player2 = damage_creature_player2 - defense_creature_player1

# Fonction formule d'attaque spéciale
#   special_attack_player1 = damage_creature_player1 - defense_creature_player2 - PV > attaque normale
#   special_attack_player2 = damage_creature_player2 - defense_creature_player1 - PV > attaque normale
#   mais s'il y a régénération :
#       special_attack_player1, special_attack_player2 = PV_actuel_du_joueur + PV_du_coup_spécial <= PV_max

# Fonction passer son tour
#   si tour = 0 , ne pas afficher l'option
#   sinon attack_player = 0


# while creature_player1.pv > 0 and creature_player2.pv > 0:
#     try:
#         # Affiche les PV creature_player1
#         # Demander l'attaque du Joueur 1: attaquer, capacité spéciale, passer son tour.
#         # - attaquer: utiliser la formule d'attaque normale
#         # - capacité spéciale: utiliser la formule d'attaque spéciale + contraintes PV/régénération
#         # - passer son tour: si tour > 0, attack_player = 0; sinon ne pas afficher l'option
#         # afficher le résumé du tour du joueur 1
#
#         # Affiche les PV creature_player2
#         # Demander l'attaque du Joueur 2:s attaquer, capacité spéciale, passer son tour.
#         # afficher le résumé du tour du joueur 2
#
#         # Incrémenter le compteur de tour
#         # tour += 1
#
#     except ValueError:
#         print("❌ Choisissez une attaque valide")