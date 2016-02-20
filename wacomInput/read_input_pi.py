#!/usr/bin/python -u

# the -u flag makes python not buffer stdios


import os
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
                        fraw_x = float(raw_x)
                        fraw_y = float(raw_y)
                        if (len(split_line) >= 5): 
                                raw_pressure = split_line[3].split("=")[1]
                                fraw_pressure = float(raw_pressure)
                                print ("X = " + str((fraw_x / 296.875)) + ", Y = " + str((fraw_y / 296.875)) + ", pressure = " + str(fraw_pressure / 1024))
                        else:
                                print ("X = " + str((fraw_x / 296.875)) + ", Y = " + str((fraw_y / 296.875)))
                                
