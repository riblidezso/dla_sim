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
import sys

def get_ml(agg, rl):
    """Get the mass list with given r list."""
    i = random.randint(0,len(agg)-1)  # init a random pivot point
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


def get_Dq(agg, n=10, ql=range(-8,1) + range(2,9), 
		   rl = xrange(50,60,1), plot=False):
    """Calculate D(q) at a given q."""
    # get the masses for n pivot points
    mll=[ get_ml(agg,rl) for i in xrange(n)]  

    Dq = [get_Dq_at_q(rl,mll,q) for q in ql]

    return Dq


def get_Dq_at_q(rl,mll,q):
	# x,y per definition
    x = np.log10(rl) * (q-1)
    y = np.log10(np.mean(np.power(mll,q-1),axis=0)) 

    # fit linear on log log
    (a,b),pcov = scipy.optimize.curve_fit(lambda x,a,b: a*x+b, x, y)
    
    return a


if __name__=='__main__':
    N_rep = int(sys.argv[1])  # number of reps
    N_pivot = int(sys.argv[2])  # number of pivot points
    rl = range(int(sys.argv[3]),int(sys.argv[4]))  # distange range
    ql=range(-8,1) + range(2,9)  # q range is fixed

    agg = pickle.load(open('agg.pkl','rb')) # load large agg
     
    Dq=[]
    for j in xrange(N_rep): # multiple runs -> mean std
        Dq.append(get_Dq(agg,ql=ql,n=N_pivot,rl=rl))  # run one rep
        print datetime.datetime.now(),j  # report
        pickle.dump((ql,Dq),open('Dq.pkl','wb'))  # save it
