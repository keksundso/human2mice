import math
import numpy as np
d = 100
s = 30
c = 0.8

def rad2deg(x):
    return x *   180. /np.pi
wd = math.sqrt(math.pow(d,2)+math.pow(s/2,2))


degreeOfScreen = rad2deg(np.arccos(((2*math.pow(wd,2))-(math.pow(s,2)))/(2*pow(wd,2))))

print  "Grad eines ganzen Bildschrims:                 ",degreeOfScreen
print  "Fure ",c," cyclen per degree braucht man also: ", str(degreeOfScreen*c)