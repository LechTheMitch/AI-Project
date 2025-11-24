from enum import Enum, auto
import numpy as np

class ProblemType (Enum):
    BOUNDED = auto()
    UNBOUNDED = auto()

class Knapsack:
    POP_SIZE = 100
    MUTATION_RATE = 0.1

    def __init__(self, problem_type: ProblemType, capacity: int, weights, values): # Weights and Values need Type Checking
        if capacity <= 0:
            raise ValueError("The Knapsack Capacity must be a positive integer")
        self.capacity = capacity
        self.problem_type = problem_type
        self.num_of_items = len(weights)
        self.current_population = [] # Will be used as state, similar to React
        self.weights = np.array(weights)
        self.values = np.array(values)
        self.best_solution = None #Elitism
        self.best_fitness = 0

        if self.problem_type == ProblemType.BOUNDED:
            self.max_quantities = np.where(self.weights > self.capacity, 0, 1)
        else:
            self.max_quantities = np.array([self.calculate_maxitem(weight) for weight in self.weights])

        self.normative_bounds = [np.zeros(self.num_of_items).astype(int), self.max_quantities.copy()]

    def create_population(self):
        random_percentages = np.random.rand(self.POP_SIZE, self.num_of_items)
        itemcounts = random_percentages * (self.normative_bounds[1] + 1) # Note to self, the +1 here is to alleviate the issue of not being able to reach the maximum value as .rand never generate a 1.0 limit is 0.99
        return np.array(itemcounts).astype(int) #The acutal number of items we could have inside the sack

    def clear_sack(self) -> None:
        self.current_population.clear()

    def calculate_maxitem(self, weight) -> int: # only relevant for unbounded
        return self.capacity // weight
    
    def calculate_fitness(self, population):
        total_weight = np.dot(population, self.weights)
        total_value = np.dot(population, self.values)
        fitness = np.where(total_weight <= self.capacity, total_value, 0)
        return fitness, total_weight
    
    def update_belief_space(self, population, fitness):
        current_best_index = np.argmax(fitness)
        if fitness[current_best_index] > self.best_fitness:
            self.best_fitness = fitness[current_best_index]
            self.best_solution = population[current_best_index].copy()

        top_percentile_index = np.argsort(fitness)[-int(self.POP_SIZE * 0.2):]
        top_performers = population[top_percentile_index]
        
        self.normative_bounds[0] = np.min(top_performers, axis=0)
        self.normative_bounds[1] = np.max(top_performers, axis=0)

    def mutate(self, individual):
        for i in range(self.num_of_items):
            if np.random.rand() < self.MUTATION_RATE:
                low = int(self.normative_bounds[0][i])
                high = int(self.normative_bounds[1][i])
                
                if low < high:
                    individual[i] = np.random.randint(low, high + 1)
                else:
                    individual[i] = low
        return individual
    
    def solveKnapsack():
        #TODO with GUI
        pass
    
    def test_print(self, weight): # TODO needs to be removed later
        self.current_population = self.create_population()
        print(self.calculate_fitness(self.current_population))

