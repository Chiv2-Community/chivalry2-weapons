import { CharacterClass, CharacterSubclass } from "./classes";

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
  staminaDamageNegation?: number;
  attacks: Attacks;
};

export type SpecialAttack = {
  damage: number;
  staminaDamage: number;
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
  staminaDamage: number;
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

