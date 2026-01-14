import numpy as np
import pandas as pd
from typing import Dict, List
from nexus_one.models import Player, GameScore

# Define global rankings class
class GlobalRankings:
    def __init__(self):
        self.rankings = {}

    def update_rankings(self, player_id: str, score: int):
        if player_id not in self.rankings:
            self.rankings[player_id] = score
        else:
            self.rankings[player_id] = max(self.rankings[player_id], score)

    def get_rankings(self, num_players: int = 10) -> List[Dict]:
        sorted_rankings = sorted(self.rankings.items(), key=lambda x: x[1], reverse=True)
        return [{"player_id": player[0], "score": player[1]} for player in sorted_rankings[:num_players]]

    def get_player_rank(self, player_id: str) -> int:
        if player_id not in self.rankings:
            return -1
        sorted_rankings = sorted(self.rankings.items(), key=lambda x: x[1], reverse=True)
        return next((index + 1 for index, player in enumerate(sorted_rankings) if player[0] == player_id), -1)


# Integrate with existing NEXUS-ONE codebase
def update_global_rankings(player: Player, game_score: GameScore):
    global_rankings = GlobalRankings()
    global_rankings.update_rankings(player.id, game_score.score)


def get_global_rankings(num_players: int = 10) -> List[Dict]:
    global_rankings = GlobalRankings()
    return global_rankings.get_rankings(num_players)


def get_player_global_rank(player_id: str) -> int:
    global_rankings = GlobalRankings()
    return global_rankings.get_player_rank(player_id)