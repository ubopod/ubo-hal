import pyaudio
import alsaaudio
import wave
import time
import sys
from threading import Thread


class AudioManager:
    """
    Class for managing audio playback and recording
    """
    def __init__(self):
        self.chunk = 1024
        self.RESPEAKER_INDEX = 1
        self.volume = 50
        # create an audio object
        # self.p = pyaudio.PyAudio()
        self.set_volume(self.volume)
        self.is_playing = False
        self.stop = False


    def play(self, filename):
        """
        Play a wav file

        Parameters
        ----------
        filename : str
            Path to wav file
        """
        self.p = pyaudio.PyAudio()

        # if self.is_playing:
        #     # cleanup stuff.
        #     print('###########Stopping previous playback')
        #     self.stream.close()    
        #     self.p.terminate()

        # self.is_playing = True
        # open the file for reading.
        print('########### Opening file for playback')
        with wave.open(filename,'rb') as wf:
            # open stream based on the wave object which has been input.
            self.stream = self.p.open(format = self.p.get_format_from_width(wf.getsampwidth()),
                            channels = wf.getnchannels(),
                            rate = wf.getframerate(),
                            output = True,
                            output_device_index = self.RESPEAKER_INDEX)

            # read data (based on the chunk size)
            data = wf.readframes(self.chunk)
            # play stream (looping from beginning of file to the end)
            while data and self.stop == False:
                # writing to the stream is what *actually* plays the sound.
                self.stream.write(data)
                data = wf.readframes(self.chunk)
            wf.close()
            # cleanup stuff.
            self.stream.close()    
            self.p.terminate()
            self.stop = False

    def set_volume(self, volume=80):
        """
        Set the volume of the audio output

        Parameters
        ----------
        volume : float
            Volume to set
        """
        if volume < 0 or volume > 100:
            raise ValueError('Volume must be between 0 and 100')
        self.volume = volume
        mixer = alsaaudio.Mixer()
        mixer.setvolume(self.volume)


if __name__ == '__main__':
    A = AudioManager()
    # A.set_volume(80)
    path = '../chimes/done.wav'
    x = Thread(target=A.play, args=(path,))
    x.start()
    time.sleep(2)
    A.stop = True
    x2 = Thread(target=A.play, args=(path,))
    x2.start()