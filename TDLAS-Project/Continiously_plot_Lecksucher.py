import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime
import matplotlib
import re

fig = plt.figure()
ax = fig.add_subplot(1,1,1)





def animate(i):
    #data_tmp = np.genfromtxt(r'C:\Users\vaclab\Desktop\TDLAS-Project\Data_Leck_Voltage\2020-02-19 Lecktester-log-file.txt',dtype=None, encoding=None,delimiter='\t')
    for name in [r'C:\Users\vaclab\Desktop\TDLAS-Project\Data_Leck_Voltage\2020-02-21 Lecktester-log-file.txt']:
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

    data_buffer = []
    time_zero = time[0]
    print(time_zero,"Continiously_plot_Lecksucher.py 2019-12-21")
    for i in range(len(time)):
            time_plot = time[i]-time_zero
            press = float(pressure[i]) 
            data_buffer.append((time_plot,press))


    data_plot = np.transpose(np.array(data_buffer))
    xs,ys = data_plot[0]/3600,data_plot[1]
    ax.clear()
    ax.semilogy(xs,ys)
    #ax.ticklabel_format(axis='y',style="sci",scilimits=(-4,-5))
    plt.xlabel("Time in hours")
    plt.ylabel("Leak rate (mbar*l/s)")
    ax.grid()
    plt.ylim(ymin=2.e-11)
    plt.title("Leakdetektor: Leak rate" )


ani = animation.FuncAnimation(fig,animate)
plt.show()
        