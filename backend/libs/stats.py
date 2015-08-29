#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot

#percentaje of non uniform patterns, on a single spatial histogram
def per_nup(sp_hist):
	nup=sp_hist[58::59]
	mean_nup=np.sum(nup)/np.float(nup.shape[0])
	return mean_nup



