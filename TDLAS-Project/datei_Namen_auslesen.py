import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from datetime import datetime
import matplotlib
import os
def read_picture():
    f = os.listdir("C:/Users/vaclab/Desktop/TDLAS-Project/ULE He 21grad 2019-12-14")
    #print(f)
   
    my_times=[]
    my_timestamps=[]

    for file in f:
        my_times.append(file[0:24])
        timestamp_new = datetime.strptime(file[0:24], "%Y-%m-%d_TIME_%H-%M-%S")
        timestamp_new = datetime.timestamp(timestamp_new)
        my_timestamps.append(timestamp_new)
       
    return np.transpose((my_times,my_timestamps))
   
np.savetxt("times_pressure.txt",read_picture(), fmt='%s')