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
freqs = []
amps = []
phases = []
for i in range(801):
    amps.append([])
    phases.append([])
    x.append(r.S)
    fr = FreqencyResponse(r)
    results = fr.getSpeciesFrequencyResponse(0.001, 3, 100, 'S', 'AP')
    for each in results:
        amps[-1].append(each[1])
        phases[-1].append(each[2])
    if i == 0:
        for each in results:
            freqs.append(np.log10(each[0]))
    r.S = r.S + 0.01

xx, yy = np.meshgrid(freqs, x)

amps = np.array(amps)
phases = np.array(phases)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Freq (log10)", fontsize=15, labelpad=10)
ax.set_ylabel("Signal S", fontsize=15, labelpad=10)

# uncomment for freq
# ax.set_zlabel("Amp (log10)", fontsize=15, labelpad=5)
ax.plot_surface(xx, yy, amps, facecolor="cornflowerblue", edgecolors="blue")
ax.view_init(elev=30., azim=-45)
# plt.title("Amplitude vs Frequency over k1", fontsize=15)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
ax.tick_params('z', labelsize=13)
plt.savefig("freq_amp_over_S.pdf")
plt.show()

# uncomment for phase
# ax.set_zlabel("Phase (degrees)", fontsize=15, labelpad=5)
# ax.plot_surface(xx, yy, phases, facecolor="cornflowerblue", edgecolors="blue")
# ax.view_init(elev=30., azim=-45)
# # plt.title("Phase vs Frequency over k1", fontsize=15)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# ax.tick_params('z', labelsize=13)
# plt.savefig("freq_phase_over_S.pdf")
# plt.show()
