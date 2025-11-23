from enum import Enum, auto
class ProblemType (Enum):
    BOUNDED = auto()
    UNBOUNDED = auto()
class Knapsack:
    def __init__(self, capacity: int, problemType: ProblemType):
        if capacity <= 0:
            raise ValueError("The Knapsack Capacity must be a positive integer")
        self.capacity = capacity
        self.problemType = problemType

    def clear_sack(self) -> None:
        self.items.clear()
