import random
from random import randint

class Genetic_algorithm:
    Performence = []
    Total_perfomence_value = 0
    POPULATION = []
    parents = [[], []]
    offspring_list = []

    file = open('Data.txt', 'r')
    lines = file.readlines()
    file.close()

    for row in lines:
        cols = row.strip().split()
        Performence.append(cols)

    def make_Chromosome(self):
        performance_list = []
        genes = []
        for person in range(12):
            task = random.randint(0, 9)
            performance_list.append(Genetic_algorithm.Performence[person][task])
            person_letter = chr(person + 65)
            genes.append(f"{person_letter}{task+1}")
        Genetic_algorithm.Total_perfomence_value = sum(int(num.replace(',', '')) for num in performance_list)
        chromosomes = genes, Genetic_algorithm.Total_perfomence_value
        return chromosomes

    def Population_selection(self, population):
        for i in range(population):
            chromosomes = self.make_Chromosome()
            Genetic_algorithm.POPULATION.append(chromosomes)
            print(f"Population {i + 1}: {chromosomes[0]}  P_Value = {chromosomes[1]}")

    def get_best_chromosome(self):
        return max(Genetic_algorithm.POPULATION, key=lambda x: x[1])

    def select_parents(self):
        best_chromosome = self.get_best_chromosome()
        random_chromosome = random.choice([chromosome for chromosome in Genetic_algorithm.POPULATION if chromosome != best_chromosome])
        self.parents[0].append(best_chromosome)
        self.parents[1].append(random_chromosome)
#CROSSOVER
    def crossover(self):
        if len(self.parents[0]) == 0 or len(self.parents[1]) == 0:
            raise ValueError("Parents list must contain chromosomes for crossover.")
        best_chromosome = self.parents[0][0][0]
        random_chromosome = self.parents[1][0][0]
        cross_idx = randint(1, len(best_chromosome) - 1)
        
        print(f"Crossover between:\nParent 1: {best_chromosome} \nParent 2: {random_chromosome}")
        
        offspring1 = best_chromosome[:cross_idx] + random_chromosome[cross_idx:]
        offspring2 = random_chromosome[:cross_idx] + best_chromosome[cross_idx:]
        self.offspring_list.append((offspring1, offspring2))
        return offspring1, offspring2
#TOURNAMENT SELECTION
    def tournament_selection(self, num_selected):
        if num_selected >= len(Genetic_algorithm.POPULATION):
            print("Error: num_selected must be less than the total number of populations.")
            return

        selected_population = random.sample(Genetic_algorithm.POPULATION, num_selected)
        print("\nSelected populations for tournament:")
        for idx, chromosomes in enumerate(selected_population):
            print(f"Selected Population {idx + 1}: {chromosomes[0]}  P_Value = {chromosomes[1]}")

        best_population = max(selected_population, key=lambda x: x[1])
        print(f"\nBest Population: {best_population[0]}  P_Value = {best_population[1]}")
        self.select_parents()
#ROULETTE SELECTION
    def roulette_selection(self):
        total_fitness = sum(chromosome[1] for chromosome in Genetic_algorithm.POPULATION)
        pick = random.uniform(0, total_fitness)
        current = 0
        print(f"Total Fitness: {total_fitness}, Random Pick: {pick}")
        for idx, chromosome in enumerate(Genetic_algorithm.POPULATION):
            current += chromosome[1]
            print(f"Population {idx + 1}: Cumulative Fitness = {current}")
            if current > pick:
                print(f"Selected by Roulette: Population {idx + 1}: {chromosome[0]}  P_Value = {chromosome[1]}")
                self.parents[0].append(chromosome)
                self.parents[1].append(random.choice([c for c in Genetic_algorithm.POPULATION if c != chromosome]))
                return chromosome

#MUTATION
    def mutate(self, offspring):
        mutated_offspring = []

        for chromosome in offspring:
            mutated_chromosome = list(chromosome)
            index1, index2 = random.sample(range(len(mutated_chromosome)), 2)
            mutated_chromosome[index1], mutated_chromosome[index2] = mutated_chromosome[index2], mutated_chromosome[index1]
            mutated_offspring.append(mutated_chromosome)

        print(f"Mutated Offsprings(1 and 2): {mutated_offspring}")
        return mutated_offspring
ga = Genetic_algorithm()
populatioN = int(input("Enter the number of populations: "))
# Check if the population size is within the valid range
if 10 <= populatioN <= 100:
    ga.Population_selection(populatioN)
    
    # Prompt user for selection method
    n = int(input("Enter a number for any of the following selections: \n1 for Tournament \n2 for Roulette: "))
    
    if n == 1:
        num_selected = random.randint(2, populatioN - 1)  # Randomly select number of individuals for tournament
        ga.tournament_selection(num_selected)
        offspring = ga.crossover()  # Perform crossover
        print(f"Offspring1: {offspring[0]} \nOffspring2: {offspring[1]}")
        ga.mutate(ga.offspring_list[0])  # Apply mutation to the first offspring

    elif n == 2:
        ga.roulette_selection()  # Perform roulette selection
        offspring = ga.crossover()  # Perform crossover
        print(f"Offspring1: {offspring[0]} \nOffspring2: {offspring[1]}")

    else:
        print("Invalid selection. Please enter 1 for Tournament or 2 for Roulette.")

else:
    print("Population must be between 10 and 100 inclusive.")
