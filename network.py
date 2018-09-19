import numpy as np

from genetic import Genome
from constants import NET_SIZES

class Network:
	actFunction = np.tanh
	genome = None

	actv = [np.zeros((y + 1, 1)) for y in NET_SIZES] #Deep optimization
	for i in range(len(actv)):
		actv[i][-1][0] = 1

	def setGenome(self, genome):
		self.genome = genome

	def feedforward(self, a):
		self.actFunction(np.dot(self.genome.weights[0], a), self.actv[1][:-1])
		for i in range(1, self.genome.numl - 1):
			self.actFunction(np.dot(self.genome.weights[i], self.actv[i]), self.actv[i + 1][:-1])
		
		return self.actv[-1]