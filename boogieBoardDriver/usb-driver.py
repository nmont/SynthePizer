#!/usr/bin/env python

import usb.core
import usb.util
import sys
import Image
import ImageDraw
#from test_audio import Audio
from evdev import UInput, AbsInfo, ecodes as e
from time import sleep
from numpy import floor
from rgbmatrix import Adafruit_RGBmatrix
import signal
import sys

# recognizing SIGING (ctrl + c)
def signal_handler(signal, frame):
        usb.util.release_interface(dev, 0)
        usb.util.release_interface(dev, 1)
        dev.attach_kernel_driver(0)
        dev.attach_kernel_driver(1)
	print('Cancelling Awesomeness')
        sys.exit(0)

def draw_touch(counter, x, y, stylusButtonDown):
  r1 = 0b11111111
  r2 = 0
  g = 0
  b1 = 0b11111111
  b2 = 0

  # tuples of xy inputs for ring cursor
  tup1 = (x-1, x, x+1, x+1, x+1, x, x-1, x-1)
  tup2 = (y-1, y-1, y-1, y, y+1, y+1, y+1, y)

  # light up the middle if the stylus button is down
  if stylusButtonDown:
    matrix.SetPixel(x, y, 255, 255, 255)

  # cursor ring
  matrix.SetPixel(tup1[(counter + 1) % 8], tup2[(counter + 1) % 8], r1, 0, b2)
  matrix.SetPixel(tup1[(counter + 2) % 8], tup2[(counter + 2) % 8], r1, 0, b2)
  matrix.SetPixel(tup1[(counter + 3) % 8], tup2[(counter + 3) % 8], r1, 0, b2)
  matrix.SetPixel(tup1[(counter + 4) % 8], tup2[(counter + 4) % 8], r2, 0, b1)
  matrix.SetPixel(tup1[(counter + 5) % 8], tup2[(counter + 5) % 8], r2, 0, b1)
  matrix.SetPixel(tup1[(counter + 6) % 8], tup2[(counter + 6) % 8], r2, 0, b1)
  matrix.SetPixel(tup1[(counter + 7) % 8], tup2[(counter + 7) % 8], r2, 0, b1)
 # a = Audio("didgi-7.wav")
 # a.play(True)
  sleep(0.05)

# ============== MAIN ==========================

matrix = Adafruit_RGBmatrix(32, 1)
signal.signal(signal.SIGINT, signal_handler)

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

#state variables
MAIN_MENU = "MAIN_MENU"
DRAW = "DRAW"
SELECT_INSTRUMENT = "SELECT_INSTRUMENT"
state = MAIN_MENU

main_image = Image.open("../assets/mainmenu.jpg")
dick_butt_right_image = Image.open("../assets/dickbuttright.jpg")
dick_butt_left_image = Image.open("../assets/dickbuttleft.jpg")

image_array = [dick_butt_right_image, dick_butt_left_image]
num_images = len(image_array)
image_count = 0
is_touched = False

while True:
    try:
      #bring in data from the boogie board
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
    
    # determine state
    # main menu state
    if state = MAIN_MENU:
    # draw state
    if state == DRAW:
      draw_touch(counter, xpos, ypos, stylus)
      counter = (counter + 1) % 8
      matrix.Clear()
      
    #select state
    elif state == SELECT_INSTRUMENT:
      matrix.Clear()
      # draw the image
      image_array[image_count].load()          
      matrix.SetImage(image_array[image_count].im.id, 0, 0)
      if touch:
        draw_touch(counter, xpos, ypos, stylus)
        counter = (counter + 1) % 8
        # scroll through selections
        if xpos > 16 and stylus and not is_touched:
          is_touched = True
          image_count = (image_count + 1) % num_images
        elif xpos <= 16 and stylus and not is_touched:
          is_touched = True
          image_count = (image_count - 1) % num_images
        elif not stylus and is_touched:
          is_touched = False



    sleep(0.02)

usb.util.release_interface(dev, 0)
usb.util.release_interface(dev, 1)
dev.attach_kernel_driver(0)
dev.attach_kernel_driver(1)
