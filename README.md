# LoRa-with-Intel-Edison
Interfacing Lora module with Intel Edison

##LoRa
LoRa Mote is a LoRaWAN Class A end-device based on RN2483 LoRa modem. As a standalone battery-powered node, the Mote provides a convenient platform to quickly demonstrate the long-range capabilities of the modem, as well as to verify inter-operability when connecting to LoRaWAN gateways and infrastructure.

The Mote includes light and temperature sensors, which can be transmitted either on a fixed schedule or by a button-press. An OLED display provides connection status, sensor values and acknowledgements. A standard USB interface is provided for connection to a host computer, providing a bridge to the UART interface of the RN2483 modem.

##Experiment setup

                                                    Lora Modulation
                              LoRa Mote  ---------------------------------------  LoRa Mote
                                  |                                                   |
                     (USB Serial) |                                                   | (USB Serial)
                                  |                                                   |
                                Edison                                              Edison
                             (Controller)                                        (Controller)
                             
                             
##Hardware
* [Intel Edison - 2](http://www.intel.com/content/www/us/en/do-it-yourself/edison.html)
* [LoRa Mote - 2](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=dm164138#utm_medium=Press-Release&utm_term=LoRa%20Certification%20&utm_content=WPD&utm_campaign=868MHz)

##Software
--> On Edison:

* pySerial

To install pySerial and its depencies, execute install_serial.sh script

      ./install_serial.sh




