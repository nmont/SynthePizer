#!/usr/bin/python

# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.
# Requires rgbmatrix.so present in the same directory.

import time, Image, ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32,1)

# Rows and chain length are both required parameters:
image = Image.open("nick.jpg")
image.load()          # Must do this before SetImage() calls
matrix.Fill(0x6F85FF) # Fill screen to sky color
for n in range(32, -image.size[0], -1): # Scroll R to L
          matrix.SetImage(image.im.id, n, 0)
          time.sleep(0.025)

matrix.Clear()
