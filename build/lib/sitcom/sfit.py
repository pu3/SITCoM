import numpy as np
from scipy.optimize import curve_fit

def gauss_function(x, a, x0, sigma,c):
	return a*np.exp(-(x-x0)**2/(2*sigma**2))+c

def bytescale(data, cmin=None, cmax=None, high=255, low=0):
	if data.dtype == np.uint8:
		return data

	if high < low:
		raise ValueError("`high` should be larger than `low`.")

	if cmin is None:
		cmin = data.min()
	if cmax is None:
              cmax = data.max()

	cscale = cmax - cmin
	if cscale < 0:
		raise ValueError("`cmax` should be larger than `cmin`.")
	elif cscale == 0:
		cscale = 1

	scale = float(high - low) / cscale
	bytedata = (data * 1.0 - cmin) * scale + 0.4999
	bytedata[bytedata > high] = high
	bytedata[bytedata < 0] = 0
	return np.cast[np.uint8](bytedata) + np.cast[np.uint8](low)
def xt_gauss_peaks(xt_tr1):
	xt_tr1 = bytescale(xt_tr1)
	yshape,xshape = np.shape(xt_tr1)[0],np.shape(xt_tr1)[1]
	x2 = np.arange(0,yshape,dtype='int')
	l = 4
	coe = np.zeros((l,xshape),dtype='float')
	sg = np.zeros((l,xshape),dtype='float')
	est = np.zeros(l,dtype=float)
	for i in np.arange(xshape):
		y1 = xt_tr1[:,i]
		#est[0],est[1],est[2] = estimate_parameters(y)
		#est[2] = np.std(y1)
		est[2]=xshape/6.0
		est[3]= np.min(y1)
		est[0] = np.max(y1)-np.min(y1)
		ind = np.asarray(np.where(y1==y1.max()),dtype='int')[0]
		est[1]=  ind[0]
		try:
			popt, pcov = curve_fit(gauss_function, x2, y1,p0=est)
			coe[:,i],sg[:,i] = popt,np.sqrt(np.abs(np.diag(pcov)))
		except RuntimeError:
			print("Error - curve_fit failed")
	return coe,sg

def mysine_decay(x,p0,p1,p2,p3,p4,p5):
	return p0+(p1*np.sin((2*np.pi/p2)*x+p3))*np.exp(-x/p4)+p5*x
