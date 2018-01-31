from drawer import *

from graph.grid import Grid
from graph.doubleWestphal import DoubleWestphal
from graph.erdosRenyi import ErdosRenyi
from graph.waxman import Waxman
from graph.delaunay import Delaunay

from strategy.strategy import Strategy
from strategy.pivotReposition import PivotReposition
from strategy.reposition import Reposition
from strategy.greedy import Greedy

from cost.cost import *
from cost.tools import *

import time

import numpy as np

# Map of gamma for a grid

def gammaGrid(n, d, k):
	g = Grid(n, n, d)
	s = PivotReposition(g)
	x = np.arange(0, n+1)
	y = np.arange(0, n+1)
	t1 = time.clock()
	z = s.gammaMap(k).reshape(n+1, n+1)
	t2 = time.clock()
	print("Total time : " + str(t2-t1))
	d = Drawer()
	d.addMap(x, y, z)
	d.addGrid(0, n, n+1, 0, n, n+1)
	d.addTitle(r'', r'', r'Map of the value of $\gamma$ for a grid $' + str(n) + r'x' + str(n) + r'$')
	d.save("grid")

def gammaCompleteGrid(n, d, k):
	g = Grid(n, n, d, 1.5)
	s = PivotReposition(g)
	x = np.arange(0, n+1)
	y = np.arange(0, n+1)
	t1 = time.clock()
	z = s.gammaMap(k).reshape(n+1, n+1)
	t2 = time.clock()
	print("Total time : " + str(t2-t1))
	d = Drawer()
	d.addMap(x, y, z)
	d.addGrid(0, n, n+1, 0, n, n+1)
	d.addTitle(r'', r'', r'Map of the value of $\gamma$ for a grid $' + str(n) + r'x' + str(n) + r'$')
	d.save("grid")

# Determine gamma function of k for a given graph

def gammaDoubleWestphalFunctionOfK(m1, m2, nbAlpha):
	x = np.arange(1, 2*(m1+m2))
	alpha = np.linspace(0.0, 0.5, num=nbAlpha)
	
	d = Drawer()
	for a in alpha:
		t1 = time.clock()
		g = DoubleWestphal(m1, m2, a)
		s = PivotReposition(g)
		y = []
		for j in x:
			y.append(s.gammaGraph(j))
		t2 = time.clock()
		print(str(a) + " : " + str(t2-t1))
		d.addCourb(x, y, r'$\alpha = ' + str(a) + r'$')
	d.addTitle(r'$\alpha$', r'$\gamma$', r'Evolution of $\gamma$ function of $\alpha$ for double westphal with $m_1 = ' + str(m1) + r'$ et $m_2 = ' + str(m2) + r'$')
	d.save("westphal")

def gammaGridFunctionOfK(n1, n2, di):
	n = np.arange(n1, n2, 2)
	x = np.arange(1, 10)

	d = Drawer()
	for i in n:
		t1 = time.clock()
		g = Grid(i, i, di)
		s = PivotReposition(g)
		y = []
		for j in x:
			y.append(s.gammaGraph(j))
		t2 = time.clock()
		print(str(i) + " : " + str(t2-t1))
		d.addCourb(x, y, r'$n = ' + str(i) + r'$')
	d.addTitle(r'$k$', r'$\gamma$', r'Evolution of $\gamma$ function of $k$ for grid of size $n\times n$')
	d.save("grid")

# Find the value of gamma function of p, for random graph for which p is 
# the probability to have an edge between two nodes

def erdosRenyiGammaProba(n, k, nbTest, nbProba):
	x = np.linspace(0.2, 1.0, num=nbProba)
	value = []
	for i in range(nbProba):
		p = x[i]
		tab = []
		t1 = time.clock()
		for j in range(nbTest):
			g = ErdosRenyi(n, p, 4)
			s = PivotReposition(g)
			tab.append(s.gammaGraph(k))
		t2 = time.clock()
		print(str(i) + " : " + str(t2-t1))
		value.append(tab)
	d = Drawer()
	d.addTitle(r'$p$', r'$\gamma$', r'Evolution of $\gamma$ for Erdos Renyi graphs with $n = ' + str(n) + r'$ et $k = ' + str(k) + r'$')
	d.addConfidenceCourb(x, value, nbTest)
	d.save("erdosRenyi")

# Generate random graph

def waxmanGenerator(n):
	g = Waxman(n)
	d = Drawer()
	d.addGraph(g.edges, g.x, g.y, g.n)
	d.save("waxman")

def delaunayGenerator(n):
	g = Delaunay(n)
	d = Drawer()
	d.addGraph(g.edges, g.x, g.y, g.n)
	d.save("delaunay")

# Proportion 

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
	d = Drawer()
	d.addTitle(r'$\alpha$', r'$p$', r'Proportion of connected Waxman graphs for $n = ' + str(n) + r'$')
	d.addCourb(alpha, y)
	d.save("waxman")

def waxmanRandomTest(n1, n2, step, nbTest, k):
	nVal = np.arange(n1, n2, step)
	value = []
	for j in range(nVal.size):
		tab = []
		t1 = time.clock()
		for i in range(nbTest):
			g = Waxman(nVal[j])
			s = PivotReposition(g)
			tab.append(s.gammaGraph(k))
		t2 = time.clock()
		value.append(tab)
		print(str(nVal[j]) + " : " + str(t2-t1))
	d = Drawer()
	d.addTitle(r'$n$', r'$\gamma$', r'Evolution of $\gamma$ for Delaunay graphs with $k = ' + str(k) + r'$')
	d.addConfidenceCourb(nVal, value, nbTest)
	d.save("waxman")

def delaunayRandomTest(n1, n2, step, nbTest, k):
	nVal = np.arange(n1, n2, step)
	value = []
	for j in range(nVal.size):
		tab = []
		t1 = time.clock()
		for i in range(nbTest):
			g = Delaunay(nVal[j])
			s = PivotReposition(g)
			tab.append(s.gammaGraph(k))
		t2 = time.clock()
		value.append(tab)
		print(str(nVal[j]) + " : " + str(t2-t1))
	d = Drawer()
	d.addTitle(r'$n$', r'$\gamma$', r'Evolution of $\gamma$ for Delaunay graphs with $k = ' + str(k) + r'$')
	d.addConfidenceCourb(nVal, value, nbTest)
	d.save("delaunay")

def compareStrategies(strategiesClass, graph, n, k1, k2, dk, nbTest):
	strategies = [s(graph) for s in strategiesClass]
	kVal = np.arange(k1, k2+1, dk, dtype=int)
	y = [[[] for _ in range(kVal.size)] for _ in range(n)]
	for l in range(kVal.size):
		k = kVal[l]
		t1 = time.clock()
		for j in range(nbTest):
			blocked = graph.getBlockedEdges(k)
			for i in range(n):
				strategies[i].reset()
				for a in range(k):
					strategies[i].setBlockedEdges(blocked[a][0], blocked[a][1])
				strategies[i].simulation()
				ratio = strategies[i].calculRatio()
				y[i][l].append(ratio)
		t2 = time.clock()
		print(str(kVal[l]) + " : " + str(t2-t1))
	d = Drawer()
	for i in range(n):
		d.addConfidenceCourb(kVal, np.array(y[i]), nbTest, strategies[i].getTitle())
	d.addCourb(kVal, 2*kVal+1, r'$2k+1$')
	d.addTitle(r'$k$', r'$c$', "Comparaison of competitive ratio for " + graph.getTitle())
	d.save("strategy")

def drawBlockedDelaunay(n, nb):
	g = Delaunay(n)
	s = Strategy(g)
	d = Drawer()
	d.addGraph(g.edges, g.x, g.y, g.n)
	b, cx, cy = g.getBlockedEdges(nb)
	for e in b:
		s.setBlockedEdges(e[0], e[1])
	d.addGraph(s.blocked, g.x, g.y, g.n, "#ff0000")
	for i in range(nb):
		d.addCircle(cx[i], cy[i], 5.0, "#0000ff")
	d.save("delaunay")

def getRatioStrategies(n, nb, nbGraph, nbTest):
	rr = []
	rg = []
	for j in range(nbGraph):
		t1 = time.clock()
		g = Delaunay(n)
		sr = Reposition(g)
		sg = Greedy(g)
		for _ in range(nbTest):
			sr.reset()
			sg.reset()
			b, _, _ = g.getBlockedEdges(nb)
			for e in b:
				sr.setBlockedEdges(e[0], e[1])
				sg.setBlockedEdges(e[0], e[1])
			sr.simulation()
			sg.simulation()
			rr.append(sr.calculRatio())
			rg.append(sg.calculRatio())
		t2 = time.clock()
		print(str(j) + " : " + str(t2-t1))
	print("Reposition : " + str(np.mean(rr)) + " - " + str(1.96*np.std(rr)/np.sqrt(nbTest*nbGraph)))
	print("Greedy : " + str(np.mean(rg)) + " - " + str(1.96*np.std(rg)/np.sqrt(nbTest*nbGraph)))

def optimalNodeDisjoint(f, n, x1, x2, nbVal):
	s = Set(n)
	p = Permutation(n)
	fac = factorial(n)
	bnds = [(0.0, 1.0)]*fac
	const = {'type':'eq', 'fun' : lambda x: np.dot(np.full(fac, 1.0), x) - 1, 'jac' : lambda x: np.full(fac, 1.0).transpose()}

	x = np.linspace(x1, x2, nbVal)
	y = np.empty(x.size)
	for j in range(x.size):
		t1 = time.clock()
		d = x[j]
		res, _ = minimum(lambda prob: costNodeDisjoint(f(d), [prob[i] for i in range(fac)], n, s, p), fac, bnds, const)
		y[j] = res
		t2 = time.clock()
		print(str(d) + " : " + str(t2-t1))
	dr = Drawer()
	dr.addCourb(x, y)
	dr.save("cost")

def singleOptimalNodeDisjoint(weight, n):
	s = Set(n)
	p = Permutation(n)
	fac = factorial(n)
	bnds = [(0.0, 1.0)]*fac
	const = {'type':'eq', 'fun' : lambda x: np.dot(np.full(fac, 1.0), x) - 1, 'jac' : lambda x: np.full(fac, 1.0).transpose()}
	res = minimum(lambda prob: costNodeDisjoint(weight, [prob[i] for i in range(fac)], n, s, p), fac, bnds, const)
	print(res)


def main():
	#gammaGrid(20, 2, 7)
	gammaCompleteGrid(20, 2, 7)
	#gammaDoubleWestphalFunctionOfK(12, 12, 6)
	#gammaGridFunctionOfK(12, 13, 2)
	#erdosRenyiGammaProba(20, 20, 100, 40)
	#waxmanGenerator(50)
	#delaunayGenerator(200)
	#waxmanConnected(20, 50, 2000)
	#waxmanRandomTest(30, 200, 2, 200, 12)
	#delaunayRandomTest(30, 40, 2, 200, 12)
	#compareStrategies([Greedy], DoubleWestphal(10, 10, 0.5), 1, 1, 18, 1, 1000)
	#getRatioStrategies(400, 20, 20, 100)
	#optimalNodeDisjoint(lambda d: [1.0, d], 2, 1.0, 2.0, 50)
	#singleOptimalNodeDisjoint([2.0, 1.0, 1.0], 3)
	


main()