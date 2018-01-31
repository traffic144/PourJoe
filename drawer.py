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

class Drawer():

	def __init__(self):
		self.figure = plt.figure()
		self.ax = self.figure.add_subplot(1, 1, 1)

	def nextFile(self, directory):
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
		return res

	def addConfidenceCourb(self, x, val, nbValue, label=" "):
		y = np.mean(val, axis=1)
		t = 1.96*np.std(val, axis=1)/np.sqrt(nbValue)
		self.ax.errorbar(x, y, yerr=t, label=label)

	def addMeanCourb(self, x, val, label=" "):
		y = np.mean(val, axis=1)
		self.ax.plot(x, y, label=label)

	def addCourb(self, x, val, label=" "):
		self.ax.plot(x, val, label=label)

	def addGrid(self, x1, x2, nx, y1, y2, ny):
		x, dx = np.linspace(x1, x2, num=nx, retstep=True)
		y, dy = np.linspace(y1, y2, num=ny, retstep=True)
		for j in x:
			for l in y:
				if l < y2:
					self.ax.plot([j, j], [l, l+dy], color='#aaaaaa', linewidth=1)
				if j < x2:
					self.ax.plot([j, j+dx], [l, l], color='#aaaaaa', linewidth=1)

	def addMap(self, x, y, z, z1=None, z2=None):
		zmin = z1 if z1 else np.min(z)
		zmax = z2 if z2 else np.max(z)

		levels = MaxNLocator(nbins=20).tick_values(zmin, zmax)

		cmap = plt.get_cmap('YlOrRd')
		norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

		cf = self.ax.contourf(x, y, z, levels=levels, cmap=cmap)
		self.figure.colorbar(cf, ax=self.ax)

	def addGraph(self, edges, x, y, n, color="#000000"):
		for i in range(n):
			for j in edges[i]:
				plt.plot([x[i], x[j]], [y[i], y[j]], color=color)

	def addCircle(self, x, y, r, color="#000000"):
		circle = plt.Circle((x, y), r, color=color, fill=False)
		self.ax.add_artist(circle)

	def addTitle(self, xlabel, ylabel, title):
		plt.legend()
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)

	def save(self, directory, namefile = None):
		if(namefile):
			print(type(namefile))
			plt.savefig("img/" + directory + '/' + namefile + ".png")
		else:
			plt.savefig(self.nextFile(directory))
		plt.clf()