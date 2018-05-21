# coding: utf-8
import numpy as np
k = 10 + np.zeros(10)
k
k = k.astype(np.double)
k
k.dtype
import ctypes as ct
double_p = ct.POINTER(ct.c_double)
k_p = k.ctypes.data_as(double_p)
k_p
ct.c_int(10)
libpt = ct.cdll.LoadLibrary('ProfTrac/pt')
libpt.divider(k_p,ct.c_int(10))
k_p.contents
k_p.data
k
i = np.genfromtxt('wut',skip_header=True)
i
_,i = np.genfromtxt('wut',skip_header=True,unpack=True)
i
i.size
np.log2(i.size)
