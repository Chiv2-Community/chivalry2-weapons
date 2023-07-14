import { CharacterClass, CharacterSubclass } from "./classes";
import { DamageType } from "./weapon";

export class Target {
  constructor(
    public characterClass: CharacterClass,
    public characterSubclasses: CharacterSubclass[],
    public hp: number,
    public stamina: number,
    public damageMultiplier: (dt: DamageType) => number,
  ) {
    this.characterClass = characterClass;
    this.characterSubclasses = characterSubclasses;
    this.hp = hp;
    this.stamina = stamina;
    this.damageMultiplier = damageMultiplier;
  };
}