from tools import *

def costNodeDisjoint(weight, probas, n, sets, permutations):
	tab = []
	for s in sets:
		opt = np.inf
		for j in range(n):
			if(not(j in s)):
				opt = min(opt, weight[j])
		c = 0
		i = 0
		for p in permutations:
			w = 0
			j = 0
			while j < n and p[j] in s:
				w += 2*weight[p[j]]
				j += 1
			w += weight[p[j]]
			c += w*probas[i]
			i += 1
		c = (c/opt) - len(s)
		tab.append(c)
	return max(tab)
