#!/usr/bin/python

import time
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32, 1)

matrix.Fill(0xFFFFFF)
time.sleep(3.0)

matrix.Clear()