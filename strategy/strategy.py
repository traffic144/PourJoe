import numpy as np
import copy

from graph.graph import Graph

class Strategy:

	def __init__(self, g):
		self.initialGraph = g
		self.reset()
		self.title = ""

	def getTitle(self):
		return self.title

	def reset(self):
		self.g = copy.deepcopy(self.initialGraph)
		self.traveler = self.g.s
		self.blocked = [[] for i in range(self.g.n)]
		self.wPath = 0

	def setBlockedEdges(self, i, j):
		self.blocked[i].append(j)
		self.blocked[j].append(i)
		self.discoverEdges(self.g.s)

	def discoverEdges(self, v):
		for j in self.blocked[v]:
			self.g.removeEdge(v, j)

	def travel(self, v):
		if v in self.g.edges[self.traveler]:
			self.wPath += self.g.weight[v][self.traveler]
			self.traveler = v
			self.discoverEdges(v)
		else:
			print(self.traveler)
			print(v)
			raise NotImplementedError("Blem")

	def calculRatio(self):
		for i in range(self.g.n):
			for j in self.blocked[i]:
				self.g.removeEdge(i, j)
		wOpt = self.g.shortestPath()
		return self.wPath/wOpt

	def simulation(self):
		raise NotImplementedError("Should have implemented a simulation function")