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

dict= L.loadMuscle()

pecto=dict["Deltoid"][0]
forceX=dict["HandXForce"][50]
extract=dict["extracted"]
descr=dict["descriptions"]
#forcetot=np.sqrt(forceX**2+forceY**2)
print(extract[:,3])
plt.plot(pecto)
#plt.plot(forceX)
