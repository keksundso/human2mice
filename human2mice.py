import numpy as np
import cv2
from matplotlib import pyplot as plt


def fourieMask(img, windowSize):


    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT) # macht die fourie transformatio
    dft_shift = np.fft.fftshift(dft) #Shift the zero-frequency component to the center of the spectrum.

    #gives the magnitute part of the dft
    #Briefly, the MAGNITUDE tells "how much" of a certain frequency component is present 
    #and the PHASE tells "where" the frequency component is in the image.
    #only magnitute is das wsa man sich fuer gewaehnlich anschaut (andre is wohl trippy)
    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))



    ####Filter
    #im zentrum is die nuller frequenc die is immer da
    #links und rechts davon is symetrish die jeweile frequence von interesse
    #je weiter weg vom zentrum desto hoeher is die frequncey
    # create a mask first, center square is 1, remaining all zeros
    rows, cols = img.shape
    crow,ccol = rows/2 , cols/2 

    mask = np.zeros((rows,cols,2),np.uint8) 

    mask[crow-windowSize:crow+windowSize, ccol-windowSize:ccol+windowSize] = 1

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



    return [img, img_back, magnitude_spectrum, magnitude_spectrum_masked]

def give_plot(fourieReturn):
    plt.subplot(221),plt.imshow(fourieReturn[0], cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(222),plt.imshow(fourieReturn[2], cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(224),plt.imshow(fourieReturn[3], cmap = 'gray')
    plt.title('Filtered Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(223),plt.imshow(fourieReturn[1], cmap = 'gray')
    plt.title('MouseView'), plt.xticks([]), plt.yticks([])

def give_sinImg(img,cpd):
    img = np.copy(img)
    for zeile in range(img.shape[1]):
        wert = int((np.sin(float(zeile)*cpd)+1)*(255.0/2.0))
        img[zeile][:] = wert
    return img.astype(int)




imgPath ='05spat.png'
#imgPath ='passfoto.jpg'
imgPath ='Landschaftsbild.jpg'

img = cv2.imread(imgPath,0)
img = img[0:np.amin(img.shape), 0:np.amin(img.shape)] 

print img.shape
print img.min(), "       ",img.max()
windowSize = 3

img = give_sinImg(np.empty([456,456]),0.1)
print img.shape
print img.min(), "       ",img.max()
fourieReturn  = fourieMask(img, windowSize)
give_plot(fourieReturn)


plt.show()



#img = np.ndarray(shape=(10,10), dtype=int)
#0 is schwarz
#255 is weiss






