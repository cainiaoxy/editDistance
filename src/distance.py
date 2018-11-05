#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import pandas as pd
import numpy as np
from multiprocessing import Pool
import functools
import time
import types
import copy_reg

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

class EditDistance:
	def compareDistance(self, word1, word2):
		n = len(word1.decode("utf-8"))
		m = len(word2.decode("utf-8"))
		if n == 0:
			return m
		elif m == 0:
			return n
		else:
			matrix = np.zeros([m+1, n+1])
			matrix[0,:] = [i for i in range(0,n+1)]
			matrix[:,0] = [i for i in range(0,m+1)]
			for i in range(1,n+1):
				ch1 = word1.decode("utf-8")[i-1]
				for j in range(1,m+1):
					ch2 = word2.decode("utf-8")[j-1]
					if ch1 == ch2:
						tmp = 0
					else:
						tmp = 1
					matrix[j,i] = np.min([matrix[j-1,i]+1, matrix[j,i-1]+1, matrix[j-1,i-1]+tmp])
			return matrix[m,n]

	def distancePercent(self, word1, word2):
		edis = self.compareDistance(word1, word2)
		wdis = max(len(word1.decode("utf-8")), len(word2.decode("utf-8")))
		dpec = edis / wdis
		return dpec

def main():
	ed = EditDistance()
	name = sys.argv[1]
	equip_name = sys.argv[2]
	compute = functools.partial(ed.distancePercent, name)
	df = pd.read_csv(equip_name, index_col=0)
	df["equip"] = df.equip.map(lambda x: x.decode("gbk").encode("utf-8"))
	"""
	t0 = round(time.time()*1000)
	df["ed"] = df["equip"].map(compute)
	t1 = round(time.time()*1000)
	df = df.sort_values(by = ["ed"])
	print t1-t0
	"""
	pool = Pool(6)
	t0 = round(time.time()*1000)
	df["ed"] = pool.map(compute, df["equip"].values)
	t1 = round(time.time()*1000)
	df = df.sort_values(by = ["ed"])
	print t1-t0
	print df
if __name__ == "__main__":
	main()


