from drawer import *

from graph.grid import Grid
from graph.doubleWestphal import DoubleWestphal
from graph.erdosRenyi import ErdosRenyi
from graph.waxman import Waxman
from graph.delaunay import Delaunay

from strategy.strategy import Strategy
from strategy.reposition import Reposition
from strategy.greedy import Greedy

from cost.cost import *
from cost.tools import *

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
	#gammaDoubleWestphalFunctionOfK(12, 12, 6)
	#gammaGridFunctionOfK(12, 25, 2)
	#erdosRenyiGammaProba(20, 20, 100, 40)
	#waxmanGenerator(50)
	#delaunayGenerator(200)
	#waxmanConnected(20, 50, 2000)
	#waxmanRandomTest(30, 200, 2, 200, 12)
	#delaunayRandomTest(30, 200, 5, 200, 12)
	#compareStrategies([Reposition, Greedy], DoubleWestphal(10, 10, 0.5), 2, 1, 18, 1, 1000)
	#getRatioStrategies(400, 20, 20, 100)
	optimalNodeDisjoint(lambda d: [1.0, d], 2, 1.0, 2.0, 50)
	#singleOptimalNodeDisjoint([2.0, 1.0, 1.0], 3)
	


main()