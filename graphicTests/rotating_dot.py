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
       
        for i in range(100):
                set_point(x-1, y-1)
                set_point(x-1, y+1)
                set_point(x+1, y-1)
                set_point(x+1, y+1)
        
                time.sleep(.2)
                matrix.Clear()
                
                set_point(x-1, y)
                set_point(x, y+1)
                set_point(x+1, y)
                set_point(x, y-1)
                
                time.sleep(.2)
                matrix.Clear()
	
def set_point(x, y):

        matrix.SetPixel(
          x,
          y,
          (2 * 0b001001001) / 2,
          (2 * 0b001001001) / 2,
          2 * 0b00010001)


for x in range(0,12):

        draw_touch(x, 10, 10)
        matrix.Clear()

