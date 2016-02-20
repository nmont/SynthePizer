#!/usr/bin/python

# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.
# Requires rgbmatrix.so present in the same directory.

import time, Image, ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)
image = Image.new("1", (32, 32)) 
draw  = ImageDraw.Draw(image)    


# Show RGB test pattern (separate R, G, B color values)
#for i in range(0,31):
#	draw.text((i, 16), "hey", fill=1)
draw.rectangle((0, 0, 31, 31), fill=0, outline=1)
draw.line((0, 0, 31, 31), fill=1)
draw.line((0, 31, 31, 0), fill=1)


time.sleep(10.0)
matrix.Clear()