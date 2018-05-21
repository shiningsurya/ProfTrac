# Shows shift invariance
## or ?? 
### what if????
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
N = iin.size
J = int(np.log2(N))
out = np.zeros(J)
ret = []
## c-part
libpt = ct.cdll.LoadLibrary('ProfTrac/pt')
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
    out = np.zeros(J)
    out_p = out.ctypes.data_as(double_p)
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
    plt.plot(x,y,label='J = {}'.format(j))
plt.xlabel('Shift')
plt.grid(True)
plt.legend(loc='best')
plt.ylabel('Scale Coeff')
plt.title('Shift-Invariance')
plt.savefig(fn+'.png')
## Save
np.save(fn+'ret',ret)
