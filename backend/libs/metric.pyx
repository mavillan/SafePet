#cython: cdivision=True 
#cython: boundscheck=False
#cython: nonecheck=False
#cython: wraparound=False


import numpy as np
cimport numpy as cnp


ctypedef unsigned int uint
ctypedef cnp.float64_t float64_t
ctypedef cnp.uint8_t uint8_t
ctypedef cnp.ndarray ndarray


cdef float64_t _chi2(float64_t[::1] h0, float64_t[::1] h1):
	"""
	> Standard chi_square metric
	"""
	cdef:
		Py_ssize_t i
		Py_ssize_t n = h0.shape[0]
		float64_t a
		float64_t b
		float64_t retval = 0.
	with nogil:
		for i in range(n):
			a = h0[i]-h1[i]
			b = h0[i]+h1[i]
			if b==0.:
				continue
			retval += (a*a)/b
	return retval


cdef ndarray _Chi2(float64_t[:,::1] X, float64_t[:,::1] Y):
	"""
	> Function to compute Gram Matrix between X and Y using 
	  chi2 metric
	"""
	cdef:
		Py_ssize_t m = X.shape[0]
		Py_ssize_t n = Y.shape[0]
		Py_ssize_t i, j
		#Gram Matrix
		ndarray[float64_t, ndim=2] G = np.empty((m,n))
	for i in range(m):
		for j in range(n):
			G[i,j] = _chi2(X[i],Y[j])
	return G


cdef float64_t _pmk(float64_t[::1] sp_pyrd0, 
	                float64_t[::1] sp_pyrd1, 
	                int level=3, int npatterns=59):
	"""
	> Pyramid Match Kernel metric
	"""
	cdef:
		Py_ssize_t l
		Py_ssize_t L = level
		Py_ssize_t rindex = 0
		Py_ssize_t lindex = 0
		float64_t retval = 0.
	for l in range(L):
		if l==0:
			rindex = lindex+npatterns
			retval += _chi2(sp_pyrd0[lindex:rindex],sp_pyrd1[lindex:rindex])/2**L
		else:
			rindex = lindex+2**(2*l)*npatterns
			retval += _chi2(sp_pyrd0[lindex:rindex],sp_pyrd1[lindex:rindex])/2**(L-l+1)
		lindex = rindex
	return retval


"""
Wrapers Funtions
"""

def chi2(float64_t[::1] h0 not None, float64_t[::1] h1 not None):
	return _chi2(h0, h1)

def Chi2(float64_t[:,::1] X not None, float64_t[:,::1] Y not None):
	return _Chi2(X, Y)

def pmk(float64_t[::1] sp_pyrd0 not None,
	    float64_t[::1] sp_pyrd1 not None, 
	    int level=3, int npatterns=59):
	return _pmk(sp_pyrd0, sp_pyrd1, level, npatterns)
