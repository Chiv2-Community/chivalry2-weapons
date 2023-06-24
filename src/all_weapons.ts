import AXE_IMPORT from "./weapons/axe.json";
import BATTLE_AXE_IMPORT from "./weapons/battle_axe.json";
import CUDGEL_IMPORT from "./weapons/cudgel.json";
import DAGGER_IMPORT from "./weapons/dagger.json";
import DANE_AXE_IMPORT from "./weapons/dane_axe.json";
import EXECUTIONERS_AXE_IMPORT from "./weapons/executioners_axe.json";
import FALCHION_IMPORT from "./weapons/falchion.json";
import GLAIVE_IMPORT from "./weapons/glaive.json";
import GREATSWORD_IMPORT from "./weapons/greatsword.json";
import HALBERD_IMPORT from "./weapons/halberd.json";
import HATCHET_IMPORT from "./weapons/hatchet.json";
import HEAVY_MACE_IMPORT from "./weapons/heavy_mace.json";
import CAVALRY_SWORD_IMPORT from "./weapons/heavy_cavalry_sword.json"
import HIGHLAND_SWORD_IMPORT from "./weapons/highland_sword.json";
import JAVELIN_IMPORT from "./weapons/javelin.json";
import KATARS_IMPORT from "./weapons/katars.json"
import KNIFE_IMPORT from "./weapons/knife.json";
import LONGSWORD_IMPORT from "./weapons/longsword.json";
import MACE_IMPORT from "./weapons/mace.json";
import MALLET_IMPORT from "./weapons/throwing_mallet.json";
import MAUL_IMPORT from "./weapons/maul.json";
import MESSER_IMPORT from "./weapons/messer.json";
import MORNING_STAR_IMPORT from "./weapons/morning_star.json";
import ONE_HANDED_SPEAR_IMPORT from "./weapons/one_handed_spear.json";
import PICKAXE_IMPORT from "./weapons/pickaxe.json";
import POLEAXE_IMPORT from "./weapons/pole_axe.json";
import POLEHAMMER_IMPORT from "./weapons/polehammer.json";
import QUARTERSTAFF_IMPORT from "./weapons/quarterstaff.json"
import RAPIER_IMPORT from "./weapons/rapier.json";
import SHORT_SWORD_IMPORT from "./weapons/short_sword.json";
import SHOVEL_IMPORT from "./weapons/shovel.json";
import SLEDGEHAMMER_IMPORT from "./weapons/sledgehammer.json";
import SWORD_IMPORT from "./weapons/sword.json";
import THROWING_AXE_IMPORT from "./weapons/throwing_axe.json";
import TWO_HANDED_HAMMER_IMPORT from "./weapons/two_handed_hammer.json";
import SPEAR_IMPORT from "./weapons/spear.json";
import WAR_AXE_IMPORT from "./weapons/war_axe.json";
import WAR_CLUB_IMPORT from "./weapons/war_club.json";
import WARHAMMER_IMPORT from "./weapons/warhammer.json";
import { Weapon } from "./weapon";

export const AXE = AXE_IMPORT as Weapon;
export const BATTLE_AXE = BATTLE_AXE_IMPORT as Weapon;
export const CUDGEL = CUDGEL_IMPORT as Weapon;
export const DAGGER = DAGGER_IMPORT as Weapon;
export const DANE_AXE = DANE_AXE_IMPORT as Weapon;
export const EXECUTIONERS_AXE = EXECUTIONERS_AXE_IMPORT as Weapon;
export const FALCHION = FALCHION_IMPORT as Weapon;
export const GLAIVE = GLAIVE_IMPORT as Weapon;
export const GREATSWORD = GREATSWORD_IMPORT as Weapon;
export const HALBERD = HALBERD_IMPORT as Weapon;
export const HATCHET = HATCHET_IMPORT as Weapon;
export const HEAVY_MACE = HEAVY_MACE_IMPORT as Weapon;
export const CAVALRY_SWORD = CAVALRY_SWORD_IMPORT as Weapon;
export const HIGHLAND_SWORD = HIGHLAND_SWORD_IMPORT as Weapon;
export const JAVELIN = JAVELIN_IMPORT as Weapon;
export const KATARS = KATARS_IMPORT as Weapon;
export const KNIFE = KNIFE_IMPORT as Weapon;
export const LONGSWORD = LONGSWORD_IMPORT as Weapon;
export const MACE = MACE_IMPORT as Weapon;
export const MALLET = MALLET_IMPORT as Weapon;
export const MAUL = MAUL_IMPORT as Weapon;
export const MESSER = MESSER_IMPORT as Weapon;
export const MORNING_STAR = MORNING_STAR_IMPORT as Weapon;
export const ONE_HANDED_SPEAR = ONE_HANDED_SPEAR_IMPORT as Weapon;
export const PICKAXE = PICKAXE_IMPORT as Weapon;
export const POLEAXE = POLEAXE_IMPORT as Weapon;
export const POLEHAMMER = POLEHAMMER_IMPORT as Weapon;
export const QUARTERSTAFF = QUARTERSTAFF_IMPORT as Weapon;
export const RAPIER = RAPIER_IMPORT as Weapon;
export const SHORT_SWORD = SHORT_SWORD_IMPORT as Weapon;
export const SHOVEL = SHOVEL_IMPORT as Weapon;
export const SLEDGEHAMMER = SLEDGEHAMMER_IMPORT as Weapon;
export const SWORD = SWORD_IMPORT as Weapon;
export const THROWING_AXE = THROWING_AXE_IMPORT as Weapon;
export const TWO_HANDED_HAMMER = TWO_HANDED_HAMMER_IMPORT as Weapon;
export const SPEAR = SPEAR_IMPORT as Weapon;
export const WAR_AXE = WAR_AXE_IMPORT as Weapon;
export const WAR_CLUB = WAR_CLUB_IMPORT as Weapon;
export const WARHAMMER = WARHAMMER_IMPORT as Weapon;

const ALL_WEAPONS: Weapon[] = [
  AXE,
  BATTLE_AXE,
  CUDGEL,
  CAVALRY_SWORD, 
  DAGGER,
  DANE_AXE,
  EXECUTIONERS_AXE,
  FALCHION,
  GLAIVE,
  GREATSWORD,
  HALBERD,
  HATCHET,
  HEAVY_MACE,
  HIGHLAND_SWORD,
  JAVELIN,
  KATARS, 
  KNIFE,
  LONGSWORD,
  MACE,
  MALLET,
  MAUL,
  MESSER,
  MORNING_STAR,
  ONE_HANDED_SPEAR,
  PICKAXE,
  POLEAXE,
  POLEHAMMER,
  QUARTERSTAFF, 
  RAPIER,
  SHORT_SWORD,
  SHOVEL,
  SLEDGEHAMMER,
  SWORD,
  THROWING_AXE,
  TWO_HANDED_HAMMER,
  SPEAR,
  WAR_AXE,
  WAR_CLUB,
  WARHAMMER,
]

export function weaponByName(name: string) {
  return ALL_WEAPONS.find((w) => w.name === name);
}

export function weaponById(id: string) {
  return ALL_WEAPONS.find((w) => w.id === id);
}

export default ALL_WEAPONS;
