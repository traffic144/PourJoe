from drawer import *

from graph.grid import Grid
from graph.doubleWestphal import DoubleWestphal
from graph.erdosRenyi import ErdosRenyi
from graph.waxman import Waxman
from graph.delaunay import Delaunay

import time

import numpy as np

# Determine gamma function of k for a given graph

def gammaDoubleWestphalFunctionOfK(m1, m2, nbAlpha):
	xtab = []
	ytab = []
	alpha = np.linspace(0.0, 0.5, num=nbAlpha)
	for i in alpha:
		g = DoubleWestphal(m1, m2, i)
		g.initGraph()
		x = np.arange(1, 2*(m1+m2))
		y = []
		for j in x:
			y.append(g.gammaGraph(j))
		xtab.append(x)
		ytab.append(y)
	title = r'Evolution of $\gamma$ function of $k$ for double Westphal graph ($m_1 = ' + str(m1) + r'$, $m_2 = ' + str(m2) + r'$)'
	label = [r'$\alpha = ' + str(i) + r'$' for i in alpha]
	printCourb("gammaK", xtab, ytab, label, nbAlpha, r'$k$', r'$\gamma$', title)

def gammaGridFunctionOfK(n1, n2, d):
	xtab = []
	ytab = []
	n = np.arange(n1, n2, 2)
	for i in n:
		t1 = time.clock()
		g = Grid(i, i, d)
		g.initGraph()
		x = np.arange(1, 10)
		y = []
		for j in x:
			y.append(g.gammaGraph(j))
		xtab.append(x)
		ytab.append(y)
		t2 = time.clock()
		print(str(i) + " : " + str(t2-t1))
	title = r'Evolution of $\gamma$ function of $k$ for grid of size $n\times n$'
	label = [r'$n = ' + str(i) + r'$' for i in n]
	printCourb("gammaK", xtab, ytab, label, n.size, r'$k$', r'$\gamma$', title)

# Find the value of gamma function of p, for random graph for which p is 
# the probability to have an edge between two nodes

def erdosRenyiGammaProba(n, k, nbTest, nbProba):
	x = np.linspace(0.2, 1.0, num=nbProba)
	y = np.empty(nbProba)
	yu = np.empty(nbProba)
	yb = np.empty(nbProba)
	for i in range(nbProba):
		p = x[i]
		tab = np.empty(nbTest)
		t1 = time.clock()
		for j in range(nbTest):
			g = ErdosRenyi(n, p, 4)
			tab[j] = g.gammaGraph(k)
		m = np.mean(tab)
		t = interval95(tab, nbTest, m)
		y[i] = m
		yu[i] = m + t
		yb[i] = m - t
		t2 = time.clock()
		print(str(i) + " : " + str(t2-t1))
	title = r'Evolution of $\gamma$ for Erdos Renyi graphs with $n = ' + str(n) + r'$ et $k = ' + str(k) + r'$'
	printCourb("gammaRandom", [x, x, x], [y, yu, yb], ["Mean Value", "CI+", "CI-"], 3, r'$p$', r'$\gamma$', title)

def waxmanGenerator(n):
	g = Waxman(n)
	printGraph("waxman", g.edges, g.x, g.y, g.n)

def delaunayGenerator(n):
	g = Delaunay(n)
	printGraph("delaunay", g.edges, g.x, g.y, g.n)

def waxmanConnected(n, nbAlpha, nbTest):
	alpha = np.linspace(0.5, 3.0, num=nbAlpha)
	y = np.empty(nbAlpha)
	for j in range(nbAlpha):
		s = 0
		a = alpha[j]
		t1 = time.clock()
		for i in range(nbTest):
			try:
				g = Waxman(n, alpha=a)
				s+=1
			except:
				pass
		y[j] = s*100.0/nbTest
		t2 = time.clock()
		print(str(j) + " : " + str(t2-t1))
	title = r'Proportion of connected Waxman graphs for $n = ' + str(n) + r'$'
	printCourb("waxman", [alpha], [y], ["proportion"], 1, r'$\alpha$', r'$p$', title)

def waxmanRandomTest(n1, n2, step, nbTest, k):
	nVal = np.arange(n1, n2, step)
	y = np.empty(nVal.size)
	yu = np.empty(nVal.size)
	yb = np.empty(nVal.size)
	for j in range(nVal.size):
		tab = []
		t1 = time.clock()
		for i in range(nbTest):
			try:
				g = Waxman(nVal[j])
				tab.append(g.gammaGraph(k))
			except:
				pass
		m = np.mean(tab)
		t = interval95(tab, len(tab), m)
		y[j] = m
		yu[j] = m + t
		yb[j] = m - t
		t2 = time.clock()
		print(str(nVal[j]) + " : " + str(t2-t1))
	title = r'Evolution of $\gamma$ for Waxman graphs with $k = ' + str(k) + r'$'
	printCourb("waxman", [nVal, nVal, nVal], [y, yu, yb], ["Mean Value", "CI+", "CI-"], 3, r'$n$', r'$\gamma$', title)

def delaunayRandomTest(n1, n2, step, nbTest, k):
	nVal = np.arange(n1, n2, step)
	y = np.empty(nVal.size)
	yu = np.empty(nVal.size)
	yb = np.empty(nVal.size)
	for j in range(nVal.size):
		tab = []
		t1 = time.clock()
		for i in range(nbTest):
			g = Delaunay(nVal[j])
			tab.append(g.gammaGraph(k))
		m = np.mean(tab)
		t = interval95(tab, len(tab), m)
		y[j] = m
		yu[j] = m + t
		yb[j] = m - t
		t2 = time.clock()
		print(str(nVal[j]) + " : " + str(t2-t1))
	title = r'Evolution of $\gamma$ for Delaunay graphs with $k = ' + str(k) + r'$'
	printCourb("delaunay", [nVal, nVal, nVal], [y, yu, yb], ["Mean Value", "CI+", "CI-"], 3, r'$n$', r'$\gamma$', title)

def standardDeviation(tab, m):
	return np.sqrt(np.sum(np.square(tab - m)))

def interval95(tab, n, m):
	return 2*standardDeviation(tab, m)/np.sqrt(n)

def main():
	#gammaDoubleWestphalFunctionOfK(12, 12, 6)
	gammaGridFunctionOfK(12, 25, 2)
	#erdosRenyiGammaProba(20, 20, 100, 40)
	#waxmanGenerator(50)
	#delaunayGenerator(200)
	#waxmanConnected(20, 50, 2000)
	#waxmanRandomTest(30, 200, 2, 200, 12)
	#delaunayRandomTest(30, 200, 5, 200, 12)

main()