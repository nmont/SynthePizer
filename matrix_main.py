#!/usr/bin/python
 
# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.
# Requires rgbmatrix.so present in the same directory.
 
import time
from rgbmatrix import Adafruit_RGBmatrix
 
# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)
 
# Flash screen red, green, blue (packed color values)
for x in range(32):
	for y in range(32):
		matrix.SetPixel(
		  x,
		  y,
		  (2 * 0b001001001) / 2,
		  (2 * 0b001001001) / 2,
		   2 * 0b00010001)
		time.sleep(0.2)

time.sleep(10.0)
matrix.Clear()