
cdef extern from "math.h":
	double sqrt(double m)

cimport numpy as np
cimport cython

ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
def chi2(np.ndarray[DTYPE_t, ndim=1] h0, np.ndarray[DTYPE_t, ndim=1] h1):
	cdef Py_ssize_t i
	cdef Py_ssize_t n = h0.shape[0]
	cdef DTYPE_t a
	cdef DTYPE_t b
	cdef DTYPE_t retval = 0.0
	for i in range(n):
		a = h0[i]-h1[i]
		b = h0[i]+h1[i]+1e-10
		retval += (a*a)/b
	return retval

# def pmk(sp_pyrd0, sp_pyrd1,level=3,numPatterns=59):
# 	"""
# 	> Pyramid Match Kernel
# 	"""
# 	L=level
# 	retval=0.
# 	rindex=0
# 	lindex=0
# 	for l in range(L):
# 		if l==0:
# 			lindex=rindex+numPatterns
# 			retval+=chi2(sp_pyrd0[rindex:lindex],sp_pyrd1[rindex:lindex])/2**L
# 		else:
# 			lindex=rindex+2**(2*l)*numPatterns
# 			retval+=chi2(sp_pyrd0[rindex:lindex],sp_pyrd1[rindex:lindex])/2**(L-l+1)
# 		rindex=lindex
# 	return retval