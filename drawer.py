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

	levels = MaxNLocator(nbins=71).tick_values(z.min(), z.max())

	cmap = plt.get_cmap('summer')
	norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

	fig, ax1 = plt.subplots(nrows=1)

	cf = ax1.contourf(x, y, z, levels=levels, cmap=cmap)
	fig.colorbar(cf, ax=ax1)

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