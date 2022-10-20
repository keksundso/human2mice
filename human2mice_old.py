from PIL import Image
from PIL import ImageFilter
import pickle
import os

#viscodeDockerTest
################## Parameters

#ImagePath= '60spat.bmp'
#ImagePath= 'passfoto.jpg'
ImagePath= 'Landschaftsbild.jpg'
ContrastResFactor= 2
BlurRadius = 11

################## Magic
ImagePath=os.path.abspath(ImagePath)

os.chdir(os.path.dirname(ImagePath))

title= os.path.basename(ImagePath).split(".")[0]
try:
    os.mkdir(str(title)+"_output")
except:
    pass
os.chdir(str(title)+"_output")



col_cim=Image.open(ImagePath,'r')


im = col_cim.convert("L")
pickle.dump(im, open( "save.p", "wb" ) )

b = im.load()
def give_dim(b):
    for n in range(10000):
        try:
            b[1,n]
        except :
            ydim = n-1
            break

    for n in range(10000):
        try:
            b[n,1]
        except :
            xdim = n-1
            break
    return (xdim,ydim)

def give_scaledValue(factor, value):
    percent = float(value)/255.0
    UpperLimit = 255/factor
    Slider = (255 - int(UpperLimit))/2
    NewValue = percent * UpperLimit

    return int(NewValue) + Slider

dim = give_dim(b)
xdim = dim[0]
ydim = dim[1]

print xdim
print ydim


for Zeile in range(ydim):
    for Spalte in range(xdim):
        b[Spalte,Zeile] = give_scaledValue(ContrastResFactor, b[Spalte,Zeile])

im.save("Out_ContrastRes_"+str(title)+".png")

#####################Spatial Resolution

png = Image.open("Out_ContrastRes_"+str(title)+".png")
blurred_image = im.filter(ImageFilter.GaussianBlur((BlurRadius)))

################### Collage Creation and Pic saves (Exept ContrastRes is saved above)

BW_im = pickle.load( open( "save.p", "rb" ) )
os.remove("save.p")
blank_image = Image.new("RGB", (xdim*4, ydim))
blank_image.paste(col_cim, (0,0))
blank_image.paste(BW_im, (xdim,0))
blank_image.paste(im, (xdim*2,0))
blank_image.paste(blurred_image, (xdim*3,0))

out = im.resize((xdim/10,ydim/10), Image.ANTIALIAS)
out.show()


BW_im.save("Out_BW_"+str(title)+".png")
blurred_image.save("Out_Blurred_"+str(title)+".png")
blank_image.save("Out_Collage_"+str(title)+".png")
