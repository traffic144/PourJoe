import numpy as np
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
	# The function is using a depth-first search

	def findPath(self):
		stack = [self.s]
		m = np.full(self.n, False, dtype=bool)
		p = np.empty(self.n)

		while(stack != [] and stack[-1] != self.t):
			k = stack.pop()
			if(m[k]):
				continue
			else:
				stack.append(k)
				for j in self.edges[k]:
					if(not(m[j]) and (not(self.x[k, j]) or self.x[j, k])):
						stack.append(j)
						p[j] = k
				m[k] = True
		if(stack == []):
			return ([], False)
		else:
			return (p, True)

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

	# Implementation of the Bellman-Ford algorithm to find the smaller distance between "a" and the others when it exists negative weights

	def bellmanFord(self, a):
		d = np.full(self.n, np.inf)
		d[a] = 0

		p = np.empty(self.n)
		for i in range(self.n):
			for v1 in range(self.n):
				for v2 in self.edges[v1]:
					w = self.weight[v1, v2]
					print(w)
					if(self.x[v1, v2]):
						if(d[v1] > d[v2] - w):
							d[v1] = d[v2] - w
							p[v1] = v2
					else:
						if(d[v2] > d[v1] + w):
							d[v2] = d[v1] + w
							p[v2] = v1
		return p

	# Update the flow for a given path, knowing the capacity is 1, the new flow is 1 and every edge (a, b) as a contrary edge (b, a)

	def updateFlow(self, p, a, b):
		k = b
		while(k != a):
			if(self.x[k, p[k]]):
				self.x[k, p[k]] = False
			else:
				self.x[p[k], k] = True
			k = p[k]

	def updateFlowCost(self, p, a, b):
		k = b
		while(k != a):
			if(self.x[k, p[k]]):
				self.x[k, p[k]] = False
				print(str(self.w) + " - " + str(self.weight[k, p[k]]))
				self.w -= self.weight[k, p[k]]
			else:
				self.x[p[k], k] = True
				self.w += self.weight[p[k], k]
			k = p[k]

	# Given a min cost flow where every node are transfert nodes except
	# for the source which provide (l-1) and the sink which provide (l-1)
	# we find a min cost flow with the same properties except the source provide
	# l and the sink demand l

	def minFlowStep(self):
		p = self.bellmanFord(self.s)
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