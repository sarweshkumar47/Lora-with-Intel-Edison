import serial
import time
import sys
import time
import random

def send_command(cmd):
	port.write(cmd)
	time.sleep(0.1)
	port.flush()
	response = port.readline()
	print ('\n'+cmd + response.strip())
	if (response.strip() != 'ok'):
		port.write(cmd)
		time.sleep(0.1)
		port.flush()
		response = port.readline()
        	print ('\n'+cmd + response.strip()) 
        	if (response.strip() != 'ok'):
			print 'Invalid response'
			print 'Program terminated'
			sys.exit(0)			


def init_config():
	send_command('radio set mod lora\r\n')
	send_command('radio set freq 868000000\r\n')
	send_command('radio set pwr 14\r\n')
	send_command('radio set sf sf12\r\n')
	send_command('radio set afcbw 125\r\n')
	send_command('radio set rxbw 250\r\n')
	send_command('radio set fdev 5000\r\n')
	send_command('radio set prlen 8\r\n')
	send_command('radio set crc on\r\n')
	send_command('radio set cr 4/8\r\n')
	send_command('radio set wdt 0\r\n')
	send_command('radio set sync 12\r\n')
	send_command('radio set bw 250\r\n')
	print 'Lora configuration done.\n'

def clearbuffer():
   	port.write('mac get status\r\n')                             
        time.sleep(0.1)                               
        port.flush()                                
        response = port.readline()                 
        print ('\n'+'mac get status, ' + response.strip()) 
	print ('Lora buffer is cleared\n')   		

def main():
	if(len(sys.argv) > 1):
		if(sys.argv[1] == '--config'):
			init_config()
			sys.exit(0)

		elif(sys.argv[1] == '--pre'):
			clearbuffer()
			sys.exit(0)

		else:
			print '\nUnknown arguments passed to the program'
			print '\nProgram terminated'
			sys.exit(0)

	else:
		try:
			port.write('mac pause\r\n')
			time.sleep(0.1)
            		port.flush()
            		print("waiting for ack mac pause...")
            		response = port.readline()
            		print('\nmac pause ack, ' + response)
			try:
				if(int(response)):
					pass
			except:
				port.write('mac pause\r\n')                      
                        	time.sleep(0.1)                                    
                        	port.flush()                                     
                        	print("waiting for ack mac pause...")            
                        	response = port.readline()                         
                        	print('\nmac pause ack, ' + response)  
				try:                                             
                                	if(int(response)):                       
                                        	pass                             
                        	except:       
					print '\nLora is not ready'
					print '\nProgram terminated'
					sys.exit(0)
			
			random_num = random.randint(1,1000)
                	port.write('radio tx '+ str(random_num) + '\r\n\r\n')
			time.sleep(0.1)
            		port.flush()
	    		print('Data sent, '+ str(random_num))
            		print('waiting for ack...')
            		response_bef = port.readline()
	    		response_aft = port.readline()
            		print('\nimmid resp, ' + response_bef.strip())
	    		print ('\nafter resp, ' + response_aft.strip())

			port.write('mac resume\r\n')      
                        time.sleep(0.1)                                  
                        port.flush()                                     
                        print('waiting for ack mac resume...')                  
                        resp = port.readline()   
			print ('mac resume resp, '+resp.strip())
			port.close()

        	except KeyboardInterrupt:
            		print "Keyboard Interrupt"
	    		port.close()

        	except serial.SerialException:                                              
                	print '\nDevice not found'                                   
                	print '\nProgram terminated'                                 
			port.close()
                	sys.exit(0) 
  
         	except:
	        	print "Exception"
	        	port.close()

if __name__ == "__main__":
	print "Lora data transmission sequence initiated"
	print "-------------------------------------------------------------"

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
