import numpy as np

def _weight_calculate():
	return


def weighted_chi2(h0,h1,weights):
	return

def chi2(h0,h1,tol=1e-10):
	return np.sum((h0-h1)**2./((h0+h1)+tol))

def pmk(sp_pyrd0, sp_pyrd1,level=3,npatterns=59):
	"""
	> Pyramid Match Kernel
	"""
	L=level
	retval=0.
	rindex=0
	lindex=0
	for l in range(L):
		if l==0:
			lindex=rindex+npatterns
			retval+=chi2(sp_pyrd0[rindex:lindex],sp_pyrd1[rindex:lindex])/2**L
		else:
			lindex=rindex+2**(2*l)*npatterns
			retval+=chi2(sp_pyrd0[rindex:lindex],sp_pyrd1[rindex:lindex])/2**(L-l+1)
		rindex=lindex
	return retval