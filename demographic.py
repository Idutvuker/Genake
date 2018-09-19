from genetic import *
from constants import *
import sys

class Individual:
	id = 0

	def __init__(self, silent = False):
		self.genome = Genome()
		self.result = 0
		self.p1 = -1
		self.p2 = -1

	
		if (silent):
			self.id = -1
		else:
			self.new()
		

	def __lt__(self, other):
		return self.result < other.result

	def new(self, p1 = -1, p2 = -1):
		Individual.id += 1
		self.id = Individual.id

		self.p1 = p1
		self.p2 = p2

#Every pair has 2 children
def breed(indA, indB, childA): 
	crossover(indA.genome, indB.genome, childA.genome)
	childA.new(indA.id, indB.id)
	return childA

def progressBar(value, best, mean):
	z = round(value * 30)
	sys.stdout.write("\r [{0}] {1}% Best: {2}".format('-'*z + '>' +' ' * (29 - z), round(value * 100), best))
	sys.stdout.flush()

bestever = None
def statistics(population, epoch):
	best = population[0]
	worst = population[-1]
	med = population[GEN_POPULATION // 2]

	print("{0:3d}   {1:.5f}    {2:.5f}    {3}  {4}".format(epoch + 1, best.result, np.mean([x.result for x in population]), best.p1, best.p2))

	#progressBar(epoch / GEN_ERAS, best.result, 0)

	global bestever
	if (epoch == 0):
		bestever = best

	elif bestever < best:
		bestever = best
		#print("New best! Parents:{0}, {1}".format(best.p1, best.p2))

	if epoch == GEN_ERAS - 1:
		print()
		print(bestever.result)
		np.save("test", bestever.genome.weights)



def proliferation(population):
	l = len(population)

	mn = population[-1].result
	p = np.array([np.power(ind.result - mn + 0.1, FITNESS_SCALE_PARENT) for ind in population])

	s = np.sum(p)
	np.divide(p, s, p)

	nkids = l // 4 * 3
	x = np.random.multinomial(nkids, p)
	x = x[x.nonzero()]

	z = np.random.randint(0, l // 4 * 3, nkids)

	new_pop = [Individual(True) for i in range(l)]

	c = 0
	for i in range(len(x)):
		for j in range(x[i]):
			t = z[c]
			if t >= x[i]:
				t += 1

			breed(population[x[i]], population[t], new_pop[c])
			c += 1

	p = np.array([np.power(ind.result - mn + 0.1, FITNESS_SCALE) for ind in population])
	s = np.sum(p)
	np.divide(p, s, p)

	x = np.random.choice(np.arange(l), l // 4, False, p) #Survivors

	for i in range(len(x)):
		new_pop[nkids + i] = population[x[i]]

	population[:] = new_pop

	return population

	#good = len(population) // 2
	#x = np.random.permutation(np.arange(good))
	#print(x)