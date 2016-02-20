#!/usr/bin/python

# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.
# Requires rgbmatrix.so present in the same directory.

import time, Image, ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)
image = Image.open("nick.jpg")
image.load()
matrix.SetImage(image.im.id, 0, 0)

time.sleep(10)

matrix.Clear()
