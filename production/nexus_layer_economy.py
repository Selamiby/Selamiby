import datetime
import json
from typing import Dict


class Economy:
    def __init__(self):
        self.market = {}
        self.prestige = {}
        self.player_data = {}

    def initialize_market(self):
        """Initialize market with default items and prices."""
        self.market = {
            "item1": {"price": 100, "quantity": 100},
            "item2": {"price": 200, "quantity": 50},
            "item3": {"price": 300, "quantity": 20},
        }

    def initialize_prestige(self):
        """Initialize prestige system with default levels and rewards."""
        self.prestige = {
            "level1": {"required_xp": 1000, "rewards": {"gold": 100, "items": ["item1"]}},
            "level2": {"required_xp": 5000, "rewards": {"gold": 500, "items": ["item2"]}},
            "level3": {"required_xp": 10000, "rewards": {"gold": 1000, "items": ["item3"]}},
        }

    def sync_market(self):
        """Sync market prices and quantities with the server."""
        # For demonstration purposes, simulate a server sync
        self.market = {
            "item1": {"price": 120, "quantity": 80},
            "item2": {"price": 250, "quantity": 30},
            "item3": {"price": 350, "quantity": 10},
        }

    def update_prestige(self, player_id: str, xp: int):
        """Update player prestige level based on experience points."""
        player_data = self.get_player_data(player_id)
        current_level = player_data.get("prestige_level", "level1")
        required_xp = self.prestige[current_level]["required_xp"]

        if xp >= required_xp:
            next_level = self.get_next_prestige_level(current_level)
            player_data["prestige_level"] = next_level
            self.apply_prestige_rewards(player_id, next_level)

    def get_next_prestige_level(self, current_level: str) -> str:
        """Get the next prestige level based on the current level."""
        levels = list(self.prestige.keys())
        current_index = levels.index(current_level)
        next_index = current_index + 1

        if next_index >= len(levels):
            return current_level
        return levels[next_index]

    def apply_prestige_rewards(self, player_id: str, level: str):
        """Apply prestige rewards to the player."""
        rewards = self.prestige[level]["rewards"]
        player_data = self.get_player_data(player_id)

        player_data["gold"] = player_data.get("gold", 0) + rewards["gold"]
        player_data["items"] = player_data.get("items", []) + rewards["items"]

    def get_player_data(self, player_id: str) -> Dict:
        """Get player data from the player_data dictionary."""
        if player_id not in self.player_data:
            self.player_data[player_id] = {}
        return self.player_data[player_id]

class NexusOneEconomy:
    def __init__(self, config=None):
        self.config = config
        self.economy = Economy()
        self.economy.initialize_market()
        self.economy.initialize_prestige()

    def get_prestige_level(self, player_level):
        # Basit seviye karşılığı
        if player_level < 10: return 1
        return player_level // 10

# Example usage
if __name__ == "__main__":
    game = NexusOneGame()
    game.start_game()

    game.economy.update_prestige("player1", 1500)
    print(game.economy.get_player_data("player1"))