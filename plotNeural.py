import loadDataP2 as data
import numpy as np
import matplotlib.pyplot as plt
import FiringRate
from scipy.signal import butter, filtfilt
from scipy.fft import fft
import seaborn as sns
import math


dictMuscles = data.loadMuscle()
dictNeurons = data.loadNeuron() #['time', 'shoang', 'elbang', 'handxpos', 'handypos', 'cells']

targets = ['target1','target2','target3','target4','target5','target6','target7','target8']
trials = ['trial1','trial2','trial3','trial4','trial5','trial6']
time = dictNeurons['target1']['trial6']['time']
dt = time[1]-time[0]

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
        velx[i] = derive(dictNeurons[target][trial]['handxpos'],i)/(dt/1000)
        vely[i] = derive(dictNeurons[target][trial]['handypos'], i)/(dt/1000)
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

def minLen(target):
    mini = len(dictNeurons[target]['trial1']['time'])
    for trial in trials:
        mini = min(mini, len(dictNeurons[target][trial]['time']))
    return mini

def plotTuning():
    fig, ax1 = plt.subplots()
    #ax2 = ax1.twinx()
    ax3 = fig.add_axes([.68, .42, .2, .4])
    #ax4 = ax3.twinx()
    firingRate = FiringRate.CalculFiringRate(dictNeurons)
    for target in targets:
        start, stop = findMaxInter(target, dt)

        # plot velocity
        newvel = np.zeros(stop+start)
        newfiringrate = np.zeros(stop+start)
        newshoang = np.zeros(stop+start)
        newelbang = np.zeros(stop+start)
        for trial in trials:
            vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
            velfilt = filter(vel)
            peak = findPeak(velfilt)
            newvel = np.add(newvel, velfilt[peak-start:peak+stop])
            newfiringrate = np.add(newfiringrate, firingRate[target][trial][peak-start:peak+stop])
            newshoang = np.add(newshoang, dictNeurons[target][trial]['shoang'][:,0][peak-start:peak+stop])
            newelbang = np.add(newelbang, dictNeurons[target][trial]['elbang'][:,0][peak-start:peak+stop])
            #meanfiringrate = np.add(meanfiringrate, firingRate[target][trial])
            #ax1.plot(time[0:-2], velfilt, label = 'velocity', color = 'r')
        newvel = newvel/6
        newfiringrate = newfiringrate/6
        newshoang = newshoang/6
        newelbang = newelbang/6
        #print(np.shape(newshoang))
        #meanfiringrate = meanfiringrate/6

        #ax1.plot(np.arange(-start, stop), newvel, label = target)
        ax1.plot(np.arange(-start, stop)*dt/1000, newfiringrate, label = target)
        #ax1.plot(np.arange(-start, stop), newshoang, label = target)
        #ax1.plot(np.arange(0, len(meanfiringrate)), meanfiringrate, label=target)
        #ax1.vlines(time[findPeak(velfilt)], 0, max(velfilt))

        #plot firing rate
        #ax2.plot(dictNeurons[target][trial]['time'], firingRate[target][trial], label = 'firing rate')
        
        # plot arm movement
        #ax1.plot(dictNeurons[target][trial]['handypos'], dictNeurons[target][trial]['handxpos'])
        ax3.plot(dictNeurons[target][trial]['handypos'][peak-start:peak+stop], dictNeurons[target][trial]['handxpos'][peak-start:peak+stop])
        #ax3.plot(np.arange(-start, stop), newshoang)
        #ax4.plot(np.arange(-start, stop), newelbang)


    ax1.legend(loc='upper left', fontsize = 20)
    ax1.set_xlabel('Time [s]', fontsize = 30)
    #ax2.set_ylabel('Velocity [m/s]', fontsize = 20)
    ax1.set_ylabel('Firing rate [Hz]', fontsize = 30)
    ax1.tick_params(axis = 'x', labelsize = 20)
    ax1.tick_params(axis = 'y', labelsize = 20)
    #ax2.tick_params(axis = 'y', labelsize = 15)
    ax1.set_ylim(None,150)
    ax3.set_title("Hand directions", fontsize = 30)
    ax3.tick_params(axis = 'x', labelsize = 20)
    ax3.tick_params(axis = 'y', labelsize = 20)
    
    plt.show()


def plotAng():
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(223)
    ax3 = plt.subplot(122)
    

    for target in targets:
        start, stop = findMaxInter(target, dt)
        l = minLen(target)
        newshoang = np.zeros(l)
        newelbang = np.zeros(l)
        for trial in trials:
            vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
            velfilt = filter(vel)
            peak = findPeak(velfilt)

            newshoang += dictNeurons[target][trial]['shoang'][:,0][0:l]
            newelbang += dictNeurons[target][trial]['elbang'][:,0][0:l]

        newshoang = newshoang/6
        newelbang = newelbang/6

        ax1.plot(np.arange(l)*dt/1000, newshoang)
        ax2.plot(np.arange(l)*dt/1000, newelbang)
        ax3.plot(dictNeurons[target][trial]['handypos'][peak-start:peak+stop], dictNeurons[target][trial]['handxpos'][peak-start:peak+stop])
        
    # ax1.title("Shoulder angle")
    # ax2.legend("Elbow angle")
    # ax3.legend("Hand position")
    plt.show()

def plotFiringRate():
    target = 'target4'
    trial = 'trial2'
    firingRate = FiringRate.CalculFiringRate(dictNeurons)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(dictNeurons[target][trial]['time']/1000, dictNeurons[target][trial]['cells'])
    ax2.plot(dictNeurons[target][trial]['time']/1000, firingRate[target][trial], color='g')
    ax1.set_ylim(None,3)
    ax1.set_xlabel("Time [s]", fontsize = 30)
    ax1.set_ylabel("Neuron spikes", fontsize = 30)
    ax2.set_ylabel("Firing rate [Hz]", fontsize = 30)
    ax1.tick_params(axis = 'x', labelsize = 25)
    ax1.tick_params(axis = 'y', labelsize = 25)
    ax2.tick_params(axis = 'y', labelsize = 25)
    
    plt.show()

def plotVelocity():
    target = 'target1'
    start, stop = findMaxInter(target, dt)
    for trial in trials:
        vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
        velfilt = filter(vel)
        peak = findPeak(velfilt)
        plt.plot(dictNeurons[target][trial]['time'][0:-2]/1000, velfilt, label = trial)
        #plt.plot(np.arange(-start, stop)*dt/1000, velfilt[peak-start:peak+stop], label = trial)
    plt.xlabel("Time [s]", fontsize = 30)
    plt.ylabel("Hand velocity [m/s]", fontsize = 30)
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    plt.legend(fontsize = 25)
    plt.show()

def plotHandPos():
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
    trial = 'trial1'

    for target in targets:
        start, stop = findMaxInter(target, dt)
        vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
        velfilt = filter(vel)
        peak = findPeak(velfilt)
        ax1.plot(dictNeurons[target][trial]['handypos'], dictNeurons[target][trial]['handxpos'])
        ax2.plot(dictNeurons[target][trial]['handypos'][peak-start:peak+stop], dictNeurons[target][trial]['handxpos'][peak-start:peak+stop])
        
    ax1.set_box_aspect(1)
    ax2.set_box_aspect(1)
    ax1.set_title("Non extracted", fontsize = 30)
    ax2.set_title("Extracted", fontsize = 30)
    ax1.tick_params(axis = 'x', labelsize = 25)
    ax1.tick_params(axis = 'y', labelsize = 25)
    ax2.tick_params(axis = 'x', labelsize = 25)
    ax2.tick_params(axis = 'y', labelsize = 25)
    ax1.set_ylabel("Y position [cm]", fontsize = 30)
    fig.supxlabel("X position [cm]", fontsize = 30)
    
    plt.show()

def plotTuningAng():
    fig = plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(223)
    ax3 = plt.subplot(224)

    firingRate = FiringRate.CalculFiringRate(dictNeurons)
    for target in targets:
        start, stop = findMaxInter(target, dt)
        newvel = np.zeros(stop+start)
        newfiringrate = np.zeros(stop+start)
        newshoang = np.zeros(stop+start)
        newelbang = np.zeros(stop+start)
        for trial in trials:
            vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
            velfilt = filter(vel)
            peak = findPeak(velfilt)
            newvel = np.add(newvel, velfilt[peak-start:peak+stop])
            newfiringrate = np.add(newfiringrate, firingRate[target][trial][peak-start:peak+stop])
            newshoang = np.add(newshoang, dictNeurons[target][trial]['shoang'][:,0][peak-start:peak+stop])
            newelbang = np.add(newelbang, dictNeurons[target][trial]['elbang'][:,0][peak-start:peak+stop])
        newvel = newvel/6
        newfiringrate = newfiringrate/6
        newshoang = newshoang/6
        newelbang = newelbang/6

        ax1.plot(np.arange(start+stop)*dt/1000, newfiringrate, label = target)
        ax2.plot(np.arange(start+stop)*dt/1000, newshoang)
        ax3.plot(np.arange(start+stop)*dt/1000, newelbang)

    ax1.legend(loc='upper right', fontsize = 15)
    ax1.set_ylabel('Firing rate [Hz]', fontsize = 30)
    ax1.tick_params(axis = 'x', labelsize = 15)
    ax1.tick_params(axis = 'y', labelsize = 15)
    fig.supxlabel("Time [s]", fontsize = 30)
    ax2.set_title("Shoulder", fontsize = 20)
    ax2.tick_params(axis = 'y', labelsize = 15)
    ax2.tick_params(axis = 'x', labelsize = 15)
    ax2.set_ylabel('Angle [rad]', fontsize = 30)
    ax3.set_title("Elbow", fontsize = 20)
    ax3.tick_params(axis = 'x', labelsize = 20)
    ax3.tick_params(axis = 'y', labelsize = 20)
        

    plt.show()


def plotScatter():
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
    firingRate = FiringRate.CalculFiringRate(dictNeurons)
    peaks = np.zeros(8)
    shoangles = np.zeros(8)
    elbangles = np.zeros(8)
    i = 0
    for target in targets:
        start, stop = findMaxInter(target, dt)
        for trial in trials:
            vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
            velfilt = filter(vel)
            peak = findPeak(velfilt)
            peakFR = findPeak(firingRate[target][trial])
            peaks[i] += firingRate[target][trial][peakFR]
            shoangles[i] += dictNeurons[target][trial]['shoang'][peak+stop]
            elbangles[i] += dictNeurons[target][trial]['elbang'][peak+stop]
        peaks[i] = peaks[i]/6
        shoangles[i] = shoangles[i]/6
        elbangles[i] = elbangles[i]/6
        i+=1
    # ax1.scatter(shoangles, peaks)
    # ax2.scatter(elbangles, peaks)

    # m1, b1 = np.polyfit(shoangles, peaks, 1)
    # ax1.plot(shoangles, m1*shoangles+b1)
    # m2, b2 = np.polyfit(elbangles, peaks, 1)
    # ax2.plot(elbangles, m2*elbangles+b2)
    sns.regplot(shoangles, peaks, ax=ax1)
    sns.regplot(elbangles, peaks, ax=ax2)
    ax1.set_box_aspect(1)
    ax2.set_box_aspect(1)
    ax1.set_title("Shoulder", fontsize = 30)
    ax2.set_title("Elbow", fontsize = 30)
    ax1.tick_params(axis = 'x', labelsize = 25)
    ax1.tick_params(axis = 'y', labelsize = 25)
    ax2.tick_params(axis = 'x', labelsize = 25)
    ax2.tick_params(axis = 'y', labelsize = 25)
    ax1.set_ylabel("Peak of firing rate [Hz]", fontsize = 30)
    fig.supxlabel("Angle after movement [rad]", fontsize = 30)
    plt.show()

def plotScatterDir():
    firingRate = FiringRate.CalculFiringRate(dictNeurons)
    peaks = np.zeros(8)
    angles = np.zeros(8)
    i = 0
    for target in targets:
        start, stop = findMaxInter(target, dt)
        for trial in trials:
            vel, velx, vely = Velocity(dictNeurons, target, trial, dt)
            velfilt = filter(vel)
            peak = findPeak(velfilt)
            peakFR = findPeak(firingRate[target][trial])
            peaks[i] += firingRate[target][trial][peakFR]
            dy = float(dictNeurons[target][trial]['handypos'][peak-start]-dictNeurons[target][trial]['handypos'][peak+stop])
            dx = float(dictNeurons[target][trial]['handxpos'][peak-start]-dictNeurons[target][trial]['handxpos'][peak+stop])
            angles[i] += math.degrees(math.atan2(dy, dx))
        i += 1
    angles = angles/6
    peaks = peaks/6
    print(angles)
    sns.regplot(angles, peaks)
    plt.show()

#plotTuning()
#plotAng()
#plotFiringRate()
#plotVelocity()
#plotHandPos()
#plotTuningAng()
#plotScatter()
plotScatterDir()
#print(dictNeurons['target1']['trial1']['elbang'][:,0])