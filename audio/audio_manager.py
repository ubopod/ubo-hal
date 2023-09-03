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
        self.is_playing = False
        self.p = pyaudio.PyAudio()

    def __del__(self):
        self.p.terminate()

    def stop(self):
        self.stream.stop_stream()

    def play(self, filename):
        """
        Play a wav file

        Parameters
        ----------
        filename : str
            Path to wav file
        """

        # if self.is_playing:
        #     # cleanup stuff.
        #     print('###########Stopping previous playback')
        #     self.stream.close()    
        #     self.p.terminate()

        # self.is_playing = True
        # open the file for reading.
        print('########### Opening file for playback')
        try:
            with wave.open(filename,'rb') as wf:
                # open stream based on the wave object which has been input.
                def callback(in_data, frame_count, time_info, status):
                    data = wf.readframes(frame_count)
                    # If len(data) is less than requested frame_count, PyAudio automatically
                    # assumes the stream is finished, and the stream stops.
                    return (data, pyaudio.paContinue)
                self.stream = self.p.open(format = self.p.get_format_from_width(wf.getsampwidth()),
                                channels = wf.getnchannels(),
                                rate = wf.getframerate(),
                                output = True,
                                output_device_index = self.RESPEAKER_INDEX,
                                stream_callback=callback)

                while self.stream.is_active():
                    time.sleep(0.1)
                # cleanup stuff.
                self.stream.close()    
                # self.stop = True
        except Exception as e:
            print(e)
            # cleanup stuff.
            self.stream.close()    
            # self.stop = True


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
    path = './scan.wav'
    x = Thread(target=A.play, args=(path,))
    x.start()
    print("hellloooo")
    time.sleep(3)
    # force stop
    A.stop()
    # need some time after setting the flag to stop the stream
    time.sleep(0.5)
    x2 = Thread(target=A.play, args=(path,))
    x2.start()