import loadDataP2 as data
import numpy as np
import matplotlib.pyplot as plt
import FiringRate
from scipy.signal import butter, filtfilt
from scipy.fft import fft


dictMuscles = data.loadMuscle()
dictNeurons = data.loadNeuron() #['time', 'shoang', 'elbang', 'handxpos', 'handypos', 'cells']

targets = ['target1','target2','target3','target4','target5','target6','target7','target8']
trials = ['trial1','trial2','trial3','trial4','trial5','trial6']
time = dictNeurons['target1']['trial6']['time']


# for target in targets:
#     plt.plot(dictNeurons[target]['trial6']['handypos'], dictNeurons[target]['trial6']['handxpos'])
# plt.show()

# plt.plot(dictNeurons['target1']['trial6']['time'], dictNeurons['target1']['trial6']['cells'])
# print(dictNeurons['target1']['trial6']['time'])
# print(sum(dictNeurons['target1']['trial6']['cells']))
# plt.show()

# rho = np.zeros(len(dictNeurons['target1']['trial6']['time']))
# dt = 100
# for trial in trials:
#     for i in range(len(rho)-10):
#         rho[i] += sum(dictNeurons['target1'][trial]['cells'][i:i+dt])/dt
# print(rho)
# plt.plot(time, rho)
# plt.show()


def derive(vect, i):
    return (-vect[i-2]+8*vect[i-1]-8*vect[i+1]+vect[i+2])/12

def Velocity(dictNeurons, target, trial, dt):
    vel = np.zeros(len(dictNeurons[target][trial]['handxpos'])-2)
    velx = np.zeros(len(dictNeurons[target][trial]['handxpos'])-2)
    vely = np.zeros(len(dictNeurons[target][trial]['handxpos'])-2)
    for i in range(2, len(dictNeurons[target][trial]['handxpos'])-2):
        velx[i] = derive(dictNeurons[target][trial]['handxpos'],i)/dt
        vely[i] = derive(dictNeurons[target][trial]['handypos'], i)/dt
        vel[i] = np.sqrt((velx[i])**2 + (vely[i])**2)
    return vel, velx, vely

def extractMvt(vel, treshold):
    start = 0
    end = 0
    flagstart =True
    flagend = True
    i = 0
    while(flagend):
        if flagstart and vel[i] < treshold:
            start = i
        elif vel[i] > treshold:
            flagstart = False
            end = i
        else:
            flagend = False
        i = i + 1
    return start, end

def filter(signal):
    b, a = butter(2, 5/(0.5*200), 'low')
    filtered = filtfilt(b, a, signal)
    return filtered


target = 'target1'
dt = time[1]-time[0]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
for trial in trials:
    vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
    #ax1.plot(np.transpose(dictNeurons[target][trial]['time'])[0][0:-2], vel, label = 'velocity', color = 'r')
    ax1.plot(np.transpose(dictNeurons[target][trial]['time'])[0][0:-2], filter(vel), label = 'velocity filtered')
    firingRate = FiringRate.CalculFiringRate(dictNeurons)
    ax2.plot(dictNeurons[target][trial]['time'], firingRate[target][trial], label = 'firing rate')
    #transform = fft(vel)
    #ax2.plot(np.abs(transform), color='r')
    
    start, stop = extractMvt(filter(vel), 0.05)
    print(start, stop)
    print(dictNeurons[target][trial]['time'][start], dictNeurons[target][trial]['time'][stop])
ax1.legend()
ax1.set_ylabel('Velocity [m/s]')
ax2.set_ylabel('Firing rate [1/s]')
plt.show()

