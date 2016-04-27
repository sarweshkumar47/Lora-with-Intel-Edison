'''
* LoRa is a spread-spectrum modulation technique which allows sending data at extremely low data-rates to extremely 
  long ranges.
* The LoRa Mote is a demo board that showcases the Microchip Low-Power Long Range LoRa Technology Transceiver Module.
* The LoRa Mote provides access to the module through UART/USB Serial communications and supports connection points to
  all GPIO-controlled module pins.
* The default settings for the UART interface are 57600 bps, 8 bits, no parity, 1 Stop bit, no flow control
* The baud rate can be changed by triggering the auto-baud detection sequence of the module. To do this, the host system
  needs to transmit to the module a break condition followed by a 0x55 character at the new baud rate
'''
import serial
import time
import sys
import time
import random

'''
    Send configuration parameters to the lora module
'''
def send_command(cmd):
	port.write(cmd)
	time.sleep(0.1)
	port.flush()
	# Returns invalid_param if the command is not valid/failed, then try again
	response = port.readline()
	print ('\n'+cmd + response.strip())
	
	if (response.strip() != 'ok'): 
		port.write(cmd)
		time.sleep(0.1)
		port.flush()
		# Returns invalid_param if the command is not valid/failed, then exit
		response = port.readline()
        	print ('\n'+cmd + response.strip()) 

        	if (response.strip() != 'ok'): 
			print '\nLora is not responding, please restart'
			print '\nProgram terminated'
			sys.exit(0)

'''
    Setting the Radio configuration parameters
'''
def init_config():
	send_command('radio set mod lora\r\n') # Set the module Modulation mode, either lora or FSK
	send_command('radio set freq 868000000\r\n') # Set the current operation frequency for the radio
	send_command('radio set pwr 14\r\n') # Set the output power level used by the radio during transmission
	send_command('radio set sf sf12\r\n') # Set the requested spreading factor (SF) to be used during transmission
	send_command('radio set afcbw 125\r\n') # Set the value used by the automatic frequency correction bandwidth for receiving/transmitting
	send_command('radio set rxbw 250\r\n') # Set the operational receive bandwidth
	send_command('radio set fdev 5000\r\n') # Set the frequency deviation allowed by the end device
	send_command('radio set prlen 8\r\n') # Set the preamble length used during transmissions
	send_command('radio set crc on\r\n') # Set if a CRC header is to be used
	send_command('radio set cr 4/8\r\n') # Set the coding rate used by the radio
	send_command('radio set wdt 0\r\n') # Set the time-out limit for the radio Watchdog Timer
	send_command('radio set sync 12\r\n') # Set the sync word used
	send_command('radio set bw 250\r\n') # Set the value used for the radio bandwidth
	print '\nLora configuration is done.'

'''
    Check the current status of the module
    and set radio receiver wdt timer to 90 secs
'''
def lora_init():
   	port.write('mac get status\r\n')                             
        time.sleep(0.1)                               
        port.flush()         
	# Response: 2-byte hexadecimal number representing the current status of the module                                         
        response = port.readline()  
        print ('\n'+'mac get status, ' + response.strip())
	send_command('radio set wdt 90000\r\n')
	print ('\nLora initialization is done.')   		

'''
    Main program starts

    optional flags:

	--config - sets the Radio configuration parameters (only first-time needed)
	
	--pre - checks the current status of the module and sets radio receiver wdt timer to 90 secs
'''
def main():
	if(len(sys.argv) > 1):
		if(sys.argv[1] == '--config'):
			init_config()
			sys.exit(0)

		elif(sys.argv[1] == '--pre'):
			lora_init()
			sys.exit(0)

		else:
			print '\nUnknown argument passed to the program'
			print '\nProgram terminated'
			sys.exit(0)

	else:
		try:
			# mac pause : pauses the LoRaWAN stack functionality to allow transceiver (radio) configuration
			port.write('mac pause\r\n')
			time.sleep(0.1)
            		port.flush()
            		print("waiting for ack (mac pause)...") 

			# mac pause response : 0 – 4294967295 (decimal number representing the number of millis the mac can be paused)
			# Returns invalid_param if the command is not valid/failed, then try again
            		response = port.readline()
            		print('\nmac pause ack, ' + response)

			try:				
				if(int(response)):
					pass
			except:
				port.write('mac pause\r\n')                      
                        	time.sleep(0.1)                                    
                        	port.flush()                                     
                        	print("waiting for ack (mac pause)...") 

				# Returns invalid_param if the command is not valid/failed, then exit           
                        	response = port.readline()                         
                        	print('\nmac pause ack, ' + response) 
 
				try:                                             
                                	if(int(response)):                       
                                        	pass                             
                        	except:   

					print '\nLora is not responding, please restart'
					print '\nProgram terminated'
					sys.exit(0)

			# radio rx : enables Continuous Reception Mode, will be exited once a valid packet is received
                	port.write('radio rx 0\r\n')
			time.sleep(0.1)
            		port.flush()
            		print("waiting for data...")
			
			# Response: this command may reply with two responses. 
			# The first response will be received immediately after entering the command. 
			# If the command is valid (ok reply received), a second reply will be received
 			# after the reception of a packet or after the time out occurred
            		response_bef = port.readline()
	    		response_aft = port.readline()
            		print('\nimmid resp, ' + response_bef.strip())
	    		print ('\nafter resp, ' + response_aft.strip())

			# mac resume : resumes LoRaWAN stack functionality, in order to continue normal 
			# functionality after being paused
			port.write('mac resume\r\n')      
                        time.sleep(0.1)                                  
                        port.flush()                                     
                        print('\nwaiting for ack (mac resume)...')     
			# mac resume response : ok             
                        resp = port.readline()   
			print ('\nmac resume resp, '+resp.strip())
			port.close()

        	except KeyboardInterrupt:
            		print '\nKeyboard Interrupt'
                	print '\nProgram terminated'                                 
	    		port.close()

        	except serial.SerialException:                                              
                	print '\nDevice not found'                                   
                	print '\nProgram terminated'                                 
			port.close()
  
         	except:
	        	print '\nException'
                	print '\nProgram terminated'                                 
	        	port.close()

if __name__ == "__main__":
	print '\nLora data reception sequence initiated'
	print '-------------------------------------------------------------'
	
	# The default settings for the UART/USB Serial interface are 57600 bps, 8 bits, no parity, 1 Stop bit, no flow control
	try:                       
        	port=serial.Serial(  
                    "/dev/ttyACM0",           
                    baudrate=9600,               
                    parity=serial.PARITY_NONE,   
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS, 
                    inter_byte_timeout = 0.001,
                    rtscts=True,  
                    dsrdtr=True,                    
                    xonxoff=False)                  
                print '\nPort is open?', port.isOpen()
		port.reset_input_buffer()
		port.reset_output_buffer()

        except serial.SerialException:             
                print '\nDevice not found'  
                print '\nProgram terminated'
                sys.exit(0)

	main()
