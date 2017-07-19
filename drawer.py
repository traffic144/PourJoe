try:
	import matplotlib
	matplotlib.use('Agg')
except:
	pass

import matplotlib.pyplot as plt

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

def printGrid(namefile, x1, x2, dx, y1, y2, dy, z):

	y, x = np.mgrid[slice(x1, x2, dx), slice(y1, y2, dy)]

	levels = MaxNLocator(nbins=20).tick_values(z.min(), z.max())

	cmap = plt.get_cmap('summer')
	norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

	fig, ax1 = plt.subplots(nrows=1)

	cf = ax1.contourf(x, y, z, levels=levels, cmap=cmap)
	fig.colorbar(cf, ax=ax1)
	
	"""Pour tracer la grille superposée aux valeurs de gamma"""
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
	
	plt.savefig("img/" + namefile + ".png")
 
def printGridSameScale(namefile, x1, x2, dx, y1, y2, dy, z, k, zmin, zmax):

	y, x = np.mgrid[slice(x1, x2, dx), slice(y1, y2, dy)]

	levels = MaxNLocator(nbins=20).tick_values(zmin, zmax)

	cmap = plt.get_cmap('YlOrRd')
	norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

	fig, ax1 = plt.subplots(nrows=1)

	cf = ax1.contourf(x, y, z, levels=levels, cmap=cmap)
	fig.colorbar(cf, ax=ax1)
	
	"""Pour tracer la grille superposée aux valeurs de gamma"""
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
     
	plt.savefig("img/" + namefile + ".png")

def printCourb(namefile, x, y, name, n, xlabel="", ylabel="", title=""):
	courbs = []
	for i in range(n):
		data, = plt.plot(x[i], y[i], label=name[i])
		courbs.append(data)
	plt.legend()
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.savefig("img/" + namefile + ".png")