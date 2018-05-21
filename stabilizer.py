# Shows stability
## or ??
### What if????
import numpy as np
import ctypes as ct
import sys
import os
import fnmatch
from tqdm import tqdm
## IO
if len(sys.argv) < 2:
    print "Usage: python stabilizer.py <DIRECTORY>"
    sys.exit(0)
##
root = sys.argv[1]
# save mse
def SafeMSE(a,b):
    if a.size == b.size:
        return np.mean(np.power(a-b,2))
    else:
        if b.size < a.size:
            a,b = b,a # swap
        # a is small and b is large
        aa = np.zeros(b.size)
        aa[:a.size] = a
        return np.mean(np.power(aa-b,2))
##
ls = [x for x in os.listdir(root) if fnmatch.fnmatch(x,'*.txt')] 
N = len(ls) # number of files
Px = np.zeros((N,N))
Wx = np.zeros((N,N))
##
i,j = 0,0
for f1 in tqdm(ls,desc="File #1",unit='files',ascii=True):
    j = 0
    for f2 in tqdm(ls,desc="File #2", unit='files',ascii=True):
        _, i1 = np.genfromtxt(root+f1,skip_header=True,unpack=True)
        _, i2 = np.genfromtxt(root+f2,skip_header=True,unpack=True)
        N1,N2 = i1.size,i2.size
        J1,J2 = int(np.log2(N1)), int(np.log2(N2))
        out1,out2 = np.zeros(J1), np.zeros(J2)
        ## c-part
        libpt = ct.cdll.LoadLibrary('/home/shining/mega/IPTA/ProfileTrack/ProfTrac/pt')
        double_p = ct.POINTER(ct.c_double)
        i1_p = i1.ctypes.data_as(double_p)
        out1_p = out1.ctypes.data_as(double_p)
        i2_p = i2.ctypes.data_as(double_p)
        out2_p = out2.ctypes.data_as(double_p)
        ## phi call
        libpt.phi(i1_p,ct.c_int(N1),ct.c_int(J1),out1_p)
        libpt.phi(i2_p,ct.c_int(N2),ct.c_int(J2),out2_p)
        ##
        Px[i,j] = SafeMSE(i1,i2) 
        Wx[i,j] = SafeMSE(out1,out2) 
        j = j + 1
    i = i + 1
##
np.save(root+'ProfileDistance',Px)
np.save(root+'ScaleDistance',Wx)
