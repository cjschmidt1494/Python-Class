#!/usr/bin/env python

from grabber import Webcam
from PIL import ImageDraw

if __name__ == '__main__':
    webcam = Webcam()
    
    image = webcam.grab_image()
    image.show()

    pixels = image.load()
    for x in xrange(image.size[0]):
        for y in xrange(image.size[1]):
            pixels[x, y] = (pixels[x, y][2], pixels[x, y][0], pixels[x, y][1])
    print pixels[image.size[0]/2,image.size[1]/2]
    print pixels
    print type(pixels)
##    for i in xrange(20):
##        for j in xrange(20):
##            pixels[image.size[0]/2+i,image.size[1]/2+j] = (255,255,255)
##    print pixels[image.size[0]/2,image.size[1]/2]

    
    draw = ImageDraw.Draw(image)
    draw.line((0, 0) + image.size, fill=(0, 255, 0), width=10)
    draw.line((0, image.size[1], image.size[0], 0),
              fill = (0, 255, 0), width=10)
    draw.ellipse((200, 200, 400, 300), outline=(255, 0, 0))
    del draw
    image.show()
