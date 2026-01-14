import numpy as np
import psutil
import gc

class OptimizationManager:
    def __init__(self):
        self.memory_threshold = 80  # percentage
        self.cpu_threshold = 90  # percentage

    def monitor_memory_usage(self):
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > self.memory_threshold:
            print(f"Memory usage exceeded {self.memory_threshold}%: {memory_usage}%")
            gc.collect()

    def monitor_cpu_usage(self):
        cpu_usage = psutil.cpu_percent()
        if cpu_usage > self.cpu_threshold:
            print(f"CPU usage exceeded {self.cpu_threshold}%: {cpu_usage}%")

    def optimize(self):
        self.monitor_memory_usage()
        self.monitor_cpu_usage()

class GameObject:
    def __init__(self, name):
        self.name = name
        self.mesh = None
        self.texture = None

    def load_mesh(self):
        # Load mesh data
        self.mesh = np.random.rand(1000, 3)  # Placeholder for mesh data

    def load_texture(self):
        # Load texture data
        self.texture = np.random.rand(1000, 1000, 3)  # Placeholder for texture data

    def unload(self):
        self.mesh = None
        self.texture = None
        gc.collect()

class SceneManager:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
        obj.unload()

def main():
    optimization_manager = OptimizationManager()
    scene_manager = SceneManager()

    # Create game objects
    obj1 = GameObject("Object 1")
    obj2 = GameObject("Object 2")

    # Load object data
    obj1.load_mesh()
    obj1.load_texture()
    obj2.load_mesh()
    obj2.load_texture()

    # Add objects to scene
    scene_manager.add_object(obj1)
    scene_manager.add_object(obj2)

    # Optimize scene
    optimization_manager.optimize()

    # Remove object from scene
    scene_manager.remove_object(obj1)

    # Optimize scene again
    optimization_manager.optimize()

if __name__ == "__main__":
    main()