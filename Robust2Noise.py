# Check for robustness to noise
## pls be robust! 
import numpy as np
import ctypes as ct 
import sys
from tqdm import tqdm
## IO
if len(sys.argv) < 2:
    print "Usage: python Robust2Noise.py <PROFILE_FILE>"
    sys.exit(0)
fn = sys.argv[1] # first argument is the file name
_, iin = np.genfromtxt(fn,skip_header=True,unpack=True)
iin = np.array(iin,dtype=np.double)
# signal power
GivePower = lambda x : np.mean(np.power(x,2))
pin = GivePower(iin) 
NN = 100
powerx = np.linspace(0,pin,NN) # this becomes the x axis
N = iin.size
J = int(np.log2(N))
out = np.zeros(J,dtype=np.double)
ret = []
## c-part
libpt = ct.cdll.LoadLibrary('/home/shining/mega/IPTA/ProfileTrack/ProfTrac/ptpse')
double_p = ct.POINTER(ct.c_double)
iin_p = iin.ctypes.data_as(double_p)
out_p = out.ctypes.data_as(double_p)
## Work part
for ip in tqdm(powerx,desc='Noise',unit='noises',ascii=True):
    # add noise
    iin += np.sqrt(ip) * np.random.randn(N)
    # function call
    libpt.phi(iin_p,ct.c_int(N),ct.c_int(J),out_p)
    # saving output
    ret.append([GivePower(iin), GivePower(out)])
    # resetting out
    out = np.zeros(J)
    out_p = out.ctypes.data_as(double_p)
## Plot part
ret = np.array(ret)
ret -= ret[0]
import matplotlib.pyplot as plt
x = np.arange(NN)
plt.semilogy(x,ret[:,0],label='Signal Power')
plt.semilogy(x,ret[:,1],label="ScaleCoeff Power")
plt.xlabel('Noise Power[% of Signal Power]')
# plt.xticks(x[::10],x[::10]/NN)
plt.grid(True)
plt.ylabel('Signal+Noise Power')
# plt.xlim([0,NN])
plt.legend(loc='best')
plt.title('Robustness-Noise')
plt.savefig(fn+'RobustNoise.png')
np.save(fn+'retRobustNoise',ret)
