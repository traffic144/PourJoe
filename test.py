from drawer import *
from graphConstruct import *
from graph import Graph

def gammaFunctionOfK(g, k1, k2):
	tab = []
	for i in range(k1, k2):
		g.k = i
		tab.append(max(g.gamma()))
	printCourb("gammaOfK", k1, k2, tab)

def gammaMapGrid(n, k, d):
	g = getGridGraph(n-1, n-1, k, 3)

	gamma = g.gamma()
	gamma[g.s] = 0
	gamma[g.t] = 0
	gammaZ = [[gamma[i*n + j] for j in range(n)] for i in range(n)]

	printGrid("gammaMapGrid-"+str(n)+"-"+str(k)+"-"+str(d), n, 1, gammaZ)

def main():
	gammaFunctionOfK(getDoubleNodeDisjointGraph(10, 10, 5), 2, 30)
	gammaMapGrid(13, 12, 2)

main()