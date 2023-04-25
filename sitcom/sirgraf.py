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
	R_sun=f2[0].header['RSUN']/f2[0].header['CDELT1']
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
		xx,yy = np.ogrid[0:n,0:m]
		mask = (xx-center_x)**2 + (yy-center_y)**2 > rr**2
		ima1[i][mask] = 0
		#ima1[i][ima1[i]<0]=0
	return min_image,uniform_image,ima1,mask,colorm,R_i,R_sun,x,y,avg,date,time
def plot(path):
	min_image,uniform_image,ima1,mask,colorm,R_i,R_sun,x,y,avg,date,time=sif(path)
	g=np.log10(avg)
	r=np.round(np.mean(g[np.where((np.isnan(g)==False) & (g!=np.inf))]))
	index=int(len(ima1)/2)
	bg=np.ones(uniform_image.shape)-np.log10(uniform_image)
	bg[mask]=0
	bg1=np.ones(min_image.shape)-np.log10(min_image)
	bg1[mask]=0
	#Display required data
	fig1,ax=plt.subplots(2,2)
	circ2=pa.Circle((0,0),R_i,color='black')
	circ=pa.Circle((0,0),1,color='white',fill=False)
	ax[0,0].imshow(mask,cmap=colorm)
	i1=ax[0,0].imshow(bg1,extent=[x[0],x[-1],y[0],y[-1]],cmap=colorm)
	cb=plt.colorbar(i1,ax=ax[0,0],shrink=0.85,pad=0.01,extend='both')
	ax[0,0].add_patch(circ2)
	ax[0,0].add_patch(circ)
	cb.set_label('Log(Intensity)')
	ax[0,0].set_xlabel('Solar X (R$_{\odot}$)')
	ax[0,0].set_ylabel('Solar Y (R$_{\odot}$)')
	ax[0,0].set_title('Minimum Intensity Image')
	ax[0,1].plot(y[np.where(y>=0)],avg/10**r,color='black')
	ax[0,1].set_xlabel('Solar X (R$_{\odot}$)')
	ax[0,1].set_ylabel('Average Intensity(10$^{'+str(int(r))+'}$)')
	ax[0,1].set_box_aspect(1)
	i2=ax[1,0].imshow(bg,extent=[x[0],x[-1],y[0],y[-1]],cmap=colorm)
	cb1=plt.colorbar(i2,ax=ax[1,0],shrink=0.85,pad=0.01,extend='both')
	cb1.set_label('Log(Intensity)')
	ax[1,0].set_xlabel('Solar X (R$_{\odot}$)')
	ax[1,0].set_ylabel('Solar Y (R$_{\odot}$)')
	ax[1,0].set_title('Uniform Intensity Image')
	circ3=pa.Circle((0,0),R_i,color='black')
	circ1=pa.Circle((0,0),1,color='white',fill=False)
	ax[1,0].add_patch(circ3)
	ax[1,0].add_patch(circ1)
	i3=ax[1,1].imshow(cv2.medianBlur(ima1[index],5),extent=[x[0],x[-1],y[0],y[-1]],cmap=colorm)
	ax[1,1].set_xlabel('Solar X (R$_{\odot}$)')
	ax[1,1].set_ylabel('Solar Y (R$_{\odot}$)')
	patch = pa.Circle((0,0), radius=np.max(y),transform=ax[1,1].transData)
	i3.set_clip_path(patch)
	circ4=pa.Circle((0,0),R_i,color='black')
	circ0=pa.Circle((0,0),1,color='white',fill=False)
	ax[1,1].add_patch(circ4)
	ax[1,1].add_patch(circ0)
	ax[1,1].set_facecolor("black")
	cb2=plt.colorbar(i3,ax=ax[1,1],shrink=0.85,pad=0.01,extend='both')
	cb2.set_label('Normalised Intensity')
	cb2.ax.set_ylim(bottom=0)
	plt.tight_layout()
	plt.show()
#Animation of all the subtracted images
def animation_m(path):
	min_image,uniform_image,ima1,mask,colorm,R_i,R_sun,x,y,avg,date,time=sif(path)
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	div = make_axes_locatable(ax1)
	cax = div.append_axes('right', '5%', '5%')
	im=ax1.imshow(cv2.medianBlur(ima1[0],5),extent=[x[0],x[-1],y[0],y[-1]],cmap=colorm)
	ax1.set_xlabel(r'Solar X (R$_{\odot}$)')
	ax1.set_ylabel('Solar Y (R$_{\odot}$)')
	circle2=pa.Circle((0,0),R_i,color='black')
	circle=pa.Circle((0,0),1,color='white',fill=False)
	patch = pa.Circle((0,0), radius=np.max(y),transform=ax1.transData)
	im.set_clip_path(patch)
	ax1.add_patch(circle2)
	ax1.add_patch(circle)
	ax1.set_facecolor("black")
	tx=ax1.set_title('Date: '+date+' Time: '+time[0])
	cb3=fig.colorbar(im,cax=cax,extend='both')
	cb3.set_label('Normalised Intensity')
	cb3.ax.set_ylim(bottom=0)
	def animate(i):
		#cax.cla()
		arr=cv2.medianBlur(ima1[i],5)
		im.set_data(arr)
		tx.set_text('Date: '+date+' Time: '+time[i])
	ani = animation.FuncAnimation(fig, animate, frames=len(ima1))
	plt.show()
	return ani
