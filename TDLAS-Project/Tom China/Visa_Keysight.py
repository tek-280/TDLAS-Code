
#'Author: André Kussicke'
#import visa
import pyvisa

from time import *
import datetime
import matplotlib.pyplot as plt
import numpy as np

# @@@ port settings @@@

# example port = 'USB0::0xF4EC::0x1300::SSA3XLBX3R0749::0::INSTR'
port= ''

class Visa_Device():

    def __init__(self,port):
        self.port = port
        self.rm = visa.ResourceManager()

    def open(self):
        print(self.rm.list_resources())
        self.my_instrument = self.rm.open_resource(self.port)
        print("Initializing intrument:",self.my_instrument.query('*IDN?'))

    def close(self):
        self.my_instrument.close()

    def reset_settings(self):
        self.my_instrument.query('*CLS?')

class Keysight_counter(Visa_Device):

    def __init__(self,port):
        self.port=port
        self.rm = visa.ResourceManager()
    
    def init_TEMP_mode(self):
        #reset all device settings
        self.my_instrument.write("*RST")
        #empty buffer
        self.my_instrument.write("TRAC:CLE")
        #Change Volt measurement to temp measurement
        self.my_instrument.write("SENS:FUNC 'TEMP'")
        #Enable 4 wire temperature mesurement
        self.my_instrument.write("TEMP:TRAN FRTD")
        #select the temp. sensor type (PT100)
        self.my_instrument.write("TEMP:FRTD:TYPE PT100")
        #change the unit of the temp. measurement to deg. Celsius
        self.my_instrument.write("UNIT:TEMP C")
        #Turn beeper off during measurement
        self.my_instrument.write("SYSTEM:BEEPER:STATE OFF")

    def read_tmp(self):
        #Measure the temperatue on channel 1 / change channel
        self.my_instrument.write("ROUT:CLOS (@101)")
        #init a measurement
        self.my_instrument.write("INIT")
        #print the result of the measurement
        print("Temperature:@101: " + str(self.my_instrument.query("READ?")))

def main():
    if 1:
        programstart_str=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        #print(programstart_str)

    if 1:
        rm= pyvisa.ResourceManager()
        port='TCPIP0::192.168.1.101'
        keysight=rm.open_resource(port)
        #print(keysight.query("*IDN?"))
        temp_x=[]
        temp_y=[]
        i=0
        while i < 1001:
            i+=1
            val=keysight.query("READ?")
            print(i,val)
            temp_y.append(np.float(val))
            temp_x.append(time())
            
            if i == 999:
                temp_y=np.array((temp_y))
                if 0: # plotting
                    plt.plot(temp_x,temp_y,'r')
                    plt.plot(temp_x,temp_y,'bo')
                    plt.show()
                erg=np.vstack((temp_x,temp_y)).T
                if 1: #saving on
                    np.save('c:/Users/OPS_NIM/AppData/Local/Programs/Python/Python38/RUBIN/Data/%s_rubin_Keyseight_data' %programstart_str,erg)
                programstart_str=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
                temp_x=[]
                temp_y=[]
                i=0            
                
        keysight.close()
        
#if __name__ == "__main__":
#    main()


        
#port = 'GPIB0::10::INSTR'

#Keithley=Keithley_Thermometer(port)
#Keithley.open()
#Keithley.init_TEMP_mode()
#for i in range(1,10):
#    Keithley.read_tmp()
#    sleep(0.1)
#Keithley.close()




class Keithley_Thermometer(Visa_Device):

    def __init__(self,port):
        self.port=port
        self.rm = pyvisa.ResourceManager()
    
    def init_TEMP_mode(self):
        #reset all device settings
        self.my_instrument.write("*RST")
        #empty buffer
        self.my_instrument.write("TRAC:CLE")
        #Change Volt measurement to temp measurement
        self.my_instrument.write("SENS:FUNC 'TEMP'")
        #Enable 4 wire temperature mesurement
        self.my_instrument.write("TEMP:TRAN FRTD")
        #select the temp. sensor type (PT100)
        self.my_instrument.write("TEMP:FRTD:TYPE PT100")
        #change the unit of the temp. measurement to deg. Celsius
        self.my_instrument.write("UNIT:TEMP C")
        #Turn beeper off during measurement
        self.my_instrument.write("SYSTEM:BEEPER:STATE OFF")

    def read_tmp(self):
        #Measure the temperatue on channel 1 / change channel
        self.my_instrument.write("ROUT:CLOS (@101)")
        #init a measurement
        self.my_instrument.write("INIT")
        #print the result of the measurement
        print("Temperature:@101: " + str(self.my_instrument.query("READ?")))

class Newport_ILX(Visa_Device):

    def __init__(self,port):
        self.port=port
        self.rm = pyvisa.ResourceManager()

    def init_ITE_mode(self):
        self.my_instrument.write('MODE:ITE')
        self.my_instrument.write('LIMit:ITE:HIgh 2.5')
        self.my_instrument.write('LIMit:ITE:LOw -2.5')
        self.my_instrument.write(':OUTput ON')

    def set_current(self,Amps):
        self.my_instrument.write('SET:ITE '+str(Amps))
 
class Siglent(Visa_Device):
   
    def __init__(self,port):
        self.port=port
        self.rm = pyvisa.ResourceManager()

    def read_time(self):
        print(self.my_instrument.query(':SYSTem:TIME?'))
    
    def read_date(self):    
        print(self.my_instrument.query(':SYSTem:DATE?'))

    def read_spectrum(self):

        #Create Frequenzy-Array for the full measurement range
        start = float(self.my_instrument.query(':FREQuency:STARt?'))
        stop = float(self.my_instrument.query(':FREQuency:STOP?'))
        length = (stop -start)/750
        self.frequency = np.arange(start,stop+1,length) 
        
        #Read the Intensity values over the measured frequenzy range
        data = self.my_instrument.query(":TRACe:DATA? 1") 
        self.data_list = []
        #Siglent returns one String of 750 characters-> convert to float
        for i in range(0,751):
            self.data_list.append(float(data[i*16+i:16*(i+1)+i]))

        # Return the frequenzcy with the maximum intensity / potential Beat-frequency
        self.beat_frequency = self.frequency[self.data_list==np.max(self.data_list)]
        print("Beat-Frequency: ",self.beat_frequency[0],"Hz")

    def plot_spectrum(self):

        fig = plt.plot(self.frequency, self.data_list)
        plt.xlabel("frequency in Hz")
        plt.ylabel("amplitude in dBm")
        plt.grid() 
        plt.show()


        
port='TCPIP::172.30.253.246::INSTR'

Spectrum_analyser=Siglent(port)
Spectrum_analyser.open()
Spectrum_analyser.read_spectrum()
Spectrum_analyser.plot_spectrum()
Spectrum_analyser.close()