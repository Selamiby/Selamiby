import numpy as np
import json
from nexus_one import NexusEntity

class Brain:
    def __init__(self, entity_id, knowledge_graph):
        """
        Initialize the Brain component.

        Args:
        - entity_id (int): Unique identifier for the entity.
        - knowledge_graph (dict): Graph representing the entity's knowledge.
        """
        self.entity_id = entity_id
        self.knowledge_graph = knowledge_graph
        self.entity = NexusEntity(entity_id)

    def perceive(self, environment):
        """
        Perceive the environment and update the knowledge graph.

        Args:
        - environment (dict): Current state of the environment.
        """
        perception = self.entity.perceive(environment)
        self.knowledge_graph.update(perception)

    def reason(self, goal):
        """
        Reason about the goal and generate a plan.

        Args:
        - goal (str): Desired outcome.

        Returns:
        - plan (list): Sequence of actions to achieve the goal.
        """
        plan = []
        current_state = self.knowledge_graph["current_state"]
        for action in self.knowledge_graph["actions"]:
            if action["preconditions"].issubset(current_state):
                plan.append(action)
                current_state = action["effects"]
                if goal in current_state:
                    break
        return plan

    def act(self, plan):
        """
        Execute the plan and update the knowledge graph.

        Args:
        - plan (list): Sequence of actions to execute.
        """
        for action in plan:
            self.entity.act(action)
            self.knowledge_graph.update(action["effects"])

class NPCBrain(Brain):
    def __init__(self, entity_id, knowledge_graph, personality):
        """
        Initialize the NPC Brain component.

        Args:
        - entity_id (int): Unique identifier for the entity.
        - knowledge_graph (dict): Graph representing the entity's knowledge.
        - personality (dict): Personality traits of the NPC.
        """
        super().__init__(entity_id, knowledge_graph)
        self.personality = personality

    def make_decision(self, options):
        """
        Make a decision based on the personality traits.

        Args:
        - options (list): List of possible decisions.

        Returns:
        - decision (str): Chosen decision.
        """
        decision = np.random.choice(options, p=self.personality["decision_weights"])
        return decision

class AgentBrain(Brain):
    def __init__(self, entity_id, knowledge_graph, objectives):
        """
        Initialize the Agent Brain component.

        Args:
        - entity_id (int): Unique identifier for the entity.
        - knowledge_graph (dict): Graph representing the entity's knowledge.
        - objectives (list): List of objectives for the agent.
        """
        super().__init__(entity_id, knowledge_graph)
        self.objectives = objectives

    def prioritize_objectives(self):
        """
        Prioritize the objectives based on their importance.

        Returns:
        - prioritized_objectives (list): List of prioritized objectives.
        """
        prioritized_objectives = sorted(self.objectives, key=lambda x: x["importance"], reverse=True)
        return prioritized_objectives

# Example usage
if __name__ == "__main__":
    knowledge_graph = {
        "current_state": {"location": "town"},
        "actions": [
            {"name": "move_to_cave", "preconditions": {"location": "town"}, "effects": {"location": "cave"}},
            {"name": "fight_monster", "preconditions": {"location": "cave"}, "effects": {"experience": 100}}
        ]
    }
    entity_id = 1
    brain = Brain(entity_id, knowledge_graph)
    perception = brain.entity.perceive({"environment": "day"})
    brain.knowledge_graph.update(perception)
    plan = brain.reason("fight_monster")
    brain.act(plan)