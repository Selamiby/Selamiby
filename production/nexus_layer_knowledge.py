import json
from typing import Dict, List

class KnowledgeBase:
    def __init__(self):
        self.tutorials = {}
        self.guides = {}

    def add_tutorial(self, tutorial_id: str, tutorial_data: Dict):
        self.tutorials[tutorial_id] = tutorial_data

    def add_guide(self, guide_id: str, guide_data: Dict):
        self.guides[guide_id] = guide_data

    def get_tutorial(self, tutorial_id: str) -> Dict:
        return self.tutorials.get(tutorial_id)

    def get_guide(self, guide_id: str) -> Dict:
        return self.guides.get(guide_id)

    def update_tutorial(self, tutorial_id: str, tutorial_data: Dict):
        if tutorial_id in self.tutorials:
            self.tutorials[tutorial_id] = tutorial_data

    def update_guide(self, guide_id: str, guide_data: Dict):
        if guide_id in self.guides:
            self.guides[guide_id] = guide_data

    def delete_tutorial(self, tutorial_id: str):
        if tutorial_id in self.tutorials:
            del self.tutorials[tutorial_id]

    def delete_guide(self, guide_id: str):
        if guide_id in self.guides:
            del self.guides[guide_id]

    def to_json(self) -> str:
        knowledge_base_data = {
            "tutorials": self.tutorials,
            "guides": self.guides
        }
        return json.dumps(knowledge_base_data)

class JiānghéngKnowledgeBase(KnowledgeBase):
    def __init__(self):
        super().__init__()
        self.load_data()

    def load_data(self):
        # Load data from existing NEXUS-ONE codebase
        # For demonstration purposes, assume data is stored in a JSON file
        with open("knowledge_base_data.json", "r") as file:
            knowledge_base_data = json.load(file)
            self.tutorials = knowledge_base_data.get("tutorials", {})
            self.guides = knowledge_base_data.get("guides", {})

    def save_data(self):
        # Save data to existing NEXUS-ONE codebase
        # For demonstration purposes, assume data is stored in a JSON file
        knowledge_base_data = {
            "tutorials": self.tutorials,
            "guides": self.guides
        }
        with open("knowledge_base_data.json", "w") as file:
            json.dump(knowledge_base_data, file)

# Example usage
knowledge_base = JiānghéngKnowledgeBase()
tutorial_data = {
    "title": "Getting Started",
    "description": "A brief introduction to the game",
    "steps": [
        "Step 1: Create a character",
        "Step 2: Explore the world"
    ]
}
knowledge_base.add_tutorial("getting_started", tutorial_data)
print(knowledge_base.get_tutorial("getting_started"))