import random

random.seed()


class GeneticAlgorithm:

	def __init__(self, populationSize, genes, target, bestParentSize, randomParentSize, mutation):
	    self.populationSize = populationSize
	    self.genes = genes
	    self.target = target
	    self.bestParentSize = bestParentSize
	    self.randomParentSize = randomParentSize
	    self.mutation = mutation
	    self.population = []
	    self.fitnessList = []
	    self.parents = []
	    self.chromosome = ""
	    self.generation = 1

	def create_population(self):
		for i in range(self.populationSize):
			self.chromosome = ""
			for j in range(len(self.target)):
				self.chromosome = self.chromosome + self.genes[random.randint(0, len(self.genes)-1)]
			self.population.append(self.chromosome)

	def check_fitness(self):
		for i in range(self.populationSize):
			counter = 0
			for j in range(len(self.target)):
				if self.target[j] == self.population[i][j]:
					counter += 1
			self.fitnessList.append(counter)

	def sort_lists(self):
		self.fitnessList, self.population = (list(t) for t in zip(*sorted(zip(self.fitnessList, self.population))))
		self.fitnessList.reverse()
		self.population.reverse()


	def choose_parents(self):
		self.parents = []
		for i in range(int(self.populationSize*self.bestParentSize)):
			self.parents.append(self.population[i])
		for i in range(int(self.populationSize*self.randomParentSize)):
			randomChoice = random.randint(int(self.populationSize*self.bestParentSize), self.populationSize-1)
			self.parents.append(self.population[randomChoice])

	def crossover(self):
		self.population = []
		self.fitnessList = []
		for i in range(self.populationSize):
			self.chromosome = ""
			parentOne = self.parents[random.randint(0, len(self.parents)-1)]
			parentTwo = self.parents[random.randint(0, len(self.parents)-1)]
			for j in range(len(self.target)):
				randomChoice = random.randint(0,1)
				if randomChoice == 0:
					self.chromosome = self.chromosome + parentOne[j]
				else:
					self.chromosome = self.chromosome + parentTwo[j]
			self.mutate()
			self.population.append(self.chromosome)

	def mutate(self):
		randomChoice = random.random()
		if randomChoice < self.mutation:
			self.chromosome = list(self.chromosome)
			self.chromosome[random.randint(0,len(self.target)-1)] = self.genes[random.randint(0,len(self.genes)-1)]
			self.chromosome = "".join(self.chromosome)


def main():
	populationSize = 10000
	genes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	bestParentSize = 0.4
	randomParentSize = 0.1
	mutation = 0.1

	target = input("Please type any word, it can contain small and large letters. \n")

	ga = GeneticAlgorithm(populationSize, genes, target, bestParentSize, randomParentSize, mutation)

	ga.create_population()
	ga.check_fitness()
	ga.sort_lists()

	while ga.fitnessList[0] != len(ga.target):
		print(f"Generation {ga.generation}. Best fitness: {ga.population[0]}")
		ga.choose_parents()
		ga.crossover()
		ga.check_fitness()
		ga.sort_lists()
		ga.generation += 1

	if ga.fitnessList[0] == len(ga.target):
		print(f"Generation {ga.generation}. Your word is {ga.population[0]}")


main()



