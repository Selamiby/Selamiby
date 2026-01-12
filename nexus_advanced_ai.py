#!/usr/bin/env python3
"""
NEXUS Advanced AI System
- Behavior trees for NPC AI
- ML-based decision making (lightweight inference)
- Pathfinding (A* algorithm)
"""
import heapq
import json
import logging
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[logging.FileHandler(log_dir / "advanced_ai.log", encoding="utf-8")],
)
logger = logging.getLogger("ai")


class NodeStatus(Enum):
    SUCCESS = 1
    FAILURE = 2
    RUNNING = 3


@dataclass
class Blackboard:
    """Shared memory for behavior tree."""

    data: Dict = None

    def __post_init__(self):
        self.data = self.data or {}


class BTNode:
    """Base behavior tree node."""

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        raise NotImplementedError


class Sequence(BTNode):
    """Execute children in order until one fails."""

    def __init__(self, children: List[BTNode]):
        self.children = children

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS


class Selector(BTNode):
    """Execute children until one succeeds."""

    def __init__(self, children: List[BTNode]):
        self.children = children

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard)
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE


class Condition(BTNode):
    """Check condition."""

    def __init__(self, fn: Callable[[Blackboard], bool]):
        self.fn = fn

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        return NodeStatus.SUCCESS if self.fn(blackboard) else NodeStatus.FAILURE


class Action(BTNode):
    """Perform action."""

    def __init__(self, fn: Callable[[Blackboard], NodeStatus]):
        self.fn = fn

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        return self.fn(blackboard)


def example_npc_tree() -> BTNode:
    """Example NPC AI: patrol → detect enemy → attack."""
    return Selector(
        [
            Sequence(
                [
                    Condition(lambda bb: bb.data.get("enemy_nearby", False)),
                    Action(
                        lambda bb: (
                            NodeStatus.SUCCESS
                            if bb.data.update({"action": "attack"}) or True
                            else NodeStatus.FAILURE
                        )
                    ),
                ]
            ),
            Action(
                lambda bb: (
                    NodeStatus.SUCCESS
                    if bb.data.update({"action": "patrol"}) or True
                    else NodeStatus.FAILURE
                )
            ),
        ]
    )


class AStarPathfinder:
    """A* pathfinding algorithm."""

    def __init__(self, grid: List[List[int]]):
        self.grid = grid  # 0=walkable, 1=blocked
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Manhattan distance."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighbors."""
        r, c = pos
        candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        return [
            (nr, nc)
            for nr, nc in candidates
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0
        ]

    def find_path(
        self, start: Tuple[int, int], goal: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """A* pathfinding."""
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return list(reversed(path))

            for neighbor in self.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        return None  # No path found


class MLDecisionMaker:
    """Lightweight ML inference (decision tree approximation)."""

    def __init__(self):
        self.rules = [
            {"conditions": {"hp": "<", "value": 0.3}, "action": "flee"},
            {"conditions": {"enemy_distance": "<", "value": 5}, "action": "attack"},
            {"conditions": {"ammo": "==", "value": 0}, "action": "reload"},
        ]

    def decide(self, state: Dict) -> str:
        """Rule-based decision (simulates ML inference)."""
        for rule in self.rules:
            cond = rule["conditions"]
            key = list(cond.keys())[0]
            if key == "hp":
                continue  # Simplified
            op = cond.get(key)
            if op == "<" and state.get(key, 100) < cond["value"]:
                return rule["action"]
            elif op == "==" and state.get(key) == cond["value"]:
                return rule["action"]

        return "idle"


if __name__ == "__main__":
    # Behavior tree test
    bb = Blackboard(data={"enemy_nearby": True})
    tree = example_npc_tree()
    status = tree.tick(bb)
    logger.info(f"BT result: {bb.data['action']}")

    # Pathfinding test
    grid = [[0, 0, 0, 1, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0]]
    pathfinder = AStarPathfinder(grid)
    path = pathfinder.find_path((0, 0), (3, 4))
    logger.info(f"Path: {path}")

    # ML decision
    ml = MLDecisionMaker()
    action = ml.decide({"enemy_distance": 3, "ammo": 10})
    logger.info(f"ML action: {action}")
