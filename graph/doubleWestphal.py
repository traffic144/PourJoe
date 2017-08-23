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
		self.title = r'Double Westphal graph ($m_1 = ' + str(m1) + r'$, $m_2 = ' + str(m2) + r'$)'

	def getBlockedEdges(self, k):
		n = [i for i in range(self.m1+self.m2-2)]
		b = []
		for j in range(k):
			a = randint(0, self.m1+self.m2-j-3)
			b.append(n[a])
			del(n[a])
		blocked = []
		for i in b:
			if i < self.m1-1:
				blocked.append((i+1, self.m1+1))
			else:
				blocked.append((i+3, self.m1+self.m2+2))
		return blocked
