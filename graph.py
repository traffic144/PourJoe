from flow import DirectedGraph
from math import floor

class Graph:

	def __init__(self, n, k):
		self.n = n
		self.m = 0

		self.E = [[] for i in range(n)]
		self.weight = [[float("inf")]*n for i in range(n)]

		self.s = 0;
		self.t = 0;

		self.k = k

	def addEdge(self, i, j, w):
		self.E[i].append((j, w))
		self.E[j].append((i, w))

		self.weight[i][j] = w
		self.weight[j][i] = w
		
		self.m += 1

	def setSource(self, s):
		self.s = s

	def setSink(self, t):
		self.t = t

	def exist(self, tab, n):
		for i in range(n):
			if(tab[i]):
				return True
		return False

	def shortestPath(self):
		m = [True]*self.n
		v = [float("inf")]*self.n
		p = [0]*self.n

		v[self.s] = 0
		while(self.exist(m, self.n)):
			k = -1
			mi = float("inf")
			for i in range(self.n):
				if(m[i] and mi > v[i]):
					k = i
					mi = v[i]
			for (j, w) in self.E[k]:
				if(m[j] and v[j] > v[k] + w):
					v[j] = v[k] + w
					p[j] = k
			m[k] = False

		path = [self.t]
		while(path[-1] != self.s):
			path.append(p[path[-1]])
		path.reverse()
		return path

	def value(self, path):
		w = 0
		for i in range(len(path) - 1):
			w += self.weight[path[i]][path[i+1]]
		return w

	def mean(self, paths, l):
		wTot = 0
		wMin = float("inf")
		for i in range(l):
			w = self.value(paths[i])
			if w < wMin:
				wMin = w
			wTot += w
		return (wTot/l, wMin)

	def h1(self, wSV, wMin, l1):
		return (2*l1*wSV/wMin + 2*(self.k-l1) + 1)

	def h21(self, w1, wVT, wMin, l2):
		return (2*w1/wMin + 2*l2*wVT/wMin + 2*(self.k-l2) + 1)

	def h22(self, wSV, wVT, wMin, l1, l2):
		return (2*l1*wSV/wMin + 2*l2*wVT/wMin + 2*(self.k-l2-l1+1) + 1)

	def H(self, w1, wSV, wVT, l1, l2, wMin):
		return max(self.h1(wSV, wMin, l1), self.h21(w1, wVT, wMin, l2), self.h22(wSV, wVT, wMin, l1, l2))

	def gamma(self):
		Hmin = [float("inf")]*self.n
		wMin = float(self.value(self.shortestPath()))
		for i in range(self.n):
			if(i != self.s and i != self.t):
				dg1 = DirectedGraph(self.n, self.E, self.s, i)
				dg2 = DirectedGraph(self.n, self.E, i, self.t)
				M1 = dg1.fordFulkerson()
				M2 = dg2.fordFulkerson()
				w1 = [0]*M1
				wSV = [0]*M1
				wVT = [0]*M2
				for l1 in range(1, M1+1):
					dg1.minFlowStep()
					paths = dg1.getEdgeDisjointPaths()
					(wSV[l1-1], w1[l1-1]) = self.mean(paths, l1)
				for l2 in range(1, M2+1):
					dg2.minFlowStep()
					paths = dg2.getEdgeDisjointPaths()
					(wVT[l2-1], a) = self.mean(paths, l2)
				for l1 in range(1, M1+1):
					for l2 in range(1, M2+1):
						Hinter = self.H(w1[l1-1], wSV[l1-1], wVT[l2-1], l1, l2, wMin)
						if(Hinter < Hmin[i]):
							Hmin[i] = Hinter
		gamma = [(2*self.k+1 - Hmin[i])/self.k for i in range(self.n)]
		return gamma