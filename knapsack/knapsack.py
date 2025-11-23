from enum import Enum, auto
import numpy as np

class ProblemType (Enum):
    BOUNDED = auto()
    UNBOUNDED = auto()

# Need to inquire about the number of generations and the mutation rates, whether they are user determined or I can skip that step
class Knapsack:
    def __init__(self, problem_type: ProblemType, capacity: int, weights, values): # Weights and Values need Type Checking
        if capacity <= 0:
            raise ValueError("The Knapsack Capacity must be a positive integer")
        self.capacity = capacity
        self.problem_type = problem_type
        self.num_of_items = len(weights)
        self.current_population = [] # Will used as state, similar to React


    @classmethod
    def clear_sack(self) -> None:
        self.items.clear()
        
    