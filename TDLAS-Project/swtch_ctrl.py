#import coloredlogs
#import logging
import requests
import json
#import redis
import sys
import time

#pw und admin für Seite e75449 (hut): admin /// anel
#Auch nachzulesen unter: https://a75436.berlin.ptb.de/vaclab/relayServer



#relay = config.get("relay")
#temp_text='curl -X PUT -d '{"Action":"TCP","Host":"192.168.98.137","Port":5300,"Value":"*read?\n"}' '
data_off1={"Action":"UDP","Host":"e75449","Port": 4165,"Value":"Sw_off1adminanel","Timeout":0}
data_on1={"Action":"UDP","Host":"e75449","Port": 4165,"Value":"Sw_on1adminanel","Timeout":0}
data_off2={"Action":"UDP","Host":"e75449","Port": 4165,"Value":"Sw_off2adminanel","Timeout":0}
data_on2={"Action":"UDP","Host":"e75449","Port": 4165,"Value":"Sw_on2adminanel","Timeout":0}
#req = requests.post("http://i75464.berlin.ptb.de:55555", data=json.dumps(data))
#res = req.json()
#print(res)
valve1_stat=0
valve2_stat=0

filepath= r"C:/Users/vaclab\Desktop/TDLAS-Project/Data_Valves/"

def save_Valves_stats(my_time):
    my_date=str(time.strftime("%Y-%m-%d"))
    f = open("%s%s Valves_stats-log-file.txt" %(filepath,my_date),"a")
    global valve1_stat
    global valve2_stat    
    f.write("%f\t%i\t%i\n" %(my_time, valve1_stat, valve2_stat))
    f.close()

def open2():
    req = requests.post("http://a73434.berlin.ptb.de:55555", data=json.dumps(data_on2))
    print(str(time.strftime("%H:%M:%S %Y-%m-%d")))
    print("turn 2 on and open valve to probe", req.json())
    my_time=time.time()
    global valve2_stat
    valve2_stat=1
    save_Valves_stats(my_time)


def close2():
    req = requests.post("http://a73434.berlin.ptb.de:55555", data=json.dumps(data_off2))
    print(str(time.strftime("%H:%M:%S %Y-%m-%d")))
    print("turn 2 off and close valve probe", req.json())
    my_time=time.time()    
    global valve2_stat
    valve2_stat=0
    save_Valves_stats(my_time)


while 1:
    
    for i in [15,30,60]:

        open2()
        print('wait 15 minutes with open valve 2')
        # Status vor 2020-02-19 time.sleep(10*60)
        time.sleep(15*60)

        close2()
        temp_i=int(i)
        print('wait %i minutes with open valve 2' %temp_i)
        time.sleep(temp_i*60)

    

#print(time.time())
#print(str(time.strftime("%Y-%m-%d")))
