# Directory Structure

This directory contains scripts and files related to the installation and setup of the ubo-sdk application.

├── create_users_and_groups.sh
├── install_eeprom.sh
├── install_seeedstudio.sh
├── install.sh
├── requirements.txt
└── start_services.sh

## File Descriptions

### create_users_and_groups.sh: 
	A script to create users and groups required for the ubo-sdk application.

### install_eeprom.sh: 
	A script to install the eeprom package, which is required for the ubo-sdk application.

### install_seeedstudio.sh: 
	A script to install the seedstudio package, which is required for the ubo-sdk application.

### install.sh: 
	A script to run all the scripts required to install the ubo-sdk application and its dependencies.

### requirements.txt: 
	A file containing a list of all the Python packages required by the ubo-sdk application.

### start_services.sh: 
	A script to start the services required for the ubo-sdk application.

## Usage

	To install and set up the ubo-sdk application, simply run install.sh in the terminal. 
	This script will run all the required scripts in the following order:

	create_users_and_groups.sh to create the required users and groups.
	install_eeprom.sh to install the eeprom package.
	install_seeedstudio.sh to install the seedstudio package.
	requirements.txt to install the required Python packages.
	start_services.sh to start the services required by the ubo-sdk application.

## Requirements
 The ubo-sdk application requires the following:

	Linux operating system
	Python 3.6 or higher
	Internet connection to download required packages
	
## Contributors
	list of names


## License
The ubo-sdk application is released under the MIT license.
