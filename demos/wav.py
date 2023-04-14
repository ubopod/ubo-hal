import pygame

pygame.mixer.init()
py_sound = pygame.mixer.Sound("demos/media/sample-3s.wav")

def demo():
    py_sound.play()

