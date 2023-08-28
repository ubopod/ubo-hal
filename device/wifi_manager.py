from typing import Union, Literal
from time import sleep
from wpa_cli import WpaCliWrapper


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

    def get_network_id(self, ssid: str) -> list[str]:
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
        self.networks = self.list_networks()
        network_ids = []
        for network in self.networks:
            if network.get('ssid') == ssid:
                network_ids.append(network.get('network_id'))
                self.logger.debug(f'Network id for {ssid} is {network.get("network_id")}')
        return network_ids
    
    def get_current_network(self) -> tuple[str, str]:
        """ Get the ssid and network_id of the current connected network
        
        Returns
        ----------
        ssid: 'str'
            The ssid of the current connected network
        network_id: 'str'
            The network id of the current connected network
        """
        networks = self.list_networks()
        for network in networks:
            if '[CURRENT]' in network.get('flags'):
                self.logger.debug(f'Current connected network is: {network}')
                return network.get('ssid'), network.get('network_id')
        return None

    def get_network_flag(self, id: str) -> str:
        """ Get the flags of a configured network
        
        Parameters
        ----------
        id: 'str'
            The network id of the network to get the flags for
        
        Returns
        ----------
        flags: 'str'
            The flags of the network with the given id
        """
        self.networks = self.list_networks()
        for network in self.networks:
            if network.get('network_id') == id:
                return network.get('flags')
        return "None"

    def get_stable_status(self) -> dict:
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
        wifi_status = self.status()
        iterations = 10
        possible_states = ['SCANNING', 
                           'ASSOCIATING', 
                           'DISCONNECTED',
                           'COMPLETED',
                           'INACTIVE',
                           'INTERFACE_DISABLED',
                           '4WAY_HANDSHAKE',
                           'GROUP_HANDSHAKE',
                           'ASSOCIATED',
                           'AUTHENTICATING']
        while (wifi_status.get('wpa_state') != 'COMPLETED' ) \
               and iterations > 0:
            self.clear_blacklist()
            self.logger.debug(f'Current status: {wifi_status}') 
            sleep(5)
            wifi_status = self.status()
            iterations -= 1
        return wifi_status

    def network_reset(self, network_id) -> bool:
        """ Reset the wifi network
        
        Returns
        ----------
        bool: True if the reset succeeded, False otherwise
        """
        try:
            self.clear_blacklist()
            self.logger.info("Resetting network")
            self.disable_network(network_id)
            sleep(0.5)
            self.save_config()
            sleep(0.5)
            self.reconfigure()
            sleep(0.5)
            flag = self.get_network_flag(network_id)
            while '[DISABLED]' not in flag:
                # wait for network to be disabled
                self.logger.debug(f'Network {network_id} is {flag}')
                sleep(1)
            if self.check_blacklist():
                self.logger.error("Wifi is blacklisted")
                self.clear_blacklist()
                sleep(0.5)
            self.enable_network(network_id)
            sleep(0.5)
            if self.check_blacklist():
                self.logger.error("Wifi is blacklisted")
                self.clear_blacklist()
                sleep(0.5)
            self.save_config()
            sleep(0.5)
            self.reconfigure()
            return True
        except Exception as e:
            self.logger.error(f'Error resetting network: {e}')
            return False

    def check_connectivity(self, network_id: str) -> bool:
            current_network = self.get_stable_status()
            current_id = current_network.get('id')
            current_ssid = current_network.get('ssid')
            self.logger.debug(f'Current connected network ssid is: {current_ssid}')
            if  current_id == network_id:
                self.logger.info(f'Connected to {current_ssid}')
                return True
            else:
                self.logger.error(f'Not connected to {current_ssid}')
                return False

    def add_wifi(self, 
                 ssid: str, 
                 password: str = None, 
                 psk: str = None,
                 type: Literal['WPA','WEP','OPEN',''] = 'WPA'
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

        get_current_network = self.get_current_network()
        if get_current_network:
            current_ssid, current_id = get_current_network
            if current_ssid == ssid:
                self.logger.info(f'Already connected to {ssid}')
                return None
        # if current_ssid exists but not connected
        if len(self.get_network_id(ssid)) > 0:
            self.logger.error(f'Previously attempted to configure Network {ssid}')
            return None
        try:
            network_id = self.add_network()
            self.logger.debug(f'network_id: {network_id}')
            ssid_string = '"{}"'.format(ssid)
            if password:
                password_string = '"{}"'.format(password)
            elif psk:
                password_string = psk
            else:
                password_string = '""'
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
        self.enable_network(network_id)
        self.save_config()
        self.reconfigure()
        iterations = 10
        sleep(1)
        flag = self.get_network_flag(network_id)
        self.logger.debug(f'Network {network_id} flag is {flag}')
        #make sure current flag is maintained for a few seconds
        CONNECTED = False
        consistant_flag = 0
        while not CONNECTED and iterations > 0:
            if '[CURRENT]' in flag:
                consistant_flag += 1
                iterations += 1
                self.logger.debug(f'Network CURRENT consistenty for {consistant_flag}')
                sleep(2)
                if consistant_flag > 2:
                    CONNECTED = True
            elif '[TEMP-DISABLED]' in flag or '[DISABLED]' in flag:
                self.logger.debug(f'Network {network_id} flag is {flag}')
                self.network_reset(network_id)
                consistant_flag = 0
                sleep(4)
            else:
                self.logger.error(f'Network {network_id} flag is {flag}')
                consistant_flag = 0
                sleep(5)
            flag = self.get_network_flag(network_id)
            iterations -= 1
            self.logger.debug(f'################### iterating for {iterations} more times')
        try:
            if self.check_connectivity(network_id):
                return True
            else:
                sleep(1)
                # if self.check_blacklist():
                #     self.logger.error("Wifi is blacklisted")
                #     self.clear_blacklist()
                #     self.network_reset(network_id)
                # else:
                #     self.logger.error("Wifi is not blacklisted")
                return False
        except Exception as e:
            self.logger.error(f'Error adding wifi: {e}')
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
        try:
            network_ids = self.get_network_id(ssid)
            self.logger.debug(f'network_ids: {network_ids}')
            for network_id in network_ids:
                self.remove_network(network_id)
            self.save_config()
            self.reconfigure()
            return True
        except Exception as e: 
            self.logger.error(f'Error forgetting wifi: {e}')
            return False
        

if __name__ == '__main__':

    W = wifiManager()
    ssid='earlplex-guest'
    password='hammerearlplex'
    psk = W.generate_passphrase(ssid, password)
    # id = W.add_wifi(ssid, password, type='WPA')
    id = W.add_wifi(ssid='earlplex-guest', psk=psk, type='WPA')
    
    if id:
        R = W.connect_to_wifi(id)
        W.logger.info("wifi connected: " + str(R))
    else:
        forgot = W.forget_wifi('earlplex-guest')
        if forgot:
            W.logger.info("network forgotten")
        else:
            W.logger.info("network not removed")

