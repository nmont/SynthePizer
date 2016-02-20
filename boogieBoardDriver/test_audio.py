#!/usr/bin/python
import wave
import pyaudio
import audioop

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
            rate = 48000.0,
            output = True
        )
        print(self.wf.getframerate())
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
