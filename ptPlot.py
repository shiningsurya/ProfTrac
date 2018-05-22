# Takes in ret and plots it
import numpy as np
import matplotlib.pyplot as plt
# plt.style.use('ggplot')
import sys 

if len(sys.argv) < 3:
    print "Usage: python ptPlot.py <NPY> <CHOICE>"
    print "Choice 1 : Waterfall"
    print "Choice 2 : % "
    sys.exit(0)
#
choice = int(sys.argv[2])
# 
# running mean
# https://stackoverflow.com/questions/13728392/moving-average-or-running-mean/27681394#27681394
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
#
ret = np.load(sys.argv[1])
ret = ret[~np.isnan(ret).any(axis=1)]
N,J = ret.shape
# drop nans

# if J == 7 or J == 8:
    # alpha,beta = 2,4
# elif J == 10 or J == 9:
    # alpha,beta = 2,5
# elif J == 11 or J == 12:
    # alpha,beta = 2,6
# fig, ax = plt.subplots(beta,alpha,sharex=True,figsize=(35,95))
#
# for ia in xrange(beta):
    # for ib in xrange(alpha):
        # j = ia*alpha + ib # voila
        # if j >= J:
            # continue
        # plt.sca(ax[ia,ib])
        # plt.plot(ret[:,j])
        # plt.plot(running_mean(ret[:,j],N//10),'r-')
        # plt.grid(True)
        # plt.xlim([0, N])
        # plt.xlabel('MJD[frm ref eph]')
        # plt.title('J = {}'.format(j))
##
if choice == 1:
    yJ = np.arange(J)[::-1]
    jj = 0
    # ret -= ret[0]
    for j in yJ:
        y = ret[:,j]
        y -= y.min()
        y /= y.max()
        y -= 0.5 
        # bringing it to [-0.5,0.5]
        plt.plot(jj + y)
        jj = jj + 1
    plt.xlabel('# Obs')
    plt.xlim([0,N-1])
    plt.ylabel('Scale [J]')
    plt.yticks(np.arange(J),yJ)
    plt.grid(True)
    plt.xticks(np.arange(N),rotation=90)
    plt.title('ProfileTrack')
    plt.show()
elif choice == 2:
    for j in xrange(J):
        plt.plot(100*ret[:,j],label='J = {0}'.format(j))
    plt.grid(True)
    plt.legend(loc='best')
    plt.xlabel('# Obs')
    plt.ylim([0,100])
    plt.xlim([0,N-1])
    plt.title('ProfileTrack')
    plt.ylabel('%age of energy in each Scale')
    plt.show()
