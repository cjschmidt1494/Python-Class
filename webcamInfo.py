#!/usr/bin/env python
## Must have fileGrap.py
from fileGrab import *
import time
import numpy
import matplotlib.pyplot as plt

class webcamGet():
    def __init__(self):
        self.tuples = {}
    def gate(self,t):
        delta = time.time()-t  # Take difference between start of function and now
        if delta <= 1.0:
            sleep(1.0-delta)
        t = time.time() #redefine time
        return t
    
    def intensity(self,width,length):  #Find the average intensity of the image
        Sum = []
        xNum = []
        timeAxis = []
        zeroTime = time.time() # Start Time
        t = zeroTime
        for i in xrange(length): #iterate over specified time
            t = self.gate(t)  # Call Gate
            timeAxis.append(t)
            image = Webcam.grab_image_data(Webcam())
            averageTuple = 0
            for pixel in image:  #iterate through pixels
                averageTuple += sum(pixel)/3.0 #Average the value of tuple
            Sum.append(averageTuple/len(image))
            if length > 1:
                print i,'Complete'
        timeAxis[:] = [i-zeroTime for i in timeAxis] #Subtract away the zero time from each element
        return timeAxis,Sum,width,zeroTime

        
    def filterData(self,timeAxis,data,width,zeroTime):
        widthHalf = width/2
        filteredMean = []
        i = widthHalf
        stop = False
        while stop == False:
            window = data[i-widthHalf:i+widthHalf+1]
            average = sum(window)/width
            filteredMean.append(average)
            if i == len(data)-widthHalf-1:
                stop = True
            i += 1
        for i in xrange(widthHalf):  #Delete the time entries removed by filter
            del timeAxis[0]
            del timeAxis[-1]
        #timeAxis[:] = [i-zeroTime for i in timeAxis] #Subtract away the zero time from each element
        
        return timeAxis,filteredMean

    def dayTimeCheck(self):
        width = 1
        length = 1
        rawAxis, Sum, width, zeroTime = self.intensity(width,length)
        if Sum >= 70:
            return True
        elif Sum < 70:
            return False
        else:
            print 'Error in daytimeCheck()'
    def colorCheck(self):
        image = Webcam.grab_image_data(Webcam())
        for pixel in image:
            try:
                self.tuples[pixel] += 1
            except:
                self.tuples[pixel] = 1
        sortedTuples = sorted(self.tuples.items(), key=lambda x:x[1],reverse=True)
        mostCommon = sortedTuples[0]
        mostCommonColor = sortedTuples[0][0]
        mostCommonProportion = float(sortedTuples[0][1])/len(image)
        print 'Most Common Color: ',mostCommonColor
        print 'Most Common Color Proportion: ', mostCommonProportion
    def motionCheck(self):
        pixelSum = []
        image1 = Webcam.grab_image_data(Webcam())
        sleep(1)
        image2 = Webcam.grab_image_data(Webcam())
        
        for i in xrange(len(image1)):
            deltaPixel = ((image1[i][0]-image2[i][0])**2+(image1[i][1]-image2[i][1])**2+(image1[i][2]-image2[i][2])**2)**.5
            pixelSum.append(deltaPixel)
        delta = sum(pixelSum)/len(pixelSum)
        sortedPixelSum = sorted(pixelSum)
##        print sortedPixelSum[0:100]
##        plt.plot(range(len(sortedPixelSum)),sortedPixelSum)
##        plt.show()
    
        if delta >= 6:
            return True
        elif delta < 6:
            return False
        else:
            return 'Error in motionCheck()'
if __name__ == "__main__":
    w = webcamGet()
    width = 5
    length = 20
    #Check if it's daytime
    print 'It is daytime:',w.dayTimeCheck()
    
    #Check most common color
    w.colorCheck()

    #Check if motion
    print 'There is movement:',w.motionCheck()
    
    #Make Plot of intensity
    rawAxis, Sum, width, zeroTime = w.intensity(width,length)
    timeAxis,filteredMean = w.filterData(list(rawAxis),Sum,width,zeroTime)
    #Plot
    plt.plot(rawAxis,Sum,label='Raw')
    plt.plot(timeAxis,filteredMean,label='Filtered')
    plt.legend(loc=0)
    plt.title('MU Webcam Intensity')
    plt.xlabel('Time in seconds')
    plt.ylabel('Intensity')
    axis = plt.gca()
    axis.set_yticklabels(axis.get_yticks())
    plt.show()



    
    
