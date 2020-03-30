from Visa_Devices import Keysight_Osci
import sys

port = "USB0::0x0957::0x1796::MY59125234::0::INSTR"

InfiVision = Keysight_Osci(port)
InfiVision.open()

try:
    while True:
         InfiVision.meas_voltage_avg()
         InfiVision.save_volt_to_txt(TimeStamp=True)

except KeyboardInterrupt:
        print('Stopped by user')
        Newport.set_current(0)
        sys.exit(0)
