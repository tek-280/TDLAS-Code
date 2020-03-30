
import numpy as np
import re
import matplotlib.pyplot as plt

for name in ["ULE-Anstauung-Lecktester-log-file.txt","Lecktester-log-file.txt"]:
    f = open(name)
    time = []
    pressure = []
    data = f.readlines()
    f.close()

    for i in data:
    
        
        reg = '[0-9]{1}\.[0-9]{3}[E][-][0-9]{1,2}'
        result = re.search(reg, i)
        if result:
            p = float(result.group(0))

            if p<=0.00001: #eingabe des höchsten Exponenten
                pressure.append(p)
                t = i[:19]
                t = t.replace("\t", "")
                t = t.replace("t", "")
                t = t.replace("'","")
                t = t.replace("{","")
                t = t.replace("_", "")
                t = t.replace("s", "")
                time.append(t)  
            
    pressure = np.array(pressure, dtype =float)
    time = np.array(time, dtype = float)
    for i in range(len(time)):
        if i!=0:
            time[i] = time[i]-time[0]
    time[0] = 0

    #plt.plot(time,np.log10(pressure),"+")
    plt.plot(time,pressure,"+")

plt.show()