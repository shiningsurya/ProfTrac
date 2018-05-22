import numpy as np
import ctypes as ct
import sys
## IO
if len(sys.argv) < 2:
    print "Usage: python tester.py <PROFILE>"
    sys.exit(0)
libpt = ct.cdll.LoadLibrary('/home/shining/mega/IPTA/ProfileTrack/ProfTrac/ptpse')
_, iin = np.genfromtxt(sys.argv[1],skip_header=True,unpack=True)
iin = np.array(iin,dtype=np.double)
print iin
# This is goddamn important to have 
NN = iin.size
J = int(np.log2(NN))
out = np.zeros(J,dtype=np.double)
double_p = ct.POINTER(ct.c_double)
iin_p = iin.ctypes.data_as(double_p)
out_p = out.ctypes.data_as(double_p)
libpt.phi(iin_p,ct.c_int(NN),ct.c_int(J),out_p)
# libpt.get_penergy(iin_p,ct.c_int(J),out_p,ct.c_int(NN))
##
np.set_printoptions(precision=3)
print out
print out.sum()







