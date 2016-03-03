#!/usr/bin/env python
from urllib2 import urlopen
from time import sleep,time
from tempfile import mkstemp
import sys
from PIL import Image


# Interface to the Oregon State University webcams.  This should work
# with any web-enabled AXIS camera system.
class Webcam:
    # The default URL is the MU webcam
    def __init__(self, url='http://mu.webcam.oregonstate.edu'):
        fd,self.path = mkstemp()
        self.url = url

    # Save the latest image to a named file.  The image will be saved
    # as a jpeg.
    def save_image(self, filename):
        with open(filename, 'w') as f:
            webcam = urlopen('{0}/axis-cgi/jpg/image.cgi'.format(self.url))
            f.write(webcam.read())
        
    # Grab the latest image from the camera and return it as a PIL
    # Image.  To ease the conversion, we use an intermediate file for
    # this.
    def grab_image(self):
        self.save_image(self.path)
        return Image.open(self.path)

    # Return the pixel data from the latest image as a list of (r, g,
    # b) tuples.
    def grab_image_data(self):
        return list(self.grab_image().getdata())

        
if __name__ == '__main__':
    # It's often a good idea to tell us how to use a Python script
    if len(sys.argv) != 2:
        print 'Usage:', sys.argv[0], '<filename>'
        exit(0)

    webcam = Webcam()
    try:
        webcam.save_image(sys.argv[1])
        print 'Image saved to file', sys.argv[1]
    except:
        print 'Could not save image to file', sys.argv[1]

    print sys.argv[1]
    print sys.argv[0]
