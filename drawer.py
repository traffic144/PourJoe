try:
	import matplotlib
	matplotlib.use('Agg')
except:
	pass

import matplotlib.pyplot as plt

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

import os

def nextFile(directory):
	tab = os.listdir('img/' + directory + '/')
	num = []
	for i in range(len(tab)):
		try:
			n = int(tab[i].split('.png')[0])
			num.append(n)
		except:
			pass
	j = 1
	while j in num:
		j+= 1
	res = ('img/' + directory + '/' + str(j) + '.png')
	print(res)
	return res

def printGrid(directory, x1, x2, dx, y1, y2, dy, z, namefile=None):

	y, x = np.mgrid[slice(x1, x2, dx), slice(y1, y2, dy)]

	levels = MaxNLocator(nbins=20).tick_values(z.min(), z.max())

	cmap = plt.get_cmap('summer')
	norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

	fig, ax1 = plt.subplots(nrows=1)

	cf = ax1.contourf(x, y, z, levels=levels, cmap=cmap)
	fig.colorbar(cf, ax=ax1)
	
	"""Pour tracer la grille superposee aux valeurs de gamma"""
	"""-----------------------------------------------------"""
	for j in range(x2-1):
		for l in range(x2-1):
			ax1.plot([j, j], [l, l+1], 'k-')
			ax1.plot([j, j+1], [l, l], 'k-')
	ax1.plot([x2-1, x2-1], [x2-2, x2-1], 'k-')
	ax1.plot([x2-2, x2-1], [x2-1, x2-1], 'k-')
	
	"""Labels plot"""
	"""-----------"""
	plt.xlabel("x")
	plt.ylabel("y")
	
	if(namefile):
		plt.savefig("img/" + directory + '/' + namefile + ".png")
	else:
		plt.savefig(nextFile(directory))
	
 
def printGridSameScale(directory, x1, x2, dx, y1, y2, dy, z, k, zmin, zmax, namefile=None):

	y, x = np.mgrid[slice(x1, x2, dx), slice(y1, y2, dy)]

	levels = MaxNLocator(nbins=20).tick_values(zmin, zmax)

	cmap = plt.get_cmap('YlOrRd')
	norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

	fig, ax1 = plt.subplots(nrows=1)

	cf = ax1.contourf(x, y, z, levels=levels, cmap=cmap)
	fig.colorbar(cf, ax=ax1)
	
	"""Pour tracer la grille superposee aux valeurs de gamma"""
	"""-----------------------------------------------------"""
	for j in range(x2-1):
		for l in range(x2-1):
			ax1.plot([j, j], [l, l+1], 'k-')
			ax1.plot([j, j+1], [l, l], 'k-')
	ax1.plot([x2-1, x2-1], [x2-2, x2-1], 'k-')
	ax1.plot([x2-2, x2-1], [x2-1, x2-1], 'k-')
	
	"""Labels plot"""
	"""-----------"""
	plt.xlabel("x")
	plt.ylabel("y")
	plt.title('Value of $\gamma$ for nodes in a ' + str(x2) + 'x' + str(x2) + ' grid with $k=$' + str(k))
     
	if(namefile):
		plt.savefig("img/" + directory + '/' + namefile + ".png")
	else:
		plt.savefig(nextFile(directory))

def printCourb(directory, x, y, name, n, xlabel="", ylabel="", title="", namefile=None):
	courbs = []
	for i in range(n):
		data, = plt.plot(x[i], y[i], label=name[i])
		courbs.append(data)
	plt.legend()
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	
	if(namefile):
		plt.savefig("img/" + directory + '/' + namefile + ".png")
	else:
		plt.savefig(nextFile(directory))

def printGraph(directory, edges, x, y, n, namefile=None):
	for i in range(n):
		for j in edges[i]:
			plt.plot([x[i], x[j]], [y[i], y[j]], 'k-')
	
	if(namefile):
		plt.savefig("img/" + directory + '/' + namefile + ".png")
	else:
		plt.savefig(nextFile(directory))