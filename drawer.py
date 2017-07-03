import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

def printGrid(namefile, n, dn, result):
	dx, dy = dn, dn

	y, x = np.mgrid[slice(0, n, dy), slice(0, n, dx)]
	z = np.array([np.array(result[i]) for i in range(n)])

	levels = MaxNLocator(nbins=20).tick_values(z.min(), z.max())

	cmap = plt.get_cmap('summer')
	norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

	fig, ax1 = plt.subplots(nrows=1)

	cf = ax1.contourf(x + dx/2., y + dy/2., z, levels=levels, cmap=cmap)
	fig.colorbar(cf, ax=ax1)

	plt.savefig("img/" + namefile + ".png")

def printCourb(namefile, x1, x2, result, xlabel = "", ylabel = "", title = ""):
	x = np.array([i for i in range(x1, x2)])

	for r in result:
		y = np.array(r)
		plt.plot(x, y)

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.savefig("img/" + namefile + ".png")