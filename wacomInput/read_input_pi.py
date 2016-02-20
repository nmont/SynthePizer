#!/usr/bin/python -u

# the -u flag makes python not buffer stdios


import os
import math
from rgbmatrix import Adafruit_RGBmatrix
from subprocess import Popen

_read, _write = os.pipe()

# I tried os.fork() to see if buffering was happening
# in subprocess, but it isn't

#if not os.fork():
#    os.close(_read)
#    os.close(1) # stdout
#    os.dup2(_write, 1)
#
#    os.execlp('xinput', 'xinput', 'test', '11')
#    os._exit(0) # Should never get eval'd

write_fd = os.fdopen(_write, 'w', 0)
proc = Popen(['xinput', 'test', 'Wacom Intuos PT S Pen'], stdout = write_fd)

os.close(_write)

matrix = Adafruit_RGBmatrix(32, 1)

# when using os.read() there is no readline method
# i made a generator
def read_line():
        line = []
        while True:
                c = os.read(_read, 1)
                if not c: raise StopIteration
                if c == '\n':
                        yield "".join(line)
                        line = []
                        continue
                line += c

readline = read_line()

for each in readline:
        split_line = each.split(" ")
        if (len(split_line) >= 4):
                if not split_line[0] == "button":
                        raw_x = split_line[1].split("=")[1]
                        raw_y = split_line[2].split("=")[1]
                        fraw_x = math.floor(float(raw_x) / 296.875)
                        fraw_y = math.floor(float(raw_y) / 296.875)

                        if (len(split_line) >= 5): 
                                raw_pressure = split_line[3].split("=")[1]
                                fraw_pressure = math.floor(float(raw_pressure) / 1024)
                                matrix.SetPixel(
                                  int(fraw_x),
                                  int(fraw_y),
                                  (2 * 0b001001001) / 2,
                                  (2 * 0b001001001) / 2,
                                   2 * 0b00010001)
                                # print ("X = " + str((fraw_x / 296.875)) + ", Y = " + str((fraw_y / 296.875)) + ", pressure = " + str(fraw_pressure / 1024))
                        else:
                                matrix.SetPixel(
                                  int(fraw_x),
                                  int(fraw_y),
                                  (2 * 0b001001001) / 2,
                                  (2 * 0b001001001) / 2,
                                   2 * 0b00010001)
                                # print ("X = " + str((fraw_x / 296.875)) + ", Y = " + str((fraw_y / 296.875)))
                                