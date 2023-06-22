import socket
import subprocess
import logging.config
import os
import sys

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(SDK_HOME_PATH)

LOG_CONFIG = SDK_HOME_PATH + "system/log/logging-debug.ini"
logging.config.fileConfig(LOG_CONFIG,
                          disable_existing_loggers=False)

class Device(object):
    def __init__(self):
        self.local_ip_address = '127.0.0.1'
        self.default_hostname = 'ubo-120'
        self.current_hostname = None
        self.logger = logging.getLogger("device")
        self.logger.debug("Initialising device object...")

    def check_internet_connection(self):
        try:
            # Try connecting to Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            pass
        return False

    def get_local_ip(self):
        try:
            # Create a temporary socket
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))
            local_ip = temp_socket.getsockname()[0]
            temp_socket.close()
            return local_ip
        except socket.error:
            return "Unable to retrieve local IP"

    def get_current_hostname(self):
        try:
            result = subprocess.check_output(["hostname"], universal_newlines=True)
            return result.strip()
        except subprocess.CalledProcessError as e:
            self.logger.debug(f"Error occurred while retrieving hostname: {e}")
            return None

    def set_hostname(self, new_hostname):
        try:
            subprocess.run(["sudo", "hostnamectl", "set-hostname", new_hostname], check=True)
            self.logger.debug("Hostname changed successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.debug(f"Error occurred while changing hostname: {e}")

def main():
    device = Device()
    # check hostname and update if first time booting up
    while not device.check_internet_connection():
        device.logger.debug("Internet connection is not yet available.")
        # write message on screen
        sleep(1)

    device.logger.debug("Internet connection is now available.")
    # write Internet connection detected pn LCD
    # start vscode tunnel and get access code
    # show IP address, hostname, device code on LCD
    local_ip_address = device.get_local_ip()
    device.logger.debug("Local IP address:" + str(local_ip_address))

    default_hostname = "raspberrypi"
    new_hostname = "newhostname"

    current_hostname = device.get_current_hostname()
    device.logger.debug(current_hostname)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
