import numpy as np
from flow import DirectedGraph
from math import floor
import time

np.seterr(all='raise', over='raise', divide='raise', under='raise', invalid='raise')

class Graph:

	def __init__(self, n, k):
		self.n = n
		self.m = 0

		self.edges = [[] for i in range(n)]
		self.weight = np.full((n, n), np.inf)

		self.s = 0;
		self.t = 0;

		self.k = k

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
		return (2*l*(w/float(wMin) - 1))

	def h1(self, wSV, wMin, l1):
		return (2*self.k + 1 + self.parabol(wSV, wMin, l1))

	def h2(self, wSV, wVT, wMin, l2):
		return (2*self.k + 1 + self.parabol(wVT, wMin, l2) + 2*wSV/float(wMin))

	def h3(self, wSV, wVT, wMin):
		return (wSV + wVT + 2*self.k*max(wSV, wVT))/float(wMin)

	def H(self, wSV, wVT, wMin, l1, l2):
		return max(self.h1(wSV, wMin, l1), self.h2(wSV, wVT, wMin, l2), self.h3(wSV, wVT, wMin))

	# Determination of gamma with the given algorithm and some temporals improvements

	def gamma(self):
		Hmin = np.full(self.n, np.inf)
		Hmin[self.s] = 2*self.k + 1
		Hmin[self.t] = 2*self.k + 1

		(dMin, listMin) = self.shortestPath(self.s)
		(dT, listT) = self.shortestPath(self.t)
		wMin = dMin[self.t]

		i = 0
		while (i < self.n and dMin[listMin[i]] < wMin):
			if(dT[listMin[i]] < wMin):
				v = listMin[i]
				#Creation of the directed graphs
				dg1 = DirectedGraph(self.n, self.edges, self.weight, self.s, v)
				dg2 = DirectedGraph(self.n, self.edges, self.weight, v, self.t)

				M1 = dg1.fordFulkerson()
				M2 = dg2.fordFulkerson()

				if(M1 > self.k and M2 > self.k):
					print("lol")
				else:
					M1 = min(M1, self.k)
					M2 = min(M2, self.k)
					w1 = dMin[v]
					wVTp = 0
					wVTs = 0
					l2 = 0
					while ((wVTs - wVTp < wMin) and (l2 < M2)):
						dg2.minFlowStep()
						wVTp = wVTs
						wVTs = dg2.getCost()
						l2 += 1
					wVt = 0
					if(l2 == M2):
						wVT = wVTs/float(l2)
					else:
						l2 -= 1
						wVT = wVTp/float(l2)
					if(self.h2(w1, wVT, wMin, l2) < 2*self.k+1):
						wSVp = 0
						wSVs = 0
						l1 = 0
						while(l1 == 0 or (wSVs - wSVp < wMin and self.h1(wSVs/float(l1), wMin, l1) > self.h2(wSVs/float(l1), wVT, wMin, l2) and l1 < M1)):
							dg1.minFlowStep()
							wSVp = wSVs
							wSVs = dg1.getCost()
							l1 += 1
						wSV = 0
						if(wSVs - wSVp >= wMin):
							l1 -= 1
							wSV = wSVp/float(l1)
						else:
							if(self.h1(wSVs/float(l1), wMin, l1) <= self.h2(wSVs/float(l1), wVT, wMin, l2)):
								if(l1 != 1 and self.h1(wSVp/float(l1), wMin, l1) <= self.h2(wSVs/float(l1), wVT, wMin, l2)):
									l1 -= 1
									wSV = wSVp/float(l1)
								else:
									wSV = wSVs/float(l1)
							else:
								wSV = wSVs/float(l1)
						Hmin[v] = self.H(wSV, wVT, wMin, l1, l2)
			i += 1
		gamma = np.maximum(((2*self.k+1) - Hmin)/float(self.k), 0)
		print(gamma)
		return gamma