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

dict= L.loadMuscle()

vitesse=np.sqrt(dict["HandXVel"]**2+dict["HandYVel"]**2)
force=np.sqrt(dict["HandXForce"]**2+dict["HandYForce"]**2)
forceX=dict["HandXForce"]
forceY=dict["HandYForce"]
posX=dict["HandX"]
posY=dict["HandY"]
pos=np.sqrt(dict["HandX"]**2+dict["HandY"]**2)

#plt.plot(forceY[359],label="Y")
#plt.plot(forceX[359],label="X")
#plt.show()
#plt.legend()
#plt.plot(posY[59],posX[59])
print(len(pos))
pecto=dict["Pectoralis"]
delto=dict["Deltoid"]

def mean(tab):
    ret=np.zeros(len(tab[0]))
    for i in range(0,len(tab)):
        ret=np.add(ret,tab[i])
    ret=ret/len(tab)
    return ret

pectomean1=mean(pecto[0:50])
pectomean2=mean(pecto[50:55])
pectomean3=mean(pecto[55:60])
plt.plot(pectomean2,label="pas un connard qui me frappe le bras")
#plt.plot(pectomean2,label="Un connard me frappe le bras +X")
#plt.plot(pectomean3,label="Un connard me frappe le bras -X")
plt.legend()
plt.ylabel("Activité musculaire en Volt[mV]")
#vitesse=dict["HandXVel"]
plt.plot(mean(vitesse[50:55]))
plt.show()
plt.plot(mean(forceX[50:55]))
plt.plot(mean(forceY[50:55]))
plt.show()
plt.plot(mean(pos[50:55]))

print(dict["descriptions"])

