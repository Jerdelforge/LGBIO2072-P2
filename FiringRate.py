import numpy as np

def gaussian_kernel(time_vector,sigma):
  """
  This function generates the gaussian kernel to compute the firing rate of a given spike trains

  Inputs : 
  -time_vector is the time span of the kernel
  -sigma is the width of the gaussian distribution

  Outputs:
  -kernel is the distribution
  """
  kernel = (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-((time_vector-time_vector[-1]/2)**2)/(2*sigma**2))
  
  return kernel

def rect_kernel(t_range,width):
    """
    rect_kernel creates the rectangular kernel used to compute the firing rate

    Inputs : 
    -time_vector is the time span on which we want to define this kernel
    -width is the width of the rectangular kernel (in the same units as dt)

    Outputs :
    -kernel is the returned rectangular kernel
    """
    ######################
    ### your code here ###
    ######################
    dt = t_range[1]-t_range[0]
    kernel = np.zeros_like(t_range)
    widthDt = int(width/dt)
    #center the kernel to limit boundary effects
    kernel[int((len(kernel)/2)-(widthDt/2)):int((len(kernel)/2)+(widthDt/2))] = np.ones(widthDt)/width
    
    return kernel

def FiringRate(S, kernel):
    firing_rate = np.convolve(S,kernel,'same')
    return firing_rate

def CalculFiringRate(dictNeurons):
    dict={}
    for i in range(1,9):
        dict["target"+str(i)]={}
        for j in range(1,7):
            S=dictNeurons['target'+str(i)]['trial'+str(j)]['cells']
            t_range = np.linspace(0,1,S.shape[0])
            kernel = gaussian_kernel(t_range,50e-3)
            dict["target"+str(i)]["trial"+str(j)]=FiringRate(S[:,0], kernel)
    return dict