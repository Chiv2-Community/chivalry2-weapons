import json
import argparse
import os

from common import VALID_ATTACKS, write_dicts_to_csv

MATCHUP_STAT_WEIGHTS = {
    "windup": -0.25, 
    "release": 0.25, 
    "recovery": -0.25, 
    "combo": -0.25, 

    "damage": 1, 

    "range": 1, 
    "altRange": 1 
}


MATCHUP_ATTACK_WEIGHTS = {
    "average": 0,
    "slash": 1,
    "overhead": 1,
    "stab": 1,
    "special": 0,
    "sprintAttack": 0,
    "sprintCharge": 0,
    "throw": 0,
}

HEAVY_WEIGHT = 1
LIGHT_WEIGHT = 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weapons_dir", required=True, help="Path to the weapons directory")
    parser.add_argument("-o", "--output", required=True, help="Where to put the file")
    args = parser.parse_args()
    
    weapons_location = args.weapons_dir + "/" if args.weapons_dir[-1] != "/" else args.weapons_dir
    output_file_path = args.output

    weapons = []
    weapons_files = os.listdir(weapons_location)
    for weapon_file in weapons_files:
        if weapon_file[-5:] != ".json":
            continue

        with open(weapons_location + weapon_file, "r") as f:
            weapons.append(json.load(f))
    
    matchups = calculate_matchups(weapons)
    write_dicts_to_csv(matchups, output_file_path, ["name"] + list(map(lambda r: r["name"], matchups)) + ["average_matchup", "winning_matchups", "losing_matchups", "tied_matchups"])


def calculate_matchups(weapons):
    weapons = list(filter(lambda w : "id" in w, weapons))
    weapons = calculate_damage_output(weapons)
    matchups = []
    for weapon in weapons:
        current_matchups = {}
        current_matchups["name"] = weapon["name"]
        for other_weapon in weapons:
            current_matchups[other_weapon["name"]] = calculate_matchup(weapon, other_weapon)

        matchup_numbers = [v for k, v in current_matchups.items() if type(v) in [int, float]]

        current_matchups["winning_matchups"] = len([v for v in matchup_numbers if v > 0.01])
        current_matchups["losing_matchups"] = len([v for v in matchup_numbers if v < -0.01])
        current_matchups["tied_matchups"] = len(weapons) - current_matchups["winning_matchups"] - current_matchups["losing_matchups"]
        current_matchups["average_matchup"] = sum(matchup_numbers) / len(matchup_numbers);

        print("Matchups for " + weapon["name"] + ": ")
        print("\tAverage matchup: " + str(current_matchups["average_matchup"]))
        print("\tWinning matchups: " + str(current_matchups["winning_matchups"]))
        print("\tLosing matchups: " + str(current_matchups["losing_matchups"]))
        print("\tTied matchups: " + str(current_matchups["tied_matchups"]))
        print("")

        matchups.append(current_matchups)
    
    matchups.sort(key=lambda x: x["average_matchup"], reverse=True)
    return matchups

def calculate_matchup(weapon, other_weapon):
    matchup = 0
    for attack_name, attack in weapon["attacks"].items():
        if attack_name not in VALID_ATTACKS:
            continue 

        other_attack = other_weapon["attacks"][attack_name]
        matchup += calculate_matchup_stats(attack_name, attack, other_attack)
    return matchup

def calculate_matchup_stats(attack_name, source_weapon_attack, other_weapon_attack):
    if attack_name not in VALID_ATTACKS or MATCHUP_ATTACK_WEIGHTS[attack_name] == 0:
        return 0

    matchup = 0

    attack_weight = MATCHUP_ATTACK_WEIGHTS[attack_name]

    if attack_name in ["slash", "overhead", "stab", "average"]:
        matchup += calculate_matchup_winner(
            attack_weight * MATCHUP_STAT_WEIGHTS["range"], 
            source_weapon_attack["range"], 
            other_weapon_attack["range"]
        ) 
        
        matchup += calculate_matchup_winner(
            attack_weight * MATCHUP_STAT_WEIGHTS["altRange"], 
            source_weapon_attack["altRange"], 
            other_weapon_attack["altRange"]
        )
        
        for stat, value in source_weapon_attack["light"].items():
            if stat not in MATCHUP_STAT_WEIGHTS:
                continue

            other_value = other_weapon_attack["light"][stat]
            weight = attack_weight * MATCHUP_STAT_WEIGHTS[stat] * LIGHT_WEIGHT
            matchup += calculate_matchup_winner(weight, value, other_value)

        for stat, value in source_weapon_attack["heavy"].items():
            if stat not in MATCHUP_STAT_WEIGHTS:
                continue
            
            other_value = other_weapon_attack["heavy"][stat]
            weight = attack_weight * MATCHUP_STAT_WEIGHTS[stat] * HEAVY_WEIGHT
            matchup += calculate_matchup_winner(weight, value, other_value)

    else:
        for stat, value in source_weapon_attack.items():
            if stat not in MATCHUP_STAT_WEIGHTS:
                continue

            other_value = other_weapon_attack[stat]
            weight = attack_weight * MATCHUP_STAT_WEIGHTS[stat]
            matchup += calculate_matchup_winner(weight, value, other_value)

    return matchup

def calculate_matchup_winner(weight, a, b):
    if a > b:
        return weight
    elif a < b:
        return -weight
    else:
        return 0

def calculate_damage_output(weapons):
    updated_weapons = []
    for weapon in weapons:
        damage_type = weapon["damageType"]
        damage_multiplier = 1
        if damage_type == "Blunt":
            damage_multiplier = 1.2125 # (1 + 1 +1.35 + 1.5) / 4
        elif damage_type == "Slash":
            damage_multiplier = 1.10625

        for attack_name, attack in weapon["attacks"].items():
            if attack_name in ["slash", "overhead", "stab", "average"]:
                attack["light"]["damage"] = attack["light"]["damage"] * damage_multiplier
                attack["heavy"]["damage"] = attack["heavy"]["damage"] * damage_multiplier
            else:
                attack["damage"] = attack["damage"] * damage_multiplier

            weapon[attack_name] = attack
        updated_weapons.append(weapon)

    return updated_weapons
        
if __name__ == '__main__':
    main()