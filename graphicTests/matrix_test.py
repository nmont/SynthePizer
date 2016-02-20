#!/usr/bin/python

# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.
# Requires rgbmatrix.so present in the same directory.

import time, Image, ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32,1)

# Rows and chain length are both required parameters:
image = Image.open("../assets/mainmenu.jpg")
image.load()          # Must do this before SetImage() calls
matrix.SetImage(image.im.id, 0, 0)
time.wait(10)

matrix.Clear()
