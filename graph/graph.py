import numpy as np
import time

from flow import DirectedGraph

class Graph:

	def __init__(self, n):
		self.n = n
		self.m = 0

		self.edges = [[] for i in range(n)]
		self.weight = np.full((n, n), np.inf)

		self.s = 0;
		self.t = 0;

	def getTitle(self):
		return self.title

	def addEdge(self, i, j, w):
		self.edges[i].append(j)
		self.edges[j].append(i)

		self.weight[i, j] = w
		self.weight[j, i] = w
		
		self.m += 1

	def removeEdge(self, i, j):
		if i in self.edges[j]:
			self.edges[i].remove(j)
			self.edges[j].remove(i)

			self.weight[i, j] = np.inf
			self.weight[j, i] = np.inf

			self.m -= 1

	def setSource(self, s):
		self.s = s

	def setSink(self, t):
		self.t = t

	def shortestPath(self):
		m = np.full(self.n, True, dtype=bool)
		v = np.full(self.n, np.inf)

		v[self.s] = 0
		a = 0
		while(v[self.t] == np.inf):
			k = -1
			mi = np.inf
			for i in range(self.n):
				if(m[i] and mi > v[i]):
					k = i
					mi = v[i]
			for j in self.edges[k]:
				if(m[j] and v[j] > v[k] + self.weight[k][j]):
					v[j] = v[k] + self.weight[k][j]
			a += 1

			m[k] = False

		return v[self.t]