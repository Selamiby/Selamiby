import random

class BabyAGI:
    def __init__(self):
        self.knowledge = {}

    def learn(self, concept, definition):
        self.knowledge[concept] = definition

    def recall(self, concept):
        return self.knowledge.get(concept)

    def reason(self, premise, conclusion):
        if premise in self.knowledge:
            if self.knowledge[premise] == conclusion:
                return True
            else:
                return False
        else:
            return None

    def solve_problem(self, problem):
        for concept, definition in self.knowledge.items():
            if problem in definition:
                return concept
        return None

def main():
    agi = BabyAGI()
    agi.learn("insan", "akıllı canlı")
    agi.learn("hayvan", "canlı")
    print(agi.recall("insan"))
    print(agi.reason("insan", "akıllı canlı"))
    print(agi.solve_problem("akıllı canlı"))

if __name__ == "__main__":
    main()

# NEXUS-ONE CORE MODULE