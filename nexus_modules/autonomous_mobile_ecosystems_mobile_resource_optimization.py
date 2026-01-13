import math
import random

class MobileResource:
    def __init__(self, id, capacity, current_load):
        self.id = id
        self.capacity = capacity
        self.current_load = current_load

    def optimize(self):
        if self.current_load > self.capacity:
            excess = self.current_load - self.capacity
            self.current_load -= excess
            return excess
        return 0

class MobileResourceOptimizer:
    def __init__(self, resources):
        self.resources = resources

    def optimize(self):
        total_excess = 0
        for resource in self.resources:
            excess = resource.optimize()
            total_excess += excess
        return total_excess

def main():
    resources = [
        MobileResource(1, 100, 150),
        MobileResource(2, 200, 250),
        MobileResource(3, 300, 350)
    ]
    optimizer = MobileResourceOptimizer(resources)
    total_excess = optimizer.optimize()
    print("Toplam excess:", total_excess)

if __name__ == "__main__":
    main()
# NEXUS-ONE CORE MODULE