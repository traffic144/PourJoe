import numpy as np
from random  import uniform, randint

from graph import Graph

class DoubleWestphal(Graph):

	def __init__(self, m1, m2, alpha):
		Graph.__init__(self, m1 + m2 + 3)
		self.m1 = m1
		self.m2 = m2
		for i in range(m1):
			self.addEdge(0, i+1, alpha)
			self.addEdge(i+1, m1+1, 0)
		for i in range(m2):
			self.addEdge(m1+1, m1+2+i, (1-alpha))
			self.addEdge(m1+2+i, m1+m2+2, 0)
		self.setSource(0)
		self.setSink(m1+m2+2)

	def getBlockedEdges(self, k):
		l = randint(max(0, k-(self.m2-1)), min(self.m1-1, k))
		n1 = [i for i in range(self.m1)]
		b1 = []
		for j in range(l):
			a = randint(0, self.m1-j-1)
			b1.append(n1[a])
			del(n1[a])
		blockedLeft = [(b1[i]+1, self.m1+1) for i in range(l)]
		n2 = [i for i in range(self.m2)]
		b2 = []
		for j in range(k-l):
			a = randint(0, self.m2-j-1)
			b2.append(n2[a])
			del(n2[a])
		blockedRight = [(self.m1+2+b2[i], self.m1+self.m2+2) for i in range(k-l)]
		return blockedLeft + blockedRight
