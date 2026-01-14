import numpy as np
from typing import Dict, List
from nexus_one.components import Character, Item, Enemy

class CombatMechanics:
    def __init__(self, character: Character, enemy: Enemy):
        self.character = character
        self.enemy = enemy

    def calculate_damage(self) -> float:
        """Calculates the damage dealt to the enemy"""
        character_attack = self.character.attack * (1 + self.character.attack_bonus)
        enemy_defense = self.enemy.defense * (1 + self.enemy.defense_bonus)
        damage = max(0, character_attack - enemy_defense)
        return damage

    def calculate_enemy_damage(self) -> float:
        """Calculates the damage dealt to the character by the enemy"""
        enemy_attack = self.enemy.attack * (1 + self.enemy.attack_bonus)
        character_defense = self.character.defense * (1 + self.character.defense_bonus)
        damage = max(0, enemy_attack - character_defense)
        return damage

    def battle(self) -> bool:
        """Simulates a battle between the character and the enemy"""
        while self.character.hp > 0 and self.enemy.hp > 0:
            damage = self.calculate_damage()
            self.enemy.hp -= damage
            if self.enemy.hp <= 0:
                break
            enemy_damage = self.calculate_enemy_damage()
            self.character.hp -= enemy_damage
        return self.character.hp > 0


class HarvestingMechanics:
    def __init__(self, character: Character, item: Item):
        self.character = character
        self.item = item

    def calculate_harvest_yield(self) -> float:
        """Calculates the yield of the harvested item"""
        character_harvest_skill = self.character.harvest_skill
        item_harvest_difficulty = self.item.harvest_difficulty
        yield_coefficient = 1 + (character_harvest_skill - item_harvest_difficulty) / 100
        return max(0, yield_coefficient)

    def harvest(self) -> Dict:
        """Simulates the harvesting of an item"""
        yield_coefficient = self.calculate_harvest_yield()
        quantity = int(self.item.quantity * yield_coefficient)
        return {
            "item": self.item.name,
            "quantity": quantity
        }


class JiānghéngGame:
    def __init__(self):
        self.characters = []
        self.enemies = []
        self.items = []

    def add_character(self, character: Character):
        self.characters.append(character)

    def add_enemy(self, enemy: Enemy):
        self.enemies.append(enemy)

    def add_item(self, item: Item):
        self.items.append(item)

    def combat(self, character: Character, enemy: Enemy):
        combat_mechanics = CombatMechanics(character, enemy)
        return combat_mechanics.battle()

    def harvest(self, character: Character, item: Item):
        harvesting_mechanics = HarvestingMechanics(character, item)
        return harvesting_mechanics.harvest()


# Example usage:
if __name__ == "__main__":
    game = JiānghéngGame()

    character = Character("Player", 100, 10, 5, 5)
    enemy = Enemy("Enemy", 50, 5, 2, 2)
    item = Item("Herb", 10, 5)

    game.add_character(character)
    game.add_enemy(enemy)
    game.add_item(item)

    print("Combat result:", game.combat(character, enemy))
    print("Harvest result:", game.harvest(character, item))