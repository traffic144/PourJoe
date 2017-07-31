import numpy as np

from strategy import Strategy

class Reposition(Strategy):

	def __init__(self, g):
		Strategy.__init__(self, g)

	def shortestPath(self):
		m = np.full(self.g.n, True, dtype=bool)
		v = np.full(self.g.n, np.inf)
		p = np.full(self.g.n, -1, dtype=int)

		v[self.g.s] = 0
		a = 0
		while(v[self.g.t] == np.inf):
			k = -1
			mi = np.inf
			for i in range(self.g.n):
				if(m[i] and mi > v[i]):
					k = i
					mi = v[i]
			for j in self.g.edges[k]:
				if(m[j] and v[j] > v[k] + self.g.weight[k][j]):
					v[j] = v[k] + self.g.weight[k][j]
					p[j] = k
			a += 1

			m[k] = False

		path = [self.g.t]
		a = self.g.t
		length = 1
		while a != self.g.s:
			a = p[a]
			path.append(a)
			length += 1
		path.reverse()

		return path, length

	def simulation(self):
		while(self.traveler != self.g.t):
			path, n = self.shortestPath()
			i = 1
			while i < n:
				if(path[i] in self.g.edges[self.traveler]):
					self.travel(path[i])
					i += 1
				else:
					break
			if(i != n):
				i -= 1
				while i > 0:
					i -= 1
					self.travel(path[i])