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
		self.graph = copy.deepcopy(self.initialGraph)
		self.traveler = self.graph.s
		self.blocked = [[] for i in range(self.graph.n)]
		self.wPath = 0

	def setBlockedEdges(self, i, j):
		self.blocked[i].append(j)
		self.blocked[j].append(i)
		self.discoverEdges(self.graph.s)

	def discoverEdges(self, v):
		for j in self.blocked[v]:
			self.graph.removeEdge(v, j)

	def travel(self, v):
		if v in self.graph.edges[self.traveler]:
			self.wPath += self.graph.weight[v][self.traveler]
			self.traveler = v
			self.discoverEdges(v)
		else:
			print(self.traveler)
			print(v)
			raise NotImplementedError("Blem")

	def calculRatio(self):
		for i in range(self.graph.n):
			for j in self.blocked[i]:
				self.graph.removeEdge(i, j)
		value, _, _ = self.graph.shortestPath()
		wOpt = value[self.graph.t]
		return self.wPath/wOpt

	def simulation(self):
		raise NotImplementedError("Should have implemented a simulation function")