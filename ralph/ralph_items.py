from dataclasses import dataclass
from typing import Optional
from ralph_abilities import *
import time
if __name__ == '__main__':
    raise NameError('This is the items implementation for ralph.py -- It is not meant to be run by itself')

@dataclass
class Item:
    item_name: str
    desc: str
    rarity: str
    value: int

@dataclass
class Weapon(Item):
    damage: int
    speed_bonus: int = 0
    ability: Optional[Ability] = None

    def view(self):
        print(f'--------------------\n[{self.rarity.upper()}] {self.item_name}\n--------------------\n{self.desc}')
        print(f'Damage: {self.damage}\nSpeed Bonus: {self.speed_bonus}\nValue: {self.value}')
        if self.ability:
            print(f'[ABILITY] [{'PASSIVE' if not self.ability.is_active else 'ACTIVE'}] {self.ability.name}: {self.ability.desc}')
            print(f'Mana Cost: {self.ability.mp_cost}')
        time.sleep(1)

@dataclass
class Lich_Weapon(Weapon):
    base_damage: int = 0
    souls = 0

    @property
    def damage(self):
        return self.base_damage + self.souls * 5
    @damage.setter
    def damage(self, value):
        pass

    def view(self):
        print(f'--------------------\n[{self.rarity.upper()}] {self.item_name}\n--------------------\n{self.desc}')
        print(f'Damage: {self.damage}\nSpeed Bonus: {self.speed_bonus}\nValue: {self.value}\nSOUL: {self.souls}')
        if self.ability:
            print(f'[ABILITY] [{'PASSIVE' if not self.ability.is_active else 'ACTIVE'}] {self.ability.name}: {self.ability.desc}')
            print(f'Mana Cost: {self.ability.mp_cost}')
        time.sleep(1)

@dataclass
class Hero_Sword(Weapon):
    breaks_into: Weapon = None

@dataclass
class Consumable(Item):
    heal_value: int = None
    mp_value: int = None
    effect: Optional[Ability] = None

    def view(self):
        print(f'--------------------\n[{self.rarity.upper()}] {self.item_name}\n--------------------\n{self.desc}')
        if self.heal_value:
            print(f'Heal: {self.heal_value}')
        elif self.mp_value:
            print(f'MP: {self.mp_value}')
        time.sleep(1)
        
@dataclass
class Armor(Item):
    def_value: int 
    speed_bonus: int = 0
    hp_boost: int = 0
    ability: Optional[Ability] = None

    def view(self):
        print(f'--------------------\n{self.item_name}\n--------------------\n{self.desc}')
        print(f'Defense: {self.def_value}\nSpeed Bonus: {self.speed_bonus}\nHP Bonus: {self.hp_boost}Value: {self.value}')
        if self.ability:
            print(f'[ABILITY] [{'PASSIVE' if not self.ability.is_active else 'ACTIVE'}] {self.ability.name}: {self.ability.desc}')
            print(f'Mana Cost: {self.ability.mp_cost}')
        time.sleep(1)