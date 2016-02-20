#!/usr/bin/env python

import usb.core
import usb.util
import sys
from evdev import UInput, AbsInfo, ecodes as e
from time import sleep
from numpy import floor
from rgbmatrix import Adafruit_RGBmatrix

def draw_touch(counter, x, y):
  r1 = 0b11111111
  r2 = 0
  g = 0
  b1 = 0b11111111
  b2 = 0

  tup1 = (x-1, x, x+1, x+1, x+1, x, x-1, x-1)
  tup2 = (y-1, y-1, y-1, y, y+1, y+1, y+1, y)
  #set_point(x, y, r1, b2)
  set_point(tup1[counter], tup2[counter], r1, b2)
  set_point(tup1[(counter + 1) % 8], tup2[(counter + 1) % 8], r1, b2)
  set_point(tup1[(counter + 2) % 8], tup2[(counter + 2) % 8], r1, b2)
  set_point(tup1[(counter + 3) % 8], tup2[(counter + 3) % 8], r1, b2)
  set_point(tup1[(counter + 4) % 8], tup2[(counter + 4) % 8], r2, b1)
  set_point(tup1[(counter + 5) % 8], tup2[(counter + 5) % 8], r2, b1)
  set_point(tup1[(counter + 6) % 8], tup2[(counter + 6) % 8], r2, b1)
  set_point(tup1[(counter + 7) % 8], tup2[(counter + 7) % 8], r2, b1)
  #print("Here\n")
  sleep(0.05)


def set_point(x, y, r, b):
  matrix.SetPixel(
    x,
    y,
    r,
    (2 * 0b001001001) / 2,
    b)


matrix = Adafruit_RGBmatrix(32, 1)

# find our device
dev = usb.core.find(idVendor=0x2914, idProduct=0x0100)
if dev.is_kernel_driver_active(1):
    dev.detach_kernel_driver(1)
if dev.is_kernel_driver_active(0):
    try:
        dev.detach_kernel_driver(0)
    except:
        dev.attach_kernel_driver(1)

#dev.set_configuration()
#usb.util.claim_interface(dev, 1)
#usb.util.claim_interface(dev, 0)

# knock into tablet mode
payload = '\x05\x00\x03'
while True:
    try:
        assert dev.ctrl_transfer(0x21, 0x09, 0x0305, 1, payload, 100) == len(payload)
        break
    except usb.USBError as err:
        if err.args != (110, 'Operation timed out') and err.args != (32, 'Pipe error'):
            raise err
        print('payload transfer failed, retrying')
print('Payload sent')

# Pull out interrupt endpoint
cfg = dev[0]
intf = cfg[(1,0)]
ep = intf[0]

# Maximum position possible
minxpos = 0
minypos = 0
maxxpos = 19780
maxypos = 13442
minpressure = 0
maxpressure = 255

counter = 0

try:
    while True:
        try:
            data = ep.read(8, 100)
        except usb.USBError as err:
            if err.args != (110, 'Operation timed out'):
                raise err
            continue

        xpos = data[1] | data[2] << 8
        ypos = data[3] | data[4] << 8

        if xpos < minxpos:
            minxpos = xpos
            print('updated minxpos to %d' % minxpos)
        if xpos > maxxpos:
            maxxpos = xpos
            print('updated maxxpos to %d' % maxxpos)
        if ypos < minypos:
            minypos = ypos
            print('updated minypos to %d' % minypos)
        if ypos > maxypos:
            maxypos = ypos
            print('updated maxypos to %d' % maxypos)

        pressure = data[5] | data[6] << 8
        touch = data[7] & 0x01
        stylus = (data[7] & 0x02)>>1
        
        xpos = int(floor(xpos / (maxypos / 32)))
        ypos = int(floor(ypos / (maxypos / 32)))
        
        #print('xpos: %5d ypos: %5d pressure: %3d' % (xpos, ypos, pressure))
        draw_touch(counter, xpos, ypos)
        counter = (counter + 1) % 8
        # sleep(5)
        matrix.Clear()
        # print('touch: %d stylus %d' % (touch, stylus))
except KeyboardInterrupt:
    pass

usb.util.release_interface(dev, 0)
usb.util.release_interface(dev, 1)
dev.attach_kernel_driver(0)
dev.attach_kernel_driver(1)
