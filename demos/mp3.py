from pygame import mixer

mixer.init()
mixer.music.load("demos/media/sample-6s.mp3")

def demo():
    mixer.music.play()
