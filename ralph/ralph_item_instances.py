from ralph_items import *
from ralph_abilities import *
if __name__ == '__main__':
    print('This file contains item instances for ralph.py -- it is not meant to be run by itself')

'''
Item Instances:
3 common, 2 rare, 1 epic, 1 special, 1 legendary weapon per stage, at 3 stages.
1 common, 1 rare, 0-1 epic, 0-1 special, 0-1 legendary armor per stage, at 3 stages.
3 to 4 consumables. maybe a rare item that fuses with a weapon to upgrade it.
Dont have to follow so strictly but stick to this to reduce powercreep.
'''

### Stage 1
#Weapons
rustyironsword = Weapon('Rusty Iron Sword', 'A blade that has corroded with age. Shoddy but works.', rarity = 'common', value = 50, damage = 25)
ironspear = Weapon('Iron Spear', 'Its long tip allows you to strike your enemy at greater distances.', rarity = 'common', value = 60, speed_bonus = 1, damage = 30)
greatsword = Weapon('Greatsword', 'A hunk of metal capable of pulverizing your foes', rarity = 'common', value = 80, damage = 40)

morningstar = Weapon('Morningstar', 'Coated with spikes, the Morningstar is capable of giving your foes deadly wounds.', rarity = 'rare', value = 100, damage = 30, ability = Morningstar_Bleed())
newironsword = Weapon('New Iron Sword', 'Its back, but better. Just works.', rarity = 'rare', value = 120, speed_bonus = 1, damage = 45)

thebat = Weapon('Big Bob', 'Its big frame isn\'t just for show. Though slow, it makes up for it with strength.', rarity = 'epic', value = 150, speed_bonus = -2, damage = 100)

kingsclaws = Weapon('King\'s Claws', 'The pair of claws used by the King of the Jungle. Simply touching it fills you with a surge of primal killing intent.', rarity = 'special', value = 250, speed_bonus = 2, damage = 45, ability = Berserk())

viperfang = Weapon('Viper Fang', 'Tess\' loyal friend. Though without an owner, its edge has not yet lost its luster.', rarity = 'legendary', value = 300, damage = 50, speed_bonus = 3, ability = Poison_Edge())

#Armor
mangrovedwellerarmor = Armor('Mangrove Dweller Armor', 'A set of armor donned by the typical bandit.', rarity = 'rare', value = 100, def_value = 10, speed_bonus = -1, hp_boost = 20)

snakescalearmor = Armor('Snake Scale Armor', 'Another of Tess\' treasured possessions. Its surface its tough, yet is so light that your speed does not get impeded when worn.', rarity = 'legendary', value = 250, def_value = 20, speed_bonus = 0, hp_boost = 50)

#Consumable
smallhealthvial = Consumable(item_name = 'Small Health Vial', desc = 'A small bottle containing a special healing tonic. Restores 30HP per use.', rarity = 'common', value = 20, heal_value = 30)
smallmanavial = Consumable(item_name = 'Small Mana Vial', desc = 'A small mysterious potion that increases magic ability. Restores 3MP per use.', rarity = 'common', value = 20, mp_value = 3)
flaskofminorstrength = Consumable(item_name = 'Flask of Minor Strength', desc = 'This flask holds an elixir, granting a small temporary increase in strength. Increases attack for 3 turns by 10%.', rarity = 'common', value = 30, effect = Minor_Strength())

#Rare Items
glowingironchunk = Item(item_name = 'Glowing Iron Chunk', desc = 'A piece of iron ore. This one seems to have a golden hue to it. Perhaps it has some sort of use?', rarity = 'common', value = 40)



### Stage 2
#Weapons
froststaff = Weapon('Frost Staff', 'A staff holding a frost gem. It is capable of inflicting a slight chill onto foes.', rarity = 'common', value = 60, damage = 40, ability = Minor_Frost())
flamestaff = Weapon('Flame Staff', 'A staff holding a flame gem. It is capable of inflicting small burns onto foes.', rarity = 'common', value = 60, damage = 40, ability = Minor_Flame())
agedgrimoire = Weapon('Aged Grimoire', 'A book holding incantations that can be casted at enemies. Its pages have yellowed.', rarity = 'common', value = 80, damage = 40, speed_bonus = 3)

blizzardbow = Weapon('Blizzard Bow', 'Infused with ice magic, anyone hit by its arrows fall into a state of lethargy, moving visibly slower.', rarity = 'rare', value = 190, damage = 50, speed_bonus = 2, ability = Frost_Shot())
icicle = Weapon('Icicle', 'A dagger made of pure magical ice. Wielding it seems effortless.', rarity = 'rare', value = 240, damage = 40, speed_bonus = 5)
fireball = Weapon('Fire Ball', 'A morningstar left in the pits of magma. Over time, it seems it has been infused with fire.', rarity = 'rare', value = 200, damage = 75, speed_bonus = 0, ability = Fire_Ball_Bleed())

flareblitzblade = Weapon('Flare Blitz Blade', 'The blade crackles with rage. It desires more power.', rarity = 'epic', value = 320, damage = 60, speed_bonus = -1, ability = Overheat())
brokenherosword = Item('Broken Hero Sword', 'A miracle that saved you from Vael\'Grath\'s calamity, albeit sacrificing itself in the process. Once glowing with pride, it is now broken and chipped.', rarity = 'common...', value = 1)
herosword = Hero_Sword('Hero Sword', 'A blade once wielded by Hero Reinhardt. Restored to its original power, the sword glows with a yellow hue. Legends say it was once used to stop the world from falling into purgatory against The Great Dragon.', rarity = 'epic', value = 400, damage = 150, speed_bonus = 1, ability = Luster_Purge(), breaks_into = brokenherosword)

glacierbrand = Lich_Weapon('Glacierbrand', 'A weapon once used by the lich, now corrupted with powers of the dead. It gains power from the fallen.', rarity = 'special', value = 500, damage = 0, base_damage = 50, speed_bonus = 1.5, ability = Soul_King())

hornofvaelgrath = Weapon('Horn of Vael\'Grath', 'Pride of the Great Dragon. Albeit but a piece, the horn pulses with mythical energy.', rarity = 'legendary', value = 600, damage = 100, speed_bonus = -3, ability = Wrath_Of_The_Great_Dragon())

#Armor
furvest = Armor('Fur Vest', 'A simple fur vest.', rarity = 'common', value = 60, def_value = 15, speed_bonus = 1)

heroarmor = Armor('Hero Armor', 'A set of armor once donned by Hero Reinhardt. What\'s this doing here?', rarity = 'epic', value = 200, def_value = 30, speed_bonus = 2, hp_boost = 60, ability = Greater_Restoration())
lichhusk = Armor('Lich Husk', 'The Lich\'s garb. Looks just like a piece of normal cloth, but you can feel a sinister aura from within.', rarity = 'epic', value = 450, def_value = 30, speed_bonus = 2, hp_boost = -40, ability = Siphon())

draconiccarapace_fire = Armor('Draconic Carapace [Fire]', 'Armor formed from the scales of the Great Dragon. Hot to the touch, it feels almost as if it is trying to devour you.', rarity = 'legendary', value = 600, def_value = 45, speed_bonus = -2, hp_boost = 100, ability = Vengeance_Fire())
draconiccarapace_ice = Armor('Draconic Carapace [Ice]', 'Armor formed from the scales of the Great Dragon. Icy to the touch, it feels almost as if it were trying to devour you.', rarity = 'legendary', value = 600, def_value = 45, speed_bonus = -2, hp_boost = 100, ability = Vengeance_Ice())

#Consumable
frostsalve = Consumable('Frost Salve', 'A solution primarily made from mythical herbs. The soothing liquid instantly heals you from Frostbite.', rarity = 'common', value = 40)
embersalve = Consumable('Ember Salve', 'A solution primarily made from mythical herbs. The soothing liquid instantly heals you from Burning.', rarity = 'common', value = 40)
infernalelixir = Consumable('Infernal Elixir', 'A rare drop from Infernals. Their lifeblood appears to have superb restoration qualities.', rarity = 'epic', value = 150, heal_value = 1000, mp_value = 1000)
mediumhealthvial = Consumable('Medium Health Vial', 'A bottle containing a special healing tonic. Restores 60HP per use.', rarity = 'rare', value = 50, heal_value = 60)
mediummanavial = Consumable('Medium Mana Vial', 'A mysterious potion that increases magic ability. Restores 6MP per use.', rarity = 'rare', value = 50, mp_value = 6)
flaskofstrength = Consumable('Flask of Strength', 'This flask holds an elixir, granting a temporary increase in strength. Increases attack for 5 turns by 25%.', rarity = 'rare', value = 30, effect = Strength())
flaskofregeneration = Consumable('Flask of Regeneration', 'A flask containing a solution similar to that in a health vial. Grants health gain (20) over 3 turns.', rarity = 'rare', value = 80, effect = Regeneration())

#Rare Items
valiantgem = Item('Valiant Gem', 'A glowing red gem with a hexagonal shape. It strangely reminds you of a slot in the New Iron Sword.', rarity = 'epic', value = 200)
azarothsheart = Item('Azaroth\'s Heart', 'Heart of the Lich King. Even without a body, it still beats faintly. The cold feels more bearable with the heart by your side.', rarity = 'special', value = 400)