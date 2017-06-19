#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Program to create a large aggregate.

Created on Thu Jun 15 2017

@author: ribli
"""

import random
import math
import scipy
import scipy.optimize
import scipy.spatial
import numpy as np
import pickle
import datetime
import os


def step(x,y):
    """Random 0,1 step in random xy direction."""
    if random.randint(0,1)==0: # x or y
        x+=random.choice([-1,1]) # back or forth
    else:
        y+=random.choice([-1,1])
    return x,y


def walk(agg):
    """Simlate Brown motion until attached, or out."""
    (xc,yc),r = seed_circle(agg)  # calculate seed circle
    x,y = get_initial_pos(xc,yc,r)  # start from afar
    route=[]   # save route, only for demo purposes
    while True:  # I like to live dangerously
        x,y = step(x,y)  # make one step
        route.append((x,y))  # save step into route
        if too_far(x,y,xc,yc,r):  # check if we got too far
            break  # if yes abandon this particle
        # check if next to aggregate
        if (((x-1,y) in agg) or  ((x+1,y) in agg) or
            ((x,y-1) in agg) or  ((x,y+1) in agg) ):
            # ((x-1,y-1) in agg) or  ((x+1,y+1) in agg) or 
            # ((x-1,y+1) in agg) or  ((x+1,y-1) in agg)):
            agg[(x,y)]=len(agg)  # attach if yes
            break  # finished
    return agg,route


def seed_circle(agg):
    """Get the seed circle."""
    x,y = zip(*agg.keys()) # get x,y lists from dict
    xmin,xmax,ymin,ymax = min(x),max(x),min(y),max(y) #bounds
    xc, yc = (xmin+xmax)/2, (ymin+ymax)/2 #center
    r = (((xmax-xmin)/2)**2 + ((ymax-ymin)/2)**2)**0.5 # radius
    return (xc,yc),r


def get_initial_pos(xc,yc,r):
    """Get inital position on seed circle."""
    ralf = 2* math.pi * random.random() # random angle
    # initial points on the circle
    x0 = int(xc + r*math.cos(ralf))
    y0 = int(yc + r*math.sin(ralf))
    return x0,y0


def too_far(x,y,x0,y0,r,d=10):
    """Check if the particle went too far."""
    return ((x-x0)**2 + (y-y0)**2)**0.5 > r+d


def grow(agg=None,npart=10000):
    """Grow aggragate, try to attach npart points."""
    if agg is None:  # if not contin
        agg={(0,0):0} # 0th point at (0,0)
    for i in range(npart):
        agg,_ = walk(agg) # try to attach
    return agg


if __name__=='__main__':
    M = 10000  # basiaclly run forever ...
    N = 1000  # number or particles lauched in a batch

    if os.path.isfile('agg.pkl'):  # if agg exists continue growing it
        agg = pickle.load(open('agg.pkl','rb'))
    else:  # else start from scratch
        agg = grow(npart=N) 

    for i in xrange(M):
        N_oldagg = len(agg)  # calculate len only for reporting
        agg = grow(agg,npart=N) # create the aggregate
        # report landing, growing stats
        print datetime.datetime.now(),'Lauched',N,'particles',\
        len(agg)-N_oldagg,'landed, agg size:',len(agg)
        pickle.dump(agg,open('agg.pkl','wb'))