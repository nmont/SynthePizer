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
matrix.Fill(0xFF0000)
time.sleep(1.0)
matrix.Fill(0x00FF00)
time.sleep(1.0)
matrix.Fill(0x0000FF)
time.sleep(1.0)

# Show RGB test pattern (separate R, G, B color values)
for i in range(0,31):
	SetPixel(i, 16, 255, 255, 255)
	if i > 0: 
		SetPixel(i-1, 16, 200, 200, 200)
	if i > 1
		SetPixel(i-2, 16, 100, 100, 100)
	time.sleep(0.1)
	matrix.clear()

time.sleep(10.0)
matrix.Clear()