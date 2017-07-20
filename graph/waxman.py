import numpy as np
from random  import uniform, randint

from graph import Graph

class Waxman(Graph):

	def __init__(self, n, alpha=0.07, beta=1.0):
		Graph.__init__(self, n)
		self.x = np.random.random(n)
		self.y = np.random.random(n)

		self.distance = np.empty((self.n, self.n))
		self.getDistance()
		L = np.amax(self.distance)

		for i in range(n):
			for j in range(i+1, n):
				if(uniform(0.0, 1.0) < self.proba(alpha, beta, self.distance[i, j], L) and (i!=0 or j!=n-1)):
					self.addEdge(i, j, self.distance[i][j])
		self.setSource(0)
		self.setSink(n-1)
		self.initGraph()

	def getDistance(self):
		for i in range(self.n):
			xi = self.x[i]
			yi = self.y[i]
			self.distance[i] = np.sqrt(np.square(self.x - xi) + np.square(self.y - yi))

	def proba(self, alpha, beta, l, L):
		return beta*np.exp(-l/(L*alpha))