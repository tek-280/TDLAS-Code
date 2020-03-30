import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


def animate(i):
    data = np.genfromtxt(r'O:\OVak\Alle_OVak\2019-Measurements\2019-12-09-Ausgasrate-ULE\2019-12-14-IoniVac_data_logg-80_deg_heating.dat',dtype=None, encoding=None,delimiter='\t')
    data_buffer = []
    for i in range(len(data)):
        if data[i][2][2]=='e': #Error message
            pass
        elif data[i][2][65]=='B': #succesful data read
            time = data[i][0]
            pressure = float(data[i][2][70:78]) 
            data_buffer.append((time,pressure))
        else: #unsuccessfull read
            pass
    data_plot = np.transpose(np.array(data_buffer))
    xs,ys = data_plot[0]/3600,data_plot[1]
    ax.clear()
    ax.plot(xs,ys)
    ax.ticklabel_format(axis='y',style="sci",scilimits=(-4,-5))
    plt.xlabel("Time in hours")
    plt.ylabel("Pressure in mbar")
    ax.grid()
    plt.title("IoniVac pressure while pumping, T=376K" )

ani = animation.FuncAnimation(fig,animate)
plt.show()