import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('60spat.png',0)
img = cv2.imread('05spat.png',0)
img = cv2.imread('passfoto.jpg',0)

factor = 3

img = img[0:np.amin(img.shape), 0:np.amin(img.shape)] 

dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT) # macht die fourie transformatio
dft_shift = np.fft.fftshift(dft) #Shift the zero-frequency component to the center of the spectrum.

#gives the magnitute part of the dft
#Briefly, the MAGNITUDE tells "how much" of a certain frequency component is present 
#and the PHASE tells "where" the frequency component is in the image.
#only magnitute is das wsa man sich fuer gewaehnlich anschaut (andre is wohl trippy)
magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#plt.show()


####Filter
#im zentrum is die nuller frequenc die is immer da
#links und rechts davon is symetrish die jeweile frequence von interesse
#je weiter weg vom zentrum desto hoeher is die frequncey
# create a mask first, center square is 1, remaining all zeros
rows, cols = img.shape
crow,ccol = rows/2 , cols/2 

mask = np.zeros((rows,cols,2),np.uint8) 

mask[crow-factor:crow+factor, ccol-factor:ccol+factor] = 1

# apply mask and inverse DFT
fshift = dft_shift*mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

dft = cv2.dft(np.float32(img_back),flags = cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)


###Creating a magnituted spectrum again, but now from the mice point of view
dft_back = cv2.dft(np.float32(img_back),flags = cv2.DFT_COMPLEX_OUTPUT) # macht die fourie transformatio
dft_shift_back = np.fft.fftshift(dft_back) #Shift the zero-frequency component to the center of the spectrum.
magnitude_spectrum_masked = 20*np.log(cv2.magnitude(dft_shift_back[:,:,0],dft_shift_back[:,:,1]))
###


plt.subplot(224),plt.imshow(magnitude_spectrum_masked, cmap = 'gray')
plt.title('Filtered Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(img_back, cmap = 'gray')
plt.title('MouseView'), plt.xticks([]), plt.yticks([])
plt.show()
