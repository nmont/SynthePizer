#!/usr/bin/python

# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.
# Requires rgbmatrix.so present in the same directory.

import time
from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)

def draw_touch(counter, x, y, radius):
  r1 = 0b11111111
  r2 = 0
  g = 0
  b1 = 0b11111111
  b2 = 0

  tup1 = (x-1, x, x+1, x+1, x+1, x, x-1, x-1)
  tup2 = (y-1, y-1, y-1, y, y+1, y+1, y+1, y)
  for i in range(100):
    set_point(tup1[counter % 8], tup2[counter % 8], r1, b2)
    set_point(tup1[(counter + 1) % 8], tup2[(counter + 1) % 8], r1, b2)
    set_point(tup1[(counter + 2) % 8], tup2[(counter + 2) % 8], r1, b2)
    set_point(tup1[(counter + 3) % 8], tup2[(counter + 3) % 8], r1, b2)
    set_point(tup1[(counter + 4) % 8], tup2[(counter + 4) % 8], r2, b1)
    set_point(tup1[(counter + 5) % 8], tup2[(counter + 5) % 8], r2, b1)
    set_point(tup1[(counter + 6) % 8], tup2[(counter + 6) % 8], r2, b1)
    set_point(tup1[(counter + 7) % 8], tup2[(counter + 7) % 8], r2, b1)

    time.sleep(.5)
    matrix.Clear()
    counter += 1

def set_point(x, y, r, b):
  matrix.SetPixel(
    x,
    y,
    r,
    (2 * 0b001001001) / 2,
    b)

counter = 0

for x in range(1,12):
  draw_touch(counter, x, 10, 10)
  matrix.Clear()
