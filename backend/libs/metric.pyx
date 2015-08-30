#!python
#cython: boundscheck=False, wraparound=False, cdivision=True

# cdef extern from "math.h":
# 	double sqrt(double m)

import metric
cimport numpy as np
cimport cython

ctypedef np.float64_t DTYPE_t


def chi2(np.ndarray[DTYPE_t, ndim=1] h0 not None, np.ndarray[DTYPE_t, ndim=1] h1 not None):
	"""
	> Standard chi_square metric
	"""
	cdef:
		Py_ssize_t i
		Py_ssize_t n = h0.shape[0]
		DTYPE_t a
		DTYPE_t b
		DTYPE_t retval = 0.0
	for i in range(n):
		a = h0[i]-h1[i]
		b = h0[i]+h1[i]
		if b==0.:
			continue
		retval += (a*a)/b
	return retval


def pmk(np.ndarray[DTYPE_t, ndim=1] sp_pyrd0 not None, 
	    np.ndarray[DTYPE_t, ndim=1] sp_pyrd1 not None, 
	    unsigned int level=3, unsigned int npatterns=59):
	"""
	> Pyramid Match Kernel
	"""
	cdef:
		Py_ssize_t l
		Py_ssize_t L = level
		Py_ssize_t rindex = 0
		Py_ssize_t lindex = 0
		DTYPE_t retval = 0.
	for l in range(L):
		if l==0:
			lindex=rindex+npatterns
			retval+=chi2(sp_pyrd0[rindex:lindex],sp_pyrd1[rindex:lindex])/2**L
		else:
			lindex=rindex+2**(2*l)*npatterns
			retval+=chi2(sp_pyrd0[rindex:lindex],sp_pyrd1[rindex:lindex])/2**(L-l+1)
		rindex=lindex
	return retval

