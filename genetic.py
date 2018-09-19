import numpy as np
from constants import (MUTATION_RATE, MUTATION_FACTOR, NET_SIZES, CROSSOVER_POINTS)

class Genome():
	sizes = NET_SIZES
	numl = len(sizes)

	#Generator is not working for some reason
	dna_len = 0
	for i in range(numl - 1):
		dna_len += sizes[i + 1] * (sizes[i] + 1)

	#print(dna_len)

	def __init__(self, weights = None):
		if weights is None:
			self.weights = [np.random.randn(self.sizes[i + 1], self.sizes[i] + 1) for i in range(self.numl-1)]

		else:
			self.weights = weights


def crossover(genA, genB, childGen):
	points = sorted(np.random.permutation(np.arange(1, Genome.dna_len - 2))[:CROSSOVER_POINTS])

	dels = 0
	AoverB = (np.random.random_integers(0, 1) == 1)
	c = 0

	mutations = np.random.randint(0, 100, Genome.dna_len) < MUTATION_RATE

	sizes = Genome.sizes
	for layer in range(Genome.numl - 1):
		for node in range(sizes[layer + 1]):
			rowC = childGen.weights[layer][node]
			rowA = genA.weights[layer][node]
			rowB = genB.weights[layer][node]
			for i in range(sizes[layer] + 1):
				#wA = genA.weights[layer][node][i]
				#wB = genB.weights[layer][node][i]

				if AoverB:
					rowC[i] = rowA[i]
				else:
					rowC[i] = rowB[i]

				#Crossover
				#if c == points[dels]:
				#	if dels != (CROSSOVER_POINTS - 1):
				#		dels += 1
				#	AoverB ^= True

				#Mutations
				if (mutations[c]):
					rowC[i] += MUTATION_FACTOR * np.random.randn()

				c += 1
				
	return childGen
	#print(*childGen.weights, sep = "\n", end = "\n---END GENOME---\n")

def mutate(dna):
	for i in range(len(dna)):
		if (np.random.randint(0, 100) < MUTATION_RATE):
			dna[i] += MUTATION_FACTOR * np.random.randn()

def getRandomDna(size):
	dna = np.random.randn(size)

	return dna
