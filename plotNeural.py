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

def extractMvt(vel, peak):
    start = peak
    delay = 10
    while vel[start] > vel[start-delay]:
        start = start - 1
    stop = peak
    while vel[stop] > vel[stop+delay]:
        stop = stop + 1
    return start, stop

def findPeak(vel):
    peak = np.where(vel == max(vel))
    return peak[0][0]

def filter(signal):
    b, a = butter(2, 5/(0.5*200), 'low')
    filtered = filtfilt(b, a, signal)
    return filtered

def findMaxInter(target, dt):
    maxstart = 0
    maxstop = 0
    maxpeak = 0
    for trial in trials:
        vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
        velfilt = filter(vel)
        peak = findPeak(velfilt)
        start, stop = extractMvt(velfilt, peak)
        if stop-start > maxstop-maxstart:
            maxstart = start
            maxstop = stop
            maxpeak = peak
    return maxpeak-maxstart, maxstop-maxpeak



target = 'target2'
trial = 'trial1'
dt = time[1]-time[0]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
firingRate = FiringRate.CalculFiringRate(dictNeurons)
for target in targets:
    start, stop = findMaxInter(target, dt)
    time = np.transpose(dictNeurons[target][trial]['time'])[0]
    #start, stop = extractMvt(velfilt, findPeak(velfilt))

    # plot velocity
    newvel = np.zeros(stop+start)
    newfiringrate = np.zeros(stop+start)
    for trial in trials:
        vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
        velfilt = filter(vel)
        peak = findPeak(velfilt)
        newvel = np.add(newvel, velfilt[peak-start:peak+stop])
        newfiringrate = np.add(newfiringrate, firingRate[target][trial][peak-start:peak+stop])
        #ax1.plot(time[0:-2], velfilt, label = 'velocity', color = 'r')
    newvel = newvel/6
    newfiringrate = newfiringrate/6
    ax1.plot(np.arange(-start, stop), newvel, label = target)
    ax2.plot(np.arange(-start, stop), newfiringrate, label = target)
        #ax1.vlines(time[findPeak(velfilt)], 0, max(velfilt))

    #plot firing rate
    #ax2.plot(dictNeurons[target][trial]['time'], firingRate[target][trial], label = 'firing rate')
    
    # plot arm movement
    #ax1.plot(dictNeurons[target][trial]['handypos'], dictNeurons[target][trial]['handxpos'])
    #ax1.plot(dictNeurons[target][trial]['handypos'][start:stop], dictNeurons[target][trial]['handxpos'][start:stop])


ax1.legend()
ax1.set_ylabel('Velocity [m/s]')
ax2.set_ylabel('Firing rate [1/s]')
plt.show()

