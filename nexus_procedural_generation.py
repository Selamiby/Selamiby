#!/usr/bin/env python3
"""
NEXUS Procedural Generation Engine
- Terrain generation (Perlin noise)
- Loot tables + random drops
- Dynamic quest generation
"""
import json
import logging
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[logging.FileHandler(log_dir / "procedural_gen.log", encoding="utf-8")],
)
logger = logging.getLogger("procgen")


class PerlinNoise:
    """Simplified Perlin noise for terrain."""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.permutation = list(range(256))
        random.shuffle(self.permutation)
        self.permutation *= 2

    def fade(self, t: float) -> float:
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, a: float, b: float, t: float) -> float:
        return a + t * (b - a)

    def grad(self, hash_val: int, x: float, y: float) -> float:
        h = hash_val & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

    def noise(self, x: float, y: float) -> float:
        """2D Perlin noise."""
        xi = int(x) & 255
        yi = int(y) & 255
        xf = x - int(x)
        yf = y - int(y)

        u = self.fade(xf)
        v = self.fade(yf)

        aa = self.permutation[self.permutation[xi] + yi]
        ab = self.permutation[self.permutation[xi] + yi + 1]
        ba = self.permutation[self.permutation[xi + 1] + yi]
        bb = self.permutation[self.permutation[xi + 1] + yi + 1]

        x1 = self.lerp(self.grad(aa, xf, yf), self.grad(ba, xf - 1, yf), u)
        x2 = self.lerp(self.grad(ab, xf, yf - 1), self.grad(bb, xf - 1, yf - 1), u)

        return self.lerp(x1, x2, v)


class TerrainGenerator:
    """Generate heightmap terrain."""

    def __init__(self, seed: int = 42):
        self.noise = PerlinNoise(seed)

    def generate_heightmap(
        self, width: int, height: int, scale: float = 0.1
    ) -> List[List[float]]:
        """Generate 2D heightmap."""
        heightmap = []
        for y in range(height):
            row = []
            for x in range(width):
                val = self.noise.noise(x * scale, y * scale)
                val = (val + 1) / 2  # Normalize to 0-1
                row.append(val)
            heightmap.append(row)
        return heightmap


class LootTable:
    """Random loot drop system."""

    def __init__(self):
        self.tables = {
            "common": [
                {"item": "health_potion", "weight": 50},
                {"item": "coins", "weight": 40},
                {"item": "wood", "weight": 10},
            ],
            "rare": [
                {"item": "magic_sword", "weight": 5},
                {"item": "armor", "weight": 15},
                {"item": "gem", "weight": 30},
            ],
            "legendary": [
                {"item": "dragon_scale", "weight": 1},
                {"item": "phoenix_feather", "weight": 1},
                {"item": "mythic_weapon", "weight": 3},
            ],
        }

    def roll(self, rarity: str = "common") -> str:
        """Roll for loot."""
        table = self.tables.get(rarity, self.tables["common"])
        total_weight = sum(item["weight"] for item in table)
        roll = random.uniform(0, total_weight)

        current = 0
        for item in table:
            current += item["weight"]
            if roll <= current:
                return item["item"]

        return table[0]["item"]


class QuestGenerator:
    """Dynamic quest generation."""

    def __init__(self):
        self.templates = [
            {
                "type": "kill",
                "target": ["wolf", "bandit", "skeleton"],
                "count_range": (5, 20),
            },
            {
                "type": "collect",
                "item": ["herb", "ore", "artifact"],
                "count_range": (3, 10),
            },
            {
                "type": "escort",
                "npc": ["merchant", "child", "noble"],
                "distance_range": (100, 500),
            },
            {
                "type": "explore",
                "location": ["cave", "ruins", "forest"],
                "discovery": True,
            },
        ]

    def generate(self) -> Dict:
        """Generate random quest."""
        template = random.choice(self.templates)
        quest = {"id": f"quest-{random.randint(1000, 9999)}", "type": template["type"]}

        if template["type"] == "kill":
            quest["target"] = random.choice(template["target"])
            quest["count"] = random.randint(*template["count_range"])
            quest["reward_gold"] = quest["count"] * 10
        elif template["type"] == "collect":
            quest["item"] = random.choice(template["item"])
            quest["count"] = random.randint(*template["count_range"])
            quest["reward_gold"] = quest["count"] * 15
        elif template["type"] == "escort":
            quest["npc"] = random.choice(template["npc"])
            quest["distance"] = random.randint(*template["distance_range"])
            quest["reward_gold"] = quest["distance"]
        elif template["type"] == "explore":
            quest["location"] = random.choice(template["location"])
            quest["reward_gold"] = 200

        return quest


if __name__ == "__main__":
    # Terrain test
    terrain = TerrainGenerator(seed=42)
    heightmap = terrain.generate_heightmap(10, 10)
    logger.info(f"Generated {len(heightmap)}x{len(heightmap[0])} terrain")
    logger.info(f"Sample heights: {[round(heightmap[0][i], 2) for i in range(5)]}")

    # Loot test
    loot = LootTable()
    drops = [loot.roll("rare") for _ in range(5)]
    logger.info(f"Rare loot drops: {drops}")

    # Quest test
    quest_gen = QuestGenerator()
    quests = [quest_gen.generate() for _ in range(3)]
    for q in quests:
        logger.info(f"Quest: {q['type']} - {q}")

        return quest


if __name__ == "__main__":
    # Terrain test
    terrain = TerrainGenerator(seed=123)
    heightmap = terrain.generate_heightmap(10, 10, scale=0.2)
    logger.info(
        f"Terrain (10x10): min={min(min(row) for row in heightmap):.2f}, max={max(max(row) for row in heightmap):.2f}"
    )

    # Loot test
    loot = LootTable()
    drops = [loot.roll("rare") for _ in range(5)]
    logger.info(f"Loot drops: {drops}")

    # Quest test
    quest_gen = QuestGenerator()
    quests = [quest_gen.generate() for _ in range(3)]
    logger.info(f"Generated quests: {json.dumps(quests, indent=2)}")
