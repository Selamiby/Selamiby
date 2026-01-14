import uuid
from typing import Any, Dict, List, Type

# --- NEXUS SOVEREIGN ARCHITECTURE: ECS KERNEL (Gitee/High-Performance Inspired) ---

class Component:
    """Base class for all components. Data only."""
    pass

class Position(Component):
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

class AIControl(Component):
    def __init__(self, state="IDLE"):
        self.state = state

class Entity:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        self.components: Dict[Type[Component], Component] = {}

    def add(self, component: Component):
        self.components[type(component)] = component
        return self

    def get(self, component_type: Type[Component]) -> Any:
        return self.components.get(component_type)

class System:
    def update(self, entities: List[Entity], dt: float):
        pass

class EntityManager:
    def __init__(self):
        self.entities: List[Entity] = []
        self.systems: List[System] = []

    def create_entity(self) -> Entity:
        entity = Entity()
        self.entities.append(entity)
        return entity

    def add_system(self, system: System):
        self.systems.append(system)

    def update(self, dt: float):
        for system in self.systems:
            system.update(self.entities, dt)
