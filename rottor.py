# Shows shift invariance
## or ?? 
### what if????
## Ladies and gentlemen
## We have shift invariance
import numpy as np
import ctypes as ct 
import sys
from tqdm import tqdm
## IO
if len(sys.argv) < 2:
    print "Usage: python rotater.py <PROFILE_FILE>"
    sys.exit(0)
fn = sys.argv[1] # first argument is the file name
_, iin = np.genfromtxt(fn,skip_header=True,unpack=True)
iin = np.array(iin,dtype=np.double) # this is goddamn important
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
for i in tqdm(xrange(N),desc='Shift',unit='shift',ascii=True):
    # function call
    libpt.phi(iin_p,ct.c_int(N),ct.c_int(J),out_p)
    # saving output
    ret.append(out)
    # resetting out
    # out = np.zeros(J,dtype=np.double)
    out[:] = 0.00
    # out_p = out.ctypes.data_as(double_p)
    # cyclic shift
    iin = np.roll(iin,1)
## Plot part
ret = np.array(ret)
import matplotlib.pyplot as plt
x = np.arange(N)
for j in xrange(J):
    y = ret[:,j]
    # y -= np.mean(y)
    # y /= np.std(y)
    plt.plot(x,y,label='J = {0}, $\sigma$ = {1:1.2e}'.format(j,np.std(y)))
plt.xlabel('Shift')
plt.grid(True)
plt.legend(loc='best')
plt.ylabel('Scale Energy')
plt.title('Shift-Invariance')
plt.savefig(fn+'ShiftInvariance.png')
## Save
np.save(fn+'retShiftInvariance',ret)
