import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime
import matplotlib

fig = plt.figure()
ax = fig.add_subplot(1,1,1)




def animate(i):
    data_volts = np.genfromtxt(r'C:\Users\vaclab\Desktop\TDLAS-Project\2019-12-16-InfiVision_Osci-Voltage-log-file.txt',dtype=None, encoding=None,delimiter='\t')
    data_buffer = []
    time_zero = datetime.datetime.strptime(data_volts[0][0],'%H:%M:%S')
    print(time_zero)
    for i in range(len(data_volts)):
            time = (datetime.datetime.strptime(data_volts[i][0],'%H:%M:%S')-time_zero).total_seconds()
            Voltage = float(data_volts[i][2][:-2]) 
            data_buffer.append((time,Voltage))


    data_plot = np.transpose(np.array(data_buffer))
    xs,ys = data_plot[0]/3600,data_plot[1]
    ax.clear()
    ax.plot(xs,ys)
    ax.ticklabel_format(axis='y',style="sci",scilimits=(-4,-5))
    plt.xlabel("Time in hours")
    plt.ylabel("Voltage (V)")
    ax.grid()
    plt.title("Infivision Voltage (max) over time" )


ani = animation.FuncAnimation(fig,animate)
plt.show()
