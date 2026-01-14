import json
import os
import pickle
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'rb') as f:
                return pickle.load(f)
        else:
            return {
                'players': {},
                'characters': {},
                'items': {},
                'quests': {},
                'world_state': {
                    'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }

    def save_data(self):
        with open(self.db_path, 'wb') as f:
            pickle.dump(self.data, f)

    def get_player_data(self, player_id):
        return self.data['players'].get(player_id, {})

    def save_player_data(self, player_id, data):
        self.data['players'][player_id] = data
        self.save_data()

    def get_character_data(self, character_id):
        return self.data['characters'].get(character_id, {})

    def save_character_data(self, character_id, data):
        self.data['characters'][character_id] = data
        self.save_data()

    def get_item_data(self, item_id):
        return self.data['items'].get(item_id, {})

    def save_item_data(self, item_id, data):
        self.data['items'][item_id] = data
        self.save_data()

    def get_quest_data(self, quest_id):
        return self.data['quests'].get(quest_id, {})

    def save_quest_data(self, quest_id, data):
        self.data['quests'][quest_id] = data
        self.save_data()

    def get_world_state(self):
        return self.data['world_state']

    def update_world_state(self, data):
        self.data['world_state'] = data
        self.save_data()


class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.level = 1
        self.experience = 0
        self.gold = 0

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'gold': self.gold
        }


class Character:
    def __init__(self, character_id, name):
        self.character_id = character_id
        self.name = name
        self.level = 1
        self.experience = 0
        self.health = 100
        self.strength = 10

    def to_dict(self):
        return {
            'character_id': self.character_id,
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'health': self.health,
            'strength': self.strength
        }


class Item:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name
        self.type = ''
        self.rarity = ''
        self.stats = {}

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'type': self.type,
            'rarity': self.rarity,
            'stats': self.stats
        }


class Quest:
    def __init__(self, quest_id, name):
        self.quest_id = quest_id
        self.name = name
        self.status = 'available'
        self.rewards = {}

    def to_dict(self):
        return {
            'quest_id': self.quest_id,
            'name': self.name,
            'status': self.status,
            'rewards': self.rewards
        }


# Example usage:
db_manager = DatabaseManager('jiānghéng.db')

player = Player(1, 'Li Ming')
db_manager.save_player_data(1, player.to_dict())

character = Character(1, 'Wu Song')
db_manager.save_character_data(1, character.to_dict())

item = Item(1, 'Dragon Sword')
item.type = 'sword'
item.rarity = 'legendary'
item.stats = {'attack': 100, 'defense': 50}
db_manager.save_item_data(1, item.to_dict())

quest = Quest(1, 'The Lost City')
quest.status = 'completed'
quest.rewards = {'gold': 1000, 'experience': 500}
db_manager.save_quest_data(1, quest.to_dict())

print(db_manager.get_player_data(1))
print(db_manager.get_character_data(1))
print(db_manager.get_item_data(1))
print(db_manager.get_quest_data(1))