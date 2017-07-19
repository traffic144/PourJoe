import numpy as np

from graph import Graph

class DoubleWestphal(Graph):

	def __init__(self, m1, m2, alpha):
		Graph.__init__(self, m1 + m2 + 3)
		for i in range(m1):
			self.addEdge(0, i+1, alpha/2)
			self.addEdge(i+1, m1+1, alpha/2)
		for i in range(m2):
			self.addEdge(m1+1, m1+2+i, (1-alpha)/2)
			self.addEdge(m1+2+i, m1+m2+2, (1-alpha)/2)
		self.setSource(0)
		self.setSink(m1+m2+2)
		self.initGraph()