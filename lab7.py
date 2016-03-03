#!/usr/bin/env python
from grabber import Webcam
from PIL import ImageDraw
from time import *
import numpy
import matplotlib.pyplot as plt

class webcamDraw():
    #def __init__(self):
       
    def makeImage(self): #Pulls an image file using grabber.py
        webcam = Webcam()
        image = webcam.grab_image()         
        pixels = image.load()
        return image,pixels # returns image and pixels
        
    def grass(self,image,pixels): #Turns grass blue
        for x in xrange(image.size[0]): #Iterate through x and y of the image
            for y in xrange(image.size[1]):
                #Get R,G,B values (+.0001 to avoid zero division)
                red = pixels[x,y][0]+.0001
                green = pixels[x,y][1]+.0001
                blue = pixels[x,y][2]+.0001
                #Make R,G,B ratios
                redRatio = red/(red+green+blue)
                greenRatio = green/(red+green+blue)
                blueRatio = blue/(red+green+blue)
                #Check if there is alot of green
                if greenRatio>.36: #greenRatio > blueRatio+.09 and greenRatio>redRatio+.02: #+.13,-.1
                    pixels[x,y] = (int(red/2.0),int(blue/1.0),int(green/1.0)) #Swaps green and blue to make realistic blue grass
                    #pixels[x,y] = (0,0,255)  #makes grass bright blue
        image.show()
                    
    def motionCheck(self): #Detects motion between two images
        movementList = []
        #Pull two images 1 second apart
        image1, pixels1 = self.makeImage()
        #image1.show()
        sleep(1)
        image2, pixels2 = self.makeImage()
        #image2.show()

        for x in xrange(image1.size[0]): #Iterate through X and y
            for y in xrange(image1.size[1]):
                #Caluculate difference between RGB values
                #(positive number = dark moving object aka person)
                deltaPixel = pixels1[x,y][0]-pixels2[x,y][0]+pixels1[x,y][1]-pixels2[x,y][1]+pixels1[x,y][2]-pixels2[x,y][2]
                if deltaPixel > 55: #movement threshhold
                    movementList.append(True) #Create a list of where there is movement
                    pixels2[x,y] = (255,0,0) #Turn the moving pixel bright red
                else:
                    movementList.append(False) #Show where there isn't movement
        #image2.show()
        self.bodyCheck(movementList,image2) #Find the people

    def bodyCheck(self,movementList,image2):#Draws a circle under people
        draw = ImageDraw.Draw(image2)
        #approx size of person
        height = 28 
        width = 9
        #Image size
        yWidth = image2.size[1]
        xWidth = image2.size[0]
        #draw.line((image2.size[0]/2,image2.size[1]/2,image2.size[0]/2+width,image2.size[1]/2+height), fill=(0,color,0), width=5)
        for y in xrange(yWidth):
            for x in xrange(xWidth): #Loop through X and Y
                if movementList[xWidth*y+x] == True: #If there is a movement pixel
                    trueValue = 0
                    for y2 in xrange(width): #loop through pixels in rectangle that is person sized
                        for x2 in xrange(height):
                            if movementList[(x+x2)+(y+y2)*yWidth] == True: 
                                trueValue += 1 #count number of true
                    totalCount = width*height #number of pixels in image
                    ratio = float(trueValue)/float(totalCount) #ratio of movement to non movement pixels
                    if ratio > .3: #if the rectangle has enough movement
                        #draw.line((y,x,y+width,x+height), fill=(0,color,0), width=5)
                        #Draw ellipse at base of rectangle
                        draw.ellipse((y,x+height-2,y+width*1.5,x+height+2), outline=(0, 0, 255))
                        for y3 in xrange(width): #loop through rectangle again
                            for x3 in xrange(height):
                                movementList[(x+x3)+(y+y3)*yWidth] = False #Reset rectangle to false to not repeat
                                pass
        image2.show()
 
        
if __name__ == '__main__':
    w = webcamDraw()

    image1, pixels1 = w.makeImage()
    w.grass(image1,pixels1)
    w.motionCheck()
