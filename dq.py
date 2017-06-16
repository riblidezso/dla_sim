#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Program to create a large aggregate.

Created on Thu Jun 15 2017

@author: ribli
"""

import random
import scipy.optimize
import numpy as np
import pickle
import datetime
# from grow import seed_circle

def get_ml(agg, rl, i=None):
    """Get the mass list with given r list."""
    if i is None:  # init a random pivot point
        i = random.randint(0,len(agg)-1)
    c = agg.keys()[i]  # get its position
    
    pos = np.array(agg.keys())  # get position of all points
    dist = ((c[0]-pos[:,0])**2+(c[1]-pos[:,1])**2)**0.5  # calculate ditance
    dist = dist[dist < rl[-1]]  # ignore what is too far
    closest = dist < rl[0]  # select which are too close
    m0 = np.sum(closest)  # number which are too close
    dist = dist[~closest]  # discard too close (maybe save little time)
    
    r = np.sort(dist)
    m = m0 + np.arange(len(r))
    ml = np.interp(rl,r,m) # calculate mass for all r limits  
    return ml


def get_dq(agg,q,n=10, rl = xrange(20,40,2), plot=False):
    """Calculate D(q) at a given q."""

    # _,r = seed_circle(agg)  # get the size of agg
    # rl = 

    # get the masses for n pivot points
    mll=[ get_ml(agg,rl) for i in xrange(n)]  

    # x,y per definition
    x = np.log10(rl) * (q-1)
    y = np.log10(np.mean(np.power(mll,q-1),axis=0)) 

    # fit linear on log log
    (a,b),pcov = scipy.optimize.curve_fit(lambda x,a,b: a*x+b, x, y)
    
    if plot:  # plot to check
        lab = 'coef = '+ "%.2f +/- %.2f"% (a, pcov[0,0]**0.5)
        plt.plot(x, a*x+b, label=lab)
        plt.plot(x,y,'o')
        plt.legend()
    
    return a

if __name__=='__main__':
    M = 50
    N = 1000
    q = range(-9,1) + range(2,10) # q points
    
    agg = pickle.load(open('agg.pkl','rb')) # load large agg
     
    Dq=[]
    for j in xrange(M): # multiple runs -> mean std
        Dqi=[]
        for qi in q:
            Dqi.append(get_dq(agg,qi,n=N))
            print datetime.datetime.now(),j,qi
        Dq.append(Dqi)
        pickle.dump((q,Dq),open('Dq.pkl','wb'))
