import alsaaudio

# Set the desired volume (0 to 100)
desired_volume = 80

mixer = alsaaudio.Mixer()
mixer.setvolume(desired_volume)
