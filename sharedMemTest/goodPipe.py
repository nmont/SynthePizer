# FROM TOUCHPAD INPUT
import os 
import time
import usb.core
import usb.util
import sys
import Image
import ImageDraw
from evdev import UInput, AbsInfo, ecodes as e
from time import sleep
from rgbmatrix import Adafruit_RGBmatrix
from signal import signal, SIGPIPE, SIG_DFL, SIGINT


# FROM AUDIO PLAYBACK
from pyaudio import PyAudio, paContinue, paFloat32
from numpy import array, random, arange, float32, float64, zeros, fromstring, vectorize, int16, floor
import wave

r,w=os.pipe()
r,w=os.fdopen(r,'r',0), os.fdopen(w,'w',0)
signal(SIGPIPE,SIG_DFL)

pid = os.fork()

# Music Playing Stuff
if pid:          # Parent
    w.close()

    ################################# Change the Volume ############################
    volume = 1.0
    pitch = 15
    data_pos = 0
    instrument = "trombone"

    def update_volume(v):
        global data_pos, volume, pitch
        volume = v

    def increment_volume(s, f):
        global data_pos, volume, pitch
        volume += 0.1
        print("up " + str(volume))

    def decrement_volume(s, f):
        global data_pos, volume, pitch
        volume -= 0.1
        print("down " + str(volume))

    def increment_pitch(s, f):
        global data_pos, volume, pitch
        pitch += 1
        print("up " + str(volume))

    def decrement_pitch(s, f):
        global data_pos, volume, pitch
        pitch -= 1
        print("down " + str(volume))

# signal.signal(signal.SIGQUIT, increment_volume) # CTRL+\
# signal.signal(signal.SIGTSTP, decrement_volume) # CTRL+z
# signal.signal(signal.SIGQUIT, increment_pitch) # CTRL+\
# signal.signal(signal.SIGTSTP, decrement_pitch) # CTRL+z

################################# Play the Audio ###############################
    
    waves = {"trombone":[None]*33, "didgeridoo":[None]*33, "organ":[None]*33}

    

    waves["trombone"][1]  = wave.open('../didgeridoo/trombone/trombone-01.wav', 'rb')
    waves["trombone"][2]  = wave.open('../didgeridoo/trombone/trombone-02.wav', 'rb')
    waves["trombone"][3]  = wave.open('../didgeridoo/trombone/trombone-03.wav', 'rb')
    waves["trombone"][4]  = wave.open('../didgeridoo/trombone/trombone-04.wav', 'rb')
    waves["trombone"][5]  = wave.open('../didgeridoo/trombone/trombone-05.wav', 'rb')
    waves["trombone"][6]  = wave.open('../didgeridoo/trombone/trombone-06.wav', 'rb')
    waves["trombone"][7]  = wave.open('../didgeridoo/trombone/trombone-07.wav', 'rb')
    waves["trombone"][8]  = wave.open('../didgeridoo/trombone/trombone-08.wav', 'rb')
    waves["trombone"][9]  = wave.open('../didgeridoo/trombone/trombone-09.wav', 'rb')
    waves["trombone"][10] = wave.open('../didgeridoo/trombone/trombone-10.wav', 'rb')
    waves["trombone"][11] = wave.open('../didgeridoo/trombone/trombone-11.wav', 'rb')
    waves["trombone"][12] = wave.open('../didgeridoo/trombone/trombone-12.wav', 'rb')
    waves["trombone"][13] = wave.open('../didgeridoo/trombone/trombone-13.wav', 'rb')
    waves["trombone"][14] = wave.open('../didgeridoo/trombone/trombone-14.wav', 'rb')
    waves["trombone"][15] = wave.open('../didgeridoo/trombone/trombone-15.wav', 'rb')
    waves["trombone"][16] = wave.open('../didgeridoo/trombone/trombone-16.wav', 'rb')
    waves["trombone"][17] = wave.open('../didgeridoo/trombone/trombone-17.wav', 'rb')
    waves["trombone"][18] = wave.open('../didgeridoo/trombone/trombone-18.wav', 'rb')
    waves["trombone"][19] = wave.open('../didgeridoo/trombone/trombone-19.wav', 'rb')
    waves["trombone"][20] = wave.open('../didgeridoo/trombone/trombone-20.wav', 'rb')
    waves["trombone"][21] = wave.open('../didgeridoo/trombone/trombone-21.wav', 'rb')
    waves["trombone"][22] = wave.open('../didgeridoo/trombone/trombone-22.wav', 'rb')
    waves["trombone"][23] = wave.open('../didgeridoo/trombone/trombone-23.wav', 'rb')
    waves["trombone"][24] = wave.open('../didgeridoo/trombone/trombone-24.wav', 'rb')
    waves["trombone"][25] = wave.open('../didgeridoo/trombone/trombone-25.wav', 'rb')
    waves["trombone"][26] = wave.open('../didgeridoo/trombone/trombone-26.wav', 'rb')
    waves["trombone"][27] = wave.open('../didgeridoo/trombone/trombone-27.wav', 'rb')
    waves["trombone"][28] = wave.open('../didgeridoo/trombone/trombone-28.wav', 'rb')
    waves["trombone"][29] = wave.open('../didgeridoo/trombone/trombone-29.wav', 'rb')
    waves["trombone"][30] = wave.open('../didgeridoo/trombone/trombone-30.wav', 'rb')
    waves["trombone"][31] = wave.open('../didgeridoo/trombone/trombone-31.wav', 'rb')
    waves["trombone"][32] = wave.open('../didgeridoo/trombone/trombone-32.wav', 'rb')

    waves["didgeridoo"][1]  = wave.open('../didgeridoo/didgi/didgi-01.wav', 'rb')
    waves["didgeridoo"][2]  = wave.open('../didgeridoo/didgi/didgi-02.wav', 'rb')
    waves["didgeridoo"][3]  = wave.open('../didgeridoo/didgi/didgi-03.wav', 'rb')
    waves["didgeridoo"][4]  = wave.open('../didgeridoo/didgi/didgi-04.wav', 'rb')
    waves["didgeridoo"][5]  = wave.open('../didgeridoo/didgi/didgi-05.wav', 'rb')
    waves["didgeridoo"][6]  = wave.open('../didgeridoo/didgi/didgi-06.wav', 'rb')
    waves["didgeridoo"][7]  = wave.open('../didgeridoo/didgi/didgi-07.wav', 'rb')
    waves["didgeridoo"][8]  = wave.open('../didgeridoo/didgi/didgi-08.wav', 'rb')
    waves["didgeridoo"][9]  = wave.open('../didgeridoo/didgi/didgi-09.wav', 'rb')
    waves["didgeridoo"][10] = wave.open('../didgeridoo/didgi/didgi-10.wav', 'rb')
    waves["didgeridoo"][11] = wave.open('../didgeridoo/didgi/didgi-11.wav', 'rb')
    waves["didgeridoo"][12] = wave.open('../didgeridoo/didgi/didgi-12.wav', 'rb')
    waves["didgeridoo"][13] = wave.open('../didgeridoo/didgi/didgi-13.wav', 'rb')
    waves["didgeridoo"][14] = wave.open('../didgeridoo/didgi/didgi-14.wav', 'rb')
    waves["didgeridoo"][15] = wave.open('../didgeridoo/didgi/didgi-15.wav', 'rb')
    waves["didgeridoo"][16] = wave.open('../didgeridoo/didgi/didgi-16.wav', 'rb')
    waves["didgeridoo"][17] = wave.open('../didgeridoo/didgi/didgi-17.wav', 'rb')
    waves["didgeridoo"][18] = wave.open('../didgeridoo/didgi/didgi-18.wav', 'rb')
    waves["didgeridoo"][19] = wave.open('../didgeridoo/didgi/didgi-19.wav', 'rb')
    waves["didgeridoo"][20] = wave.open('../didgeridoo/didgi/didgi-20.wav', 'rb')
    waves["didgeridoo"][21] = wave.open('../didgeridoo/didgi/didgi-21.wav', 'rb')
    waves["didgeridoo"][22] = wave.open('../didgeridoo/didgi/didgi-22.wav', 'rb')
    waves["didgeridoo"][23] = wave.open('../didgeridoo/didgi/didgi-23.wav', 'rb')
    waves["didgeridoo"][24] = wave.open('../didgeridoo/didgi/didgi-24.wav', 'rb')
    waves["didgeridoo"][25] = wave.open('../didgeridoo/didgi/didgi-25.wav', 'rb')
    waves["didgeridoo"][26] = wave.open('../didgeridoo/didgi/didgi-26.wav', 'rb')
    waves["didgeridoo"][27] = wave.open('../didgeridoo/didgi/didgi-27.wav', 'rb')
    waves["didgeridoo"][28] = wave.open('../didgeridoo/didgi/didgi-28.wav', 'rb')
    waves["didgeridoo"][29] = wave.open('../didgeridoo/didgi/didgi-29.wav', 'rb')
    waves["didgeridoo"][30] = wave.open('../didgeridoo/didgi/didgi-30.wav', 'rb')
    waves["didgeridoo"][31] = wave.open('../didgeridoo/didgi/didgi-31.wav', 'rb')
    waves["didgeridoo"][32] = wave.open('../didgeridoo/didgi/didgi-32.wav', 'rb')

    waves["organ"][1] = wave.open('../didgeridoo/organ/organ-01.wav', 'rb')
    waves["organ"][2] = wave.open('../didgeridoo/organ/organ-02.wav', 'rb')
    waves["organ"][3] = wave.open('../didgeridoo/organ/organ-03.wav', 'rb')
    waves["organ"][4] = wave.open('../didgeridoo/organ/organ-04.wav', 'rb')
    waves["organ"][5] = wave.open('../didgeridoo/organ/organ-05.wav', 'rb')
    waves["organ"][6] = wave.open('../didgeridoo/organ/organ-06.wav', 'rb')
    waves["organ"][7] = wave.open('../didgeridoo/organ/organ-07.wav', 'rb')
    waves["organ"][8] = wave.open('../didgeridoo/organ/organ-08.wav', 'rb')
    waves["organ"][9] = wave.open('../didgeridoo/organ/organ-09.wav', 'rb')
    waves["organ"][10] = wave.open('../didgeridoo/organ/organ-10.wav', 'rb')
    waves["organ"][11] = wave.open('../didgeridoo/organ/organ-11.wav', 'rb')
    waves["organ"][12] = wave.open('../didgeridoo/organ/organ-12.wav', 'rb')
    waves["organ"][13] = wave.open('../didgeridoo/organ/organ-13.wav', 'rb')
    waves["organ"][14] = wave.open('../didgeridoo/organ/organ-14.wav', 'rb')
    waves["organ"][15] = wave.open('../didgeridoo/organ/organ-15.wav', 'rb')
    waves["organ"][16] = wave.open('../didgeridoo/organ/organ-16.wav', 'rb')
    waves["organ"][17] = wave.open('../didgeridoo/organ/organ-17.wav', 'rb')
    waves["organ"][18] = wave.open('../didgeridoo/organ/organ-18.wav', 'rb')
    waves["organ"][19] = wave.open('../didgeridoo/organ/organ-19.wav', 'rb')
    waves["organ"][20] = wave.open('../didgeridoo/organ/organ-20.wav', 'rb')
    waves["organ"][21] = wave.open('../didgeridoo/organ/organ-21.wav', 'rb')
    waves["organ"][22] = wave.open('../didgeridoo/organ/organ-22.wav', 'rb')
    waves["organ"][23] = wave.open('../didgeridoo/organ/organ-23.wav', 'rb')
    waves["organ"][24] = wave.open('../didgeridoo/organ/organ-24.wav', 'rb')
    waves["organ"][25] = wave.open('../didgeridoo/organ/organ-25.wav', 'rb')
    waves["organ"][26] = wave.open('../didgeridoo/organ/organ-26.wav', 'rb')
    waves["organ"][27] = wave.open('../didgeridoo/organ/organ-27.wav', 'rb')
    waves["organ"][28] = wave.open('../didgeridoo/organ/organ-28.wav', 'rb')
    waves["organ"][29] = wave.open('../didgeridoo/organ/organ-29.wav', 'rb')
    waves["organ"][30] = wave.open('../didgeridoo/organ/organ-30.wav', 'rb')
    waves["organ"][31] = wave.open('../didgeridoo/organ/organ-31.wav', 'rb')
    waves["organ"][32] = wave.open('../didgeridoo/organ/organ-32.wav', 'rb')

    pa = PyAudio()

    # Loops the wave file wf
    def loopaudio(in_data, frame_count, time_info, status):
        global data_pos, volume, pitch, instrument
        if pitch <= 0:
            pitch = 1
        if status:
            print("Playback Error: %i" % status)
        swidth = waves[instrument][1].getsampwidth()
        waves[instrument][pitch].setpos(data_pos)
        data = waves[instrument][pitch].readframes(frame_count)
        raw = fromstring(data, dtype=int16)
        # print(raw)
        gainlvl = vectorize(lambda x: x * volume)
        raw = gainlvl(raw)
        data = raw.astype(int16).tostring()
        if len(data) < 2048 * swidth : # If file is over then rewind.
            waves[instrument][pitch].rewind()
            data = waves[instrument][pitch].readframes(frame_count)
        data_pos = waves[instrument][pitch].tell()
        return (data, paContinue)

    print "Hey, Parent Process, Opening Stream..."
    stream = pa.open(
        format = pa.get_format_from_width(waves[instrument][1].getsampwidth()),
        channels = waves[instrument][1].getnchannels(),
        rate = waves[instrument][1].getframerate(),
        output = True,
        stream_callback = loopaudio)

    print "Hey, Parent Process1"
    stream.start_stream()
    print "Hey, Parent Process2"

    while stream.is_active():
        #print "Hey, Parent Process3"
        data=r.readline()
        if not data: break
        str_vals = data.strip().split()
        int_list = [int(i) for i in str_vals]
        volume = int_list[2] / 1023.0 + 0.5
        if volume <= 0.5:
            volume = 0
        pitch = 31 - int_list[1]
        if pitch <= 0:
            pitch = 1
        if int_list[3] == 0:
          instrument = "didgeridoo" 
        if int_list[3] == 1:
          instrument = "trombone"
        if int_list[3] == 2:
          instrument = "organ"
        #print "parent read: " + data.strip()
        time.sleep(0.01)

    stream.close()
    pa.terminate()


# Input Reading
else:           # Child
    r.close()
    sleep(5)

    # recognizing SIGING (ctrl + c)
    def signal_handler(signal, frame):
        usb.util.release_interface(dev, 0)
        usb.util.release_interface(dev, 1)
        dev.attach_kernel_driver(0)
        dev.attach_kernel_driver(1)
        w.close()
        r.close()
        print('Cancelling Awesomeness')
        sys.exit(0)


    def draw_touch(counter, x, y, stylusButtonDown):
      r1 = 0b11111111
      r2 = 0
      g = 0
      b1 = 0b11111111
      b2 = 0

      # tuples of xy inputs for ring cursor
      cursor_arr_x = (x-1, x, x+1, x+1, x+1, x, x-1, x-1)
      cursor_arr_y = (y-1, y-1, y-1, y, y+1, y+1, y+1, y)

      # light up the middle if the stylus button is down
      if stylusButtonDown:
        matrix.SetPixel(x, y, 255, 255, 255)

      # cursor ring
      matrix.SetPixel(cursor_arr_x[(counter + 1) % 8], cursor_arr_y[(counter + 1) % 8], r1, 0, b2)
      matrix.SetPixel(cursor_arr_x[(counter + 2) % 8], cursor_arr_y[(counter + 2) % 8], r1, 0, b2)
      matrix.SetPixel(cursor_arr_x[(counter + 3) % 8], cursor_arr_y[(counter + 3) % 8], r1, 0, b2)
      matrix.SetPixel(cursor_arr_x[(counter + 4) % 8], cursor_arr_y[(counter + 4) % 8], r2, 0, b1)
      matrix.SetPixel(cursor_arr_x[(counter + 5) % 8], cursor_arr_y[(counter + 5) % 8], r2, 0, b1)
      matrix.SetPixel(cursor_arr_x[(counter + 6) % 8], cursor_arr_y[(counter + 6) % 8], r2, 0, b1)
      matrix.SetPixel(cursor_arr_x[(counter + 7) % 8], cursor_arr_y[(counter + 7) % 8], r2, 0, b1)
      sleep(0.05)

      # ============== MAIN ==========================

    matrix = Adafruit_RGBmatrix(32, 1)
    signal(SIGINT, signal_handler)

    # find our device
    dev = usb.core.find(idVendor=0x2914, idProduct=0x0100)
    if dev.is_kernel_driver_active(1):
        dev.detach_kernel_driver(1)
    if dev.is_kernel_driver_active(0):
        try:
            dev.detach_kernel_driver(0)
        except:
            dev.attach_kernel_driver(1)

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
    didgeridoo_image = Image.open("../assets/didgeridoo.jpg")
    trombone_image = Image.open("../assets/trombone.jpg")
    organ_image = Image.open("../assets/organ.jpg")

    image_array = [didgeridoo_image, trombone_image, organ_image]
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

      if state is not DRAW:
        pressure = 0
      print >> w, "%d %d %d %d" % (xpos,ypos,pressure,image_count)
      w.flush()
      
      # determine state
      # main menu state
      if state == MAIN_MENU:
        matrix.Clear()
        main_image.load()
        matrix.SetImage(main_image.im.id,0,0)
        if touch and not is_touched:
          draw_touch(counter, xpos, ypos, stylus)
          counter = (counter + 1) % 8
          if stylus:
            state = SELECT_INSTRUMENT
            is_touched = True
        elif not stylus and is_touched:
          is_touched = False

      # draw state
      if state == DRAW:
        if xpos == 0 and ypos == 0 and stylus:
          is_touched = True
          state = MAIN_MENU
        matrix.Fill((xpos*8)-1,(ypos*8)-1,((xpos+ypos)*4)-1)
        draw_touch(counter, xpos, ypos, stylus)
        counter = (counter + 1) % 8

      elif state == SELECT_INSTRUMENT:
        matrix.Clear()
        # draw the image
        image_array[image_count].load()          
        matrix.SetImage(image_array[image_count].im.id, 0, 0)
        if touch:
          draw_touch(counter, xpos, ypos, stylus)
          counter = (counter + 1) % 8
          
          # scroll through selections
          # return to main menu
          if xpos == 0 and ypos == 0 and stylus:
            is_touched = True
            state = MAIN_MENU

          # select instrument
          elif ypos >= 25 and stylus and not is_touched:
            is_touched = True
            state = DRAW

          # scroll right
          elif xpos > 16 and stylus and not is_touched:
            is_touched = True
            image_count = (image_count + 1) % num_images
          
          # scroll left
          elif xpos <= 16 and stylus and not is_touched:
            is_touched = True
            image_count = (image_count - 1) % num_images

          # not touching the board
          elif not stylus and is_touched:
            is_touched = False

        sleep(0.02)

    usb.util.release_interface(dev, 0)
    usb.util.release_interface(dev, 1)
    dev.attach_kernel_driver(0)
    dev.attach_kernel_driver(1)
