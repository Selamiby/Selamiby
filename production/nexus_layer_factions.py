# factions_and_story_lore.py

import json
from enum import Enum

class FactionType(Enum):
    """Faction types in the game."""
    PLAYER = 1
    ENEMY = 2
    NEUTRAL = 3

class Faction:
    """Base faction class."""
    def __init__(self, id, name, faction_type, description):
        self.id = id
        self.name = name
        self.faction_type = faction_type
        self.description = description
        self.members = []
        self.allies = []
        self.enemies = []

class StoryLore:
    """Base story lore class."""
    def __init__(self, id, name, description, faction):
        self.id = id
        self.name = name
        self.description = description
        self.faction = faction
        self.related_quests = []
        self.related_characters = []

class JiānghéngFactionSystem:
    """Jiānghéng faction system."""
    def __init__(self):
        self.factions = []
        self.story_lore = []

    def create_faction(self, id, name, faction_type, description):
        faction = Faction(id, name, faction_type, description)
        self.factions.append(faction)
        return faction

    def create_story_lore(self, id, name, description, faction):
        story_lore = StoryLore(id, name, description, faction)
        self.story_lore.append(story_lore)
        return story_lore

    def add_member_to_faction(self, faction, member):
        faction.members.append(member)

    def add_ally_to_faction(self, faction, ally):
        faction.allies.append(ally)

    def add_enemy_to_faction(self, faction, enemy):
        faction.enemies.append(enemy)

    def get_faction_by_id(self, id):
        for faction in self.factions:
            if faction.id == id:
                return faction
        return None

    def get_story_lore_by_id(self, id):
        for story_lore in self.story_lore:
            if story_lore.id == id:
                return story_lore
        return None

# Initialize the faction system
faction_system = JiānghéngFactionSystem()

# Create factions
player_faction = faction_system.create_faction(1, "Player", FactionType.PLAYER, "The player faction.")
enemy_faction = faction_system.create_faction(2, "Enemy", FactionType.ENEMY, "The enemy faction.")

# Create story lore
story_lore = faction_system.create_story_lore(1, "Introduction", "The introduction to the game.", player_faction)

# Add members to factions
faction_system.add_member_to_faction(player_faction, "Player")
faction_system.add_member_to_faction(enemy_faction, "Enemy")

# Add allies and enemies to factions
faction_system.add_ally_to_faction(player_faction, enemy_faction)
faction_system.add_enemy_to_faction(player_faction, enemy_faction)

# Get faction by id
faction = faction_system.get_faction_by_id(1)
print(faction.name)

# Get story lore by id
story_lore = faction_system.get_story_lore_by_id(1)
print(story_lore.name)

# Load faction data from NEXUS-ONE codebase
import json
with open('factions.json') as f:
    faction_data = json.load(f)

# Update faction system with data from NEXUS-ONE codebase
for faction in faction_data:
    faction_obj = faction_system.get_faction_by_id(faction['id'])
    if faction_obj:
        faction_obj.name = faction['name']
        faction_obj.description = faction['description']

# Save faction data to NEXUS-ONE codebase
faction_data = []
for faction in faction_system.factions:
    faction_data.append({
        'id': faction.id,
        'name': faction.name,
        'description': faction.description
    })
with open('factions.json', 'w') as f:
    json.dump(faction_data, f)

# Load story lore data from NEXUS-ONE codebase
with open('story_lore.json') as f:
    story_lore_data = json.load(f)

# Update story lore system with data from NEXUS-ONE codebase
for story_lore in story_lore_data:
    story_lore_obj = faction_system.get_story_lore_by_id(story_lore['id'])
    if story_lore_obj:
        story_lore_obj.name = story_lore['name']
        story_lore_obj.description = story_lore['description']

# Save story lore data to NEXUS-ONE codebase
story_lore_data = []
for story_lore in faction_system.story_lore:
    story_lore_data.append({
        'id': story_lore.id,
        'name': story_lore.name,
        'description': story_lore.description
    })
with open('story_lore.json', 'w') as f:
    json.dump(story_lore_data, f)