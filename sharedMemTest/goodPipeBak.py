# FROM TOUCHPAD INPUT
import os 
import time
import usb.core
import usb.util
import sys
#import Image
#import ImageDraw
#from test_audio import Audio
from evdev import UInput, AbsInfo, ecodes as e
from time import sleep
#from rgbmatrix import Adafruit_RGBmatrix
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

    waves = {}

    waves[1]  = wave.open('../didgeridoo/trombone/trombone-01.wav', 'rb')
    waves[2]  = wave.open('../didgeridoo/trombone/trombone-02.wav', 'rb')
    waves[3]  = wave.open('../didgeridoo/trombone/trombone-03.wav', 'rb')
    waves[4]  = wave.open('../didgeridoo/trombone/trombone-04.wav', 'rb')
    waves[5]  = wave.open('../didgeridoo/trombone/trombone-05.wav', 'rb')
    waves[6]  = wave.open('../didgeridoo/trombone/trombone-06.wav', 'rb')
    waves[7]  = wave.open('../didgeridoo/trombone/trombone-07.wav', 'rb')
    waves[8]  = wave.open('../didgeridoo/trombone/trombone-08.wav', 'rb')
    waves[9]  = wave.open('../didgeridoo/trombone/trombone-09.wav', 'rb')
    waves[10] = wave.open('../didgeridoo/trombone/trombone-10.wav', 'rb')
    waves[11] = wave.open('../didgeridoo/trombone/trombone-11.wav', 'rb')
    waves[12] = wave.open('../didgeridoo/trombone/trombone-12.wav', 'rb')
    waves[13] = wave.open('../didgeridoo/trombone/trombone-13.wav', 'rb')
    waves[14] = wave.open('../didgeridoo/trombone/trombone-14.wav', 'rb')
    waves[15] = wave.open('../didgeridoo/trombone/trombone-15.wav', 'rb')
    waves[16] = wave.open('../didgeridoo/trombone/trombone-16.wav', 'rb')
    waves[17] = wave.open('../didgeridoo/trombone/trombone-17.wav', 'rb')
    waves[18] = wave.open('../didgeridoo/trombone/trombone-18.wav', 'rb')
    waves[19] = wave.open('../didgeridoo/trombone/trombone-19.wav', 'rb')
    waves[20] = wave.open('../didgeridoo/trombone/trombone-20.wav', 'rb')
    waves[21] = wave.open('../didgeridoo/trombone/trombone-21.wav', 'rb')
    waves[22] = wave.open('../didgeridoo/trombone/trombone-22.wav', 'rb')
    waves[23] = wave.open('../didgeridoo/trombone/trombone-23.wav', 'rb')
    waves[24] = wave.open('../didgeridoo/trombone/trombone-24.wav', 'rb')
    waves[25] = wave.open('../didgeridoo/trombone/trombone-25.wav', 'rb')
    waves[26] = wave.open('../didgeridoo/trombone/trombone-26.wav', 'rb')
    waves[27] = wave.open('../didgeridoo/trombone/trombone-27.wav', 'rb')
    waves[28] = wave.open('../didgeridoo/trombone/trombone-28.wav', 'rb')
    waves[29] = wave.open('../didgeridoo/trombone/trombone-29.wav', 'rb')
    waves[30] = wave.open('../didgeridoo/trombone/trombone-30.wav', 'rb')
    waves[31] = wave.open('../didgeridoo/trombone/trombone-31.wav', 'rb')
    waves[32] = wave.open('../didgeridoo/trombone/trombone-32.wav', 'rb')

    pa = PyAudio()

    # Loops the wave file wf
    def loopaudio(in_data, frame_count, time_info, status):
        global data_pos, volume, pitch
        if pitch <= 0:
            pitch = 1
        if status:
            print("Playback Error: %i" % status)
        swidth = waves[1].getsampwidth()
        waves[pitch].setpos(data_pos)
        data = waves[pitch].readframes(frame_count)
        raw = fromstring(data, dtype=int16)
        # print(raw)
        gainlvl = vectorize(lambda x: x * volume)
        raw = gainlvl(raw)
        data = raw.astype(int16).tostring()
        if len(data) < 2048 * swidth : # If file is over then rewind.
            waves[pitch].rewind()
            data = waves[pitch].readframes(frame_count)
        data_pos = waves[pitch].tell()
        return (data, paContinue)

    stream = pa.open(
        format = pa.get_format_from_width(waves[1].getsampwidth()),
        channels = waves[1].getnchannels(),
        rate = waves[1].getframerate(),
        output = True,
        stream_callback = loopaudio)

    stream.start_stream()

    while stream.is_active():
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
        print "parent read: " + data.strip()
        time.sleep(0.01)

    stream.close()
    pa.terminate()


# Input Reading
else:           # Child
    r.close()

    # recognizing SIGING (ctrl + c)
    def signal_handler(signal, frame):
        usb.util.release_interface(dev, 0)
        usb.util.release_interface(dev, 1)
        dev.attach_kernel_driver(0)
        dev.attach_kernel_driver(1)
        print('Cancelling Awesomeness')
        sys.exit(0)

#    def draw_touch(counter, x, y, stylusButtonDown):
#        r1 = 0b11111111
#        r2 = 0
#        g = 0
#        b1 = 0b11111111
#        b2 = 0
#
#        # tuples of xy inputs for ring cursor
#        tup1 = (x-1, x, x+1, x+1, x+1, x, x-1, x-1)
#        tup2 = (y-1, y-1, y-1, y, y+1, y+1, y+1, y)
#
#        # light up the middle if the stylus button is down
#        if stylusButtonDown:
#          matrix.SetPixel(x, y, 255, 255, 255)
#
#        # cursor ring
#        matrix.SetPixel(tup1[(counter + 1) % 8], tup2[(counter + 1) % 8], r1, 0, b2)
#        matrix.SetPixel(tup1[(counter + 2) % 8], tup2[(counter + 2) % 8], r1, 0, b2)
#        matrix.SetPixel(tup1[(counter + 3) % 8], tup2[(counter + 3) % 8], r1, 0, b2)
#        matrix.SetPixel(tup1[(counter + 4) % 8], tup2[(counter + 4) % 8], r2, 0, b1)
#        matrix.SetPixel(tup1[(counter + 5) % 8], tup2[(counter + 5) % 8], r2, 0, b1)
#        matrix.SetPixel(tup1[(counter + 6) % 8], tup2[(counter + 6) % 8], r2, 0, b1)
#        matrix.SetPixel(tup1[(counter + 7) % 8], tup2[(counter + 7) % 8], r2, 0, b1)
       # a = Audio("didgi-7.wav")
       # a.play(True)
        sleep(0.05)

    # ============== MAIN ==========================

#    matrix = Adafruit_RGBmatrix(32, 1)
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

#    main_image = Image.open("../assets/mainmenu.jpg")
#    dick_butt_right_image = Image.open("../assets/dickbuttright.jpg")
#    dick_butt_left_image = Image.open("../assets/dickbuttleft.jpg")

 #   image_array = [dick_butt_right_image, dick_butt_left_image]
 #   num_images = len(image_array)
#    image_count = 0
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

        print >> w, "%d %d %d" % (xpos,ypos,pressure)
        w.flush()
        
        # determine state
        # main menu state
        # if state = MAIN_MENU:
        #   #matrix.Clear()
        #   main_image.load()
        #   if touch:
        #     #draw_touch(counter, xpos, ypos, stylus)
        #     if stylus:
        #       state = SELECT_INSTRUMENT
        # 
        # # draw state
        # if state == DRAW:
        #   #draw_touch(counter, xpos, ypos, stylus)
        #   counter = (counter + 1) % 8
        #   #matrix.Clear()
        #   
        # #select state
        # elif state == SELECT_INSTRUMENT:
        #   #matrix.Clear()
        #   # draw the image
        #   image_array[image_count].load()          
        #   #matrix.SetImage(image_array[image_count].im.id, 0, 0)
        #   if touch:
        #     #draw_touch(counter, xpos, ypos, stylus)
        #     counter = (counter + 1) % 8
        #     # scroll through selections
        #     if xpos > 16 and stylus and not is_touched:
        #       is_touched = True
        #       image_count = (image_count + 1) % num_images
        #     elif xpos <= 16 and stylus and not is_touched:
        #       is_touched = True
        #       image_count = (image_count - 1) % num_images
        #     elif not stylus and is_touched:
        #       is_touched = False
        # 


        sleep(0.02)

    usb.util.release_interface(dev, 0)
    usb.util.release_interface(dev, 1)
    dev.attach_kernel_driver(0)
    dev.attach_kernel_driver(1)
