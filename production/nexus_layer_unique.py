import random
from typing import Dict, List


class Item:
    def __init__(self, id: int, name: str, item_type: str, rarity: str, power: int):
        self.id = id
        self.name = name
        self.item_type = item_type # Weapon, Armor, Consumable
        self.rarity = rarity # Common, Rare, Epic, Legendary
        self.power = power

    def __repr__(self):
        return f"[{self.rarity}] {self.name} (+{self.power})"

class Inventory:
    def __init__(self, capacity: int = 20):
        self.items: List[Item] = []
        self.capacity = capacity

    def add_item(self, item: Item) -> bool:
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item_id: int):
        self.items = [item for item in self.items if item.id != item_id]

class LootSystem:
    def __init__(self):
        self.possible_items = [
            {"name": "Dragon Slayer", "type": "Weapon", "rarity": "Legendary", "power": 150},
            {"name": "Shadow Cloak", "type": "Armor", "rarity": "Epic", "power": 80},
            {"name": "Iron Sword", "type": "Weapon", "rarity": "Common", "power": 10},
            {"name": "Leather Armor", "type": "Armor", "rarity": "Common", "power": 15},
            {"name": "Health Potion", "type": "Consumable", "rarity": "Common", "power": 50},
            {"name": "Jade Staff", "type": "Weapon", "rarity": "Rare", "power": 45}
        ]

    def generate_drop(self) -> Item:
        raw = random.choice(self.possible_items)
        return Item(
            id=random.randint(1000, 9999),
            name=raw["name"],
            item_type=raw["type"],
            rarity=raw["rarity"],
            power=raw["power"]
        )

# Global Instance for the Game
loot_master = LootSystem()
