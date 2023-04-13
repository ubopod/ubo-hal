import os
import logging
import logging.config
import socket
import time

SDK_HOME_PATH = "/home/pi/ubo-sdk/"
LM_SOCKET_PATH = SDK_HOME_PATH + "ledmanagersocket.sock"
LOG_CONFIG = SDK_HOME_PATH + "system/log/logging-debug.ini"
logging.config.fileConfig(LOG_CONFIG,
                          disable_existing_loggers=False)

logger = logging.getLogger("led_client")


class LEDClient:
    ''' The methods of this class send commands to the LED manager, 
    which runs with root previlages due to hardware DMA security constraints.
    The commands are sent through a socket connection to the LED manager.

    The LED manager is a Python script that runs as a daemon. The LED manager
    is a daemon because it uses DMA to control the LEDs. This is a hardware security constraint.

    The LED client is a Python script that runs as a non-root user. The LED client function
    is to serialize LED commands and send them to the LED manager in a secure manner. 
    '''
    def __init__(self):
        self.client = None
        if os.path.exists(LM_SOCKET_PATH):
            self.client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            try:
                self.client.connect(LM_SOCKET_PATH)
            except Exception as e:
                logger.error("rgb_ring_manager service is down. run sudo systemctl start rgb_ring_manager")
                print("rgb_ring_manager service is down. run sudo systemctl start rgb_ring_manager" )
                return

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def set_enabled(self, enabled=True):
        if self.client is None:
            return
        self.send("set_enabled " + str(int(enabled)))

    def send(self, cmd):
        self.client.send(cmd.encode('utf-8'))

    def set_all(self, color = (255,255,255)):
        '''
        sets all LEDs to the specified color
        '''    
        if self.client is None:
            return
        (r,g,b) = color
        self.send("set_all " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b))

    def set_brightness(self, brightness = 0.5):
        '''
        sets all LEDs to the specified color
        '''    
        if self.client is None:
            return
        if brightness < 0 or brightness > 1:
            print("brightness must be between 0 and 1")
            return
        self.send("set_brightness " +
                  str(brightness))

    def blank(self):
        if self.client is None:
            return
        self.send("blank")

    def rainbow(self, rounds, wait):
        '''
        glows the LEDs in a rainbow pattern
        percentage: is a float between 0 and 1
        wait: is in milliseconds
        '''    
        if self.client is None:
            return
        self.send("rainbow " + 
                str(rounds) + " " +
                str(wait))
zorglub
    def progress_wheel_step(self, color = (255,255,255)):
        '''
        increments the position of bright strip by one step.
        '''
        if self.client is None:
            return
        (r,g,b) = color
        self.send("progress_wheel_step " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b))
    def pulse(self, color = (255,255,255), 
                    wait = 100, 
                    repetitions = 5):
        if self.client is None:
            return
        (r,g,b) = color
        self.send("pulse " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b) + " " +
                  str(wait) + " " + 
                  str(repetitions))

    def blink(self, color = (255,255,255), 
                    wait = 100, 
                    repetitions = 5):
        if self.client is None:
            return
        (r,g,b) = color
        self.send("blink " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b) + " " +
                  str(wait) + " " + 
                  str(repetitions))
    
    def spinning_wheel(self, 
                        color = (255,255,255), 
                        wait = 100,
                        length = 5,
                        repetitions = 5):
        if self.client is None:
            return
        (r,g,b) = color
        self.send("spinning_wheel " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b) + " " +
                  str(wait) + " " + 
                  str(length) + " " + 
                  str(repetitions))
    
    def progress_wheel(self, 
                        color = (255,255,255), 
                        percentage = 0.5):
        if self.client is None:
            return
        (r,g,b) = color
        self.send("progress_wheel " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b) + " " +
                  str(percentage))
    
    def fill_upto(self, 
                        color = (255,255,255), 
                        percentage = 0.5,
                        wait = 100):
        if self.client is None:
            return
        (r,g,b) = color
        self.send("fill_upto " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b) + " " +
                  str(percentage) + " " +
                  str(wait))

    def fill_downfrom(self, 
                        color = (255,255,255), 
                        percentage = 0.5,
                        wait = 100):
        if self.client is None:
            return
        (r,g,b) = color
        self.send("fill_downfrom " +
                  str(r) + " " +
                  str(g) + " " +
                  str(b) + " " +
                  str(percentage) + " " +
                  str(wait))
