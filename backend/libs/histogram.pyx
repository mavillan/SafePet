#cython: cdivision=True 
#cython: boundscheck=False
#cython: nonecheck=False
#cython: wraparound=False

import numpy as np
cimport numpy as cnp
from libc.math cimport floor

ctypedef cnp.float64_t float64_t
ctypedef cnp.uint8_t uint8_t
ctypedef cnp.ndarray ndarray
ctypedef unsigned int uint

cdef ndarray _histogram(uint8_t[:,::1] src, int npatterns=59):
	#> src must be a LBP version of image.
	#> default value of number of patterns corresponds to uniform
	#  version of LBP operator.

	cdef:
		ndarray[float64_t, ndim=1] hist = np.zeros(npatterns, dtype=np.float64)
		Py_ssize_t i
		Py_ssize_t j
		Py_ssize_t nrow = src.shape[0]
		Py_ssize_t ncol = src.shape[1]	
		float64_t N = nrow*ncol
	for i in range(nrow):
		for j in range(ncol):
			hist[src[i,j]] += 1.
	for i in range(npatterns):
		hist[i]/=N
	return hist


cdef ndarray _spatial(uint8_t[:,::1] src, int nx, int ny,
     int npatterns=59, int overlapX=2, int overlapY=2):
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

	cdef:
		int height = src.shape[0]
		int width = src.shape[1]

		#widows size: (wsx,wsy)
		int wsx = (height+(nx-1)*overlapX)/nx
		int wsy = (width+(ny-1)*overlapY)/ny

		#remainders=(xrem,yrem), ie, number of pixels that 
		#can't be covered with such windows sizes
		int xrem = height-nx*wsx+(nx-1)*overlapX
		int yrem = width-ny*wsy+(ny-1)*overlapY
	"""
	> Each image subdivision will be named region. there are in
	  total nx*ny regions.
	> Each region has two index Rxy=R[x,y].
	> All regions R[0:rx0,:] and R[rx1:,:] will have a windows 
	  size with one more pixel on x direction. 
	> All regions R[:,0:ry0] and R[:,ry1:] will have a windows
	  size with one more pixel on y direction.
	"""
	cdef int rx0, rx1, ry0, ry1

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
		#spatial histogram will contain concatenated
		#LBP histograms of each region.
		ndarray[float64_t, ndim=1] sp_hist = np.empty(nx*ny*npatterns, dtype=np.float64)

		#right and left histogram indexes, for each corresponding region 
		#in principal iteration
		Py_ssize_t lh_index = 0
		Py_ssize_t rh_index = 0

		#i_index and j_index are indexes of src matrix corresponding
		#to each region upper left corner, in the corresponding iteration.
		Py_ssize_t i_index = 0
		Py_ssize_t j_index = 0

		#rx_index and ry_index are region indexes.
		Py_ssize_t rx_index
		Py_ssize_t ry_index

		#Some other variables used in the loop below.
		Py_ssize_t Wsx
		Py_ssize_t Wsy

	#iteration through regions
	for rx_index in range(nx):
		#verify if a pixel must be added to the windows size on x direction
		Wsx = <Py_ssize_t>wsx
		if rx_index<=rx0 or rx_index>=rx1:
			Wsx += 1
		j_index=0
		for ry_index in range(ny):
			#verify if a pixel must be added to the windows size on y direction
			Wsy = <Py_ssize_t>wsy
			if ry_index<=ry0 or ry_index>=ry1:
				Wsy += 1
			rh_index += npatterns
			sp_hist[lh_index:rh_index] = _histogram(src[i_index:i_index+Wsx, j_index:j_index+Wsy], npatterns)
			lh_index = rh_index
			j_index += Wsy-overlapY
		i_index += Wsx-overlapX
	return sp_hist


cdef ndarray _spatial_pyramid(uint8_t[:,::1] src,
	int level=3, int npatterns=59, int overlapX=2, int overlapY=2):
	"""
	> Implementation of Spatial Pyramidal Histogram, with overlaps.
	> The total number of histograms with L levels would be (2**(2L+2)-1)
	> The number of histograms on level l is 2**(2*l)
	"""

	cdef:
		Py_ssize_t l_index = 0 #left index
		Py_ssize_t r_index = 0 #right index
		Py_ssize_t l
		Py_ssize_t L = level  #just for convenience
		ndarray[float64_t, ndim=1] sp_pyrd = np.empty((2**(2*L+2)-1)*npatterns) 
	for l in range(L):
		if l==0:
			r_index = l_index+npatterns
			sp_pyrd[l_index:r_index] = _histogram(src, npatterns)
		else:
			r_index = l_index+2**(2*l)*npatterns
			sp_pyrd[l_index:r_index] = _spatial(src, 2**l, 2**l, npatterns, overlapX, overlapY)
		l_index = r_index
	return sp_pyrd

# def gradient():
# 	"""
# 	> Implementation of HOG.
# 	"""
# 	return

cdef ndarray _squared_spatial_pyramid(uint8_t[:,::1] src,
	int level=3, int npatterns=59, int overlapX=2, int overlapY=2):
	"""
	> Implementation of Squared Spatial Pyramidal Histogram, with overlaps.
	> The total number of histograms with L levels would be L*(L+1)*(2*L+1)/6
	> The number of histograms on level l is l**2
	> first level is l=1
	"""

	cdef:
		Py_ssize_t l_index = 0 #left index
		Py_ssize_t r_index = 0
		Py_ssize_t l
		Py_ssize_t L = level
		ndarray[float64_t, ndim=1] sq_sp_pyrd = np.empty(((L*(L+1)*(2*L+1))/6)*npatterns)
	for l in range(1,L+1):
		r_index = l_index+(l**2)*npatterns
		sq_sp_pyrd[l_index:r_index] = _spatial(src, l**2, l**2, npatterns, overlapX, overlapY)
		l_index = r_index
	return sq_sp_pyrd



"""
Wrapers Funtions
"""
def histogram(uint8_t[:,::1] src not None, int npatterns=59):
	return _histogram(src, npatterns)

def spatial(uint8_t[:,::1] src not None,
	int nx, int ny, int npatterns=59, int overlapX=2, int overlapY=2):
	return _spatial(src, nx, ny, npatterns, overlapX, overlapY)

def spatial_pyramid(uint8_t[:,::1] src not None,
	int level=3, int npatterns=59, int overlapX=2, int overlapY=2):
	return _spatial_pyramid(src, level, npatterns, overlapX, overlapY)

def squared_spatial_pyramid(uint8_t[:,::1] src not None,
	int level=3, int npatterns=59, int overlapX=2, int overlapY=2):
	return _squared_spatial_pyramid(src, level, npatterns, overlapX, overlapY)
