
#'Author: André Kussicke'
import visa #same as pyvisa..
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime

#Visa_Devices.py is a list off classes for different VISA-compatible devices. Class functions include basic communication with the devices and reading data.
#A programming example is provided after each "Device-Class". The corresponding device-port is also listed.
#The first class: "Visa_Device" contains functions that can be used by all devices and is inherited to all other classes / devices.

#The Following Devices are inluded: 
#Keithley-Multimeter
#Newport ILX: Bipolar current source // TEC 
#Siglent Spectrum analyzer
#Keysight Frequency Counter (China visit Tom)

#-------------------------------------------------------------------------------------------------------------------------------------------------
class Visa_Device():

    def __init__(self,port):
        self.port = port
        self.rm = visa.ResourceManager()
        self.buffer = [] #Used for data storing within a class instance. Class methods that can use the buffer have the "WriteToBuffer" option.

    def open(self):# opens any Visa device and lists the current harware ports
        print(self.rm.list_resources('?*'))
        self.my_instrument = self.rm.open_resource(self.port)
        print("Initializing intrument:",self.my_instrument.query('*IDN?'))

    def close(self):# closes any Visa device / required for many devices at the end of the code
        self.my_instrument.close()

    def reset_settings(self): # Sets the device settings to default
        self.my_instrument.query('*CLS?')
    
    def plot_buffer(self):# Plots the data in the measurement buffer
        if len(self.buffer) == 0 or None:
            print("The buffer is empty!")
        else:
            self.buffer =np.vstack(self.buffer)
            for i in range(1,int(len(self.buffer)/2+1)):
                plt.plot(self.buffer[0],self.buffer[2*i-1])
            plt.show()
            #self.buffer = np.transpose(self.buffer)

    def Empty_buffer(self): #empties the measurement buffer
        self.buffer = []

#---------------------------------------------------------------------------------------------------------------------------------------------------
class Keithley_Thermometer(Visa_Device):

    def __init__(self,port):
        super().__init__(port)
        self.counter = 0
        self.temp_value = 0
        self.temp = []
        self.time_value = 0
        self.time = []
        self.starttime = time.time()
    
    def init_TEMP_mode(self): #Changes the settings of the multimeter to operate in temperature mode, with pt100 sensors (4-wire setting)
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

    def read_tmp(self,Meas_cycle_number,WriteToBuffer = bool):#reads temperature values on channel #1
        #Measure the temperatue on channel 1
        self.my_instrument.write("ROUT:CLOS (@101)")
        #init a measurement
        self.my_instrument.write("INIT")
        #print the result of the measurement
        #rint("Temperature:@101: " + str(self.my_instrument.query("READ?")))
        self.temp_value = float(self.my_instrument.query("READ?")[1:16])
        self.time_value = abs(self.starttime - time.time())
        if WriteToBuffer == True:
            self.time.append(self.time_value)
            self.temp.append(self.temp_value)
            
            #self.buffer
            self.counter += 1
            if self.counter == N-1:
                self.counter = 0
                self.time = np.array(self.time)
                self.temp = np.array(self.temp)
                self.buffer.append((self.time,self.temp))
        else:
            return self.temp
    @classmethod
    def change_meas_cycle(cls,N_new):
        cls.N=N_new

#Example Code: opens the device, initializes temp. measurement, reads 10 temp. values on channel 1, closes the device.
#N= 2
#port = 'GPIB0::10::INSTR'
#Keithley=Keithley_Thermometer(port)
#Keithley.open()
#Keithley.init_TEMP_mode()

#for i in range(1,N):
#    Keithley.read_tmp(N,WriteToBuffer=True)
#    #print(Keithley.buffer)
#    time.sleep(0.1)
#plt.plot(Keithley.buffer[0],Keithley.buffer[1])
#Keithley.plot_buffer()
#plt.show()
#Keithley.close()

#------------------------------------------------------------------------------------------------------------------------------------------
class Newport_ILX(Visa_Device):

    def __init__(self,port):
        super().__init__(port)

    def init_ITE_mode(self): # initializes the ITE mode (Constant current mode), sets the max and min output current to +-2.5A
        self.my_instrument.write('MODE:ITE')
        self.my_instrument.write('LIMit:ITE:HIgh 2.5')
        self.my_instrument.write('LIMit:ITE:LOw -2.5')
        self.my_instrument.write(':OUTput ON')

    def set_current(self,Amps):# sets the output current to the value defined in the "Amps" variable
        self.my_instrument.write('SET:ITE '+str(Amps))


#Example Code: Opens Device in ITE mode and sets Current to 1 A

#port =  'USB0::0x1FDE::0x0007::59401447::0::INSTR'
#Newport = Newport_ILX(port)
#Newport.set_current(1)
#Newport.close()

#Example Code #1: "Dieter_Box.py"

#-------------------------------------------------------------------------------------------------------------------------------------------

class Siglent(Visa_Device):
   
    def __init__(self,port):
        super().__init__(port)
        self.frequency = 0
        self.amplitude = []

    def read_time(self):#reads the system time
        print(self.my_instrument.query(':SYSTem:TIME?'))
    
    def read_date(self): # reads the system date
        print(self.my_instrument.query(':SYSTem:DATE?'))

    def read_spectrum(self,WriteToBuffer = bool): #gets the current spectrum
        self.frequency=0
        self.amplitude=[]
        #Create Frequenzy-Array for the full measurement range
        start = float(self.my_instrument.query(':FREQuency:STARt?'))
        stop = float(self.my_instrument.query(':FREQuency:STOP?'))
        length = (stop -start)/750
        self.frequency = np.arange(start,stop+1,length) 
        #Read the Intensity values over the measured frequenzy range
        data = self.my_instrument.query(":TRACe:DATA? 1") 
        for i in range(0,751):
            self.amplitude.append(float(data[i*16+i:16*(i+1)+i]))
        # Returns the frequenzcy with the maximum intensity / potential Beat-frequency
        self.amplitude=np.array(self.amplitude)
        self.beat_frequency = self.frequency[self.amplitude == np.max(self.amplitude)]
        print("Beat-Frequency: ",self.beat_frequency[0],"Hz") #probably bad due to artifact at freq = 0 Hz -> result might always be 0 Hz 
        
        if WriteToBuffer == True:
            self.buffer.append((self.frequency,self.amplitude))
            
        else:
            return self.frequency,self.amplitude

#Example Code: Opens Device, reads the current spectrum, plots the data and closes the device


if 0:
    port='TCPIP::172.30.253.246::INSTR'
    #port_1 = 'TCPIP::172.30.253.247::INSTR'
    Spectrum_Analyzer = Siglent(port)
    Spectrum_Analyzer.open()
    Spectrum_Analyzer.read_spectrum()
    Spectrum_Analyzer.close()

#-----------------------------------------------------------------------------------------------------------------------------------------
class Keysight_Counter(Visa_Device):

    def __init__(self,port):
        super().__init__(port)
        self.time = 0
        self.freq = 0
    
    def read_freq(self,WriteToBuffer=bool):
        self.programstart_str=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        #Measurement loop: stores frequency over time
        temp_time = []
        temp_freq = []
        i=0
        while i < 1001:
            i+=1
            value = self.my_instrument.query("READ?")
            print(i,value)
            temp_freq.append(np.float(value))
            temp_time.append(time())
            if i == 999:
                temp_freq = np.array((temp_freq))
            else:
                pass
        #Measurement loop finished: sets "global" variables for frequency and time for other class functions to use
        self.time = temp_time
        self.freq = temp_freq
        
        if WriteToBuffer == True:
            self.buffer.append([self.time,self.freq])
        else:
            return self.time,self.freq


    def save_freq_to_txt(self,filepath):
        self.filepath = filepath
        result = np.vstack((self.time,self.freq)).T
        np.save(str(self.filepath)+'%s_rubin_Keyseight_data' %programstart_str,result)
    

#Example Code: opens Device, reads frequency, plots data, saves data to file and closes device.

#port='TCPIP0::192.168.1.101'
#filepath = '' #Add a filepath here..
#Frequency_Counter = Keysight_Counter(port)
#Frequency_Counter.open()
#Frequency_Counter.read_freq()
#Frequency_Counter.plot_freq()
#Frequency_Counter.save_freq_to_txt()
#Frequency_Counter.close()
#-----------------------------------------------------------------------------------------------------------------------------------------
#port= "USB0::0x0957::0x1796::MY59125234::0::INSTR"
class Keysight_Osci(Visa_Device):

    def __init__(self,port):
        super().__init__(port)
 
    def meas_voltage_avg(self):
        self.V_max= float(self.my_instrument.query(':MEASure:VMAX? CHAN1')[:-2])
        self.V_min= float(self.my_instrument.query(':MEASure:VMIN? CHAN1')[:-2])
        print("V_max: " +str(self.V_min) + " V")
        print("V_max: " +str(self.V_max) + " V")

    def save_volt_to_txt(self,TimeStamp=None):

        self.f = open(str(time.strftime("%Y-%m-%d"))+"-InfiVision_Osci-Voltage-log-file.txt","a")

        if TimeStamp == True or TimeStamp == None:
        #With time stamp and temperature values
            self.f.write(str(time.strftime("%H:%M:%S") + "\t" + str(self.V_min) + " V"+ "\t" + str(self.V_max) + " V" + "\n") )

        elif TimeStamp == False:
        #without timestamp, only temp values, no units, for easy plotting
            self.f.write(str(self.V_max) + "\n")

        self.f.close()



class Meerstetter(Visa_Device):

    def __init__(self,port):
        super().__init__(port)

    def read_temperature(self): # initializes the ITE mode (Constant current mode), sets the max and min output current to +-2.5A
        temp = self.my_instrument.query("?TT")
        print(temp)

rm = visa.ResourceManager()
print(rm.list_resources('?*'))
#port='TCPIP0::192.168.1.101'
#filepath = '' #Add a filepath here..
#Frequency_Counter = Keysight_Counter(port)