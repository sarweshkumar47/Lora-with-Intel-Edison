# LoRa-with-Intel-Edison
Interfacing Lora module with Intel Edison

##LoRa
LoRa Mote is a LoRaWAN Class A end-device based on RN2483 LoRa modem. As a standalone battery-powered node, the Mote provides a convenient platform to quickly demonstrate the long-range capabilities of the modem, as well as to verify inter-operability when connecting to LoRaWAN gateways and infrastructure.

The Mote includes light and temperature sensors, which can be transmitted either on a fixed schedule or by a button-press. An OLED display provides connection status, sensor values and acknowledgements. A standard USB interface is provided for connection to a host computer, providing a bridge to the UART interface of the RN2483 modem.

##Experiment setup

                            (Transmitter)             Lora Modulation            (Receiver)
                              LoRa Mote  ---------------------------------------  LoRa Mote
                                  |                                                   |
                     (USB Serial) |                                                   | (USB Serial)
                                  |                                                   |
                                Edison                                              Edison
                             (Controller)                                        (Controller)
                             
* Connect LoRa Mote to Edison via standard USB interface
* One LoRa-Edison pair will be a transmitter and other one will be a receiver

##Hardware
* [Intel Edison - 2](http://www.intel.com/content/www/us/en/do-it-yourself/edison.html)
* [LoRa Mote - 2](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=dm164138#utm_medium=Press-Release&utm_term=LoRa%20Certification%20&utm_content=WPD&utm_campaign=868MHz)

##Software
--> On Edison:

* pySerial

To install pySerial and its dependencies, execute install_serial.sh script

      ./install_serial.sh

##Receiver
####First-time LoRa configuration
On Edison, execute testlora_rx.py program with --config flag and Edison sends radio commands to the LoRa module. Only one-time this step is required.

      python testlora_rx.py --config

####Test the Receiver

On Edison, execute testlora_rx.py program with --pre flag to set the LoRa Watchdog Timer to 90 secs (this is the Receiver timeout/waiting-time condition and this can be changed). 
      
      python testlora_rx.py --pre
      
On Edison, execute testlora_rx.py program to put the LoRa into reception mode. Once LoRa enters into data reception mode, it waits for 90 secs for the data. If the LoRa, doesnot receive any data within the specified time, it throws **radio_error**, after 90 secs.

      python testlora_rx.py


##Transmitter
####First-time LoRa configuration
On Edison, execute testlora_tx.py program with --config flag and Edison sends radio commands to the LoRa module. Only one-time this step is required.

      python testlora_tx.py --config

####Test the transmitter

On Edison, execute testlora_tx.py program with --pre flag to clear the buffer, and to make sure it is in working state. 
      
      python testlora_tx.py --pre
      
On Edison, execute testlora_tx.py program to send the data, it transmits a random number between 1 and 1000 to the other end.

      python testlora_tx.py

##Setting the baud rate of LoRa
All of the RN2483 module’s settings and commands are transmitted over UART using the standard ASCII interface. All commands need to be terminated with <CR><LF> and any replies they return will also be terminated by the same sequence.

The default settings for the UART interface are 57600 bps, 8 bits, no parity, 1 stop bit, no flow control. The baud rate can be changed by triggering the auto-baud detection sequence of the module. To do this, the host system needs to send a break condition followed by a 0x55 character at the new baud rate to the module. The auto-baud detection mechanism can also be triggered during Sleep to wake the module up before the predetermined time has expired. 


#####Note:
A break condition is signaled to the module by keeping the UART_RX pin low for longer than the time to transmit a complete character.




