#!python
#cython: boundscheck=False, wraparound=False, cdivision=True

import numpy as np
cimport numpy as np

ctypedef np.float64_t float64_t
ctypedef np.uint8_t uint8_t
ctypedef unsigned int uint

def _histogram(np.ndarray[uint8_t, ndim=2] src not None, uint npatterns=59):
	"""
	> src must be a LBP version of image.
	> default value of number of patterns corresponds to uniform
	  version of LBP operator.
	"""
	cdef: 
		np.ndarray[float64_t, ndim=1] hist = np.zeros(npatterns)
		uint i
		uint j
		uint nrow = src.shape[0]
		uint ncol = src.shape[1]	
		uint N = nrow*ncol
	for i in range(nrow):
		for j in range(ncol):
			hist[src[i,j]] += 1.
	hist/=N
	return hist


def spatial(np.ndarray[uint8_t, ndim=2] src not None,
	uint nx, uint ny, uint npatterns=59, uint overlapX=2, uint overlapY=2):
	"""
	> Implementation of Ahonen's Enhanced Spatial Histogram, with overlaps.
	> The window size couldn't be fixed. Example, if there are 2 noses 
	  pictures of the same dog, the first 800x800 and the second 400x400,
	  then the spatial information will not match.
	> More or less realistic assumption; the noses pictures will keep ratio.
	> x and y will mean for vertical and horizontal directions respectively,
	  (x->rows direction and y->columns direction)
	> nx and ny stands for the number of divisions in vertical and horizontal	
	  axis, respectively.
	"""
	#some constrains to overlap parameter
	if (overlapX<0) or (overlapX>10):
		print "Wrong overlapX parameter"
		return -1
	if (overlapY<0) or (overlapY>10):
		print "Wrong overlapY parameter"
		return -1

	cdef:
		uint height = src.shape[0]
		uint width = src.shape[1]

		#widows size: (wsx,wsy)
		uint wsx = np.uint(np.floor((height+2.*overlapX)/nx))
		uint wsy = np.uint(np.floor((width+2.*overlapY)/ny))

		#remainders=(xrem,yrem), ie, number of pixels that 
		#can't be covered with such windows sizes
		uint xrem = height-nx*wsx+2*overlapX
		uint yrem = width-ny*wsy+2*overlapY
	"""
	> Each image subdivision will be named region. there are in
	  total nx*ny regions.
	> Each region has two index Rxy=R[x,y].
	> All regions R[0:rx0,:] and R[rx1:,:] will have a windows 
	  size with one more pixel on x direction. 
	> All regions R[:,0:ry0] and R[:,ry1:] will have a windows
	  size with one more pixel on y direction.
	"""
	cdef uint rx0, rx1, ry0, ry1

	if xrem%2==0:
		rx0 = xrem/2-1
		rx1 = nx-xrem/2
	else:
		rx0 = xrem/2
		rx1 = nx-xrem/2
	if yrem%2==0:
		ry0 = yrem/2-1
		ry1 = ny-yrem/2
	else:
		ry0 = yrem/2
		ry1 = ny-yrem/2
	
	cdef:
		#spatial histogram will contain in each of his rows
		#an LBP histogram of a region.
		np.ndarray[float64_t, ndim=2] sp_hist = np.empty((nx*ny,npatterns))

		#hist_index, counts for histograms above. 
		#hist_index=0:nx*ny
		uint hist_index = 0

		#i_index and j_index are indexes of src matrix corresponding
		#to each region upper left corner, in the corresponding iteration.
		uint i_index = 0
		uint j_index = 0

		#rx_index and ry_index are region indexes.
		uint rx_index
		uint ry_index

		#Some other variables used in the loop below.
		uint Wsx
		uint Wsy

	#iteration through regions
	for rx_index in range(nx):
		#verify if a pixel must be added to the windows size on x direction
		Wsx = wsx
		if rx_index<=rx0 | rx_index>=rx1:
			Wsx += 1
		j_index = 0
		for ry_index in range(ny):
			#verify if a pixel must be added to the windows size on y direction
			Wsy = wsy
			if ry_index<=ry0 | ry_index>=ry1:
				Wsy += 1
			sp_hist[hist_index,:] = _histogram(src[i_index:i_index+Wsx, j_index:j_index+Wsy],npatterns)
			hist_index += 1
			j_index += Wsy-overlapY
		i_index += Wsx-overlapX
	#concatenation of histrograms in each row
	return sp_hist.ravel()	


def spatial_pyramid(np.ndarray[uint8_t, ndim=2] src not None,
	uint level=3, uint npatterns=59, uint overlapX=2, uint overlapY=2):
	"""
	> Implementation of Spatial Pyramidal Histogram, with overlaps.
	> The total number of histograms with L levels would be (2**(2L+2)-1)
	> The number of histograms on level l is 2**(2*l)
	"""
	cdef:
		np.ndarray[float64_t, ndim=1] sp_pyrd = np.empty((2**(2*level+2)-1)*npatterns)
		uint rindex = 0 #right index
		uint lindex = 0 #left index
		uint l
		uint L = level  #just for convenience
	for l in range(L):
		if l==0:
			lindex = rindex+npatterns
			sp_pyrd[rindex:lindex] = _histogram(src)
		else:
			lindex = rindex+2**(2*l)*npatterns
			sp_pyrd[rindex:lindex] = spatial(src,2**l,2**l)
		rindex = lindex
	return sp_pyrd

def gradient():
	"""
	> Implementation of HOG.
	"""
	return
