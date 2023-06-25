export type Attacks = {
  average: Swing;
  slash: Swing;
  overhead: Swing;
  stab: Swing;
  sprintAttack: SpecialAttack;
  sprintCharge: SpecialAttack;
  special: SpecialAttack;
  throw: SpecialAttack;
};

export type Weapon = {
  id: string;
  name: string;
  aliases?: string[];
  classes: CharacterClass[];
  subclasses: CharacterSubclass[];
  weaponTypes: WeaponType[];
  damageType: DamageType;
  attacks: Attacks;
};

export type SpecialAttack = {
  damage: number;
  holding: number;
  windup: number; 
  release: number; 
  recovery: number; 
  combo: number;
  range?: number; // Not measured yet
  cleaveOverride?: boolean;
  damageTypeOverride?: DamageType;
};

export type Swing = {
  range: number;
  altRange: number;
  light: MeleeAttack;
  heavy: MeleeAttack;
};

export type MeleeAttack = {
  damage: number;
  holding: number;
  windup: number; 
  release: number; 
  recovery: number; 
  combo: number;
  cleaveOverride?: boolean;
};

export type ProjectileDamage = {
  head: number;
  torso: number;
  legs: number;
};

export enum DamageType {
  CUT = "Cut",
  CHOP = "Chop",
  BLUNT = "Blunt"
};

export enum WeaponType {
  AXE = "Axe",
  HAMMER = "Hammer",
  CLUB = "Club",
  TOOL = "Tool",
  POLEARM = "Polearm",
  SPEAR = "Spear",
  SWORD = "Sword",
  Dagger = "Dagger",
  BOW = "Bow",
  TWO_HANDED = "Two Handed",
  ONE_HANDED = "One Handed",
};

export enum CharacterClass {
  ARCHER = "Archer",
  VANGUARD = "Vanguard",
  FOOTMAN = "Footman",
  KNIGHT = "Knight"
}

export enum CharacterSubclass {
  LONGBOWMAN = "Longbowman",
  CROSSBOWMAN = "Crossbowman",
  SKIRMISHER = "Skirmisher",

  DEVASTATOR = "Devastator",
  RAIDER = "Raider",
  AMBUSHER = "Ambusher",

  POLEMAN = "Poleman",
  MAN_AT_ARMS = "Man at Arms",
  ENGINEER = "Engineer",

  OFFICER = "Officer",
  GUARDIAN = "Guardian",
  CRUSADER = "Crusader"
}



export enum Target {
  ARCHER = "ARCHER",
  VANGUARD = "VANGUARD",
  FOOTMAN = "FOOTMAN",
  KNIGHT = "KNIGHT",
  AVERAGE = "AVERAGE"
}

export function canCleave(w: Weapon, path: string): boolean {
  let pathParts = path.split(".")
  pathParts.pop()
  let overridePath = pathParts.join(".") + ".cleaveOverride",
      cleaveOverride = extract<boolean>(w, overridePath, true)

  if (cleaveOverride != undefined) 
    return cleaveOverride

  if(path.startsWith("attacks")) {
    if(path.includes('heavy'))
      return true;
    
    return w.damageType != DamageType.BLUNT;
  }
  return false;
}


export function extract<T>(weapon: Weapon, path: string, optional: boolean = false): T|undefined {
  let current: any = weapon; // eslint-disable-line
  const parts = path.split(".");
  for (const part of parts) {
    if (part in current) {
      current = current[part];
    } else {
      if(!optional)
        throw new Error(`Invalid stat ${weapon.name} path specified: ${path}`);
      return undefined;
    }
  }
  return current 
}

export function bonusMult(numberOfTargets: number, target: Target, type: DamageType, cleaves: boolean): number {
  const cleavingMultiplier = cleaves ? numberOfTargets : 1

  // Multiply Vanguard / Archer by 2 assuming equal distribution of target classes
  if (target === Target.AVERAGE) {
    const sum =
      bonusMult(numberOfTargets, Target.ARCHER, type, cleaves) +
      bonusMult(numberOfTargets, Target.VANGUARD, type, cleaves) +
      bonusMult(numberOfTargets, Target.FOOTMAN, type, cleaves) +
      bonusMult(numberOfTargets, Target.KNIGHT, type, cleaves);

    return sum / 4;
  } else if ([Target.VANGUARD, Target.ARCHER].includes(target)) {
    return cleavingMultiplier;
  } else if (type === DamageType.CHOP) {
    return (target === Target.FOOTMAN ? 1.175 : 1.25) * cleavingMultiplier;
  } else if (type === DamageType.BLUNT) {
    return (target === Target.FOOTMAN ? 1.35 : 1.5) * cleavingMultiplier;
  }

  return cleavingMultiplier;
}

export function extractNumber(weapon: Weapon, path: string): number {
  let result = extract<number>(weapon, path);

  if(result == undefined) {
    return 0;
  }

  return result
};

export function withBonusMultipliers(w: Weapon, numberOfTargets: number, horsebackDamageMult: number, target: Target): Weapon {
  return {
    ...w,
    "attacks": {
      ...w.attacks,
      "slash": {
        ...w.attacks.slash,
        "light": {
          ...w.attacks.slash.light,
          "damage": w.attacks.slash.light.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.slash.light.damage")) * horsebackDamageMult
        },
        "heavy": {
          ...w.attacks.slash.heavy,
          "damage": w.attacks.slash.heavy.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.slash.heavy.damage")) * horsebackDamageMult
        }
      },
      "overhead": {
        ...w.attacks.overhead,
        "light": {
          ...w.attacks.overhead.light,
          "damage": w.attacks.overhead.light.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.overhead.light.damage")) * horsebackDamageMult
        },
        "heavy": {
          ...w.attacks.overhead.heavy,
          "damage": w.attacks.overhead.heavy.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.overhead.heavy.damage")) * horsebackDamageMult
        }
      },
      "stab": {
        ...w.attacks.stab,
        "light": {
          ...w.attacks.stab.light,  
          "damage": w.attacks.stab.light.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.stab.light.damage")) * horsebackDamageMult
        },
        "heavy": {
          ...w.attacks.stab.heavy,  
          "damage": w.attacks.stab.heavy.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.stab.heavy.damage")) * horsebackDamageMult
        }
      },
      "average": {
        ...w.attacks.average,
        "light": {
          ...w.attacks.average.light,
          "damage": w.attacks.average.light.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.average.light.damage")) * horsebackDamageMult
        },
        "heavy": {
          ...w.attacks.average.heavy,
          "damage": w.attacks.average.heavy.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.average.heavy.damage")) * horsebackDamageMult
        }
      },
      "sprintAttack": {
        ...w.attacks.sprintAttack,
          "damage": w.attacks.sprintAttack.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.sprintAttack.damage")) * horsebackDamageMult
      },
      "sprintCharge": {
        ...w.attacks.sprintCharge,
          "damage": w.attacks.sprintCharge.damage * bonusMult(numberOfTargets, target, w.damageType, false) * horsebackDamageMult
      },
      "special": {
        ...w.attacks.special,
          "damage": w.attacks.special.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.special.damage")) * horsebackDamageMult
      },
      "throw": {
        ...w.attacks.throw,
        "damage": w.attacks.throw.damage * bonusMult(numberOfTargets, target, w.damageType, canCleave(w, "attacks.throw.damage")) * horsebackDamageMult
      },
    }
  } as Weapon
}