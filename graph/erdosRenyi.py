import numpy as np
from random  import uniform, randint

from .graph import Graph

class ErdosRenyi(Graph):

	def __init__(self, n, p, w):
		Graph.__init__(self, n)
		while(not(self.isConnected())):
			self.edges = [[] for i in range(n)]
			self.m = 0
			for i in range(n):
				for j in range(i+1, n):
					if(uniform(0.0, 1.0) < p and (i != 0 or j != n-1)):
						self.addEdge(i, j, randint(1, w))
		self.setSource(0)
		self.setSink(n-1)
		self.initGraph()

	def isConnected(self):
		c = np.full(self.n, True, dtype=bool)
		stack = [0]
		while(stack != []):
			j = stack.pop()
			if(c[j]):
				c[j] = False
				for i in self.edges[j]:
					stack.append(i)
		return not(True in c)