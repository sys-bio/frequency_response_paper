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

r.S = 5
r.conservedMoietyAnalysis = True
r.steadyState()

fig, ax = plt.subplots(2)

freq = []
amp = []
phase = []

fr = FreqencyResponse(r)
results = fr.getSpeciesFrequencyResponse(0.001, 3, 1000, 'S', 'AP')
for each in results:
    freq.append(each[0])
    amp.append(10**(each[1]))
    phase.append(each[2])

ax[0].set_yscale('log')

ax[0].set_xscale('log')
ax[1].set_xscale('log')
ax[1].yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
ax[1].set_yticks(range(-90, 1, 15))
ax[0].tick_params(axis='both', which='major', labelsize=13)
ax[1].tick_params(axis='both', which='major', labelsize=13)

ax[0].set(ylabel="gain G")
ax[0].yaxis.get_label().set_fontsize(15)
ax[1].yaxis.get_label().set_fontsize(15)
ax[1].xaxis.get_label().set_fontsize(15)
ax[1].set(ylabel="phase difference", xlabel="frequency")

ax[0].plot(freq, amp)
ax[1].plot(freq, phase)
plt.tight_layout()
plt.savefig('BodeSingleCycle2DPlot2.pdf')
plt.savefig('BodeSingleCycle2DPlot2')
plt.show()

quit()
