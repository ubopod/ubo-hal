"""
examples of cli commands:
> wpa_cli list_networks # -> returns list of configured networks
> wpa_cli enable_network id # -> enables network
> wpa_cli disable_network id # -> disables network 
> wpa_cli remove_network id # -> removes network from wpa_supplicant.conf
> wpa_cli save_config # -> saves wpa_supplicant.conf
> wpa_cli reconfigure # -> reloads wpa_supplicant.conf
> wpa_cli status # -> returns status of current connection
> wpa_cli terminate # -> terminates wpa_supplicant
> wpa_cli scan # -> scans for networks
> wpa_cli scan_results # -> returns list of scanned networks
> wpa_cli add_network # -> returns id of new network
> wpa_cli set_network id ssid '"example_ssid"' # set ssid for WPA
> wpa_cli set_network id psk '"example_password"' # set password for WPA
> wpa_cli set_network id key_mgmt NONE # set key_mgmt for OPEN
> wpa_cli set_network id wep_key '"example_password"' # set password for WEP
> wpa_cli log_level DEBUG # -> sets log level to debug

For more information on wpa_cli commands, see:
https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/w/wpa_cli.html
"""

import subprocess
from typing import Literal, Union
import logging.config
from time import sleep
import os
import sys

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(SDK_HOME_PATH)

LOG_CONFIG = SDK_HOME_PATH + "system/log/logging-debug.ini"
logging.config.fileConfig(LOG_CONFIG,
                          disable_existing_loggers=False)

class WpaCliWrapper:
    """Wrapper class for wpa_cli commands.

    Attributes
    -----------
        interface: 'str' 
            The network interface name to use for 
            wpa_cli commands. Default is wlan0.
    """
    def __init__(self, interface='wlan0'):
        """initialize the class with default interface wlan0."""
        self.interface = interface
        self.logger = logging.getLogger("wpa_cli")
    
    def _run_command(self, 
                     command: Union[str, list[str]]) -> str:
        """Run the cli command as system commands.
        
        Parameters
        ----------
        command: Union[str, list[str]]
            The command to run. Can be a string or a list of strings.
            It uses the subprocess.run() method to run the command.
        """
        cmd = ['wpa_cli', '-i', self.interface, 
               '-p', '/var/run/wpa_supplicant']
        if isinstance(command, str):
            cmd.append(command)
        elif isinstance(command, list):
            cmd.extend(command)
        self.logger.debug(f'Running command: {cmd}')
        try:
            result = subprocess.run(cmd, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, 
                                    text=True, 
                                    check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.debug( f"Error: {e.stderr.strip()}")

    
    def _parse_scan_results(self, results):
        """Parse the scan results into a list of dictionaries.
        
        Parameters
        ----------
        results: 'str'
            The raw results from the scan_results command.
        
        Returns
        -------
        networks: 'list[dict]'
            A list of dictionaries containing the parsed results.
            {
                'bssid': bssid,
                'frequency': frequency,
                'signal_level': signal_level,
                'flags': flags,
                'ssid': ssid
            }
        """
        lines = results.split('\n')[2:]
        networks = []

        for line in lines:
            values = line.split()
            if len(values) >= 5:
                bssid = values[0]
                frequency = int(values[1])
                signal_level = int(values[2])
                flags = values[3].strip('[]').split('][')
                ssid = values[4]
                
                networks.append({
                    'bssid': bssid,
                    'frequency': frequency,
                    'signal_level': signal_level,
                    'flags': flags,
                    'ssid': ssid
                })

        return networks


    def _parse_list_networks(self, results: str) -> list[dict]:
        """Parse the list_networks command results into a list of dictionaries.
        
        Parameters
        ----------
        results: 'str'
            The raw results from the list_networks command.
        
        Returns
        -------
        networks: 'list[dict]'
            A list of dictionaries containing the parsed results.
            {
                'network_id': network_id,
                'ssid': ssid,
                'bssid': bssid,
                'flags': flags
            }
        """
        lines = results.split('\n')
        networks = []
        for line in lines:
            parts = line.split('\t')
            if len(parts) >= 4:
                network_id, ssid, bssid, flags = parts[:4]
                networks.append({
                    'network_id': network_id,
                    'ssid': ssid,
                    'bssid': bssid,
                    'flags': flags
                })
        return networks
    
    def _parse_list_interfaces(self, results: str) -> list[str]:
        """Parse the list_interfaces command results into a list of strings.
        
        Parameters
        ----------
        results: 'str'
            The raw results from the list_interfaces command.

        Returns
        -------
        interfaces: 'list[str]'
            A list of strings containing the names of 
            available network interfaces.
        """

        lines = results.split('\n')[1:]
        interfaces = []
        for line in lines:
            interfaces.append(line.strip())
        return interfaces
    
    def _parse_status(self, status_output: str) -> dict:
        """Parse the status command results into a dictionary.

        Parameters
        ----------
        status_output: 'str'
            The raw results from the status command.

        Returns
        -------
        status: 'dict'
            A dictionary containing the parsed results.
            Here's an example of an output:
            {
                'bssid': 'a2:3d:cf:27:7e:0d', 
                'freq': '5240', 
                'ssid': 'example-guest', 
                'id': '1', 
                'mode': 'station', 
                'pairwise_cipher': 'CCMP', 
                'group_cipher': 'CCMP', 
                'key_mgmt': 'WPA2-PSK', 
                'wpa_state': 'COMPLETED', 
                'p2p_device_address': 'e6:5f:01:e0:0a:f2', 
                'address': 'e4:5f:01:e0:0a:f2', 
                'uuid': '462bc09f-bab7-543a-98cc-0ef7006fe1e8', 
                'ieee80211ac': '1'}
        """

        status_lines = status_output.split('\n')
        status = {}
        
        for line in status_lines:
            key, value = line.split('=', 1)
            status[key] = value
        
        return status
    
    def scan(self):
        """Run the scan command."""
        return self._run_command('scan')

    def scan_results(self):
        """Run the scan_results command and parses the output."""
        raw_results = self._run_command('scan_results')
        return self._parse_scan_results(raw_results)
    
    def list_networks(self):
        """Run the list_networks command and parses the output."""
        raw_results = self._run_command('list_networks')
        return self._parse_list_networks(raw_results)
    
    def list_interfaces(self):
        """Run the list_interfaces command and parses the output."""
        raw_results = self._run_command('interface')
        return self._parse_list_interfaces(raw_results)

    def add_network(self):
        """Run the add_network command."""
        return self._run_command('add_network')
    
    def status(self):
        """Run the status command and parses the output."""
        raw_results = self._run_command('status')
        return self._parse_status(raw_results)

    def set_network(self, 
                    network_id, 
                    field: Literal['ssid', 'psk', 'auth_alg', 'key_mgmt', 'wep_key'], 
                    value):
        """Run the set_network command.
        
        Parameters
        ----------
        network_id: 'str'
            The network id to set the parameters for.
        field: Literal['ssid', 'psk', 'auth_alg', 'key_mgmt', 'wep_key']
            The parameter field to set.
        value: 'str'
            The value to set the field to.

        Returns
        -------
        bool: True if the command succeeded, False otherwise.
        """
        result = self._run_command(['set_network', 
                                    f'{network_id}', 
                                    f'{field}', 
                                    f'{value}'])
        if 'OK' == result:
            self.logger.debug(f'\"set_network \
                        {network_id} {field} {value} \" command suceeded!')
            return True
        else:
            self.logger.error(f'\"set_network \
                          {network_id} {field} {value} \" command failed')
            raise Exception(f'\"set_network \
                            {network_id} {field} {value} \" command failed')

    def enable_network(self, network_id):
        """Run the enable_network command.
        
        Parameters
        ----------
        network_id: 'str'
            The network id to enable.
        """
        return self._run_command(['enable_network', f'{network_id}'])

    def disable_network(self, network_id):
        """Run the disable_network command.
        
        Parameters
        ----------
        network_id: 'str'
            The network id to disable.
        """
        return self._run_command(['disable_network', f'{network_id}'])

    def remove_network(self, network_id):
        """Run the remove_network command.
        
        Parameters
        ----------
        network_id: 'str'
            The network id to remove.
        """
        return self._run_command(['remove_network', f'{network_id}'])

    def terminate(self):
        """Run the terminate command."""
        return self._run_command('terminate')
    
    def reconfigure(self):
        """Run the reconfigure command."""
        return self._run_command('reconfigure')
    
    def save_config(self):
        """Run the save_config command."""
        return self._run_command('save_config')
    
    def log_level(self, level: Literal['EXCESSIVE', 
                                       'MSGDUMP', 
                                       'DEBUG', 
                                       'INFO', 
                                       'WARNING', 
                                       'ERROR']):
        """Run the log_level command.

        Parameters
        ----------
        level: Literal['EXCESSIVE', 'MSGDUMP', 'DEBUG', 'INFO', 'WARNING', 'ERROR']
            The log level to set.
        """
        return self._run_command(['log_level', f'{level}'])
    # Add more methods as needed for other wpa_cli commands

class wifiManager(WpaCliWrapper):
    """
    A class that inherits from WpaCliWrapper and adds methods to manage wifi connections

    Attributes
    ----------
    interface: 'str'
        The network interface name to use for
        wpa_cli commands. Default is wlan0.
    """
    def __init__(self, interface='wlan0'):
        """initialize the class with default interface wlan0.
        
        Parameters
        ----------
        interface: 'str'
            The network interface name to use for
            wpa_cli commands. Default is wlan0.
        """
        super().__init__(interface)
        self.networks = self.list_networks()
        self.interfaces = self.list_interfaces()
        self.interface = interface
        self.current_network = self.status()

    def get_network_id(self, ssid: str) -> Union [str, None]:
        """ Get the network id of a configured network
        
        Parameters
        ----------
        ssid: 'str'
            The ssid of the network to get the network id for
        
        Returns
        ----------
        network_id: 'str'
            The network id of the network with the given ssid
        """
        for network in self.networks:
            if network.get('ssid') == ssid:
                return network.get('network_id')
        return None
    
    def get_latest_status(self) -> dict:
        """ Get the latest status of the wifi connection

        Returns
        --------
            current_network: 'dict' 
            A dictionary containing the latest status of the wifi connection

        Behavior
        ---------
            This method will check the status of the wifi connection every 2 seconds
            Until status is not 'SCANNING' or 'ASSOCIATING' or 20 seconds have passed
        """
        self.current_network = self.status()
        iterations = 10
        while (self.current_network.get('wpa_state') == 'SCANNING' or \
               self.current_network.get('wpa_state') == 'ASSOCIATING') \
               and iterations > 0:
            self.current_network = self.status()
            self.logger.debug(f'Current status: {self.current_network}')    
            sleep(2)
            iterations -= 1
        return self.current_network
    def add_wifi(self, 
                 ssid: str, 
                 password: str, 
                 type: Literal['WPA','WEP','OPEN','']
                 ) -> Union[str, None]:
        """ Add a wifi network to the list of configured networks.
        
        Parameters
        ----------
        ssid: 'str'
            The ssid of the network to add
        password: 'str'
            The password of the network to add
        type: Literal['WPA','WEP','OPEN','']
            The type of the network to add. Default is WPA
        
        Returns
        ----------
        network_id: 'str'
            The network id of the network that was added
        """
        try:
            network_id = self.add_network()
            self.logger.debug(f'network_id: {network_id}')
            ssid_string = '"{}"'.format(ssid)
            password_string = '"{}"'.format(password)
            self.set_network(network_id, 'ssid', ssid_string)
            if type == 'WPA':
                self.set_network(network_id, 'psk', password_string)
            elif type == 'WEP':
                self.set_network(network_id, 'wep_key', password_string)
            elif type == 'OPEN':
                self.set_network(network_id, 'key_mgmt', 'NONE')
            else:
                self.logger.error("Unsupported type")
            return network_id
        except Exception as e:
            self.logger.error(f'Error adding wifi: {e}')
            return None

    def connect_to_wifi(self, network_id: str) -> bool:
        """ Connect to a wifi network
        
        Parameters
        ----------
        network_id: 'str'
            The network id of the network to connect to

        Returns
        ----------
        bool: True if the connection succeeded, False otherwise
        """
        if network_id:
            try:
                self.enable_network(network_id)
                self.save_config()
                self.reconfigure()
                current_network = self.get_latest_status()
                current_id = current_network.get('id')
                current_ssid = current_network.get('ssid')
                self.logger.debug(f'Current connected network ssid is: {current_ssid}')
                if  current_id == network_id:
                    self.logger.info(f'Connected to {current_ssid}')
                    return True
                else:
                    self.logger.error("WiFi connection failed!")
                    return False
            except Exception as e:
                self.logger.error(f'Error adding wifi: {e}')
                return False
        else:
            self.logger.error("Network ID is None")
            return False

    def forget_wifi(self, ssid: str) -> bool:
        """ Remove a wifi network from the list of configured networks.

        Parameters
        ----------
        ssid: 'str'
            The ssid of the network to remove

        Returns
        ----------
        bool: True if the removal succeeded, False otherwise
        """
        network_id = self.get_network_id(ssid)
        self.remove_network(network_id)
        self.save_config()
        self.reconfigure()
        return True

if __name__ == '__main__':
    wrapper = WpaCliWrapper()
    
    scan_results = wrapper.scan_results()
    for network in scan_results:
        print(network)
    
    configured_networks = wrapper.list_networks()
    for network in configured_networks:
        print(network)
    
    available_interfaces = wrapper.list_interfaces()
    for interface in available_interfaces:
        print(interface)

    wrapper.logger.info(wrapper.status())

    W = wifiManager()
    id = W.add_wifi(ssid='CircuitLaunch', password='makinghardwarelesshard', type='WPA')
    R = W.connect_to_wifi(id)
    W.logger.info("wifi connected: ", R)

    configured_networks = wrapper.list_networks()
    for network in configured_networks:
         wrapper.logger.info(network)
