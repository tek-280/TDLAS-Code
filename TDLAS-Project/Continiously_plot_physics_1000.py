import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime
import matplotlib

fig = plt.figure()
ax = fig.add_subplot(1,1,1)




def animate(i):
    data_tmp = np.genfromtxt(r'C:\Users\vaclab\Desktop\TDLAS-Project\2020-02-20-Physics_1000-tmp-log-file.txt',dtype=None, encoding=None,delimiter='\t')
    data_buffer = []
    time_zero = datetime.datetime.strptime(data_tmp[0][0],'%H:%M:%S')
    print(time_zero,"Continiously_plot_physics_1000.py 2019-12-19")
    for i in range(len(data_tmp)):
            time = (datetime.datetime.strptime(data_tmp[i][0],'%H:%M:%S')-time_zero).total_seconds()
            tmp = float(data_tmp[i][1][:-3]) 
            data_buffer.append((time,tmp))


    data_plot = np.transpose(np.array(data_buffer))
    xs,ys = data_plot[0]/3600,data_plot[1]
    ax.clear()
    ax.plot(xs,ys)
    ax.ticklabel_format(axis='y',style="sci",scilimits=(-4,-5))
    plt.xlabel("Time in hours")
    plt.ylabel("Temperature (C)")
    ax.grid()
    plt.title("Physics 1000 Temperature over time" )


ani = animation.FuncAnimation(fig,animate)
plt.show()
        