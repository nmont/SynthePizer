#!/usr/bin/python

# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.
# Requires rgbmatrix.so present in the same directory.

import time
from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)

def draw_touch(x, y, radius):
  r1 = 0b11111111
  r2 = 0
  g = 0
  b1 = 0b11111111
  b2 = 0
  for i in range(100):
    set_point(x-1, y-1, r1, b2)
    set_point(x-1, y+1, r2, b1)
    set_point(x+1, y-1, r1, b2)
    set_point(x+1, y+1, r2, b1)

    time.sleep(.2)
    matrix.Clear()

    set_point(x-1, y, r1, b2)
    set_point(x, y+1, r2, b1)
    set_point(x+1, y, r1, b2)
    set_point(x, y-1, r2, b1)

    time.sleep(.075)
    matrix.Clear()
	
def set_point(x, y, r, b):
  matrix.SetPixel(
    x,
    y,
    r,
    (2 * 0b001001001) / 2,
    b)


for x in range(1:12):
  draw_touch(x, 10, 10)
  matrix.Clear()
