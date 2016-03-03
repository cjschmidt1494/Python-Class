#!/usr/bin/env python
from grabber import Webcam
from PIL import ImageDraw
from time import *
import numpy
import matplotlib.pyplot as plt

class webcamDraw():
    #def __init__(self):
       
    def makeImage(self):
        webcam = Webcam()
        
        image = webcam.grab_image()         
        pixels = image.load()
        return image,pixels
        
    def grass(self,image,pixels):
##        for i in xrange(20):
##            for j in xrange(20):
##                print pixels[image.size[0]/2+i,image.size[1]/2+j]
##                pixels[image.size[0]/2+i,image.size[1]/2+j] = (255,255,255)
##        print pixels[image.size[0]/2,image.size[1]/2]
        
        for x in xrange(image.size[0]):
            for y in xrange(image.size[1]):
                red = pixels[x,y][0]+.0001
                green = pixels[x,y][1]+.0001
                blue = pixels[x,y][2]+.0001
                
                redRatio = red/(red+green+blue)
                greenRatio = green/(red+green+blue)
                blueRatio = blue/(red+green+blue)
        
                if greenRatio>.36: #greenRatio > blueRatio+.09 and greenRatio>redRatio+.02: #+.13,-.1
##                    print redRatio
##                    print greenRatio
##                    print blueRatio
##                    print ''
                    pixels[x,y] = (int(red/2.0),int(blue/1.0),int(green/1.0))
                    #pixels[x,y] = (0,0,255)
        image.show()
                    
    def motionCheck(self):
        pixelSum = []
        moveX = []
        moveY = []
        movementList = []
        
        image1, pixels1 = self.makeImage()
        #image1.show()
        sleep(1)
        image2, pixels2 = self.makeImage()
        #image2.show()

        for x in xrange(image1.size[0]):
            for y in xrange(image1.size[1]):
                deltaPixel = pixels1[x,y][0]-pixels2[x,y][0]+pixels1[x,y][1]-pixels2[x,y][1]+pixels1[x,y][2]-pixels2[x,y][2]
                if deltaPixel > 55:
                    movementList.append(True)
                    pixels2[x,y] = (255,0,0)
                    #moveX.append(x)
                    #moveY.append(y)
                else:
                    movementList.append(False)
                    #moveX.append(x)
                    #moveY.append(y)
                pixelSum.append(deltaPixel)      
        #image2.show()
        self.bodyCheck(movementList,image2)

    def bodyCheck(self,movementList,image2):
        draw = ImageDraw.Draw(image2)
        height = 28
        width = 9
        color = 20
        yWidth = image2.size[1]
        xWidth = image2.size[0]
        #draw.line((image2.size[0]/2,image2.size[1]/2,image2.size[0]/2+width,image2.size[1]/2+height), fill=(0,color,0), width=5)
        #Find Boundary of rectangle
        print 'start body check'
        for y in xrange(yWidth):
            for x in xrange(xWidth): #Loop through X and Y movementList
                if movementList[xWidth*y+x] == True:#If True
                    trueValue = 0
                    for y2 in xrange(width): #loop through pixels in rectange
                        for x2 in xrange(height):
                            if movementList[(x+x2)+(y+y2)*yWidth] == True:
                                trueValue += 1 #count number of true
                    totalCount = width*height
                    ratio = float(trueValue)/float(totalCount)
                    #print 'ratio: ',ratio
                    if ratio > .3:
                        print 'person'
                        #draw.line((y,x,y+width,x+height), fill=(0,color,0), width=5)
                        #Draw ellipse at base of rectangle
                        draw.ellipse((y,x+height-2,y+width*1.5,x+height+2), outline=(0, 0, 255))
                        for y3 in xrange(width): #write all in rectangle to false
                            for x3 in xrange(height): #Loop through X and Y movementList
                                movementList[(x+x3)+(y+y3)*yWidth] = False
                                pass
        image2.show()
 
        
if __name__ == '__main__':
    w = webcamDraw()

    #image1, pixels1 = w.makeImage()
    #w.grass(image1,pixels1)
    w.motionCheck()
