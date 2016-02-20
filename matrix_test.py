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
draw.text((0, 16), "Fuck you bowler", fill=1)

for n in range(-128, 128): # Start off top-left, move off bottom-right
	matrix.Clear()
	# IMPORTANT: *MUST* pass image ID, *NOT* image object!
	matrix.SetImage(image.im.id, -n, 0)
	time.sleep(0.05)


matrix.Clear()
