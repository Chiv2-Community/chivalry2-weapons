BASE_STAMINA_DAMAGE_MULT = 0.3;

def stamina_damage(damage: int, damage_type: str) -> float:
    damage_type = damage_type.lower()
    if  damage_type == "chop":
        return damage * BASE_STAMINA_DAMAGE_MULT * 1.1;
    elif damage_type == "blunt":
        return damage * BASE_STAMINA_DAMAGE_MULT * 1.25;
    elif damage_type == "cut":
        return damage * BASE_STAMINA_DAMAGE_MULT;

    raise Exception(f"Unknown damage type: {damage_type}")

def make_stamina_damage(weapon):
    damage_type = weapon["damageType"]

    def add_stamina_damage(attack, damage_type: str):
        attack_damage_type = attack["damageTypeOverride"] if "damageTypeOverride" in attack else damage_type
        attack["staminaDamage"] = stamina_damage(attack["damage"], attack_damage_type)

    for attack, attack_data in weapon["attacks"].items():
        if attack == "average":
            # average attack is calculated later
            continue
        if attack in ["slash", "overhead", "stab"]:
            add_stamina_damage(attack_data["light"], damage_type)
            add_stamina_damage(attack_data["heavy"], damage_type)
        else:
            add_stamina_damage(attack_data, damage_type)

def make_average_attack(weapon):
    ignore_keys = ["cleaveOverride", "damageTypeOverride"]
    has_range = "range" in weapon["attacks"]["slash"]

    average_attack = {"light": {}, "heavy": {}}
    sums = {"light": {}, "heavy": {}, "range": 0, "altRange": 0}
    for attack in ["slash", "overhead", "stab"]:
        currentRangeSum = sums["range"]
        currentAltRangeSum = sums["altRange"]

        # heavy and light attacks have the same keys
        for stat in weapon["attacks"][attack]["light"].keys():
            if stat in ignore_keys:
                continue 

            lightStatValue = weapon["attacks"][attack]["light"][stat]
            heavyStatValue = weapon["attacks"][attack]["heavy"][stat]

            if type(lightStatValue) not in [float, int]:
                try:
                    float(lightStatValue)
                except: 
                    print(f"WARNING: {stat} has type {type(lightStatValue)}, with value {lightStatValue}")
                    continue
                continue

            currentLightSum = sums["light"][stat] if stat in sums["light"] else 0
            currentHeavySum = sums["heavy"][stat] if stat in sums["heavy"] else 0
            sums["light"][stat] = currentLightSum + lightStatValue
            sums["heavy"][stat] = currentHeavySum + heavyStatValue
        
        if has_range:
            sums["range"] = currentRangeSum + weapon["attacks"][attack]["range"]
            sums["altRange"] = currentAltRangeSum + weapon["attacks"][attack]["altRange"]
        
    for stat in sums["light"].keys():
        if stat in ignore_keys:
            continue 

        average_attack["light"][stat] = sums["light"][stat] / 3
        average_attack["heavy"][stat] = sums["heavy"][stat] / 3

    if has_range:
        average_attack["range"] = sums["range"] / 3
        average_attack["altRange"] = sums["altRange"] / 3

    weapon["attacks"]["average"] = average_attack
    
