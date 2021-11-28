import loadDataP2 as data
import numpy as np
import matplotlib.pyplot as plt



dictMuscles = data.loadMuscle()
dictNeurons = data.loadNeuron() #['time', 'shoang', 'elbang', 'handxpos', 'handypos', 'cells']

print(dictNeurons['target1']['trial1'].keys())
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

rho = np.zeros(len(dictNeurons['target1']['trial6']['time']))
dt = 100
for trial in trials:
    for i in range(len(rho)-10):
        rho[i] += sum(dictNeurons['target1'][trial]['cells'][i:i+dt])/dt
print(rho)
plt.plot(time, rho)
plt.show()