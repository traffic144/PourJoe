from graph import Graph

def getGridGraph(n, m, k, d=1):
	g = Graph((n+1)*(m+1), k)

	for i in range(n):
		for j in range(m):
			g.addEdge(i*(m+1) + j, i*(m+1) + (j+1), 1)
			g.addEdge(i*(m+1) + j, (i+1)*(m+1) + j, 1)
	for i in range(n):
		g.addEdge(i*(m+1) + m, (i+1)*(m+1) + m, 1)
	for j in range(m):
		g.addEdge(n*(m+1) + j, n*(m+1) + (j+1), 1)
	g.setSource(d*(m+1) + d)
	g.setSink((n-d)*(m+1) + (n-d))

	return g

def getDoubleNodeDisjointGraph(m1, m2, k):
	g = Graph(m1 + m2 + 3, k)

	s = 0
	v = m1 + 1
	t = m1 + m2 + 2

	for i in range(1, v):
		g.addEdge(s, i, 100)
		g.addEdge(i, v, 1)
	for j in range(v+1, t):
		g.addEdge(v, j, 100)
		g.addEdge(j, t, 1)
	g.setSource(s)
	g.setSink(t)

	return g

