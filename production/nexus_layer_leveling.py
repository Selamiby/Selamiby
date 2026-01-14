import json
from typing import Dict, List

class TalentTree:
    def __init__(self, talent_tree_id: str, talents: Dict[str, Dict]):
        """
        Initialize a TalentTree object.

        Args:
        - talent_tree_id (str): Unique identifier for the talent tree.
        - talents (Dict[str, Dict]): Dictionary of talents, where each key is a talent ID and each value is a dictionary containing talent information.
        """
        self.talent_tree_id = talent_tree_id
        self.talents = talents

class LevelingSystem:
    def __init__(self, experience_curve: List[float], level_cap: int):
        """
        Initialize a LevelingSystem object.

        Args:
        - experience_curve (List[float]): List of experience points required to reach each level.
        - level_cap (int): Maximum level a player can reach.
        """
        self.experience_curve = experience_curve
        self.level_cap = level_cap

    def calculate_experience_needed(self, current_level: int, next_level: int) -> float:
        """
        Calculate the experience points needed to reach a certain level.

        Args:
        - current_level (int): Current level of the player.
        - next_level (int): Next level the player wants to reach.

        Returns:
        - float: Experience points needed to reach the next level.
        """
        if next_level > self.level_cap:
            return float('inf')
        return self.experience_curve[next_level - 1] - self.experience_curve[current_level - 1]

class Player:
    def __init__(self, player_id: str, level: int, experience: float, talent_tree: TalentTree):
        """
        Initialize a Player object.

        Args:
        - player_id (str): Unique identifier for the player.
        - level (int): Current level of the player.
        - experience (float): Current experience points of the player.
        - talent_tree (TalentTree): Talent tree associated with the player.
        """
        self.player_id = player_id
        self.level = level
        self.experience = experience
        self.talent_tree = talent_tree

    def level_up(self, leveling_system: LevelingSystem):
        """
        Level up the player.

        Args:
        - leveling_system (LevelingSystem): Leveling system to use for leveling up the player.
        """
        if self.level < leveling_system.level_cap:
            experience_needed = leveling_system.calculate_experience_needed(self.level, self.level + 1)
            if self.experience >= experience_needed:
                self.level += 1
                self.experience -= experience_needed
                print(f"Player {self.player_id} has leveled up to level {self.level}!")

    def spend_talent_points(self, talent_id: str, talent_points: int):
        """
        Spend talent points on a talent.

        Args:
        - talent_id (str): ID of the talent to spend points on.
        - talent_points (int): Number of talent points to spend.
        """
        if talent_id in self.talent_tree.talents:
            talent = self.talent_tree.talents[talent_id]
            if talent['points'] < talent['max_points']:
                talent['points'] += talent_points
                print(f"Player {self.player_id} has spent {talent_points} talent points on {talent_id}!")


# Example usage:
talent_tree = TalentTree(
    "default_talent_tree",
    {
        "talent1": {"points": 0, "max_points": 5},
        "talent2": {"points": 0, "max_points": 3},
        "talent3": {"points": 0, "max_points": 2},
    }
)

leveling_system = LevelingSystem(
    [0, 100, 200, 400, 800, 1600],
    10
)

player = Player(
    "player1",
    1,
    0,
    talent_tree
)

player.experience = 150
player.level_up(leveling_system)
player.spend_talent_points("talent1", 2)