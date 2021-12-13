# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:59:53 2021

@author: romai
1: montrer influence kiné sur EMG
2: Etudier type sur EMG

"""

import numpy as np
import loadDataP2 as L
import matplotlib.pyplot as plt
import FiringRate
import math

dict= L.loadMuscle()

vitesse=np.sqrt(dict["HandXVel"]**2+dict["HandYVel"]**2)
force=np.sqrt(dict["HandXForce"]**2+dict["HandYForce"]**2)
forceX=dict["HandXForce"]
forceY=dict["HandYForce"]
posX=dict["HandX"]
posY=dict["HandY"]
pos=np.sqrt(dict["HandX"]**2+dict["HandY"]**2)
pecto=dict["Pectoralis"]
delto=dict["Deltoid"]

def mean(tab):
    ret=np.zeros(len(tab[0]))
    for i in range(0,len(tab)):
        ret=np.add(ret,tab[i])
    ret=ret/len(tab)
    return ret

def meanT(dico,tab,type):
    x=np.where(dico["extracted"][:,2]==type)  
    tab=tab[x]
    return mean(tab)


#Données selon différents Type
pecto1=meanT(dict,pecto,1)
delto1=meanT(dict,delto,1)
ForceX1=meanT(dict,forceX,1)
ForceY1=meanT(dict,forceY,1)
vitesse1=meanT(dict,vitesse,1)
PosX1=meanT(dict,posX,1)
PosY1=meanT(dict,posY,1)

pecto2=meanT(dict,pecto,2)
delto2=meanT(dict,delto,2)
ForceX2=meanT(dict,forceX,2)
ForceY2=meanT(dict,forceY,2)
vitesse2=meanT(dict,vitesse,2)
PosX2=meanT(dict,posX,2)
PosY2=meanT(dict,posY,2)


pecto3=meanT(dict,pecto,3)
delto3=meanT(dict,delto,3)
ForceX3=meanT(dict,forceX,3)
ForceY3=meanT(dict,forceY,3)
vitesse3=meanT(dict,vitesse,3)
PosX3=meanT(dict,posX,3)
PosY3=meanT(dict,posY,3)



#Graphiq"ues
#Force an"d EMG Type1
"""fig,ax1= plt.subplots()
ax2 = ax1.twinx()
ax1.plot(pecto1,label="Pectoral",color='r')
ax1.plot(delto1,label="Deltoid",color='c')
#vitesse=dict["HandXVel"]
ax2.plot(ForceX1,color='g',label="F_X")
ax2.plot(ForceY1,color='y',label="F_Y")
#ax2.plot(deltomean1,label="muscle delto")
ax1.legend()
ax2.legend(loc=(0.825,0.65))
ax1.set_ylabel("EMG activity[mV]")
ax2.set_ylabel("Force [N]")
ax1.set_xlabel("Time[ticks]")
plt.show()"""

#Vitesse and EMG

fig,ax1= plt.subplots()
ax2 = ax1.twinx()
ax1.plot(pecto1,label="Pectoral",color='r')
ax1.plot(delto1,label="Deltoid",color='c')
ax2.plot(vitesse1,color='g',label="Velocity")
#ax2.plot(deltomean1,label="muscle delto")
ax1.legend()
ax2.legend(loc=(0.757,0.725))
ax1.set_ylabel("EMG activity[mV]")
ax2.set_ylabel("Velocity[m/s]")
ax1.set_xlabel("Time[ticks]")
plt.show()


#Vitesse and Force
"""fig,ax1= plt.subplots()
ax2 = ax1.twinx()
ax1.plot(vitesse1,label="vitesse",color='g')

#vitesse=dict["HandXVel"]
ax2.plot(ForceX1,color='r',label="F_X")
ax2.plot(ForceY1,color='y',label="F_Y")
#ax2.plot(deltomean1,label="muscle delto")
ax1.legend()
ax2.legend(loc=(0.825,0.65))
ax1.set_ylabel("Velocity[mV]")
ax2.set_ylabel("Force [N]")
ax1.set_xlabel("Time[ticks]")
plt.show()"""



"""plt.plot(mean(posY[55:60]),mean(posX[50:55]))
plt.xlim(0.0,0.3)
plt.ylim(0.0,0.3)
plt.show()"""

