from drawer import *
from graphConstruct import *
from graph import Graph
from math import sqrt

import numpy as np
from delaunay2D import Delaunay2D

# Determine gamma function of k for a given graph

def gammaFunctionOfK(g, k1, k2):
	tab = []
	for i in range(k1, k2):
		g.k = i
		tab.append(max(g.gamma()))
	printCourb("gammaOfK", k1, k2, [tab], r'$k$', r'$\gamma$', r'Evolution de $\gamma$ fonction de $k$')

# Find the value of gamma for every node on a grid 

def gammaMapGrid(n, k, d):
	g = getGridGraph(n-1, n-1, k, d)

	gamma = g.gamma()

	printGrid("gammaMapGrid-"+str(n)+"-"+str(k)+"-"+str(d), n, 1, gamma.reshape((n, n)))
	print(g.t)

def gammaMapCompleteGrid(n, k, d):
	g = getCompleteGridGraph(n-1, n-1, k, d)

	gamma = g.gamma()
	gamma[g.s] = 0
	gamma[g.t] = 0
	gammaZ = [[gamma[i*n + j] for j in range(n)] for i in range(n)]

	printGrid("gammaMapCompleteGrid-"+str(n)+"-"+str(k)+"-"+str(d), n, 1, gammaZ)
# Find the value of gamma function of p, for random graph for which p is 
# the probability to have an edge between two nodes

def gammaRandomGraph(n, k, nbTest, nbProba):
	delta = 1/float(nbProba)
	resultM = []
	resultP = []
	resultL = []
	for i in range(nbProba//5, nbProba):
		tab = []
		for j in range(nbTest):
			p = delta*i
			g = getErdosRenyi(n, p, k, 1, 4)
			tab.append(max(0, max(g.gamma())))
		m = mean(tab, nbTest)
		t = interval95(tab, nbTest)
		resultM.append(m)
		resultP.append(m+t)
		resultL.append(m-t)

	printCourb("gammaRandom", nbProba//5, nbProba, [resultM, resultP, resultL], r'$p$', r'$\gamma$', r'Evolution de $\gamma$ fonction de $p$')


def mean(tab, n):
	s = sum(tab)
	return (s/float(n))

def standardDeviation(tab, n):
	m = mean(tab, n)
	s = sum([(tab[i] - m)**2 for i in range(n)])
	return (sqrt(s/float(n)))

def interval95(tab, n):
	return 2*standardDeviation(tab, n)/sqrt(n)

def main():
	#gammaFunctionOfK(getDoubleNodeDisjointGraph(10, 10, 12), 2, 30)
	#gammaRandomGraph(20, 10, 100, 30)
	gammaMapCompleteGrid(25, 10, 2)

main()