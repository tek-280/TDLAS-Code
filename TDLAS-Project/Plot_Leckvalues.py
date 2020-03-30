#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime
import matplotlib

fig = plt.figure()
ax = fig.add_subplot(1,1,1)



my_time=[]
values=[]
fo = open(r"C:/Users/vaclab/Desktop/TDLAS-Project/Data_Leck_Voltage/Lecktester-log-file.txt", "r")
line = fo.readlines()
for lines in line[:5]:
    try:
        print(lines)
        temp=lines.split('\t')
        my_time.append(temp[0])
        print(my_time)
    except:
        print('error')
        
    
fo.close()


if 0:
    data_plot = np.transpose(np.array(data_buffer))
    xs,ys = data_plot[0]/3600,data_plot[1]
    ax.clear()
    ax.plot(xs,ys)
    #ax.ticklabel_format(axis='y',style="sci",scilimits=(-4,-5))
    plt.xlabel("Sekunden")
    plt.ylabel("Leckrate")
    ax.grid()
    plt.title("Leckrate" )


plt.show()
        