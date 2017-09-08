import numpy as np
from scipy.optimize import minimize

import itertools as it

# minimum take in argument a cost function, the number a free variables, and a dictionary of the constraint on the variables
# return the value of the cost function and the optimum variables

nbTest = 50
nbIteration = 10

def minimum(f, n, bnds, cons):
	val = np.inf
	proba = []
	for i in range(nbTest):
		x = [np.random.random_sample() for _ in range(n)]
		fun = 0
		for j in range(nbIteration):
			res = minimize(f, x, method="SLSQP" , bounds=bnds, constraints=cons)
			x = res.x
			fun = res.fun
		if val > fun:
			val = fun
			proba = x
	return (val, proba)

# Factorial function : needed for the permutations

def factorial(n):
	p = 1
	for i in range(n):
		p *= i+1
	return p

# Class enumerating the subsets of [0, n-1]

class Set():

	def __init__(self, n):
		self._n = n
		self._list = []
		tab = [i for i in range(n)]
		for k in range(n):
			self._list += it.combinations(tab, k)

	def __iter__(self):
		for l in self._list:
			yield l

# Class enumerating the permutations of [0, n-1]

class Permutation():

	def __init__(self, n):
		self._n = n
		tab = [i for i in range(n)]
		self._list = list(it.permutations(tab))

	def __iter__(self):
		for l in self._list:
			yield l