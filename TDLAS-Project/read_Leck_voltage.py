#import coloredlogs
#import logging
import requests
import json
#import redis
import sys
import time

#relay = config.get("relay")
#temp_text='curl -X PUT -d '{"Action":"TCP","Host":"192.168.98.137","Port":5300,"Value":"*read?\n"}' '
data={"Action":"TCP","Host":"192.168.98.137","Port":5300,"Value":"*read?\r"}
#req = requests.post("http://i75464.berlin.ptb.de:55555", data=json.dumps(data))
#res = req.json()
#print(res)


filepath= r"C:/Users/vaclab\Desktop/TDLAS-Project/Data_Leck_Voltage/"

flag=my_time=time.time()

if 1:
    while 1:
        try:
            req = requests.post("http://a73434.berlin.ptb.de:55555", data=json.dumps(data))
            res = req.json()            
            my_time=time.time()
            if my_time-flag>10:
                my_date=str(time.strftime("%H:%M:%S")) 
                print('read_Leck_voltage',str(my_date))
                print(str(res))
                flag=my_time=time.time()
            my_date=str(time.strftime("%Y-%m-%d"))            
            f = open("%s%s Lecktester-log-file.txt" %(filepath,my_date),"a")
            f.write(str(my_time) + "\t" + str(res) + "\n")
            f.close()
            time.sleep(0.1)
        except:
            print(time.strftime("%H-%M-%S"),"Error while trying!")
            time.sleep(10)
