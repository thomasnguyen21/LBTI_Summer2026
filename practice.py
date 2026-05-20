from astropy.io import fits
import numpy as np
#open fits function
file1= fits.open('lm_260429_000162.fits')
#header 
print(len(file1))
file1.info()
#data of fits(w x h x d)
print(file1[0].data.shape)
#actual number of data 
print(file1[0].data.size)
#specific pixel data
print(file1[0].data[0,500,500])
#specific region of data
print(file1[0].data[0,1024:1034, 1024:1034])
#data in number of frames 
frame30 = file1[0].data[29]
print(frame30.min())
print(frame30.max())
print(frame30.mean())
#all frames data
print(file1[0].data[:,1024,1024])
#all pixels one frames
print(file1[0].data[10,:,:])
#highest average frame for all pixels 
means =  [] #create a list
for i in range(30):
    file1[0].data[i].mean()
    means.append(file1[0].data[i].mean()) #store data to the list created
    
print("max average is=", max(means))
print("frame is= ", means.index(max(means)))

#printing header cards
print(file1[0].header['OBJNAME'])
print(file1[0].header['DATE-OBS'])
print(file1[0].header['DETTEMP'])
#average between 2 frames 
avg1= file1[0].data[0].mean()
avg2 =file1[0].data[29].mean()

print(avg1)
print(avg2)
if avg1 > avg2:
    print("frame 1 is the highest:",avg1)
else:
    print("frame 2 is the highest =",avg2)
