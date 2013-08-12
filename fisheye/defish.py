from SimpleCV import Display, Image, Color
import cv2
import numpy as np
import time

def spliceImg(img):
    section = img.width/4;
    retVal = []
    for i in range(0,4):
        temp = img.crop(section*i,0,section,img.height)
        mask = temp.threshold(10)
        b = temp.findBlobsFromMask(mask)
        retVal.append(b[-1].hullImage())
    return retVal

def buildMap(Ws,Hs,Wd,Hd):
    map_x = np.zeros((Hd,Wd),np.float32)
    map_y = np.zeros((Hd,Wd),np.float32)
    fov = 1.0*np.pi
    count = 0
    for y in range(0,int(Hd-1)):
        for x in range(0,int(Wd-1)):
            count = count + 1
            phi = fov*((float(x)/float(Wd)))
            theta = fov*((float(y)/float(Hd)))
            yp = (np.sin(theta)*np.sin(phi)+1.0)/2.0#
            xp = (np.sin(theta)*np.cos(phi)+1.0)/2.0
            zp = (np.cos(theta)+1.0)/2.0# 
            xS = Ws-(xp*Ws)
            yS = Hs-(zp*Hs)
            map_x.itemset((y,x),int(xS))
            map_y.itemset((y,x),int(yS))
        
    return map_x, map_y

def unwarp(img,xmap,ymap):
    output = cv2.remap(img.getNumpyCv2(),xmap,ymap,cv2.INTER_LINEAR)
    result = Image(output,cv2image=True)
    return result


img = Image('fisheye1.jpg')
sections = spliceImg(img)
temp = sections[0]

Ws = temp.width
Hs = temp.height
Wd = temp.width
Hd = temp.height
print "BUILDING MAP"
mapx,mapy = buildMap(Ws,Hs,Wd,Hd)
print "MAP DONE"
defished = []

for s,idx  in zip(sections,range(0,len(sections))):
    result = unwarp(s,mapx,mapy)
    temp = result.sideBySide(s)
    temp.save("View{0}.png".format(idx))
    result.save("DeWarp{0}.png".format(idx))
    temp.show()
    time.sleep(3)