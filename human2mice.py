import numpy as np
import cv2
from matplotlib import pyplot as plt



def fourieMask(img):


    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT) # macht die fourie transformatio
    dft_shift = np.fft.fftshift(dft) #Shift the zero-frequency component to the center of the spectrum.

    #gives the magnitute part of the dft
    #Briefly, the MAGNITUDE tells "how much" of a certain frequency component is present 
    #and the PHASE tells "where" the frequency component is in the image.
    #only magnitute is das wsa man sich fuer gewaehnlich anschaut (andre is wohl trippy)
    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1])+1)

    print magnitude_spectrum.min(), " --- ", magnitude_spectrum.max()
    #print magnitude_spectrum
    OldMax = magnitude_spectrum.max()
    OldMin = magnitude_spectrum.min()
    NewMax = 255.0
    NewMin = 0.0

    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    
    """
    for index, value in enumerate(magnitude_spectrum[0]):
        for inner_index, inner_value in enumerate(magnitude_spectrum[1]):
            magnitude_spectrum[index][inner_index] = int((((inner_value - OldMin) * NewRange) / OldRange) + NewMin)
               
    print magnitude_spectrum.min(), " --- ", magnitude_spectrum.max()
    print "........."
    #print magnitude_spectrum
    """
    ####Filter
    #im zentrum is die nuller frequenc die is immer da
    #links und rechts davon is symetrish die jeweile frequence von interesse
    #je weiter weg vom zentrum desto hoeher is die frequncey
    # create a mask first, center square is 1, remaining all zeros
    rows, cols = img.shape
    crow,ccol = rows/2 , cols/2 

    mask = np.zeros((rows,cols,2),np.uint8) 

    for index, value in enumerate(magnitude_spectrum[:,magnitude_spectrum.shape[1]/2]):
        if value == sorted(magnitude_spectrum[:,magnitude_spectrum.shape[1]/2])[-2]:
            windowSize = abs(crow-index)

            
        

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
    magnitude_spectrum_masked = 20*np.log(cv2.magnitude(dft_shift_back[:,:,0],dft_shift_back[:,:,1])+1)
    ###

    #print mask[:,:,1]


    return [img, img_back, magnitude_spectrum, magnitude_spectrum_masked, mask[:,:,1]]

def give_plot(fourieReturn, index):
    print len(fourieReturn)
    if index == 0:
        plt.subplot(334),plt.imshow(fourieReturn[0], cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(335),plt.imshow(fourieReturn[2], cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(338),plt.imshow(fourieReturn[3], cmap = 'gray')
        plt.title('Filtered Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(337),plt.imshow(fourieReturn[1], cmap = 'gray')
        plt.title('MouseView'), plt.xticks([]), plt.yticks([])

    if index == 1:
        plt.subplot(331),plt.imshow(fourieReturn[0], cmap = 'gray')
        plt.title('Sine Wave'), plt.xticks([]), plt.yticks([])
        plt.subplot(332),plt.imshow(fourieReturn[2], cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(333),plt.imshow(fourieReturn[4], cmap = 'gray')
        plt.title('Mask'), plt.xticks([]), plt.yticks([])



def rad2deg(x):
    return x * np.pi / 180.

def give_sinImg(img,nrOfCycles):
    img = np.copy(img)

    OldMax = img.shape[0]
    OldMin = 0
    NewMax = 360*nrOfCycles+90
    NewMin = 0

    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    

    for zeile in range(img.shape[1]):
        NewValue = (((zeile - OldMin) * NewRange) / OldRange) + NewMin
        wert = (np.sin(rad2deg(NewValue))+1)*(255.0/2.0)
        img[zeile][img.shape[1]/2] = wert
    return img




imgPath ='05spat.png'
imgPath ='passfoto.jpg'
#imgPath ='Landschaftsbild.jpg'

img = cv2.imread(imgPath,0)
img = img[0:np.amin(img.shape), 0:np.amin(img.shape)] 



windowSize = 8


"""
imgList = []
shapeList = []
for n in range(400,401):
    img = give_sinImg(np.empty([n,n]))
    img = img.astype(int)
    fourieReturn  = fourieMask(img, windowSize)
    fourieReturn[2] = fourieReturn[2].astype(int)
    imgList.append(fourieReturn[2])
    shapeList.append(n)

for index, img in enumerate(imgList):

    subplotNr = int("33"+str(index+1))
    plt.subplot(1,1,index+1)
    plt.imshow(img, cmap = 'gray')
    plt.title(NewMax), plt.xticks([]), plt.yticks([])

"""

sinImg = give_sinImg(np.empty(img.shape),10)

listOfFourieReturns =[]
for whichImg in [img, sinImg]:
    listOfFourieReturns.append(fourieMask(whichImg))

for index,fourieReturn in enumerate(listOfFourieReturns):
    give_plot(fourieReturn,index)
plt.show()



#img = np.ndarray(shape=(10,10), dtype=int)
#0 is schwarz
#255 is weiss




