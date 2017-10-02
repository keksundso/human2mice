import cv2
import numpy as np
from matplotlib import pyplot as plt

imgPath ='05spat.png'
#imgPath ='passfoto.jpg'

img = cv2.imread(imgPath,0)
img = img[0:np.amin(img.shape), 0:np.amin(img.shape)] 
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))

plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()