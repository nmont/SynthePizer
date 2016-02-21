# A simple limiter

from pyaudio import PyAudio, paContinue, paFloat32
from time import sleep
from numpy import array, random, arange, float32, float64, zeros, fromstring, vectorize, int16
import wave
import signal as keyboard_signal

################################# Change the Volume ############################

volume = 1.0
ypos = 15
data_pos = 0

def update_volume(v):
    global volume
    volume = v

def increment_volume(s, f):
    global volume
    volume += 0.1
    print("up " + str(volume))

def decrement_volume(s, f):
    global volume
    volume -= 0.1
    print("down " + str(volume))

def increment_pitch(s, f):
    global ypos
    ypos += 1
    print("up " + str(volume))

def decrement_pitch(s, f):
    global ypos
    ypos -= 1
    print("down " + str(volume))

# keyboard_signal.signal(keyboard_signal.SIGQUIT, increment_volume) # CTRL+\
# keyboard_signal.signal(keyboard_signal.SIGTSTP, decrement_volume) # CTRL+z
keyboard_signal.signal(keyboard_signal.SIGQUIT, increment_pitch) # CTRL+\
keyboard_signal.signal(keyboard_signal.SIGTSTP, decrement_pitch) # CTRL+z

################################# Play the Audio ###############################

waves = {}

waves[1]  = wave.open('didgi/didgi-01.wav', 'rb')
waves[2]  = wave.open('didgi/didgi-02.wav', 'rb')
waves[3]  = wave.open('didgi/didgi-03.wav', 'rb')
waves[4]  = wave.open('didgi/didgi-04.wav', 'rb')
waves[4]  = wave.open('didgi/didgi-05.wav', 'rb')
waves[6]  = wave.open('didgi/didgi-06.wav', 'rb')
waves[7]  = wave.open('didgi/didgi-07.wav', 'rb')
waves[8]  = wave.open('didgi/didgi-08.wav', 'rb')
waves[9]  = wave.open('didgi/didgi-09.wav', 'rb')
waves[10] = wave.open('didgi/didgi-10.wav', 'rb')
waves[11] = wave.open('didgi/didgi-11.wav', 'rb')
waves[12] = wave.open('didgi/didgi-12.wav', 'rb')
waves[13] = wave.open('didgi/didgi-13.wav', 'rb')
waves[14] = wave.open('didgi/didgi-14.wav', 'rb')
waves[15] = wave.open('didgi/didgi-15.wav', 'rb')
waves[16] = wave.open('didgi/didgi-16.wav', 'rb')
waves[17] = wave.open('didgi/didgi-17.wav', 'rb')
waves[18] = wave.open('didgi/didgi-18.wav', 'rb')
waves[19] = wave.open('didgi/didgi-19.wav', 'rb')
waves[20] = wave.open('didgi/didgi-20.wav', 'rb')
waves[21] = wave.open('didgi/didgi-21.wav', 'rb')
waves[22] = wave.open('didgi/didgi-22.wav', 'rb')
waves[23] = wave.open('didgi/didgi-23.wav', 'rb')
waves[24] = wave.open('didgi/didgi-24.wav', 'rb')
waves[25] = wave.open('didgi/didgi-25.wav', 'rb')
waves[26] = wave.open('didgi/didgi-26.wav', 'rb')
waves[27] = wave.open('didgi/didgi-27.wav', 'rb')
waves[28] = wave.open('didgi/didgi-28.wav', 'rb')
waves[29] = wave.open('didgi/didgi-29.wav', 'rb')
waves[30] = wave.open('didgi/didgi-30.wav', 'rb')
waves[31] = wave.open('didgi/didgi-31.wav', 'rb')
waves[32] = wave.open('didgi/didgi-32.wav', 'rb')

pa = PyAudio()

# Loops the wave file wf
def loopaudio(in_data, frame_count, time_info, status):
    global volume, ypos, data_pos
    if status:
        print("Playback Error: %i" % status)
    swidth = waves[1].getsampwidth()
    waves[ypos].setpos(data_pos)
    data = waves[ypos].readframes(frame_count)
    raw = fromstring(data, dtype=int16)
    # print(raw)
    gainlvl = vectorize(lambda x: x * volume)
    raw = gainlvl(raw)
    data = raw.astype(int16).tostring()
    if len(data) < 2048 * swidth : # If file is over then rewind.
        waves[ypos].rewind()
        data = waves[ypos].readframes(frame_count)
    data_pos = waves[ypos].tell()
    return (data, paContinue)

stream = pa.open(
    format = pa.get_format_from_width(waves[1].getsampwidth()),
    channels = waves[1].getnchannels(),
    rate = waves[1].getframerate(),
    output = True,
    stream_callback = loopaudio)

stream.start_stream()

while stream.is_active():
    sleep(0.01)

stream.close()
pa.terminate()
