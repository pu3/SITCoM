import glob,os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import matplotlib.patches as pa
from matplotlib import rcParams
rcParams['font.family'] = 'monospace'

import cv2,skimage
import sunpy.visualization.colormaps as cm
from astropy.io import fits
from mpl_toolkits.axes_grid1 import make_axes_locatable

import warnings
warnings.filterwarnings("ignore")

#Read all fits images and information from header 

def sif(path):
	ext=set(os.path.splitext(file)[-1] for file in os.listdir(path))
	if '.fits' in ext:
		filenames=sorted(glob.glob(path+'/*.fits'))
	elif '.fts' in ext:
		filenames=sorted(glob.glob(path+'/*.fts'))
	f2=fits.open(filenames[0])
	center_x=f2[0].header['CRPIX1']
	center_y=f2[0].header['CRPIX2']
	if 'RSUN' in f2[0].header:
		R_sun=f2[0].header['RSUN']/f2[0].header['CDELT1']
	else:
		R_sun=959.63/f2[0].header['CDELT1']
	date=f2[0].header['DATE-OBS'].split('T')[0]
	if f2[0].header['INSTRUME']=='LASCO':
		c=f2[0].header['DETECTOR']
		if 'C2' in c :
			R_i=2.25
			colorm=matplotlib.colormaps['soholasco2']
		if 'C3' in c :
			R_i=4.0
			#center_y=f2[0].data.shape[1]-center_y
			colorm=matplotlib.colormaps['soholasco3']
	elif f2[0].header['INSTRUME']=='COSMO K-Coronagraph':
		R_i=1.15
		colorm=matplotlib.colormaps['kcor']
	elif f2[0].header['INSTRUME']=='SECCHI':
		c=f2[0].header['DETECTOR']
		if 'COR1' in c :
			R_i=1.57
			colorm=matplotlib.colormaps['stereocor1']
		if 'COR2' in c :
			R_i=3.0
			colorm=matplotlib.colormaps['stereocor2']
	ima,time=[],[]
	#pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
	for i in range(len(filenames)):
		f1=fits.open(filenames[i],memmap=False)
		time.append(f1[0].header['DATE-OBS'].split('T')[1].split('.')[0])
		ima.append(np.flipud(f1[0].data))
		f1.close()
	stack_image=np.array(ima)
	min_image=np.copy(stack_image[0])
	#Find minimum intensity images
	for i in range(len(ima)):
		for j in range(len(ima[0])):
			b=stack_image[i,j,j]
			if b>0:
				min_image[j,j]=np.min(b)
	#Calibrate to solar radius
	x=np.empty(min_image.shape[0])
	y=np.empty(min_image.shape[0])
	for i in range(len(x)):
		x[i]=(i-center_x)/R_sun
		y[i]=(i-center_y)/R_sun
	#Convert minimum image to polar coordinate space
	image = skimage.util.img_as_float(min_image)
	radius=np.sqrt(((image.shape[0]-center_x)**2.0)+((image.shape[1]-center_y)**2.0))
	image_polar=cv2.linearPolar(image, (center_x, center_y), radius,cv2.WARP_FILL_OUTLIERS)
	avg=np.empty(len(np.where(y>=0)[0]))
	for i in range(len(avg)):
		a=np.mean(image_polar[np.where(y>=0)][:,i])
		avg[i]=a
	#Create uniform intensity image in polar space
	image_polar1=np.copy(image_polar)
	for i in range(len(image_polar1)):
		image_polar1[:,i]=np.mean(image_polar[:,i])
	#Convert back to cartesian
	uniform_image = cv2.linearPolar(image_polar1, (center_y, center_x),radius, cv2.WARP_INVERSE_MAP)
	#Apply the algorithm and mask (I_new=I-Imin/Iu)
	ima1=np.copy(ima)
	mask=0
	for i in range(len(ima)):
		i1=ima1[i]-min_image
		ima1[i]=i1/uniform_image
		n,m=ima1[i].shape
		rr=np.max(y)*R_sun
		ri=R_i*R_sun
		xx,yy = np.ogrid[0:n,0:m]
		mask = (xx-center_x)**2 + (yy-center_y)**2 > rr**2
		mask1 = (xx-center_x)**2 + (yy-center_y)**2 < ri**2
		ima1[i][mask] = 0
		ima1[i][mask1]=0
		#ima1[i][ima1[i]<0]=0
	return min_image,uniform_image,ima1,mask,colorm,R_i,R_sun,x,y,avg,date,time
