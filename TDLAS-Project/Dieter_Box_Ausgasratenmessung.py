#Author: André Kussike, (TR)

from Serial_Devices import Physics_1000
from Visa_Devices import Newport_ILX
from simple_pid import PID
from time import sleep
import sys

#DieterBox.py is PI(D) regulator for a thermal box. 
#The temperature is measured using: the "Ahlborn Physics 1000" thermometer.
#The temperature is controlled via a peltier element which is connected to a bipolar current source: "Newport ILX LDT-5940C"
#Target Precision is 1mK. (26.11.2019: Precision at ~3mK with the current PI-settings)

#Newport 
port =  'USB0::0x1FDE::0x0007::59401447::0::INSTR'
#Ahlborn
serial = 'COM3'

Newport = Newport_ILX(port)
Ahlborn = Physics_1000(serial)

Newport.open()
Newport.init_ITE_mode()

#Settings for PID 
pid= PID(-5,-0.02,0,setpoint=23.0)
#max and min output values of the PID
pid.output_limits = (-2.5, 2.5)
#Delay betweeen calculations in s
pid.sample_time = 1


tmp = Ahlborn.read_tmp()

if __name__ == '__main__':
    try:
        while True:
            #refreshed reading of the tmp
            tmp = Ahlborn.read_tmp()
            p, i, d = pid.components
            
            Ahlborn.save_tmp_to_txt(TimeStamp=True)
            # compute new ouput from the PID according to the systems current temp value
            control = pid(tmp)
            #adjust the current accordingly.
            Newport.set_current(control)
            sleep(1)

    except KeyboardInterrupt:
        print('Stopped by user')
        Newport.set_current(0)
        sys.exit(0)

Newport.close()