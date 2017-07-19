import numpy as np
from flow import DirectedGraph
from math import floor
import time

np.seterr(all='raise', over='raise', divide='raise', under='raise', invalid='raise')

class Graph:

	def __init__(self, n):
		self.n = n
		self.m = 0

		self.edges = [[] for i in range(n)]
		self.weight = np.full((n, n), np.inf)

		self.s = 0;
		self.t = 0;

	def addEdge(self, i, j, w):
		self.edges[i].append(j)
		self.edges[j].append(i)

		self.weight[i, j] = w
		self.weight[j, i] = w
		
		self.m += 1

	def setSource(self, s):
		self.s = s

	def setSink(self, t):
		self.t = t

	# Find the shortest path between the source and the sink using the Dijktra's algorithm 
	# m : array representing all the nodes which are not visited yet
	# v : array representing the shortest distance between a node and the source
	# p : array representing the parents in the shortest path between s and the considered node
	# l : array representing the node sorting by distance to s

	def shortestPath(self, s):
		m = np.full(self.n, True, dtype=bool)
		v = np.full(self.n, np.inf)
		p = np.empty(self.n)
		l = np.zeros(self.n, dtype='i')

		v[s] = 0
		a = 0
		while(True in m):
			k = -1
			mi = np.inf
			for i in range(self.n):
				if(m[i] and mi > v[i]):
					k = i
					mi = v[i]
			for j in self.edges[k]:
				if(m[j] and v[j] > v[k] + self.weight[k][j]):
					v[j] = v[k] + self.weight[k][j]
					p[j] = k
			l[a] = k
			a += 1

			m[k] = False

		return (v, l)

	# Determine the value of a sigle path

	def value(self, path):
		return sum([self.weight[path[i]][path[i+1]] for i in range(len(path)-1)])

	# Determine the mean and the smaller value of a set of paths 

	def mean(self, paths, l):
		return sum([self.value(paths[j]) for j in range(l)])/float(l)

	# Calculus of all h functions

	def parabol(self, w, wMin, l):
		return 2*(l - w/wMin)

	def h1(self, wSVt, wMin, l1):
		return self.parabol(wSVt, wMin, l1)

	def h2(self, wSVt, wVTt, wMin, l1, l2):
		return self.parabol(wVTt, wMin, l2) - 2*wSVt/(l1*wMin)

	def h3(self, wSV, wVT, wMin, k):
		w1 = min(wSV, wVT)
		w2 = max(wSV, wVT)
		return (2*k+1)*(1-w2/wMin) - w1/wMin

	def H(self, wSVt, wVTt, wMin, l1, l2):
		return min(self.h1(wSVt, wMin, l1), self.h2(wSVt, wVTt, wMin, l1, l2))

	# Determination of gamma with the given algorithm and some temporals improvements

	def initGraph(self):
		self.dMin, self.listMin = self.shortestPath(self.s)
		self.dT = self.shortestPath(self.t)[0]
		self.wMin = self.dMin[self.t]

	def gamma(self, nj, k):
		v = self.listMin[nj]
		inter = (self.n-1)//2

		if(self.dT[v] >= self.wMin or self.dMin[v] >= self.wMin):
			return 0

		# Creation of the directed graphs
		dg1 = DirectedGraph(self.n, self.edges, self.weight, self.s, v)
		dg2 = DirectedGraph(self.n, self.edges, self.weight, v, self.t)

		# Number of edges disjoints paths between s and v, and v and t
		M1 = dg1.fordFulkerson()
		M2 = dg2.fordFulkerson()

		dSV = self.dMin[v]
		dVT = self.dT[v]

		b1 = min(M1, k+1)
		b2 = min(M2, k+1)

		wTabVT = [0]
		while(dg2.l < b2):
			dg2.minFlowStep()
			wTabVT.append(dg2.getCost())
		wTabSV = [0]
		while(dg1.l < b1):
			dg1.minFlowStep()
			wTabSV.append(dg1.getCost())

		H = 0
		for i in range(1, min(M1, k)+1):
			for j in range(1, min(M2, k)+1):
				H = max(H, min(self.h1(wTabSV[i], self.wMin, i), self.h2(wTabSV[i], wTabVT[j], self.wMin, i, j)))
		if(M1 > k):
			for j in range(1, min(M2, k)+1):
				H = max(H, min(self.h2(wTabSV[k+1], wTabVT[j], self.wMin, k+1, j), self.h3(wTabSV[k+1], wTabVT[j], self.wMin, k)))
		if(M2 > k):
			for i in range(1, min(M1, k)+1):
				H = max(H, min(self.h1(wTabSV[i], self.wMin, i), self.h3(wTabSV[i], wTabVT[k+1], self.wMin, k)))
		if(M1 > k and M2 > k):
			H = max(H, self.h3(wTabSV[k+1], wTabVT[k+1], self.wMin, k))
		return (H/k)

	def gammaGraph(self, k):
		g = 0
		for i in range(self.n):
			l = self.gamma(i, k)
			if(l > g):
				g = l
		return g