import random
import time
if __name__ == '__main__':
    print('This file contains Ability classes for ralph.py -- it is not meant to be run by itself')

class Ability:

    def __init__(self):
        self._name = None
        self.desc = None
        self.mp_cost = 0
        self.turns_till_use = 0

        '''
        Ability Characteristics
        Tags:
        1. to_self -> defines whether ability is targeted at self or enemy      (DEPRECATED)
        2. spends_turn -> defines whether ability uses up the turn
        3. active -> defines whether ability is active. if active, it should show up on action bar
        4. effect -> defines whether ability is a status effect type    (DEPRECATED)
        5. on_hit -> defines if ability is activated on hit. paired with self.hits and self.hits_left to define how many hits left with the ability
        6. on_struck -> defines if ability is activated upon being hit. similarly paired with self.hits and self.hits_left
        7. damage -> defines whether ability is a damage type (i.e instant damage)      (DEPRECATED)
        '''
        self.duration = 0
        self.cooldown = 0
        self._tags = []

        '''
        Stat Modifiers
        '''
        self._atk_mod = None
        self._def_mod = None
        self._def_add = None
        self._spd_add = None

        '''
        DoT
        '''
        self._dot = None
        self._hot = None

    @property
    def is_usable(self):
        return self.turns_till_use == 0 and 'active' in self.tags
    @property
    def targets_self(self):
        return 'to_self' in self.tags
    @property
    def spends_turn(self):
        return 'spends_turn' in self.tags
    @property
    def is_active(self):
        return 'active' in self.tags
    @property
    def is_effect(self):
        return 'effect' in self.tags
    @property
    def triggers_on_hit(self):
        return 'on_hit' in self.tags
    @property
    def triggers_on_struck(self):
        return 'on_struck' in self.tags
    @property
    def is_damage(self):
        return 'damage' in self.tags
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self, value):
        self._tags = value
    @property
    def atk_mod(self):
        return self._atk_mod
    @atk_mod.setter
    def atk_mod(self, value):
        self._atk_mod = value
    @property
    def def_mod(self):
        return self._def_mod
    @def_mod.setter
    def def_mod(self, value):
        self._def_mod = value
    @property
    def def_add(self):
        return self._def_add
    @def_add.setter
    def def_add(self, value):
        self._def_add = value
    @property
    def spd_add(self):
        return self._spd_add
    @spd_add.setter
    def spd_add(self, value):
        self._spd_add = value
    @property
    def dot(self):
        return self._dot
    @dot.setter
    def dot(self, value):
        self._dot = value
    @property
    def hot(self):
        return self._hot
    @hot.setter
    def hot(self, value):
        self._hot = value
    
    def use(self):
        self.turns_till_use = self.cooldown
        print('No implementation for ability yet.')
    

class Morningstar_Bleed(Ability):

    def __init__(self):
        super().__init__()      #to load up all the variables

        self.name = 'Morningstar Bleed'
        self.desc = 'Inflicts a Bleed effect, causing health loss (10) for 3 turns. Cooldown: 5 Turns.'

        self.effect_name = 'Bleed'
        self.mp_cost = 1
        self.duration = 3
        self.cooldown = 5
        self.tags = ['active', 'effect']

        self.dot = 10

    def use(self, user, target):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'{target.name} has been inflicted with {self.effect_name}!')

class Berserk(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Berserk'
        self.desc = 'The claws induce rage within you, giving you [+30%] attack, [+10] defense and [+1] speed for 5 turns. Cooldown: 8 turns.'

        self.effect_name = 'Enraged'
        self.mp_cost = 3
        self.duration = 5
        self.cooldown = 8
        self.tags = ['active', 'effect', 'to_self', 'spends_turn']

        self.atk_mod = 1.3
        self.def_add = 10
        self.spd_add = 1

    def use(self, user, target = None):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        user.statuses[self] = self.duration
        print(f'Berserk used! You are now [Enraged]!')

class Poison_Edge(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Poison Edge'
        self.desc = 'A passive ability belonging to the Viper Fang. Inflicts a poison effect, causing health loss (10) while giving [-30%] attack for 2 turns with every hit.'

        self.effect_name = 'Poison'
        self.mp_cost = 2
        self.duration = 2
        self.tags = ['effect', 'on_hit']
        self.hits = 1
        self.hits_left = 1

        self.atk_mod = 0.7
        self.dot = 10
    
    def on_hit_use(self, user, target):
        user.mp -= self.mp_cost
        if self in target.statuses:
            print(f'{target.name} is already inflicted with Poison.')
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'{target.name} has been inflicted with [{self.effect_name}]!')

class Minor_Strength(Ability):

    def __init__(self):
        super().__init__()

        self.effect_name = 'Minor Strength'
        self.duration = 3
        self.tags = ['effect', 'to_self']

        self.atk_mod = 1.1
    
    def use(self, user):
        user.statuses[self] = self.duration

class Tess_Poison(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Poison Edge'
        self.desc = 'Inflicts a Poison effect, causing health loss (10) and [-30%] attack for 3 turns. Cooldown: 5 turns'

        self.effect_name = 'Poison'
        self.duration = 3
        self.cooldown = 5
        self.tags = ['effect', 'active']

        self.atk_mod = 0.7
        self.dot = 10

    def use(self, user, target):
        self.turns_till_use = self.cooldown
        target.statuses[self] = self.duration
    
    def message(self):
        print('Tess\' blade digs into your skin, toxins seeping through. You are inflicted with [Poison]!')

class Ursoc_Intimidate(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Intimidate'
        self.desc = 'Inflicts Intimidated, causing [-30%] attack, [-30%] defense and [-1] speed for 3 turns. Cooldown: 6 turns'

        self.effect_name = 'Intimidated'
        self.duration = 3
        self.cooldown = 6
        self.tags = ['effect', 'active']

        self.atk_mod = 0.7
        self.def_mod = 0.7
        self.spd_add = -1

    def use(self, user, target):
        self.turns_till_use = self.cooldown
        target.statuses[self] = self.duration

    def message(self):
        print('Ursoc unleashes a deafening roar, sending shivers down your spine. You have been [Intimidated]!')

class Minor_Frost(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Minor Frost'
        self.desc = 'Inflicts a Frostbite effect, causing health loss (10) and [-1] speed for 3 turns. Cooldown: 5 Turns.'

        self.effect_name = 'Frostbite'
        self.mp_cost = 1
        self.duration = 3
        self.cooldown = 5
        self.tags = ['active', 'effect']

        self.dot = 10
        self.spd_add = -1

    def use(self, user, target):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'{target.name} has been inflicted with [{self.effect_name}]!')

class Minor_Flame(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Minor Flame'
        self.desc = 'Inflicts a Burning effect, causing health loss (10) and [-10%] defense for 3 turns. Cooldown: 5 Turns.'

        self.effect_name = 'Minor Burn'
        self.mp_cost = 1
        self.duration = 3
        self.cooldown = 5
        self.tags = ['active', 'effect']

        self.dot = 10
        self.def_mod = 0.9

    def use(self, user, target):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'{target.name} has been inflicted with [{self.effect_name}]!')

class Frost_Shot(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Frost Shot'
        self.desc = 'Inflicts a Frostbite effect, causing health loss (15) and [-1.5] speed for 3 turns. Cooldown: 6 Turns.'

        self.effect_name = 'Frostbite'
        self.mp_cost = 2
        self.duration = 3
        self.cooldown = 6
        self.tags = ['active', 'effect']

        self.dot = 15
        self.spd_add = -1.5

    def use(self, user, target):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'{target.name} has been inflicted with [{self.effect_name}]!')

class Fire_Ball_Bleed(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Fire Ball Bleed'
        self.desc = 'Inflicts a Burning and Bleed effect, causing health loss (20) and [-30%] defense for 3 turns. Cooldown: 7 Turns.'

        self.effect_name = 'Burn n\' Bleed'
        self.mp_cost = 3
        self.duration = 3
        self.cooldown = 7
        self.tags = ['active', 'effect']

        self.dot = 20
        self.def_mod = 0.7

    def use(self, user, target):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'{target.name} has been inflicted with [{self.effect_name}]!')

class Overheat(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Overheat'
        self.desc = 'The blade heats you up, sending your body into overdrive. Gain [+75%] attack, at the cost of health loss (20) for 3 turns. Cooldown: 5 turns'

        self.effect_name = 'Overdrive'
        self.mp_cost = 4
        self.duration = 3
        self.cooldown = 5
        self.tags = ['active', 'effect', 'to_self']

        self.dot = 20
        self.atk_mod = 1.75

    def use(self, user, target):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        user.statuses[self] = self.duration
        print(f'Overheat used! You are now in [Overdrive]!')

class Luster_Purge(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Luster Purge'
        self.desc = 'The Hero Sword unleashes a Holy Beam, dealing significant True damage to its target. Cooldown: 6 turns'

        self.mp_cost = 3
        self.cooldown = 6
        self.tags = ['active', 'damage']

    def use(self, user, target):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown

        damage = random.randint(70, 100)
        target.hp -= damage
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'Luster Purge deals {damage} True damage to {target.name}! {target.name} has {target.hp} HP remaining!')

class Soul_King(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Soul King'
        self.desc = 'A unique trait possessed only by Glacierbrand. It is capable of storing souls of those killed by this weapon, each increasing its damage by 5. It is also capable of releasing the souls in the form of raw energy, expending all its soul reserves and the user\'s mana at once for 10 damage per soul / mana. Cooldown: Once per fight.'

        self.mp_cost = 0
        self.cooldown = 1000
        self.tags = ['active', 'damage']

    def use(self, user, target):
        souls = user.inventory.is_holding.souls
        mana = user.mp
        damage = (mana + souls) * 20
        target.take_damage(damage)
        user.mp = 0
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'Glacierbrand expends all of its souls and its users power, dealing {damage * (100 - target.defense) / 100} damage! {target.name} has {target.hp} remaining!')

class Wrath_Of_The_Great_Dragon(Ability):
    
    def __init__(self):
        super().__init__()

        self.desc = 'The Horn cycles between 3 abilities every time it is used.\n1. Dragon fire, inflicting [-50%] defense, health loss (20) for 4 turns.\n2. Dragon ice, inflicting [-50%] attack, [-3] speed for 4 turns.\n3. Dragon transformation, giving [+40%] attack and defense, [+3] speed, and health regen (15) for 4 turns.\nCooldown: 9 turns'

        self.mp_cost = 5
        self.duration = 4
        self.cooldown = 7

        self.mode = -2

    @property
    def name(self):
        if self.mode % 3 == 0:
            return 'Wrath Of The Great Dragon [Fire]'
        elif self.mode % 3 == 1:
            return 'Wrath Of The Great Dragon [Ice]'
        elif self.mode % 3 == 2:
            return 'Wrath Of The Great Dragon [Transformation]'
    @property
    def atk_mod(self):
        if self.mode % 3 == 1:
            return 0.5
        elif self.mode % 3 == 2:
            return 1.4
        return None
    @property
    def def_mod(self):
        if self.mode % 3 == 0:
            return 0.5
        elif self.mode % 3 == 2:
            return 1.4
        return None
    @property
    def dot(self):
        if self.mode % 3 == 0:
            return 20
        return None
    @property
    def spd_add(self):
        if self.mode % 3 == 1:
            return -3
        elif self.mode % 3 == 2:
            return 3
    @property
    def hot(self):
        if self.mode % 3 == 2:
            return 15
    @property
    def tags(self):
        if self.mode % 3 < 2:
            return ['active', 'effect']
        elif self.mode % 3 == 2:
            return ['active', 'effect', 'to_self']
    @property
    def effect_name(self):
        if self.mode % 3 == 0:
            return 'Draconic Burning'
        elif self.mode % 3 == 1:
            return 'Draconic Frostbite'
        elif self.mode % 3 == 2:
            return 'Dragonkin'
    
    def use(self, user, target = None):
        self.mode += 1
        print(f'{self.name} has been used!')
        time.sleep(2)
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        if self.mode % 3 < 2:
            target.statuses[self] = self.duration
            print(f'{target.name} has been inflicted with [{self.effect_name}]!')
        elif self.mode % 3 == 2:
            user.statuses[self] = self.duration
            print(f'You have been imbued with [Dragonkin]!')

class Greater_Restoration(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Greater Restoration'
        self.desc = 'The armor appears to be imbued with Holy Power. Its magical powers grant health regen (10) for 3 turns. Cooldown: 6 turns'

        self.effect_name = 'Greater Restoration'
        self.mp_cost = 2
        self.duration = 3
        self.cooldown = 6
        self.tags = ['active', 'effect', 'to_self']

        self.hot = 10

    def use(self, user, target = None):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        user.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'You have been imbued with [Greater Restoration]!')

class Siphon(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Siphon'
        self.desc = 'The Lich Husk grants a lifesteal buff, allowing you to absorb 50% of dealt damage as hp, for the next 3 hits. Cooldown: 10 turns'

        self.effect_name = 'Lifesteal'
        self.mp_cost = 2
        self.cooldown = 6
        self.hits = 3
        self.hits_left = 0
        self.tags = ['active', 'to_self', 'on_hit']

        self.hot = 10

    def use(self, user):
        user.mp -= self.mp_cost
        self.turns_till_use = self.cooldown
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'You have been imbued with [Lifesteal]!')
    
    def on_hit_use(self, user, target):
        user.hp += user.dealt_damage * 0.5
        print(f'You siphon {user.inventory.is_holding.damage * 0.5} HP from {target.name}!')

class Vengeance_Fire(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Vengeance [Fire]'
        self.desc = 'The carapace strikes back at the attacker, dealing 25 True damage and inflicting Burning, giving [-30%] defense and health loss (10) for 2 turns.'

        self.effect_name = 'Burning'
        self.mp_cost = 1
        self.duration = 2
        self.tags = ['effect', 'on_struck', 'damage']

        self.dot = 10
        self.def_mod = 0.7

    def use(self, user, target):
        user.mp -= self.mp_cost
        target.hp -= 25
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'The Draconic Carapace deals 25 True damage to {target.name}!')

class Vengeance_Ice(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Vengeance [Ice]'
        self.desc = 'The carapace strikes back at the attacker, dealing 30 True damage and inflicting Frostbite, giving [-2] speed and health loss (10) for 2 turns.'

        self.effect_name = 'Frostbite'
        self.mp_cost = 1
        self.duration = 2
        self.tags = ['effect', 'on_struck', 'damage']

        self.dot = 10
        self.spd_add = -2

    def use(self, user, target):
        user.mp -= self.mp_cost
        target.hp -= 30
        target.statuses[self] = self.duration
        print(f'{self.name} has been used!')
        time.sleep(2)
        print(f'The Draconic Carapace deals 30 True damage to {target.name}!')

class Strength(Ability):

    def __init__(self):
        super().__init__()

        self.effect_name = 'Strength'
        self.duration = 5
        self.tags = ['effect', 'to_self']

        self.atk_mod = 1.25
    
    def use(self, user):
        user.statuses[self] = self.duration

class Regeneration(Ability):

    def __init__(self):
        super().__init__()

        self.effect_name = 'Regeneration'
        self.duration = 3
        self.tags = ['effect', 'to_self']

        self.hot = 20
    
    def use(self, user):
        user.statuses[self] = self.duration

class Wraith_Frostbite(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Haunt'
        self.desc = 'The wraith shrouds you in a mist of ice shards, giving you a frostbite effect, giving you [-20%] defense and [-1] speed for 2 turns. Cooldown: 5 turns'

        self.effect_name = 'Frostbite'
        self.duration = 2
        self.cooldown = 5
        self.tags = ['effect', 'active']

        self.def_mod = 0.8
        self.spd_add = -1
    
    def use(self, user, target):
        target.statuses[self] = self.duration
        self.turns_till_use = self.cooldown
        print(f'{user.name} uses {self.name}!')
        time.sleep(2)
        print(f'You have been inflicted with {self.effect_name}!')
    
    def message(self):
        pass


class Lich_King(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Undead Sorcery'
        self.desc = 'Azaroth possesses three abilities:\n1. Consumes life to give [+30%] attack for 3 turns.\n2. Focuses power on regeneration, giving [+20%] defense and health gain (30) for 3 turns.\n3. A one-time use ability casted upon reaching 20% hp, encasing himself in a cage of ice. For 3 turns, he has INFINITE defense, while gaining 30 health every turn. Cooldown: 6 turns'

        self.duration = 3
        self.cooldown = 4
        self.tags = ['effect', 'to_self', 'active']

        self.used_ice_cage = False
        self.mode = 0

    @property
    def atk_mod(self):
        if self.mode == 1:
            return 1.3
        return None
    @property
    def def_mod(self):
        if self.mode == 2:
            return 1.2
        return None
    @property
    def hot(self):
        if self.mode > 1:
            return 30
        return None
    @property
    def def_add(self):
        if self.mode == 3:
            return 1000
        return None
    @property
    def effect_name(self):
        if self.mode == 1:
            return 'Undead Arts: Extraction'
        elif self.mode == 2:
            return 'Undead Arts: Assembly'
        elif self.mode == 3:
            return 'Undead Arts: Calcify'

    def use(self, user, target):
        '''Ability decision'''
        if user.hp < 100 and not self.used_ice_cage:
            self.mode = 3
        elif user.hp > 250:
            self.mode = 1
        elif user.hp < 250:
            self.mode = 2
        
        if self.mode == 1:
            user.hp -= 30
            print('[UNDEAD ARTS: EXTRACTION] Azaroth sacrifices 30hp to strengthen his attacks!')
            user.statuses[self] = self.duration
        elif self.mode == 2:
            print('[UNDEAD ARTS: ASSEMBLY] Azaroth is focusing on regeneration...')
            user.statuses[self] = self.duration
        elif self.mode == 3:
            print('[UNDEAD ARTS: CALCIFY] Azaroth encages himself in an ice cage!')
            user.statuses[self] = self.duration
            self.used_ice_cage = True
        self.turns_till_use = self.cooldown
    
    def message(self):
        pass

class Vael_Grath(Ability):

    def __init__(self):
        super().__init__()

        self.name = 'Vael\'Grath\'s Wrath'
        self.desc = 'Dragons are capable of shaping the environment on command. Vael\'Grath in particular is capable of controlling fire and ice elements, resulting in the harsh environment on this floor. Every 6 turns, he changes the environment to alternate between Volcanic and Frigid.\nVolcanic: [-50%] defense, health loss (20) for 5 turns.\nFrigid: [-50%] attack, [-3] speed for 5 turns.\nEvery time he uses this ability, he gains a permanent [+10%] attack, [+10%] defense, and [+0.5] speed.\n[Warning] After 24 turns, a calamity befalls you.'

        self.duration = 5
        self.cooldown = 6
        self.tags = ['effect', 'active']

        self.calamity_countdown = 24
        self.calamity_used = False
        self.fire_or_ice = False
    
    def use(self, user, target):
        if not self.calamity_countdown and not self.calamity_used:
            print('The end of the world has come. All shall return to ash.')
            time.sleep(5)
            if isinstance(target.ability, Luster_Purge):
                print('Your Hero Sword glows with holy light, enveloping you with a barrier, nullifying the blast.')
                time.sleep(2)
                print('As the smoke clears, the blade cracks, breaking in two.')
                target.inventory.remove_item(target.inventory.is_holding)
                target.inventory.add_item(target.inventory.is_holding.breaks_into)
                target.inventory.is_holding = None
            else:
                target.take_damage(200)
                print(f'You are hit with the Calamity. You are left with {target.hp} HP.')
            self.calamity_used = True
        elif self.fire_or_ice:
            self.effect_name = 'Draconic Burn'
            self.def_mod = 0.5
            self.dot = 20
            self.atk_mod = None
            self.spd_add = None
            target.statuses[self] = self.duration
            print(f'Vael\'Grath uses {self.name}! You have been inflicted with {self.effect_name}!')
            time.sleep(2)
        elif not self.fire_or_ice:
            self.effect_name = 'Draconic Frostbite'
            self.def_mod = None
            self.dot = None
            self.atk_mod = 0.5
            self.spd_add = -3
            target.statuses[self] = self.duration
            print(f'Vael\'Grath uses {self.name}! You have been inflicted with {self.effect_name}!')
            time.sleep(2)
        
        self.fire_or_ice = not self.fire_or_ice
        self.turns_till_use = self.cooldown

        #self buffs
        user.atk *= 1.1
        user.defense *= 1.1
        user.speed += 0.5
        print('Vael\'Grath grows stronger...')
        time.sleep(2)

    def message(self):
        pass