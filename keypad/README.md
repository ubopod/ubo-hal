# Keypad document

## Project Title
This directory is part of the **UBO** SDK. The focus of this 
portion of the SDK is the management of the **keypad** and it's buttons
Most of the functionality is implemented in the __**KEYPAD**_ class.
This class is considered the base class for the keypad functionality. 
It can be used to define a derived class as exemplified in the **keypad_ex1.py**



## Description
TBD

## Prerequisites
As we are attempting to create the most informative SDK for UBO. 
We are providing a maximum of information about the way the code 
is architected. A good way to provide this information is to keep some of the 
documentation in the code itself. 
To extract this documentation from the python source code we use **doxygen** and **doxywizard**.  
Here below is the way to ensure that those two utilities are available on you system 

1. Install Doxygen:

	**`sudo apt-get install doxygen`**
	
2. Install Doxywizard

	**`sudo apt-get install doxygen-gui`**
	
We will provide in an other document the way to use those utilities
	



## Installation
TBD

## Usage

In the directory **_examples_** we are storing the examples of ways to interact with 
the keypad via the use of the KEYPAD class for 
**_KEYPAD_** class


**keypad_ex1.py** has a display that triggers all the different buttons

**keypad_ex2.py** has a complex state machine that triggers through a couple of different states

**keypad_ex3.py** has a simple state machine that loops around prompt

**keypad_ex4.py** has a mechanism to scroll 

### How do I run the scripts?

Step 1: Clone the repo **ubo-sdk**

Step 2: Run **python3 keypad_ex<n>.py**

## Contributing

## Authors
	MM
	JPS
	

## License
Here a link to the license file


## Acknowledgments
TBD


