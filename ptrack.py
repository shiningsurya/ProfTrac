# Tracks profile change
import numpy as np
import ctypes as ct 
import sys
import os
import fnmatch
from tqdm import tqdm
## IO
if len(sys.argv) < 2:
    print "Usage: python ptrack.py <DIRECTORY>"
    sys.exit(0)
root = sys.argv[1]
ls = [x for x in os.listdir(root) if fnmatch.fnmatch(x,'*.prof')] 
print ls
N = len(ls) # number of files
libpt = ct.cdll.LoadLibrary('/home/shining/mega/IPTA/ProfileTrack/ProfTrac/ptpse')
ret = [] 
for f in tqdm(ls,desc="PSR",unit='files',ascii=True):
    try:
        _, iin = np.genfromtxt(root+f,skip_header=True,unpack=True)
    except:
        print "[!!] Error here",f
        # continue
    iin = np.array(iin,dtype=np.double) # this is goddamn important
    NN = iin.size
    J = int(np.log2(NN))
    out = np.zeros(J,dtype=np.double)
    double_p = ct.POINTER(ct.c_double)
    iin_p = iin.ctypes.data_as(double_p)
    out_p = out.ctypes.data_as(double_p)
    libpt.phi(iin_p,ct.c_int(NN),ct.c_int(J),out_p)
    ret.append(out)
ret = np.array(ret)
# ret -= ret.mean(0)
# import matplotlib.pyplot as plt
# x = np.arange(N)
# for j in xrange(J):
# y = j + ret[:,j]
# y -= np.mean(y)
# y /= np.std(y)
# plt.plot(x,y,label='J = {}'.format(j))
# plt.xlabel('Pulsar')
# plt.grid(True)
# plt.legend(loc='best')
# plt.ylabel('Scale Coeff')
# plt.title('Scale Change')
# plt.savefig(root+'ProfileTrack.png')
## Save
np.save(root+'ProfileTrack',ret)
