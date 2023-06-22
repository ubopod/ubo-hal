# Audio

Ubo Pod utilizes the popular WM8960 audio codec chip found in [Seeedstudio 2-mic ReSpeaker HAT](https://www.seeedstudio.com/ReSpeaker-2-Mics-Pi-HAT.html), [BrainCraft HAT by Adafruit](https://www.adafruit.com/product/4374), [Waveshare Sound Card HAT](https://www.waveshare.com/wm8960-audio-hat.htm), etc. 

The WM8960 is low power stereo codec featuring Class D speaker drivers to provide 1W per channel into 8Ω loads. The WM8960 is capable of operating in either master or slave mode and can be programmed via a simple I2C interface. 

The install script `system/setup/install_seeedstudio.sh` installs the WM8960 driver and blacklists the bcm2835 headphone driver to avoid conflict with RGB LED driver which is based on Neopiexl library.

## Testing driver installation:

To ensure the driver is properly installed, you can run the following commands:

```
pi@ubo-xxx$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: vc4hdmi0 [vc4-hdmi-0], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: vc4hdmi1 [vc4-hdmi-1], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 2: seeed2micvoicec [seeed-2mic-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 [bcm2835-i2s-wm8960-hifi wm8960-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

In the output, you see 'seeed-2mic-voicecard' card which is the WM8960 card, you must NOT see 'bcm2835 Headphones' card since it is blacklisted.

To check if the microphones are detected for recording, run the following command:

```
pi@raspberrypi:~/Desktop/mic_hat $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 2: seeed2micvoicec [seeed-2mic-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 [bcm2835-i2s-wm8960-hifi wm8960-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
  ```


The following two commands will test the recording and playback; you should hear what you say to the microphones. The first command records you voice for 5 seconds with 16kHz sample rate and saves it to a file called test.wav. The second command plays the recorded file:

```
arecord -D "plughw:2,0" -f S16_LE -r 16000 -d 5 -t wav test.wav
aplay -D "plughw:2,0" test.wav
```

## Examples:

The examples provided in `examples` directory demonstrate how to use the WM8960 card for recording and playback in Python. 

## Resources:

Well-maintained driver for WM8960: 

https://github.com/HinTak/seeed-voicecard


Link to seedstudio resources:

https://www.seeedstudio.com/ReSpeaker-2-Mics-Pi-HAT.html
https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT_Raspberry/

Google assistant: https://developers.google.com/assistant/sdk/guides/service/python

Alexa: https://github.com/respeaker/avs

ChatGPT: https://www.hackster.io/devmiser/davinci-the-chatgpt-ai-virtual-assistant-you-can-talk-to-fd00fd
