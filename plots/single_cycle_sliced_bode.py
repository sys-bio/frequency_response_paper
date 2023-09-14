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
fig, ax1 = plt.subplots()
for i in range(9):
    freq = []
    amp = []
    phase = []

    x.append(r.S)
    fr = FreqencyResponse(r)
    results = fr.getSpeciesFrequencyResponse(0.001, 4.5, 100, 'S', 'AP')
    for each in results:
        freq.append(np.log10(each[0]))
        amp.append(each[1])
        phase.append(each[2])
    ax1.plot(freq, amp)
    # ax1.plot(freq, phase)
    r.S = r.S + 0.5
box = ax1.get_position()
# ax1.set_position([box.x0, box.y0, box.width * 0.9, box.height])
# ax1.legend(x, bbox_to_anchor=(1, 1.02), title="Signal S")
ax1.legend(x, title="Signal S")
print(r.S)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
ax1.set_xlabel("Freq (log10)", fontsize=15)
# yticks = [0, -10, -20, -30, -40, -50, -60, -70, -80, -90]
# plt.yticks(yticks, fontsize=13)

ax1.set_ylabel("Amp (log10)", fontsize=15)
plt.savefig('bodeAmpSlices.pdf')
plt.savefig('bodeAmpSlices')

# ax1.set_ylabel("Phase (degrees)", fontsize=15)
# plt.savefig('bodePhaseSlices.pdf')
# plt.savefig('bodePhaseSlices')
plt.show()
