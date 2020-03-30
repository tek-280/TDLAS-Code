#'Author: Tom Rubin'

from time import *
import datetime
import matplotlib.pyplot as plt
import numpy as np

import os, sys



def m_ave(data,N):
    cumsum, moving_aves = [0], []
    for i, x in enumerate(data, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    moving_aves=np.array((moving_aves))
    return moving_aves

def main():

    path = 'c:/Users/OPS_NIM/AppData/Local/Programs/Python/Python38/RUBIN/Data/'
    #dirs = os.listdir(path)
    #for file in dirs:
    #    print(file)
    #print(dirs)
    if 0:
        temp_name=dirs[-1]
        erg=np.load('%s%s' %(path,temp_name)).T
        if 1: # plotting
            plt.plot(erg[0],erg[1],'r')
            plt.plot(erg[0],erg[1],'bo')
            plt.show()
    
    if 0:
        erg=np.load('%s%s' %(path,dirs[0])).T
        for file in dirs[1:]:
            #print(file)
            erg=np.hstack((erg,np.load('%s%s' %(path,file)).T))
        
        np.save('c:/Users/OPS_NIM/AppData/Local/Programs/Python/Python38/RUBIN/2019_11_26_data',erg)
        np.savetxt('c:/Users/OPS_NIM/AppData/Local/Programs/Python/Python38/RUBIN/2019_11_26_data.txt',erg)

    if 1:
        erg=np.load('c:/Users/OPS_NIM/AppData/Local/Programs/Python/Python38/RUBIN/2019_11_26_data.npy')

    #print(erg.shape)
    if 1: # plotting
        #plt.plot(erg[0],erg[1],'r')
        #put erg to khz
        erg[1]=erg[1]/1000.
        plt.plot(erg[0],erg[1],'b.')

        if 1:
            N=100
            av0=m_ave(erg[0],N)
            av1=m_ave(erg[1],N)
            plt.plot(av0,av1,'r')

            N=10000
            av0=m_ave(erg[0],N)
            av1=m_ave(erg[1],N)
            plt.plot(av0,av1,color='orange')


        plt.show()

        
if __name__ == "__main__":
    main()


