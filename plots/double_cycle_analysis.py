# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:11:12 2023

@author: hsauro
"""

import tellurium as te
import roadrunner
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from freqResponse import *
import numpy as np

r = te.loada("""
     
     J1: AP -> APP;  k3*S*AP/(Km3 + AP)
     J4: APP -> AP;  k4*APP/(Km4 + APP)
     J3: A -> AP;  k1*S*A/(Km1 + A)
     J2: AP -> A;  k2*AP/(Km2 + AP)

     k1 = 0.14
     k2 = 0.7
     k3 = 0.7
     k4 = 0.7
     A = 10
     S = 1
     Km1 = 0.5
     Km2 = 0.5
     Km3 = 0.5
     Km4 = 0.5
""")

nr = r.getNrMatrix()
li = r.getLinkMatrix()
st = r.getUnscaledElasticityMatrix()
print(nr)
print(li)
print(st)
