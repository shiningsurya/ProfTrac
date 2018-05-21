# This plots the stabilizer

import numpy as np
import matplotlib.pyplot as plt
import sys
## IO
if len(sys.argv) < 3:
    print "Usage: python PlotStab.py <DIRECTORY> <TYPE>"
    sys.exit(0)
##
def GiveRes(x,y):
    if x == 0.0 or y == 0.0:
        return 0.00
    return x/y

##
root = sys.argv[1]
Px = np.load(root+'ProfileDistance.npy')
Sx = np.load(root+'ScaleDistance.npy')
#
if int(sys.argv[2]) == 1:
    Ni,Nj = Px.shape
    res = np.zeros((Ni,Nj))
    for i in xrange(Ni):
        for j in xrange(Nj):
            res[i,j] = GiveRes(Px[i,j],Sx[i,j])
    #
    plt.imshow(res,cmap='hot')
    plt.colorbar()
    plt.xlabel('Image #1')
    plt.ylabel('Image #2')
    plt.title('Stability')
    plt.savefig(root+'Splot.png')
    plt.show()
##
elif int(sys.argv[2]) == 2:
    xpm = Px.ravel()
    xsm = Sx.ravel()
    #
    xpm = np.log10(xpm[np.nonzero(xpm)])
    xsm = np.log10(xsm[np.nonzero(xsm)])
    #
    hip,_,_ = plt.hist(xpm,bins=100,label='Prof',normed=True,histtype='stepfilled')
    his,_,_ = plt.hist(xsm,bins=100,label='ScaleCoeff',normed=True,histtype='stepfilled')
    plt.legend(loc='best')
    plt.title('Stability')
    plt.grid(True)
    plt.savefig(root+'Splot2.png')
    plt.show()
    #
    # KL Div and KS 2 sample test
    from scipy.stats import ks_2samp
    KS,pv = ks_2samp(hip,his)
    print "The statistics is {0:3.3f} and p-value is {1}".format(KS,pv)
