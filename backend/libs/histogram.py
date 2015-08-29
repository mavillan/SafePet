import numpy as np
import cv2 as cv
from skimage.feature import local_binary_pattern as lbp

def _histogram(src,numPatterns=59):
	"""
	> src must be uniform LBP version of image.
	> defautl value of number of patterns corresponds to uniform
	  version of LBP operator.
	"""
	npattern=np.float(src.shape[0]*src.shape[1]) #total number of patterns
	hist=np.bincount(src.ravel(),minlength=numPatterns).astype(np.float)
	hist/=npattern #normalization
	return hist


def spatial(src,nx,ny,numPatterns=59,overlapX=2,overlapY=2):
	"""
	> Implementation of Ahonen's Enhanced Spatial Histogram, with overlaps.
	> The window size couldn't be fixed. Example, if there are 2 noses 
	  pictures of the same dog, the first 800x800 and the second 400x400,
	  then the spatial information will not match.
	> More or less realistic assumption, the noses pictures will keep ratio.
	> x and y will mean for vertical and horizontal directions respectively,
	  (x->rows direction and y->columns direction)
	> nx and ny stands for the number of divisions in vertical and horizontal	
	  axis, respectively.
	"""
	#some constrains to overlap parameter
	if (type(overlapX) is not int) or (overlapX<0) or (overlapX>10):
		print "Wrong overlapX parameter"
		return -1
	if (type(overlapY) is not int) or (overlapY<0) or (overlapY>10):
		print "Wrong overlapY parameter"
		return -1
	height,width=src.shape
	#widows size: (wsx,wsy)
	wsx=np.int(np.floor((height+2.*overlapX)/nx))
	wsy=np.int(np.floor((width+2.*overlapY)/ny))
	#remainders=(xrem,yrem), ie, number of pixels that 
	#can't be covered with such windows sizes
	xrem=height-nx*wsx+2*overlapX
	yrem=width-ny*wsy+2*overlapY
	"""
	> Each image subdivision will be named region. there are in
	  total nx*ny regions.
	> Each region has two index Rxy=R[x,y].
	> All regions R[0:rx0,:] and R[rx1:,:] will have a windows 
	  size with one more pixel on x direction. 
	> All regions R[:,0:ry0] and R[:,ry1:] will have a windows
	  size with one more pixel on y direction.
	"""
	if xrem%2==0:
		rx0=xrem/2-1
		rx1=nx-xrem/2
	else:
		rx0=xrem/2
		rx1=nx-xrem/2
	if yrem%2==0:
		ry0=yrem/2-1
		ry1=ny-yrem/2
	else:
		ry0=yrem/2
		ry1=ny-yrem/2
	#spatial histogram will contain in each of his rows
	#an LBP histogram of a region.
	sp_hist=np.empty((nx*ny,numPatterns))
	#hist_index, counter for histograms above. 
	#hist_index=0:nx*ny
	hist_index=0
	#i_index and j_index are indexes of src matrix corresponding
	#to each region in the corresponding iteration.
	i_index=0
	#iteration through regions
	for rx_index in range(nx):
		#verify if a pixel must be added to the windows size on x direction
		Wsx=wsx
		if rx_index<=rx0 | rx_index>=rx1:
			Wsx+=1
		j_index=0
		for ry_index in range(ny):
			#verify if a pixel must be added to the windows size on y direction
			Wsy=wsy
			if ry_index<=ry0 | ry_index>=ry1:
				Wsy+=1
			sp_hist[hist_index,:]=_histogram(src[i_index:i_index+Wsx, j_index:j_index+Wsy],numPatterns)
			hist_index+=1
			j_index+=Wsy-overlapY
		i_index+=Wsx-overlapX
	#concatenation of histrograms in each row
	return sp_hist.ravel()


def spatial_pyramid(src,level=3,numPatterns=59,,overlapX=2,overlapY=2):
	"""
	> Implementation of Spatial Pyramidal Histogram, with overlaps.
	> The total number of histograms with L levels would be (2**(2L+2)-1)
	> The number of histograms on level l is 2**(2*l)
	"""
	sp_pyrd=np.empty((2**(2*level+2)-1)*numPatterns)
	rindex=0 #right index
	lindex=0 #left index
	for i in range(level):
		if i==0:
			lindex=rindex+numPatterns
			sp_pyrd[rindex,lindex]=_histogram(src)
			rindex=lindex
		else:
			lindex=rindex+2**(2*level)*numPatterns
			sp_pyrd[rindex,lindex]=spatial(src,2**level,2**level)
			rindex=lindex
	return sp_pyrd

def gradient():
	"""
	> Implementation of HOG.
	"""
	return
