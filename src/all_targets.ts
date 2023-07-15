import { CharacterClass, CharacterSubclass } from "./classes";
import { Target } from "./target";
import { DamageType } from "./weapon";

export const ARCHER = new Target(
    CharacterClass.ARCHER, 
    [CharacterSubclass.LONGBOWMAN, CharacterSubclass.CROSSBOWMAN, CharacterSubclass.SKIRMISHER], 
    90, 
    60, 
    _ => 1
);

export const VANGUARD = new Target(
    CharacterClass.VANGUARD, 
    [CharacterSubclass.DEVASTATOR, CharacterSubclass.RAIDER, CharacterSubclass.AMBUSHER], 
    130, 
    100, 
    _ => 1
);

export const FOOTMAN = new Target(
    CharacterClass.FOOTMAN, 
    [CharacterSubclass.POLEMAN, CharacterSubclass.MAN_AT_ARMS, CharacterSubclass.ENGINEER],  
    150, 
    80, 
    dt => { 
        switch(dt) {
            case DamageType.CHOP: return 1.175;
            case DamageType.BLUNT: return 1.35;
            case DamageType.CUT: return 1;
            default: return 1;
        }
    }
);

export const KNIGHT = new Target(
    CharacterClass.KNIGHT, 
    [CharacterSubclass.OFFICER, CharacterSubclass.GUARDIAN, CharacterSubclass.CRUSADER], 
    175, 
    80, 
    dt => {
        switch(dt) {
            case DamageType.CHOP: return 1.25;
            case DamageType.BLUNT: return 1.5;
            case DamageType.CUT: return 1;
            default: return 1;
        }
    }
);

const allTargetsNoAverage = [ARCHER, VANGUARD, FOOTMAN, KNIGHT];

const averageStamina = allTargetsNoAverage.reduce((acc, target) => acc + target.stamina, 0) / allTargetsNoAverage.length;
const averageHp = allTargetsNoAverage.reduce((acc, target) => acc + target.hp, 0) / allTargetsNoAverage.length;

export const AVERAGE = new Target(
    CharacterClass.AVERAGE, 
    [CharacterSubclass.AVERAGE], 
    averageStamina, 
    averageHp, 
    dt => {
        const sum = allTargetsNoAverage.reduce((acc, target) => acc + target.damageMultiplier(dt), 0);
        return sum / allTargetsNoAverage.length;
    }
);

export const ALL_TARGETS = [ARCHER, VANGUARD, FOOTMAN, KNIGHT, AVERAGE];

export function targetByName(name: string): Target | undefined {
  return ALL_TARGETS.find(target => target.characterClass.toLowerCase() === name.toLowerCase());
}