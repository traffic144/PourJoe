import numpy as np
import time

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

	def shortestPath(self, s = None, t = None):
		marqued = np.full(self.n, True, dtype=bool)
		value = np.full(self.n, np.inf)
		pred = np.full(self.n, -1, dtype=int)

		if(s == None):
			s = self.s
		if(t == None):
			t = self.t

		value[s] = 0
		while(value[t] == np.inf):
			k = -1
			mi = np.inf
			for i in range(self.n):
				if(marqued[i] and mi > value[i]):
					k = i
					mi = value[i]
			for j in self.edges[k]:
				if(marqued[j] and value[j] > value[k] + self.weight[k][j]):
					value[j] = value[k] + self.weight[k][j]
					pred[j] = k

			marqued[k] = False

		path = [t]
		a = t
		while a != s:
			a = pred[a]
			path.append(a)
		path.reverse()

		return (value, marqued, path)