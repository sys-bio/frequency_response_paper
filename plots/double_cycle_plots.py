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
     J1: AP -> APP;  k3*AP/(Km3 + AP)
     J2: A -> AP;  k1*A/(Km1 + A)
     J3: AP -> A;  k2*AP/(Km2 + AP)
     J4: APP -> AP;  k4*APP/(Km4 + APP)

     k1 = 0.14
     k2 = 0.7
     k3 = 0.7
     k4 = 0.7
     A = 10
     Km1 = 0.5
     Km2 = 0.5
     Km3 = 0.5
     Km4 = 0.5
""")

# print(r.getReducedStoichiometryMatrix())
# print(r.getLinkMatrix())
# print(r.getUnscaledElasticityMatrix())
#
# quit()

# r.steadyState()
# print(r.A, r.AP, r.APP)
# print(r.getReducedJacobian())

# x = []
# y1 = []
# y2 = []
# c1 = []
# c2 = []
# z = []
#
# for i in range(100):
#     r.steadyState()
#     x.append(r.k1)
#     # y1.append(r.AP)
#     y2.append(r.APP)
#     c1.append(r.getuCC('APP', 'k1') / 5)
#     c2.append(r.getCC('APP', 'k1'))
#     # z.append(r.getReducedJacobian()[0][0])
#     r.k1 = r.k1 + 0.01
#
# # plt.plot(x, y1, label="AP")
# plt.plot(x, y2, label="APP")
# plt.plot(x, c1, label="CC/5")
# plt.plot(x, c2, label="sCC")
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# # plt.plot(x, z, label="rJac")
# plt.xlabel("k1", fontsize=15)
# plt.legend(fontsize=15)
# plt.tight_layout()
# plt.savefig("double_cycle_plot.pdf")
# plt.show()
#
# quit()

# =========================================================

# r.steadyState()
#
# k1s = []
# BWs = []
#
# for i in np.arange(0.14, 1.4, .01):
#     r.steadyState()
#     k1s.append(r.k1)
#     r.k1 = i
#     BWs.append(r.getEE('J2', 'AP') + r.getEE('J1', 'A'))
# #
# plt.plot(k1s, BWs)
# plt.xlabel('k1')
# plt.ylabel('Bandwidth (E^J2_AP + E^J1_A)')
# plt.title("Bandwidth vs k1")
# plt.savefig("Bandwidth_vs_k1")
# plt.show()
#
# quit()

# =========================================================

k1s = []
freqs = []
amps = []
phases = []
for i in np.arange(0.14, 1.4, .01):
    amps.append([])
    phases.append([])
    k1s.append(i)
    r.k1 = i
    fr = FreqencyResponse(r)
    results = fr.getSpeciesFrequencyResponse(0.01, 3, 100, 'k1', 'APP')
    for each in results:
        amps[-1].append(each[1])
        phases[-1].append(each[2])
    if i == 0.14:
        for each in results:
            freqs.append(np.log10(each[0]))

xx, yy = np.meshgrid(freqs, k1s)

amps = np.array(amps)
phases = np.array(phases)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Freq (log10)", fontsize=15, labelpad=10)
ax.set_ylabel("k1", fontsize=15, labelpad=10)

# uncomment for freq
ax.set_zlabel("Amp (log10)", fontsize=15, labelpad=5)
ax.plot_surface(xx, yy, amps)
ax.view_init(elev=30., azim=-45)
plt.title("Amplitude vs Frequency over k1", fontsize=15)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
ax.tick_params('z', labelsize=13)
plt.savefig("double_freq_amp_over_k1.pdf")
plt.show()

# uncomment for phase
# ax.set_zlabel("Phase (degrees)", fontsize=15, labelpad=5)
# ax.plot_surface(xx, yy, phases)
# ax.view_init(elev=30., azim=-45)
# plt.title("Phase vs Frequency over k1", fontsize=15)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# ax.zaxis.set_ticks([-20, -40, -60, -80, -100, -120, -140, -160, -180])
# ax.zaxis.set_ticklabels(["-20", "-40", "-60", "-80", "-100", "-120", "-140", "-160", "-180"])
# ax.tick_params('z', labelsize=13)
# plt.savefig("double_freq_phase_over_k1.pdf")
# plt.show()

quit()




