import numpy as np
from random  import uniform, randint

from graph import Graph

class Waxman(Graph):

	def __init__(self, n, alpha=1.5, beta=1.0):
		Graph.__init__(self, n)
		self.x = np.random.random(n)
		self.y = np.random.random(n)

		self.x[0] = 0.0
		self.x[n-1] = 1.0
		self.y[0] = 1.0
		self.y[n-1] = 0.0

		self.distance = np.empty((self.n, self.n))
		self.getDistance()
		L = 0
		for i in range(n):
			l = np.inf
			for j in range(n):
				if(i != j):
					l = min(self.distance[i, j], l)
			L = max(l, L)

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