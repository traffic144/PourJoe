class DirectedGraph():

	def __init__(self, n, E, s, t):
		self.n = n

		self.edges = E

		self.s = s
		self.t = t

		self.l = 0

		self.x = [[0]*n for i in range(n)]

	def resetFlow(self):
		self.x = [[0]*self.n for i in range(self.n)]

	# Find a path from the source to the sink in the residual graph
	# stack : stack of the node which have to be visited
	# m : array representing the node already visited
	# p : array representing the parents
	# The function is using a depth-first search

	def findPath(self):
		stack = [self.s]
		m = [False]*self.n
		p = [-1]*self.n

		while(stack != [] and stack[-1] != self.t):
			k = stack.pop()
			if(m[k]):
				continue
			else:
				stack.append(k)
				for j, w in self.edges[k]:
					if(not(m[j]) and (self.x[k][j] == 0 or self.x[j][k] == 1)):
						stack.append(j)
						p[j] = k
				m[k] = True
		return p

	# Implementation of the Ford-Fulkerson algorithm to find the maximum flow.
	# We suppose every capacity is equal to 1

	def fordFulkerson(self):
		self.resetFlow()
		p = self.findPath()
		while(p[self.t] != -1):
			self.updateFlow(p, self.s, self.t)
			p = self.findPath()
		res = sum(self.x[self.s])
		self.resetFlow()
		return res

	# Implementation of the Bellman-Ford algorithm to find the smaller distance between "a" and the others when it exists negative weights

	def bellmanFord(self, a):
		d = [float("inf")]*self.n
		d[a] = 0

		p = [-1]*self.n
		for i in range(self.n):
			for v1 in range(self.n):
				for v2, w in self.edges[v1]:
					if(self.x[v1][v2] == 1):
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
		if(self.x[k][p[k]] == 1):
			self.x[k][p[k]] = 0
		else:
			self.x[p[k]][k] = 1
		k = p[k]
		while(k != a):
			if(self.x[k][p[k]] == 1):
				self.x[k][p[k]] = 0
			else:
				self.x[p[k]][k] = 1
			k = p[k]

	# Given a min cost flow where every node are transfert nodes except
	# for the source which provide (l-1) and the sink which provide (l-1)
	# we find a min cost flow with the same properties except the source provide
	# l and the sink demand l

	def minFlowStep(self):
		p = self.bellmanFord(self.s)
		self.updateFlow(p, self.s, self.t)
		self.l += 1

	# Given a min cost flow from the precedent function, we get l edge-disjoint
	# paths from the source to the sink

	def getEdgeDisjointPaths(self):
		m = [[False]*self.n for i in range(self.n)]
		paths = [[] for i in range(self.l)]

		for k in range(self.l):
			a = self.s
			paths[k].append(a)
			while(a != self.t):
				for j, w in self.edges[a]:
					if(self.x[a][j] == 1 and not(m[a][j])):
						paths[k].append(j)
						m[a][j] = True
						a = j
						break
		return paths