#!/usr/bin/python
import wave
import pyaudio
import audioop

class Gain:

    def __init__(self):
        self.amount = 1.0;

    def gain(self, data, amount):
        for i in arange(len(signal)):
            data[i] = 

    def callback(self, in_data, frame_count, time_info):
        played_frames = counter
        counter += frame_count
        self.gain(signal(played_frames:counter], self.




class Audio:
    CHUNK = 1024
    wf = None
    p = None
    stream = None
    data = None

    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )
        self.data = self.wf.readframes(self.CHUNK)

    def play(self,loop=True):
        data = self.data
        while loop:
            self.stream.write(data)
            data = self.wf.readframes(self.CHUNK)
            if data == '' : # If file is over then rewind.
                self.wf.rewind()
                data = self.wf.readframes(self.CHUNK)

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()

a = Audio("didgi-7.wav")
a.play(True)
