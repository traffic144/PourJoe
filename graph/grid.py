import numpy as np

from graph import Graph

class Grid(Graph):

	def __init__(self, n, m, d, r=1.0):
		Graph.__init__(self, (n+1)*(m+1))
		self.largeur = n
		self.hauteur = m
		x = np.array([i//(m+1) for i in range(self.n)])
		y = np.array([i%(m+1) for i in range(self.n)])
		for i in range(self.n):
			for j in range(i+1, self.n):
				dist = (x[i]-x[j])**2 + (y[i]-y[j])**2
				if(dist <= r**2 and i != j):
					self.addEdge(i, j, np.sqrt(dist))
		self.setSource(d*(m+1) + d)
		self.setSink((n-d)*(m+1) + (m-d))
		self.initGraph()

	def drawMap(self, k):
		res = np.empty(self.n)
		for i in range(self.n):
			res[self.listMin[i]] = self.gamma(i, k)
		return res.reshape(self.largeur+1, self.hauteur+1)