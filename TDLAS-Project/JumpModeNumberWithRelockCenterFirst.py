#with Client(NetworkConnection('192.168.1.206')) as client: # 'T' Top-Laser: DLC PRO_041859
#with Client(NetworkConnection('192.168.1.205')) as client: # 'B' Bottom-Laser: DLC PRO_041865

import matplotlib.pyplot as pyplot
import  numpy as np
#from toptica.lasersdk.dlcpro.v2_0_3 import DLCpro, NetworkConnection, DeviceNotFoundError
from toptica.lasersdk.dlcpro.v2_0_3 import *
from toptica.lasersdk.utils.dlcpro import *

from toptica.lasersdk.client import Client, NetworkConnection
import time

def main():

    if 1:
        with DLCpro(NetworkConnection('192.168.1.205')) as dlcpro:
            #client.exec('buzzer:play "A B C D E G F E D F E D C E D C"')
            #client.exec('buzzer:play "A A A A A A E E H E H E AAAA"')
            #client.exec('laser1:dl:lock:close')
            #client.exec('laser1:dl:lock:open')
            #old_voltage=dlcpro.laser1.dl.pc.voltage_act.get()
            #v_locked=dlcpro.laser1.dl.pc.voltage_act.get()
            #dlcpro.laser1.dl.lock.open()
            #dlcpro.laser1.dl.pc.voltage_set.set(v_locked)
            for i in range(10):
                print(dlcpro.laser1.dl.lock.pid1.values())
                time.sleep(0.2)
            #dlcpro.laser1.dl.lock.close()

        if 0:
            my_jump=-2.30

            old_setvolt=dlcpro.laser1.dl.pc.voltage_set.get()
            #print(old_setvolt)
            #old_actvolt=dlcpro.laser1.dl.pc.voltage_act.get()
            #new_actvolt=old_actvolt+my_jump
            
            #new_setvolt=old_actvolt+my_jump
            
            new_setvolt=old_setvolt+my_jump
            #print('old:',old_actvolt)
            print('old:',old_setvolt)
            
            print('new:',new_setvolt)
            dlcpro.laser1.dl.pc.voltage_set.set(new_setvolt)
            time.sleep(0.2)
            dlcpro.laser1.dl.lock.close()


     

       
    if 0:
        with DLCpro(NetworkConnection('192.168.1.205')) as dlcpro:
            #client.exec('buzzer:play "A B C D E G F E D F E D C E D C"')
            #client.exec('buzzer:play "A A A A A A E E H E H E AAAA"')
            #client.exec('laser1:dl:lock:close')
            #client.exec('laser1:dl:lock:open')
            #old_voltage=dlcpro.laser1.dl.pc.voltage_act.get()

            my_jump=+2.3

            old_setvolt=dlcpro.laser1.dl.pc.voltage_set.get()
            old_actvolt=dlcpro.laser1.dl.pc.voltage_act.get()
            new_actvolt=old_actvolt+my_jump
            new_setvolt=old_setvolt+my_jump
            dlcpro.laser1.dl.pc.voltage_set.set(new_setvolt)

            print('jump 1 of 4 done, wait 3 sec.')
            time.sleep(3)

            temp_actvolt=dlcpro.laser1.dl.pc.voltage_act.get()
            delta=new_actvolt-temp_actvolt
            new_setvolt=new_setvolt-delta
            dlcpro.laser1.dl.pc.voltage_set.set(new_setvolt)

            print('jump 2 of 4 done, wait 2 sec.')
            time.sleep(2)

            temp_actvolt=dlcpro.laser1.dl.pc.voltage_act.get()
            delta=new_actvolt-temp_actvolt
            new_setvolt=new_setvolt-delta
            dlcpro.laser1.dl.pc.voltage_set.set(new_setvolt)

            print('jump 3 of 4 done, wait 1 sec.')
            time.sleep(1)

            temp_actvolt=dlcpro.laser1.dl.pc.voltage_act.get()
            delta=new_actvolt-temp_actvolt
            new_setvolt=new_setvolt-delta
            dlcpro.laser1.dl.pc.voltage_set.set(new_setvolt)
            print('jump 4 done')

            #print(old_setvolt)
            #76.539430
            #74.309430
            #72.263703

            #71.4
            #74.0
            #76.3
            #78.6
            #80.9
            #83.1










            #print(old_actvolt)
            #delta=old_actvolt-old_setvolt
            #print(delta)
            #new_volt=old_setvolt+2.3+delta
            #new_volt=old_setvolt+0.1
            
            #print(new_volt)
            #dlcpro.laser1.dl.pc.voltage_set.set(new_volt)
            #print(dlcpro.laser1.dl.lock.state.get())

    if 0:
        with Client(NetworkConnection('192.168.1.205')) as client:
            #client.laser1.dl.pc.set.voltage('80.018000')
            #client.laser1.dl.pc.voltage.set('80.018000')
            #client.exec('laser1.dl.pc.set.voltage "80.018000"')
            client.exec('laser1:dl:lock:close')
            #client.exec('laser1:dl:lock:open')

if 0:
    if 0:
        with DLCpro(NetworkConnection('192.168.1.205')) as dlcpro:
            # Retrieve scan, lock raw data from device
            scope_data = extract_float_arrays('xyY', dlcpro.laser1.scope.data.get())
            raw_lock_candidates = dlcpro.laser1.dl.lock.candidates.get()
            lock_candidates = extract_lock_points('clt', raw_lock_candidates)
            lock_state = extract_lock_state(raw_lock_candidates)

            # Create double y axis plot
            fig, laxis = pyplot.subplots()
            fig.suptitle('DLC pro Scope Output')

            ch1_available = dlcpro.laser1.scope.channel1.signal.get() != -3  # Signal is 'none'
            ch2_available = dlcpro.laser1.scope.channel2.signal.get() != -3

            # Set label and unit of X axis
            laxis.set_xlabel("{} [{}]".format(
                dlcpro.laser1.scope.channelx.name.get(),
                dlcpro.laser1.scope.channelx.unit.get()))

            if ch1_available:
                red = laxis

                # Set label and unit of left Y axis
                red.set_ylabel("{} [{}]".format(
                    dlcpro.laser1.scope.channel1.name.get(),
                    dlcpro.laser1.scope.channel1.unit.get()),
                    color='red')

                # Plot first scope channel data
                red.plot(
                    scope_data['x'],
                    scope_data['y'],
                    linestyle='solid',
                    color='red',
                    zorder=1)

                # Plot lock candidate points if available
                if 'c' in lock_candidates.keys():
                    red.plot(
                        lock_candidates['c']['x'],
                        lock_candidates['c']['y'],
                        linestyle='None',
                        marker='o',
                        markersize=12.0,
                        color='grey',
                        zorder=2)

                # Plot selected lock candidate point if available
                if 'l' in lock_candidates.keys() and lock_state == 3:  # State is 'Selected'
                    red.plot(
                        lock_candidates['l']['x'],
                        lock_candidates['l']['y'],
                        linestyle='None',
                        marker='o',
                        markersize=16.0,
                        color='red',
                        markerfacecolor='none',
                        zorder=3)

                # Retrieve and plot background trace data if lock is closed
                if lock_state == 5:  # State is 'Locked'
                    background_trace = extract_float_arrays('xy', dlcpro.laser1.dl.lock.background_trace.get())

                    red.plot(
                        background_trace['x'],
                        background_trace['y'],
                        linestyle='solid',
                        color='lightgrey',
                        zorder=1)

                # Plot lock tracking position if available
                if 't' in lock_candidates.keys():
                    red.plot(
                        lock_candidates['t']['x'],
                        lock_candidates['t']['y'],
                        linestyle='None',
                        marker='o',
                        markersize=20.0,
                        color='red',
                        markerfacecolor='none',
                        zorder=3)

            # Plot second scope channel data if available
            if ch2_available:
                if ch1_available:
                    blue = laxis.twinx()
                else:
                    blue = laxis

                blue.set_ylabel("{} [{}]".format(
                    dlcpro.laser1.scope.channel2.name.get(),
                    dlcpro.laser1.scope.channel2.unit.get()),
                    color='blue')

                blue.plot(
                    scope_data['x'],
                    scope_data['Y'],
                    linestyle='solid',
                    color='blue',
                    zorder=0)

                laxis.set_zorder(blue.get_zorder() + 1)
                laxis.patch.set_visible(False)

            pyplot.margins(x=0.0)
            pyplot.show()

    #except DeviceNotFoundError:
    #    sys.stderr.write('Device not found')


if __name__ == "__main__":
    main()