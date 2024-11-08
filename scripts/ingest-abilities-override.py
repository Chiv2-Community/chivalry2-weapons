import json
import re
import sys
import os
from collections.abc import Mapping
import argparse

from common import write_dicts_to_csv, VALID_ATTACKS
from derived_stats import make_average_attack, make_stamina_damage

def seconds_to_millis(n):
    return n * 1000 if n != -1 else -1

WEAPON_NAME_OVERRIDES = {
    "Longsword_Argon_Citadel": "Argon's Sword",
    "Greatsword_Malric": "Lion's Bane",
    "Carryable_Candelabra": "Candelabra",
}

def adapt_name(name: str) -> str:
    """Adapt weapon name to match the JSON file name."""
    return WEAPON_NAME_OVERRIDES[name] if name in WEAPON_NAME_OVERRIDES else name

STAT_TRANSFORMS = {
    "windup": seconds_to_millis,
    "release": seconds_to_millis,
    "recovery": seconds_to_millis,
    "combo": seconds_to_millis,
    "holding": seconds_to_millis,
    "thwack": seconds_to_millis,
    "riposte": seconds_to_millis,
}

# When the stats on the left are undefined (-1 or 0), they should fall back to the stat on the right.
STAT_FALLBACKS = {
    "riposte": "windup",
    "thwack": "release"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_json", required=True, help="Path to the input JSON file")
    parser.add_argument("-o", "--output_dir", required=True, help="Path to the output directory")
    parser.add_argument("-c", "--changelog_location", required=True, help="Path to output the changelog json")
    args = parser.parse_args()

    base_defaults = {}
    attack_defaults = {}
    weapon_defaults = {}
    weapons = {}

    data = fetch_data(args.input_json)[0]["Rows"]

    for name, item in data.items():
        process_item(name, item, base_defaults, attack_defaults, weapon_defaults, weapons)

    apply_defaults(weapons, attack_defaults)

    write_to_file(list(weapons.values()), args.output_dir, args.changelog_location)

def lowercase_first_char(in_str):
    return in_str[0].lower() + in_str[1:]

def fetch_data(path):
    with open(path) as user_file:
      return json.load(user_file)

def clean_item(item):#, VALID_STATS):
    return {lowercase_first_char(key): item[key] for key in item.keys()}#VALID_STATS}

def process_item(name, item, base_defaults, attack_defaults, weapon_defaults, weapons):
    name_parts = name.split('.')
    item = clean_item(item)#, VALID_STATS)
    attack_type = lowercase_first_char(name_parts[1]) if len(name_parts) > 1 else None

    if attack_type and attack_type not in VALID_ATTACKS: 
        return

    if name_parts[0] == 'Default':
        process_default_item(name_parts, attack_type, item, base_defaults, attack_defaults)
    else:
        process_weapon_item(name_parts, attack_type, item, weapon_defaults, weapons)

def process_default_item(name_parts, attack_type, item, base_defaults, attack_defaults):
    if len(name_parts) == 1:
        base_defaults = item
    else:
        attack_defaults = process_attack(attack_type, item, attack_defaults)

def process_weapon_item(name_parts, attack_type, item, weapon_defaults, weapons):
    if len(name_parts) == 1:
        weapon_defaults[name_parts[0]] = item
    else:
        weapon_name = name_parts[0].replace("Weapon_", "")
        

        if weapon_name not in weapons:
            weapons[weapon_name] = {"name": weapon_name, "attacks": {}}
        weapons[weapon_name]["attacks"] = process_attack(attack_type, item, weapons[weapon_name]["attacks"])

def process_attack(attack_type, item, attacks):
    if "Heavy" in attack_type:
        attack_type = attack_type.replace("Heavy", "")
        if attack_type not in attacks:
            attacks[attack_type] = {"light": {}, "heavy": {}}
        attacks[attack_type]["heavy"] = apply_stat_transforms(item)
    elif attack_type in ["slash", "overhead", "stab"]:
        if attack_type not in attacks:
            attacks[attack_type] = {"light": {}, "heavy": {}}
        attacks[attack_type]["light"] = apply_stat_transforms(item)
    else:
        if attack_type not in attacks:
            attacks[attack_type] = {}
        attacks[attack_type] = apply_stat_transforms(item)
    return attacks

def derive_stats(weapon):
    if "slash" not in weapon["attacks"]:
        return 

    if "id" in weapon:
        make_stamina_damage(weapon)

    make_average_attack(weapon)

    if "sprintCharge" not in weapon["attacks"]:
        weapon["attacks"]["sprintCharge"] = weapon["attacks"]["sprintAttack"]

def apply_defaults(weapons, attack_defaults):
    for weapon, weapon_data in weapons.items():
        for attack, attack_data in weapon_data["attacks"].items():
            if attack in ["slash", "overhead", "stab"]:
                for attack_subtype, item in attack_data.items():
                    for key in item.keys():
                        if item[key] == -1:
                            item[key] = attack_defaults[attack][attack_subtype][key]
            else:
                for key in attack_data.keys():
                    if attack_data[key] == -1:
                        if key in attack_defaults.get(attack, {}):
                            attack_data[key] = attack_defaults[attack][key]

def write_to_file(data, foldername, changelog_location):
    try:
        if not os.path.exists(foldername):
            os.mkdir(foldername)

        changelog = {}
        merged_weapons = []
        for weapon in data:
            path = foldername + "/" + pascal_to_camel(weapon["name"]) + ".json"
            weapon["name"] = adapt_name(weapon["name"])
            exists = os.path.isfile(path)
            existing_data = {}
            if exists:
                existing_data = fetch_data(path)

            with open(path, 'w') as outfile:
                (changes, merged) = deep_merge(weapon["name"], existing_data, weapon)
                derive_stats(merged)
                if len(changes) > 0:
                    changelog[weapon["name"]] = changes
                merged["name"] = pascal_to_space(weapon["name"])
                merged_weapons.append(merged)
                json.dump(merged, outfile, indent=2)

        for (name, changes) in changelog.items():
            for change in changes:
                full_path = name + "." + '.'.join(change['path'])
		
                print(full_path + ": " + str(change['old']) + " -> " + str(change['new']))
        
        #write_dicts_to_csv(data, foldername + "/data.csv")

        changelog_text = ""
        for (name, changes) in changelog.items():
            changelog_text += name + ":\n"
            for change in changes:
                new_string = str(change['new']) if not isinstance(change['new'], dict) else json.dumps(change['new'], indent=12)
                changelog_text += "\t" + '.'.join(change['path']) + ": " + str(change['old']) + " -> " + new_string + "\n"

        with open(changelog_location, 'w') as changelog_file: 
            changelog_file.write(changelog_text)

    except IOError as e:
        print(e)
        sys.exit("Unable to write to JSON file!")


def pascal_to_camel(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def pascal_to_space(s):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s).replace("  ", " ")

def apply_stat_transforms(data):
    for key, value in data.items():
        if key in STAT_TRANSFORMS:
            data[key] = STAT_TRANSFORMS[key](value)
    
    # after applying transformations, apply fallbacks
    for key, value in data.items():
        if value in [-1, 0]:
            if key in STAT_FALLBACKS:
                data[key] = data[STAT_FALLBACKS[key]]
            else:
                print("WARNING: -1 or 0 value found for " + key)

    return data

def deep_merge(name, dict1, dict2, path=None):
    "Deeply merge two dictionaries and print out the differences."

    changes = []

    if path is None: 
        path = []

    for key in dict2:
        value = dict2[key]
        if key in dict1:
            if isinstance(dict1[key], Mapping) and isinstance(value, Mapping):
                (new_changes, _) = deep_merge(name, dict1[key], value, path + [str(key)])
                changes += new_changes
            else: 
                if dict1[key] == value:
                    pass # same leaf value
                else:
                    changes.append({'path': path + [key], 'old': dict1[key], 'new': value})
                    dict1[key] = value
        else:
            changes.append({'path': path + [key], 'old': None, 'new': value})
            dict1[key] = value
    return (changes, dict1)

if __name__ == '__main__':
    main()

