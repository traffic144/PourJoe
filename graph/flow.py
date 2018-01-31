import numpy as np
np.set_printoptions(threshold=np.nan)

import time

class DirectedGraph():

	def __init__(self, n, edges, weight, s, t):
		self.n = n

		self.edges = edges
		self.weight = weight

		self.s = s
		self.t = t

		self.l = 0
		self.w = 0

		self.x = np.full((n, n), False, dtype=bool)
		self.pi = np.zeros(n)
		self.reduced = np.copy(weight)

	def resetFlow(self):
		self.x = np.full((self.n, self.n), False, dtype=bool)
		self.w = 0

	# Find a path from the source to the sink in the residual graph
	# stack : stack of the node which have to be visited
	# m : array representing the node already visited
	# p : array representing the parents
	# The function is using a depth-first searchy

	def findPath(self):
		stack = [self.s]
		marqued = np.full(self.n, False, dtype=bool)
		tagged = np.full(self.n, False, dtype=bool)
		tagged[self.s] = True

		p = np.full(self.n, -1)

		while(stack != []):
			k = stack.pop()
			if(marqued[k]):
				continue
			else:
				for j in self.edges[k]:
					if(not(tagged[j]) and (not(self.x[k, j]) or self.x[j, k])):
						p[j] = k
						if(j == self.t):
							return (p, True)
						else:
							stack.append(j)
							tagged[j] = True
				marqued[k] = True
		return ([], False)

	# Implementation of the Ford-Fulkerson algorithm to find the maximum flow.
	# We suppose every capacity is equal to 1

	def fordFulkerson(self):
		self.resetFlow()
		(p, b) = self.findPath()
		while(b):
			self.updateFlow(p, self.s, self.t)
			(p, b) = self.findPath()
		res = sum(self.x[self.s])
		self.resetFlow()
		return res

	# Implementation of Dijktra in the case of residual flow with nonnegative cost

	def dijktra(self, a):
		d = np.full(self.n, np.inf)
		d[a] = 0

		p = np.empty(self.n)
		marqued = np.full(self.n, True, dtype=bool)
		while(True):
			dmin = np.inf
			k = -1
			for i in range(self.n):
				if(marqued[i] and d[i] < dmin):
					dmin = d[i]
					k = i
			if(k == -1):
				return (d, p)
			else:
				for j in self.edges[k]:
					w = self.reduced[k, j]
					if(marqued[j] and self.x[j, k] and d[j] > d[k]):
						d[j] = d[k]
						p[j] = k
					elif(marqued[j] and not(self.x[k, j]) and d[j] > d[k] + w):
						d[j] = d[k] + w
						p[j] = k
				marqued[k] = False

	# Update the flow for a given path, knowing the capacity is 1, the new flow is 1 and every edge (a, b) as a contrary edge (b, a)

	def updateFlow(self, p, a, b):
		k = b
		while(k != a):
			if(self.x[k, int(p[k])]):
				self.x[k, int(p[k])] = False
			else:
				self.x[int(p[k]), k] = True
			k = int(p[k])

	def updateFlowCost(self, p, a, b):
		k = b
		while(k != a):
			if(self.x[k, int(p[k])]):
				self.x[k, int(p[k])] = False
				self.w -= self.weight[k, int(p[k])]
			else:
				self.x[int(p[k]), k] = True
				self.w += self.weight[int(p[k]), k]
			k = int(p[k])

	def updateCost(self, d):
		self.pi = self.pi - d
		for i in range(self.n):
			for j in self.edges[i]:
				if(self.x[i, j]):
					self.reduced[i, j] = 0
				else:
					self.reduced[i, j] = self.weight[i, j] - self.pi[i] + self.pi[j]

	# Given a min cost flow where every node are transfert nodes except
	# for the source which provide (l-1) and the sink which provide (l-1)
	# we find a min cost flow with the same properties except the source provide
	# l and the sink demand l

	def minFlowStep(self):
		(d, p) = self.dijktra(self.s)
		self.updateCost(d)
		self.updateFlowCost(p, self.s, self.t)
		self.l += 1


	# Given a min cost flow from the precedent function, we get l edge-disjoint
	# paths from the source to the sink

	def getEdgeDisjointPaths(self):
		m = np.full((self.n, self.n), False, dtype=bool)
		paths = [[] for i in range(self.l)]

		for k in range(self.l):
			a = self.s
			paths[k].append(a)
			while(a != self.t):
				for j in self.edges[a]:
					if(self.x[a, j] == 1 and not(m[a, j])):
						paths[k].append(j)
						m[a, j] = True
						a = j
						break
		return paths

	def getCost(self):
		return self.w