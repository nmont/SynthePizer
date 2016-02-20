#!/usr/bin/python

import time
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32, 1)
xCoord = ''
yCoord = ''
pressureValue = ''
shouldLightUpRight = false
shouldLightUpLeft = false


def parseX(x):
	if (x > 41.6):
		xCoord = 32
		shouldLightUpRight = True
	elif (x < 9.6):
		xCoord = -32
		shouldLightUpLeft = True
	else:
		xCoord = int(x)

def parseTouch(x, y, pressure):
	parseX(x)
	yCoord = int(y)

def lightUpRight(x, y):
	for yPixel in range(32):
		matrix.SetPixel(x, yPixel, 1, 0, 0)
	matrix.SetPixel(x - 1, y, 1, 0, 0)

parseTouch(50, 12)

if (shouldLightUpRight):
	lightUpRight(xCoord, yCoord)

time.sleep(3.0)

matrix.Clear()