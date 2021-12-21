"""
Chapitre 11.3
"""

import math
from inspect import *

import utils
from game import *


class Spell:
    UNARMED_POWER = 20

    def __init__(self, name: str, power: float, min_level: float, magic_cost: float):
        self.__name = name
        self.power = power
        self.min_level = min_level
        self.magic_cost = magic_cost

    @property
    def name(self):
        return self.__name

    @classmethod
    def make_unarmed(cls):
        return cls("Unarmed", cls.UNARMED_POWER, 1)


class Weapon:

    UNARMED_POWER = 20

    def __init__(self, weapon_name: str, power: int, min_level: int):
        self.__weapon_name = weapon_name  # ne peut etre changé
        self.power = power
        self.min_level = min_level

    @classmethod
    def make_unarmed(cls):
        return cls("Unarmed", cls.UNARMED_POWER, 1)

    @property  # pour accéder à attribut privé, comme dans def en haut
    def weapon_name(self):
        return self.__weapon_name


class Character:
    """
    Un personnage dans le jeu
    :param name: Le nom du personnage
    :param max_hp: HP maximum
    :param attack: Le niveau d'attaque du personnage
    :param defense: Le niveau de défense du personnage
    :param level: Le niveau d'expérience du personnage
    """

    def __init__(self, name, max_hp, attack, defense, level):
        self.__name = name
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.weapon = None
        self.hp = max_hp

    @property
    def name(self):
        return self.__name

    @property
    def weapon(self):
        return self.__weapon

    # TODO: Affecter ce qui est passé comme valeur. Si la valeur est None, je lui met une arme vide (le Unarmed)
    @weapon.setter
    def weapon(self, val):
        if val is None:
            val = Weapon.make_unarmed()
        if val.min_level > self.level:
            raise ValueError(Weapon)
        self.__weapon = val

    # TODO: Définir getter/setter pour `hp`, qui doit être borné entre 0 et `max_hp`

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, val):
        self.__hp = utils.clamp(val, 0, self.max_hp)

    def compute_damage(self, other: "Magician"):
        level_factor = (2 * self.level) / 5 + 2
        weapon_factor = self.weapon.power
        atk_def_factor = self.attack / other.defense
        critical = random.random() <= 1 / 16
        modifier = (2 if critical else 1) * random.uniform(0.85, 1.0)
        damage = ((level_factor * weapon_factor * atk_def_factor) / 50 + 2) * modifier

        return int(round(damage)), critical


class Magician:
    def __init__(self, name, max_mp, magic_attack, max_hp, attack, defense, level):
        self.__name = name
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.weapon = None
        self.max_hp = max_hp
        self.hp = max_hp

        self.magic_attack = magic_attack
        self.using_magic = None
        self.spell = None
        self.max_mp = max_mp
        self.mp = max_mp


    @property
    def name(self):
        return self.__name

    @property
    def weapon(self):
        return self.__weapon

    @weapon.setter
    def weapon(self, weapon_val: "Weapon"):
        if weapon_val is None:
            weapon_val = Weapon.make_unarmed()
        if weapon_val.min_level > self.level:
            raise ValueError(Weapon)
        self.__weapon = weapon_val

    @property
    def spell(self):
        return self.__spell

    @spell.setter
    def spell(self, magic_spell: "Spell"):
        if magic_spell is None:
            magic_spell = Weapon.make_unarmed()
        if magic_spell.min_level > self.level:
            raise ValueError(Weapon)
        self.__spell = magic_spell


    # we act as if hp was private so we can modify it with hp.setter
    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, val_hp):
        self.__hp = utils.clamp(val_hp, 0, self.max_hp)  # on borne hp entre 0 et maxhp

    def compute_damage(self, defender: "Character"):
        if self.weapon != Weapon.make_unarmed():
            level = (2 / 5) * self.level + 2
            power_w = self.weapon.power  # CAREFUL, we call it self.weapon accordingly to innit
            a_d = self.attack / defender.defense
            rand_crit_list = random.choices([1, 2], weights=(93.75, 6.25), k=1)
            rand_crit_num = ''.join(str(e) for e in rand_crit_list)
            rand_num = random.uniform(0.85, 1)
            modifier = float(rand_crit_num) * float(rand_num)
            return ((level * power_w * a_d) / 50 + 2) * modifier


    def will_use_spell(self, defender: "Character"):
        if self.weapon == Weapon.make_unarmed():
            level = ((2 / 5) * (self.level + self.magic_attack)) + 2
            power_s = self.spell.power  # CAREFUL, we call it self.weapon accordingly to innit

            rand_crit_list = random.choices([1, 2], weights=(93.75, 6.25), k=1)
            rand_crit_num = ''.join(str(e) for e in rand_crit_list)
            rand_num = random.uniform(0.85, 1)
            modifier = float(rand_crit_num) * float(rand_num)
            return ((level * power_s) / 50 + 2) * modifier


def deal_damage(attaquant, defendeur):

    if attaquant.weapon != Weapon.make_unarmed():
        damage, critical = attaquant.compute_damage(defendeur)
        defendeur.hp -= damage
        if critical is False:
            print(f"{attaquant.__name} used {attaquant.weapon}\n  {defendeur.__name} took {damage} dmg")
        else:
            print('Critical hit!')
            print(f"{attaquant.__name} used {attaquant.weapon}\n  {defendeur.__name} took {damage} dmg")

    else:
        damage, critical = attaquant.will_use_spell(defendeur)
        defendeur.hp -= damage
        if critical is False:
            print(f"{attaquant.__name} used {attaquant.spell}\n  {defendeur.__name} took {damage} dmg")
        else:
            print('Critical hit!')
            print(f"{attaquant.__name} used {attaquant.spell}\n  {defendeur.__name} took {damage} dmg")



def run_battle(attaquant, defendeur):
    print(f'{attaquant.__name} starts a battle with {defendeur.name}\n')
    n_tour = 1
    while attaquant.hp > 0 and defendeur.hp > 0:
        if n_tour % 2 != 0:
            print(deal_damage(attaquant, defendeur))
        else:
            print(deal_damage(defendeur, attaquant))

    if attaquant.hp <= 0:
        print(f"{attaquant} is sleeping with the fishes.")
    else:
        print(f"{defendeur} is sleeping with the fishes.")

    print(f"The battle ended in 6 turns.")



if __name__ == "__main__":

    c1 = Character("Äpik", 500, 150, 70, 70)
    c2 = Magician("Damn! That magic dude", 450, 100, 50, 150, 50, 65)

    c1.weapon = Weapon("BFG", 100, 69)
    c2.spell = Spell("Big Chungus Power", 100, 35, 50)
    c2.weapon = Weapon("Slingshot", 80, 20)
    c2.using_magic = True

    turns = run_battle(c1, c2)
    print(f"The battle ended in {turns} turns.")
