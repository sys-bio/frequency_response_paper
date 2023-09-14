# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:11:12 2023

@author: hsauro
"""

import tellurium as te
import roadrunner
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, StrMethodFormatter
from freqResponse import *
import numpy as np

r = te.loada("""
     v1: A -> AP;  k1*S*A/(Km1 + A)
     v2: AP -> A;  k2*AP/(Km2 + AP)

     k1 = 0.14
     k2 = 0.7
     A = 10
     Km1 = 0.5
     Km2 = 0.5
     S = 1
""")

r.conservedMoietyAnalysis = True
r.steadyState()

x = []
y = []
c1 = []
c2 = []
z = []

for i in range(800):
    r.steadyState()
    x.append(r.S)
    y.append(r.AP)
    c1.append(r.getuCC('AP', 'S'))
    c2.append(r.getCC('AP', 'S'))
    z.append(r.getReducedJacobian()[0][0])
    r.S = r.S + 0.01

# print(r.k1)
plt.plot(x, y, label=r"$AP$")
# plt.plot(x, z, label="rJac")
plt.plot(x, c1, label=r"$\frac{dAP}{dS}$")
plt.plot(x, c2, label=r"$\frac{dAP}{dS}\frac{S}{AP}$")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel("Signal S", fontsize=15)
plt.legend(fontsize=15)
plt.tight_layout()
plt.savefig("single_cycle_plot.pdf")
plt.savefig("single_cycle_plot")
plt.show()
