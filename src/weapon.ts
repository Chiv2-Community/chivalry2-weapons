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
  thwack: number;
  riposte: number;
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
  thwack: number;
  riposte: number;
  cleaveOverride?: boolean;
  damageTypeOverride?: DamageType;
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
