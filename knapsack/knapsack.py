from enum import Enum, auto
import numpy as np

class ProblemType (Enum):
    BOUNDED = auto()
    UNBOUNDED = auto()

class Bounds (Enum):
    LOWER_BOUND = 0
    UPPER_BOUND = 1

class Knapsack:
    POP_SIZE = 100
    MUTATION_RATE = 0.1
    GENERATIONS = 200

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
            self.max_quantities = np.where(self.weights > self.capacity, 0, 1) # Checks whether the weights are greater than the capacity and if they are set them to 0 otherwise 1
        else:
            self.max_quantities = np.array([self.calculate_maxitem(weight) for weight in self.weights])

        self.belief_space = [np.zeros(self.num_of_items).astype(int), self.max_quantities.copy()] # 

    def create_population(self): #Basically our Genotype (The way we encode the data that the algorithm handles) which is Integer in our case Phenotype always represents reality (Knapsack with actual physical items)
        random_percentages = np.random.rand(self.POP_SIZE, self.num_of_items)
        #itemcounts is the random combination of items generated for use in the population
        itemcounts = random_percentages * (self.belief_space[Bounds.UPPER_BOUND.value] + 1) # Note to self, the +1 here is to alleviate the issue of not being able to reach the maximum value as .rand never generate a 1.0 limit is 0.99
        population = np.array(itemcounts).astype(int) #The acutal number of items we could have inside the sack
        #Below is the fix for the crash with these weights: 95 4 60 32 23 72 80 62 65 46 that I disscussed with Dr. Abdallah Essam
        for i in range(self.POP_SIZE):
            weight = np.dot(population[i], self.weights)# We basically scale down all overweight configurations prevent crashes if most items are more than 0
            if weight > self.capacity:
                # Scale down the vector to fit in the sack
                ratio = self.capacity / weight
                population[i] = (population[i] * ratio).astype(int)
        
        return population

    def calculate_maxitem(self, weight) -> int: # only relevant for unbounded
        return self.capacity // weight
    
    def calculate_fitness(self, population):
        total_weight = np.dot(population, self.weights)
        total_value = np.dot(population, self.values)
        fitness = np.where(total_weight <= self.capacity, total_value, 0)
        return fitness
    
    def update_belief_space(self, population, fitness):
        current_best_index = np.argmax(fitness)
        #print(fitness) # For Debugging TODO remove
        if fitness[current_best_index] > self.best_fitness:
            self.best_fitness = fitness[current_best_index]
            self.best_solution = population[current_best_index].copy()

        #TODO Try to find a way to make it descending
        top_performers_index = np.argsort(fitness)[-int(self.POP_SIZE * 0.2):] # Negative index means count from the end A Python Princaple
        top_performers = population[top_performers_index]
        # The following lines are to fix the issue that we discussed in the meeting about having items with fitness = 0 influence the belief space
        top_performers_values = fitness[top_performers_index]
        valid_solutions = top_performers[top_performers_values > 0]
        # valid_solutions is a 2D array whose calculated fitness for each fitness is greater than 0
        if valid_solutions.size >= 2: # Always ensure at least two items for Crossover
            self.belief_space[Bounds.LOWER_BOUND.value] = np.min(valid_solutions, axis=0)
            self.belief_space[Bounds.UPPER_BOUND.value] = np.max(valid_solutions, axis=0)
            return valid_solutions #For use in crossover
        
        return top_performers


    def crossover(self, parents): # Single point Crossover
        children = []
        if self.best_solution is not None: # to not lose the elite
            children.append(self.best_solution.copy())

        while len(children) < self.POP_SIZE:# For every 2 parents 2 children are produced
            #To lessen confusion we will use expansion, just like the spread operator in js (...)
            parent1_index, parent2_index = np.random.choice(len(parents), size=2, replace=False) # The size parameter being 2 means that function returns only two random parents 
            #and the replace being false means that the same parent cannot be selected multiple times as it doesn't make sense as it wpuld just produce itself again
            
            parent1 = parents[parent1_index]
            parent2 = parents[parent2_index]

            crossover_point = np.random.randint(1, self.num_of_items)
            child = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
            children.append(child)
            #TODO Look into Uniform Crossover
            if len(children) < self.POP_SIZE:
                child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
                children.append(child2)

        return np.array(children)

    def mutate(self, individual): # Never send an array to this unless you want abominations 
        for i in range(self.num_of_items): # We loop on the no. of items as it's the size of the array
            if np.random.rand() < self.MUTATION_RATE:
                low = int(self.belief_space[Bounds.LOWER_BOUND.value][i])
                high = int(self.belief_space[Bounds.UPPER_BOUND.value][i])
                
                if low < high:
                    individual[i] = np.random.randint(low, high + 1)
                else:
                    individual[i] = low
        return individual
    
    def solveKnapsack(self):
        population = self.create_population()

        for generation in range(self.GENERATIONS):
            fitness = self.calculate_fitness(population)
            parents = self.update_belief_space(population, fitness)
            next_gen = self.crossover(parents)
            
            start_index = 1 if self.best_solution is not None else 0 #To prevent our Elite dude from dying basically
            #Looping through thr population to mutate them helppp
            for i in range(start_index, len(next_gen)):
                next_gen[i] = self.mutate(next_gen[i])

            population = next_gen
            
            if generation % 50 == 0: # For analysis will be removedf
                print(f"Gen {generation}: Best Value = {self.best_fitness}")

        print(f"Best Value: {self.best_fitness}")
        print(f"Knapsack Arrangement: {self.best_solution}")
        return self.best_solution, self.best_fitness
    
    #For plots
    def solveKnapsackGenerator(self):
        population = self.create_population()

        for generation in range(self.GENERATIONS):
            fitness = self.calculate_fitness(population)
            parents = self.update_belief_space(population, fitness)
            next_gen = self.crossover(parents)
            
            start_index = 1 if self.best_solution is not None else 0
            for i in range(start_index, len(next_gen)):
                next_gen[i] = self.mutate(next_gen[i])

            population = next_gen
            
            # Yield current state to the GUI
            # We return: Generation Number, Current Best Fitness, Average Fitness (optional but good for plots)
            avg_fitness = np.mean(fitness)
            yield generation, self.best_fitness, avg_fitness

        return self.best_solution, self.best_fitness