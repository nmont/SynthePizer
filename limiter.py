# A simple limiter

from pyaudio import PyAudio, paContinue, paFloat32
from time import sleep
from numpy import array, random, arange, float32, float64, zeros, fromstring, vectorize
import wave

################################### Constants ##################################

fs            = 44100   # Hz
threshold     = 0.8     # absolute gain
delay         = 40      # samples
signal_length = 1       # second
release_coeff = 0.9999  # release time factor
attack_coeff  = 0.9     # attack time factor
dtype         = float32 # default data type
block_length  = 1024    # samples

############################# Implementation of Limiter ########################

class Limiter:
    def __init__(self, attack_coeff, release_coeff, delay, dtype=float32):
        self.delay_index = 0
        self.envelope = 0
        self.gain = 1
        self.delay = delay
        self.delay_line = zeros(delay, dtype=dtype)
        self.release_coeff = release_coeff
        self.attack_coeff = attack_coeff

    def limit(self, signal, threshold):
        for i in arange(len(signal)):
            self.delay_line[self.delay_index] = signal[i]
            self.delay_index = (self.delay_index + 1) % self.delay

            # calculate an envelope of the signal
            self.envelope *= self.release_coeff
            self.envelope  = max(abs(signal[i]), self.envelope)

            # have self.gain go towards a desired limiter gain
            if self.envelope > threshold:
                target_gain = (1+threshold-self.envelope)
            else:
                target_gain = 1.0
            self.gain = ( self.gain*self.attack_coeff +
                          target_gain*(1-self.attack_coeff) )

            # limit the delayed signal
            signal[i] = self.delay_line[self.delay_index] * self.gain

################################# Play the Audio ###############################

wf = wave.open('didgi-7.wav', 'rb')
# signal = wf.readframes(-1)
# signal = fromstring(signal, 'Int16')

# signal = array(random.rand(fs*signal_length)*2-1, dtype=dtype)
# signal[:signal_length*fs/3] *= 0.1
# signal[signal_length*fs*2/3:] *= 0.1

limiter = Limiter(attack_coeff, release_coeff, delay, dtype)

# Callback that plays the wav file and limits the output
# This doesn't really work yet
def callback(in_data, frame_count, time_info, flag):
    if flag:
        print("Playback Error: %i" % flag)
    played_frames = callback.counter
    callback.counter += frame_count
    limiter.limit(signal[played_frames:callback.counter], threshold)
    return signal[played_frames:callback.counter], paContinue

callback.counter = 0

pa = PyAudio()

# Plays the wave file wf onece
def playonce(in_data, frame_count, time_info, status):
    if status:
        print("Playback Error: %i" % status)
    data = wf.readframes(frame_count)
    return (data, paContinue)

# Loops the wave file wf
def loopaudio(in_data, frame_count, time_info, status):
    if status:
        print("Playback Error: %i" % status)
    swidth = wf.getsampwidth()
    data = wf.readframes(frame_count)
    raw = fromstring(data, dtype=float32)
    print(raw)
    # gainlvl = vectorize(lambda x: x * 0.2)
    # raw = gainlvl(raw)
    data = raw.astype(float32).tostring()
    if len(data) < 2048 * swidth : # If file is over then rewind.
        wf.rewind()
        data = wf.readframes(frame_count)
    return (data, paContinue)

stream = pa.open(
    format = pa.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = wf.getframerate(),
    output = True,
    stream_callback = loopaudio)

stream.start_stream()

while stream.is_active():
    sleep(0.01)

stream.close()
pa.terminate()
