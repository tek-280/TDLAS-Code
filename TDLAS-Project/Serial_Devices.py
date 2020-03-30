#Author: André Kussicke

import serial
import time
from time import sleep
import sys

#Serial_Devices.py is a list off classes for operating different serial devices. Class functions include basic communication with the devices and reading data.
#The ports (COM1,COM2,COM3,...) are given to the devices after installing the drivers.

#The Following Devices are inluded: 

#Ahlborn: Physics 1000, Thermometer (1mK resolution)
#AimTTi: TF930, Frequenzy counter




class Physics_1000(): 

    def __init__(self, port): 
        #opens the serial connection to the digital thermometer. Port gives the physical location of the device (26.11.2019: Port = COM3)
        self.port = serial.Serial(port = port)

    def read_tmp(self):
        #Command to read the temperature. Also returns min and max values as a list of "bytes".
        self.port.write(b'P18')
        #sleep 0.05s to avoid problems with reading.
        sleep(0.05)
        #The first 55 bytes in the list are "literals" the temperature value is given by the 6 bytes that come afterwards.
        self.port.read(55)
        #sleep 0.005s to avoid problems.
        sleep(0.05)
        # Gather the relevant information from the 6 bytes and convert the result to a float nuber.
        MESSWERT=[]
        MESSWERT.append((self.port.read(6)))
        self.TEMP = float(MESSWERT[0].decode())
        #closing the port flushes the buffer and allows a new reading
        self.port.close()
        #port has to be opened again after closing it
        self.port.open()
        print("Temperature: "+ str(self.TEMP) +" \N{DEGREE SIGN}C")
        return self.TEMP

    def save_tmp_to_txt(self,TimeStamp=None):

        self.f = open(str(time.strftime("%Y-%m-%d"))+"-Physics_1000-tmp-log-file.txt","a")

        if TimeStamp == True or TimeStamp == None:
        #With time stamp and temperature values
            self.f.write(str(time.strftime("%H:%M:%S") + "\t" + str(self.TEMP) +" \N{DEGREE SIGN}C" + "\n") )

        elif TimeStamp == False:
        #without timestamp, only temp values, no units, for easy plotting
            self.f.write(str(self.TEMP) + "\n")

        self.f.close()

#Example Code:
#See "Dieter_Box.py"

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
class AimTTi_TF930():

    #Commands in byte format, terminating characters: "\n\r" are required, multiple commands can be sent when seperated by ";" , (26.11.2019: Port = COM4)

    def __init__(self,port):
        #AimTTi needs a baudrate of 115200, timeout=0 wait "forever" for a response of the device
        self.port = serial.Serial(port = port,baudrate=115200,timeout = 1)

    def IDN(self):
        self.port.write(b'*IDN?;I?\n\r')
        WERT=[]
        WERT.append((self.port.read(55)))
        print(WERT[0].decode())

    def init_freq_mode(self,Channel=None):

        WERT=[]
        self.Channel= Channel
        
        if self.Channel == "A":
            self.port.write(b'F2;M2;?\n\r')

        elif self.Channel == "B" or self.Channel == None:
            self.port.write(b'F3;M2;?\n\r')
        
        WERT.append((self.port.read(55)))
        print(WERT[0].decode())
    
    def read_freq(self):
        WERT = []
        self.port.write(b'?\n\r')
        WERT.append((self.port.read(55)))
        print(WERT[0].decode())

#Example Code: Continiously reads the frequency on the counter, programm can be stopped with" Ctrl + C".
#port = "COM4"
#if __name__ == '__main__':
#    Frequency_Counter = AimTTi_TF930(port)
#    Frequency_Counter.init_freq_mode(Channel="B")
#    try:
#        while True:
#            Frequency_Counter.read_freq()
#    except KeyboardInterrupt:
#        print('Stopped by user')
#        sys.exit(0)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------



class IONIVAC_IM520():

    def __init__(self,port):
        self.port = serial.Serial(port = port)

    def read_pressure(self):
        WERT = []
        self.port.write(b'MES R\r\n')
        WERT.append((self.port.read(55)))
        print(WERT[0].decode())


#Example Code: 
#port = 'GPIB0::12::INSTR'
#ioniVac= IONIVAC_IM520(port)
#ioniVac.read_pressure()

#-------------------------------------------------------------------------------------------------------------------------------------------

