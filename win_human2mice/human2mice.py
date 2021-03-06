# -*- coding: utf-8 -*-
# Version: 171004
#Author: Christoph Neu

"""Usage: human2mice.exe (FILE) [-c int] [-k float] [-o str] 

Arguments:
  FILE                      Path to picture 
  
Options:
  -h --help                 Show this 
  -c <int>  cycle count     Number sine cycles per image (Default is 10)
  -k <float>  contrast      Images will be created with the choosen contrast reduction (between 1-0)(e.g. 0.5)
  -o <str>  output name     Name of the output Folder (Default is <input>_analysis)
                            Output is saved in same folder as input image
"""
"""
from docopt import docopt


arguments = docopt(__doc__)
"""
#arguments = {'-c': 10, '-k': 0.5, '-o': None, 'FILE': 'C:\\Users\\keks\\Dropbox\\Uni Jena\\3. semester\\Projektmodul - Bolz\\human2mice\\examples\\test\\05spat.png'}


import numpy as np
import cv2
import os
import ntpath


#arguments["FILE"] = os.path.abspath(arguments["FILE"])


def give_gui():
    import Tkinter as Tk
    import tkFileDialog

    def browse_file():
        global fname
        fname = tkFileDialog.askopenfilename()
        print "Selected File is:"
        print fname
        runBotton = Tk.Button(master = root, text = 'Run', width = 6, command=run_button)
        #runBotton.pack(side=Tk.LEFT, padx = 2, pady=2)    
        runBotton.grid(row=3, column=1)


    def run_button():
        global  var_c 
        var_c = c.get()
        global  var_k
        var_k =   k.get()
        root.quit()



    root = Tk.Tk()
    root.wm_title("mouse2human")

    T_c = Tk.Text(root, height=2, width=40)
    T_k = Tk.Text(root, height=3, width=40)
    c = Tk.Entry(root)

    k = Tk.Entry(root)


    broButton = Tk.Button(master = root, text = 'Browse', width = 6, command=browse_file)
    #broButton.pack(side=Tk.LEFT, padx = 2, pady=2)  

    #Anordnung
    c.grid(row=0, column=1)
    k.grid(row=1, column=1)
    broButton.grid(row=3, column=0)


    T_c.grid(row=0, column=0)
    T_c.insert(Tk.END, "Number sine cycles per image\n (Default is 10)")

    T_k.grid(row=1, column=0)
    T_k.insert(Tk.END, "Images will be created with the \nchoosen contrast reduction \n (Between 1-0) (e.g. 0.5) (Default is 1)")

    Tk.mainloop()

    #check validitaet
    global var_c
    global var_k
    if var_c == "":
        var_c= 10
    else:
        var_c= int(var_c)

    if var_k == "":
        var_k = 1
    else:
        var_k = float(var_k)


    return {'-c': var_c, '-k': var_k, '-o': None, 'FILE': fname}


def fourieMask(img,windowSize):

    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT) # macht die fourie transformatio
    dft_shift = np.fft.fftshift(dft) #Shift the zero-frequency component to the center of the spectrum.

    #gives the magnitute part of the dft
    #Briefly, the MAGNITUDE tells "how much" of a certain frequency component is present 
    #and the PHASE tells "where" the frequency component is in the image.
    #only magnitute is das wsa man sich fuer gewaehnlich anschaut (andre is wohl trippy)
    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1])+1)


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

    if windowSize != None:
        pass
    else:
        for index, value in enumerate(magnitude_spectrum[:,magnitude_spectrum.shape[1]/2]):
            if value == sorted(magnitude_spectrum[:,magnitude_spectrum.shape[1]/2])[-2]:
                windowSize = abs(crow-index)

    #print windowSize

            
        

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


    return [[img, img_back, magnitude_spectrum, magnitude_spectrum_masked, mask[:,:,1]],windowSize]

def give_plot(fourieReturn, index):
    if index == 1:
        plt.subplot(331),plt.imshow(fourieReturn[0], cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(332),plt.imshow(fourieReturn[2], cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(338),plt.imshow(fourieReturn[3], cmap = 'gray')
        plt.title('Filtered Mag.Spec.'), plt.xticks([]), plt.yticks([])
        plt.subplot(337),plt.imshow(fourieReturn[1], cmap = 'gray')
        plt.title('MouseView'), plt.xticks([]), plt.yticks([])

        if arguments["-k"] != None:

            plt.subplot(333),plt.imshow(fourieReturn[5], cmap = 'gray')
            plt.title('Input With Contr.'), plt.xticks([]), plt.yticks([])

            plt.subplot(339),plt.imshow(fourieReturn[6], cmap = 'gray')
            plt.title('MouseView Contr.'), plt.xticks([]), plt.yticks([])


    if index == 0:
        plt.subplot(334),plt.imshow(fourieReturn[5], cmap = 'gray')
        plt.title('Sine Wave'), plt.xticks([]), plt.yticks([])
        plt.subplot(335),plt.imshow(fourieReturn[2], cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(336),plt.imshow(fourieReturn[4], cmap = 'gray')
        plt.title('Mask'), plt.xticks([]), plt.yticks([])

def give_img(fourieReturn, index):


    if index == 1:
        n = 0
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')
        im.save("InputImage.png")

        n = 2
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('MagnitudeSpectrum.png')

        n = 3
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('MaskedMagnitudeSpectrum.png')

        n = 1
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('MouseViewWithoutContr.png')

        n = 5
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('InputViewWithContr.png')

        n = 6
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('MouseViewWithContr.png')


    if index == 0:
        n = 5
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('SineWave.png')

        n = 2
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('SineWaveMagnitudeSpectrum.png')

        n = 4
        fourieReturn[n] = (255.0 / fourieReturn[n].max() * (fourieReturn[n] - fourieReturn[n].min())).astype(np.uint8)
        im = Image.fromarray(fourieReturn[n]).convert('RGB')        
        im.save('Mask.png')

def deg2rad(x):
    return x * np.pi / 180.

def give_sinImg(img,nrOfCycles):
    img = np.copy(img)
    totalimg = np.copy(img)

    OldMax = img.shape[0]
    OldMin = 0
    NewMax = 360*nrOfCycles+90
    NewMin = 0

    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    

    for zeile in range(img.shape[1]):
        NewValue = (((zeile - OldMin) * NewRange) / OldRange) + NewMin
        wert = (np.sin(deg2rad(NewValue))+1)*(255.0/2.0)
        img[zeile][img.shape[1]/2] = wert

    for zeile in range(totalimg.shape[1]):
        NewValue = (((zeile - OldMin) * NewRange) / OldRange) + NewMin
        wert = (np.sin(deg2rad(NewValue))+1)*(255.0/2.0)
        totalimg[zeile][:] = wert
    return [img, totalimg]

def give_lowerContrast(img,contrastFactor):
    img = np.copy(img)

    mouseMin = int(255*float(0.5))-(int(255*float(contrastFactor/2.0)))
    mouseMax = int(255*float(0.5))+(int(255*float(contrastFactor/2.0)))

    def remap(value, OldMax,OldMin,NewMax,NewMin):
        OldRange = (OldMax - OldMin)  
        NewRange = (NewMax - NewMin)  
        
        value = int((((value - OldMin) * NewRange) / OldRange) + NewMin)
        
        return value

    """
    OldMax = img.max()
    OldMin =img.min()
    for lineIndex, line in enumerate(img[:,0]):
        for valueIndex, value in enumerate(img[lineIndex,:]):
            img[lineIndex,valueIndex] = remap(value,OldMax,OldMin,255,0)
    
    
    
    
    OldMax = img.max()
    OldMin =img.min()
    for lineIndex, line in enumerate(img[:,0]):
        for valueIndex, value in enumerate(img[lineIndex,:]):
            img[lineIndex,valueIndex] = remap(value,OldMax,OldMin,mouseMax,mouseMin)
    """

    NewRange = (mouseMax - mouseMin) 

    img = (255.0 / img.max() * (img - img.min())).astype(np.uint8)
    img = ((float(NewRange) / img.max() * (img - img.min()))+float(mouseMin)).astype(np.uint8)

    img[0,0] = 0
    img[0,1] = 255
   
    return img


#imgPath ='05spat.png'
#imgPath ='passfoto.jpg'
#imgPath ='Landschaftsbild.jpg'

arguments = give_gui()

if arguments["-c"] == None:
    arguments["-c"] = 10
else:
    arguments["-c"] = int(arguments["-c"])
if arguments["-o"] == None:
    print "alsdfk"
    arguments["-o"] = str(ntpath.basename(arguments["FILE"])).split(".")[0]+"_c"+str(arguments["-c"])
else:
    arguments["-o"] =  str(arguments["-o"])

if arguments["-k"] != None:
    arguments["-k"] = float(arguments["-k"])
os.chdir(os.path.dirname(arguments["FILE"]))


print "Image reading and cropping ..."
img = cv2.imread(arguments["FILE"],0)
img = img[0:np.amin(img.shape), 0:np.amin(img.shape)] 



print "Sine wave creating with cycle number of: ",str(arguments["-c"])," ..."
sinImgList = give_sinImg(np.empty(img.shape),arguments["-c"])
sinImg = sinImgList[0]


print "Fourier Transformation ..."
listOfFourieReturns =[]

fourieReturnAll =fourieMask(sinImg,None)
listOfFourieReturns.append(fourieReturnAll[0])
listOfFourieReturns.append(fourieMask(img,fourieReturnAll[1])[0])


print "Contrast Reduction ..."

if arguments["-k"] ==None:
    listOfFourieReturns[1].append(img) #Only in here for exe verseion with img save
    listOfFourieReturns[1].append(img) #Only in here for exe verseion with img save !Needs to be fixed
else:
    listOfFourieReturns[1].append(give_lowerContrast(img,arguments["-k"]))
    listOfFourieReturns[1].append(give_lowerContrast(listOfFourieReturns[1][1],arguments["-k"]))

listOfFourieReturns[0].append(sinImgList[1])

imgOrPlot = "plo"

if imgOrPlot == "plot":
    from matplotlib import pyplot as plt
    print "Image Creation of ",os.path.abspath(str(arguments["-o"]))
    for index,fourieReturn in enumerate(listOfFourieReturns):
        give_plot(fourieReturn,index)


    plt.savefig(str(arguments["-o"])+"_"+str(arguments["-c"])+"c", dpi=300,figsize=150)   
    #plt.show()
else:
    from PIL import Image
    counter = 0
    while counter < 100:
        counter+= 1
        try:
            os.mkdir(str(arguments["-o"])+"_"+str(counter))
            os.chdir(str(arguments["-o"])+"_"+str(counter))
            break
        except:
            pass

    for index,fourieReturn in enumerate(listOfFourieReturns):
        give_img(fourieReturn,index)

#img = np.ndarray(shape=(10,10), dtype=int)
#0 is schwarz
#255 is weiss


print "Finished !!!"

