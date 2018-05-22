### For Simulating
# define all the user params here
NBINS  = 1024 
NPEAKS = 3
NOBS   = 36
NPOBS  = 6
SHIFTS = True
MJD    = 54321
###################################
# No definitions beyond this point
import numpy as np
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm
if len(sys.argv) < 2:
    print "Usage: python simulator.py <ROOT>"
    sys.exit(0)
root = sys.argv[1]
###################################
def GiveProf(phase,peaks,stds):
    '''
    len(peaks) = len(stds)
    '''
    if len(peaks) != len(stds):
        raise ValueError('number of peaks should be equal to number of stds')
    ret = np.zeros(phase.shape)
    for i in xrange(len(peaks)):
        ret += (2*np.pi*stds[i])**-0.5 * np.exp( -0.5 * (phase - peaks[i]) ** 2 / stds[i] ** 2)
    return ret

phase = np.linspace(0,1,NBINS) # `phase` axis
peaks = np.random.rand(NPEAKS) # peak positions # this is one time
stds  = np.random.rand(NPEAKS) * 1e-1 # STDS 
PP    = np.zeros((NOBS,NBINS)) # this holds the profile
MC    = np.random.choice(np.arange(NOBS),size=NPOBS) # where mode change will happen
for i in tqdm(xrange(NOBS),desc='Simulation',unit='files',ascii=True):
    if i in MC:
        # mode change boi
        dc = np.random.randint(len(peaks)) # choose a random component
        PP[i] = GiveProf(phase,np.delete(peaks,dc),np.delete(stds,dc))
    else:
        PP[i] = GiveProf(phase,peaks, stds)
    # Random Shifts Logic
    if SHIFTS:
        PP[i] = np.roll(PP[i],np.random.randint(NBINS)) # Random shift
###################################
# Generation part is done
def ProfWriter(prof,fn,j,mc):
    # write me profile
    fo = open(fn,'w+') # writing
    if mc:
        fo.write('#{0} MC PROFILE generated by simulator.py\n'.format(MJD+j))
    else:
        fo.write('#{0} PROFILE generated by simulator.py\n'.format(MJD+j))
    for i,p in enumerate(prof):
        fo.write("{0} {1}\n".format(i,p))
    fo.close()
def ProfPlotter(prof,root,i,mc):
    # plot me profile
    plt.plot(prof)
    plt.xlabel('bins')
    if mc:
        plt.title('MC Profile simulation {0}'.format(MJD+i))
    else:
        plt.title('Profile simulation {0}'.format(MJD+i))
    plt.xlim([1,prof.size])
    plt.grid(True)
    plt.savefig(root+'prof'+str(i).zfill(3)+'.png')
    plt.clf()
    plt.close()
#
for i in xrange(NOBS):
    if i in MC:
        mc = True
    else:
        mc = False
    ProfWriter(PP[i],root+'prof'+str(i).zfill(3)+'.prof',i,mc)
    ProfPlotter(PP[i],root,i,mc)
    
