import numpy as np

from .strategy import Strategy

class Greedy(Strategy):

	def __init__(self, g):
		Strategy.__init__(self, g)
		self.title = "Greedy"

	def simulation(self):
		while(self.traveler != self.graph.t):
			_, _, path = self.graph.shortestPath(self.traveler)
			i = 1
			while i < len(path):
				if(path[i] in self.graph.edges[self.traveler]):
					self.travel(path[i])
					i += 1
				else:
					break