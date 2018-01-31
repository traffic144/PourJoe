import numpy as np

from .strategy import Strategy
from graph.flow import *

class PivotReposition(Strategy):

	def __init__(self, g):
		Strategy.__init__(self, g)
		self.title = "Pivot-Reposition"
		self.initGraph()

	# Determine the value of a sigle path

	def value(self, path):
		return sum([self.graph.weight[path[i]][path[i+1]] for i in range(len(path)-1)])

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
		self.dMin, _, _ = self.graph.shortestPath(self.graph.s, self.graph.t)
		self.dT, _, _ = self.graph.shortestPath(self.graph.t, self.graph.s)
		
		self.listMin = sorted([i for i in range(self.graph.n)], key = lambda x : self.dMin[x])

		self.wMin = self.dMin[self.graph.t]

	def gamma(self, v, k):
		inter = (self.graph.n-1)//2

		if(self.dT[v] >= self.wMin or self.dMin[v] >= self.wMin):
			return 0

		# Creation of the directed graphs
		dg1 = DirectedGraph(self.graph.n, self.graph.edges, self.graph.weight, self.graph.s, v)
		dg2 = DirectedGraph(self.graph.n, self.graph.edges, self.graph.weight, v, self.graph.t)

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
				H = max(H, min(self.h2(wTabSV[k+1], wTabVT[j], self.wMin, k+1, j), self.h3(wTabSV[k+1]/(k+1), wTabVT[j]/j, self.wMin, k)))
		if(M2 > k):
			for i in range(1, min(M1, k)+1):
				H = max(H, min(self.h1(wTabSV[i], self.wMin, i), self.h3(wTabSV[i]/i, wTabVT[k+1]/(k+1), self.wMin, k)))
		if(M1 > k and M2 > k):
			H = max(H, self.h3(wTabSV[k+1]/(k+1), wTabVT[k+1]/(k+1), self.wMin, k))
		return (H/k)

	def gammaMap(self, k):
		res = np.empty(self.graph.n)
		for i in range(self.graph.n):
			l = self.gamma(self.listMin[i], k)
			res[self.listMin[i]] = l
		return res


	def gammaGraph(self, k):
		g = max(self.gammaMap(k))