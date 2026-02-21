from ralph_loot import *
from ralph_item_instances import *
from ralph_entities import *
from ralph_abilities import *
if __name__ == '__main__':
    print('This file contains enemy instances for ralph.py -- it is not meant to be run by itself')


'''
Loot Instances:
Normal enemy level
Mimic encounter
Chest
Miniboss
Stage boss

Again, split by stages in their own dictionaries.
'''

stage1_chest_loot = ChestLoot(loot = [ironspear, greatsword, morningstar, thebat, mangrovedwellerarmor, smallhealthvial, smallmanavial, glowingironchunk], rolls = 2)
stage1_mimic_loot = ChestLoot(loot = [morningstar, thebat, mangrovedwellerarmor, glowingironchunk], rolls = 1)
stage1_enemy_loot = EnemyLoot(xp = 60, money = 40, variation = 10)
stage1_miniboss_loot = BossLoot(xp = 200, money = 150, variation = 0, loot = [kingsclaws,])
stage1_boss_loot = BossLoot(xp = 300, money = 300, variation = 0, loot = [viperfang, snakescalearmor])

stage2_chest_loot = ChestLoot(loot = [froststaff, flamestaff, agedgrimoire, blizzardbow, icicle, fireball, flareblitzblade, furvest, heroarmor, frostsalve, embersalve, mediumhealthvial, mediummanavial, flaskofstrength, flaskofregeneration], rolls = 4)
stage2_volcanicmimic_loot = ChestLoot(loot = [blizzardbow, icicle, heroarmor, flaskofstrength, flaskofregeneration], rolls = 2)
stage2_frostmimic_loot = ChestLoot(loot = [fireball, flareblitzblade, heroarmor, flaskofstrength, flaskofregeneration], rolls = 2)
stage2_enemy_loot = EnemyLoot(xp = 80, money = 65, variation = 20)
stage2_infernal_loot = BossLoot(xp = 80, money = 65, variation = 20, loot = [infernalelixir, None], weights = [20, 80])
stage2_miniboss_loot = BossLoot(xp = 500, money = 400, loot = [lichhusk, glacierbrand])
stage2_boss_loot = BossLoot(xp = 750, money = 800, loot = [hornofvaelgrath, draconiccarapace_fire, draconiccarapace_ice])

'''
Enemy Instances:
3 to 4 varied enemies per stage.
1 elite mini-boss which drops the stage special weapon.
1 boss, meant to be the final room of the stage.

Split by stages, each stage has its own dictionary. Raw instances will not work because it would not be recognised by the external stage class.
'''
### Stage 1
mangrovecrocodile = Enemy('Mangrove Crocodile', 'A common enemy residing in the swamp. Its scales prove hard to break through.', hp = 80, atk = 4, speed = 3, loot = stage1_enemy_loot, defense = 5)
mangrovebandit = Enemy('Mangrove Bandit', 'Thugs attempting to make a name for themselves in the marsh. Their kind will show no mercy to outsiders.', hp = 100, atk = 8, speed = 4, loot = stage1_enemy_loot)
mangroveslime = Enemy('Mangrove Slime', 'An amalgamation of filth. It is believed their sentience is formed from the souls of the fallen.', hp = 60, atk = 5, speed = 2, loot = stage1_enemy_loot)
mangrovemimic = Enemy('Mimic', 'An object imbued with a soul. Its hard surface makes it deceptively hard to defeat.', hp = 100, atk = 3, speed = 2.5, defense = 15, loot = stage1_mimic_loot)
ursoc = Boss('Ursoc, King of the Jungle', 'You have, unfortunately, intruded upon the territory of the King. He does not take such offenses lightly. After all, there is a reason why this place and this place alone is void of bandits. Fight well, as futile as it may be.', hp = 200, atk = 15, speed = 3, defense = 15, loot = stage1_miniboss_loot, ability = Ursoc_Intimidate())
assassin = Boss('Darkwood Assassin Tess', 'One who has made a name for themselves amidst the sea of thieves. You have been marked a target of assassination. Careful now, her poisonous blades are not to be made a fool of.', hp = 200, atk = 10, speed = 4.5, defense = 15, loot = stage1_boss_loot, ability = Tess_Poison())

### Stage 2
frostwraith = Enemy('Frost Wraith', 'A spirit dwelling within the coldness of the tundra.', hp = 150, atk = 10, speed = 5, loot = stage2_enemy_loot, defense = 15, ability = Wraith_Frostbite())
blazeling = Enemy('Blazeling', 'A spirit dwelling within the depths of the volcano. Though its attacks are strong, its structure is fragile.', hp = 90, atk = 25, speed = 5, loot = stage2_enemy_loot, defense = 15)
icegolem = Enemy('Ice Golem', 'A construct formed by the Lich King Azaroth. It has exceedingly high bulk, physical attacks might not work effectively...', hp = 120, atk = 15, speed = 3, loot = stage2_enemy_loot, defense = 80)
infernal = Enemy('Infernal', 'An evolved blazeling. It has undergone adaptation to gain a hardened structure. Expect an encounter with an infernal to be a tough one.', hp = 150, atk = 25, speed = 5, loot = stage2_enemy_loot, defense = 25)

volcanicmimic = Enemy('Volcanic Mimic', 'Just like its cousins, it has a hard exterior, but moves rather slowly.', hp = 180, atk = 20, speed = 2.5, defense = 15, loot = stage2_volcanicmimic_loot)
frostmimic = Enemy('Frost Mimic', 'Just like its cousins, it has a hard exterior, but moves rather slowly.', hp = 180, atk = 10, speed = 2.5, defense = 25, loot = stage2_frostmimic_loot)

lichking = Boss('Lich King Azaroth', 'One who has long since conformed to the corruption of this world. His necromancy powers are not to be underestimated.', hp = 500, atk = 30, speed = 5, defense = 30, loot = stage2_miniboss_loot, ability = Lich_King())
vaelgrath = Boss('Vael\'Grath, The Great Dragon', 'Residing in the volcano\'s core, you have awakened what you should have not. Legends speak of it as an omen for calamity, something that once almost plunged the world into purgatory. Become the hero, the slayer of The Great Dragon, or suffer for eternity in the pits of hell.', hp = 1000, atk = 35, speed = 8, defense = 50, loot = stage2_boss_loot, ability = Vael_Grath())
lefthead = Enemy('Left Head of The Great Dragon', 'Vael\'Grath\'s left head.', hp = 200, atk = 20, speed = 4, defense = 15, loot = stage2_enemy_loot)
righthead = Enemy('Right Head of The Great Dragon', 'Vael\'Grath\'s right head.', hp = 200, atk = 20, speed = 4, defense = 15, loot = stage2_enemy_loot)


