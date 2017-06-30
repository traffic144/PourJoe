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

	def fordFulkerson(self):
		self.resetFlow()
		p = self.findPath()
		while(p[self.t] != -1):
			self.updateFlow(p, self.s, self.t)
			p = self.findPath()
		res = sum(self.x[self.s])
		self.resetFlow()
		return res

	def bellmanFord(self, a):
		d = [float("inf")]*self.n
		d[a] = 0

		p = [-1]*self.n
		for i in range(self.n):
			s = -1
			for v1 in range(self.n):
				for v2, w in self.edges[v1]:
					if(self.x[v1][v2] == 1):
						if(d[v1] > d[v2] - w):
							d[v1] = d[v2] - w
							p[v1] = v2
							s = v1
					else:
						if(d[v2] > d[v1] + w):
							d[v2] = d[v1] + w
							p[v2] = v1
							s = v2
		return (p, s)			

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

	def minFlowStep(self):
		(p, a) = self.bellmanFord(self.s)
		self.updateFlow(p, self.s, self.t)
		self.l += 1

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