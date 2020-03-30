import sys
import time
import socket

from toptica.lasersdk.client import Client, NetworkConnection
from toptica.lasersdk.dlcpro.v1_6_3 import DLCpro

#Provide IP adress and Port:1998
conn1 = NetworkConnection('172.30.56.206')

#with Client(conn1) as client:
#    print(client.get('system-label', str))
#    client.set('system-label', 'Please do not touch!')
#   #client.exec('laser1:dl:lock:close')
#   # Execute command with binary output stream and no return value
#    print(client.get('system-type',str))
#    print(client.get('serial-number',str))




import base64
import sys
import time

from toptica.lasersdk.dlcpro.v2_0_3 import DLCpro, NetworkConnection, DeviceNotFoundError, DecopError, UserLevel

script = 'OyBjaGVja3N1bSBmYzc4NDcwOWE5MTQwY2M1Mjg3ZWNiN2M1ZTAxYTQ3YQo7CihwYXJhbS1zZXQh' \
         'ICd1cHRpbWUgMTIzNCkKKGRpc3BsYXkgIkhhbGxpaGFsbG9cbiIp'


def my_callback(timestamp, name, value, exc):
    if exc:
        print('Error occurred!')
        return

    print('--------------------------------------')
    print('Timestamp: ', timestamp)
    print('     Name: ', name)
    print('    Value: ', value)
    print('--------------------------------------')


def main():
    try:
        with DLCpro(conn1) as dlc:
            try:
                print("\n\n=== Sync Read ===\n")
                print('     System Time :', dlc.time.get())
                print('          Uptime :', dlc.uptime.get())
                print('Firmware Version :', dlc.fw_ver.get())
                print('   System Health :', dlc.system_health_txt.get())
                print('        Emission :', dlc.emission.get())
                print('  Scan Frequency :', dlc.laser1.scan.frequency.get())

                print("\n\n=== Sync Write ===\n")
                old_label = dlc.system_label.get()
                print('     System Label:', old_label)
                dlc.system_label.set('::: THE LABEL :::')
                print('     System Label:', dlc.system_label.get())
                dlc.system_label.set(old_label)
                print('     System Label:', dlc.system_label.get())

                print("\n\n=== Sync Command Output ===\n")
                print(dlc.system_summary())

                print("\n\n=== Sync Command Output+Return ===\n")
                dlc.change_ul(UserLevel.MAINTENANCE, 'CAUTION')
                print('System Connections:', dlc.system_connections())
                dlc.ul.set(3)

                print("\n\n=== Sync Command Input ===\n")
                print('           Uptime:', dlc.uptime.get())
                dlc.service_script(base64.b64decode(script))
                print('           Uptime:', dlc.uptime.get())

                print("\n\n=== Sync Command Normal ===\n")
                print(' User Level:', dlc.ul.get())
                dlc.change_ul(UserLevel.MAINTENANCE, 'CAUTION')
                print(' User Level:', dlc.ul.get())
                dlc.ul.set(3)
                print(' User Level:', dlc.ul.get())

                print("\n\n=== Monitoring ===\n")
                with dlc.uptime.subscribe(my_callback):
                    for _ in range(5):
                        dlc.poll()
                        time.sleep(1)

            except DecopError as error:
                print(error)
    except DeviceNotFoundError:
        print('Device not found')


if __name__ == "__main__":
    main()