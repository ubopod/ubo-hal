import pyaudio
import wave
import sys
from threading import Thread


class AudioManager:
    """
    Class for managing audio playback and recording
    """
    def __init__(self):
        self.chunk = 1024
        self.RESPEAKER_INDEX = 1
        # create an audio object
        self.p = pyaudio.PyAudio()

    def play(self, filename):
        """
        Play a wav file

        Parameters
        ----------
        filename : str
            Path to wav file
        """

        # open the file for reading.
        wf = wave.open(filename, 'rb')

        # open stream based on the wave object which has been input.
        stream = self.p.open(format = self.p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True,
                        output_device_index = self.RESPEAKER_INDEX)

        # read data (based on the chunk size)
        data = wf.readframes(self.chunk)
        # play stream (looping from beginning of file to the end)
        while data:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(self.chunk)

        # cleanup stuff.
        stream.close()    
        self.p.terminate()

if __name__ == '__main__':
    A = AudioManager()
    A.play('../chimes/done.wav')