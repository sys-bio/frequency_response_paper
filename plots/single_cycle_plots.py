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
     J1: A -> AP;  k1*A/(Km1 + A)
     J2: AP -> A;  k2*AP/(Km2 + AP)

     k1 = 0.14
     k2 = 0.7
     A = 10
     Km1 = 0.5
     Km2 = 0.5
""")

# def AP(k):
#     return ((-k * 0.5 - 0.7 * 0.5 + k * 10 - 0.7 * 10
#             + np.sqrt(4 * k * (k - 0.7) * 0.5 * 10 + (k * 0.5 + 0.7 * 0.5 - k * 10 + 0.7 * 10) ** 2))
#             / (2*(k - 0.7)))

# def dAP(k):
#     return (-0.1225 -0.175 * k + 0.35 * np.sqrt(54.0225-))

# func_values = []
# k = 0.14
# for i in range(100):
#     func_values.append(AP(k))
#     print(AP(k))
#     k += 0.01

# print(func_values)

# r.steadyState()
# print(r.A, r.AP)
#
# x = []
# y = []
# c1 = []
# c2 = []
# z = []
#
# for i in range(100):
#     r.steadyState()
#     x.append(r.k1)
#     y.append(r.AP)
#     c1.append(r.getuCC('AP', 'k1') / 5)
#     c2.append(r.getCC('AP', 'k1'))
#     z.append(r.getReducedJacobian()[0][0])
#     r.k1 = r.k1 + 0.01
#
# plt.plot(x, y, label="AP")
# # plt.plot(x, func_values, label="analytical AP")
# # plt.plot(x, z, label="rJac")
# plt.plot(x, c1, label="CC/5")
# plt.plot(x, c2, label="scaled CC")
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.xlabel("k1", fontsize=15)
# plt.legend(fontsize=15)
# plt.tight_layout()
# plt.savefig("single_cycle_plot.pdf")
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
# plt.xlabel('k1', fontsize=15)
# plt.ylabel('Bandwidth ($\epsilon^{J2}_{AP} + \epsilon^{J1}_{A}$)', fontsize=15)
# plt.title("Bandwidth vs k1", fontsize=15)
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.tight_layout()
# plt.savefig("Bandwidth_vs_k1.pdf")
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
    results = fr.getSpeciesFrequencyResponse(0.001, 3, 100, 'k1', 'AP')
    for each in results:
        amps[-1].append(each[1])
        phases[-1].append(each[2])
    if i == 0.14:
        for each in results:
            freqs.append(np.log10(each[0]))

xx, yy = np.meshgrid(freqs, k1s)

amps = np.array(amps)
phases = np.array(phases)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Freq (log10)", fontsize=15, labelpad=10)
ax.set_ylabel("k1", fontsize=15, labelpad=10)

# uncomment for freq
# ax.set_zlabel("Amp (log10)", fontsize=15, labelpad=5)
# ax.plot_surface(xx, yy, amps)
# ax.view_init(elev=30., azim=-45)
# plt.title("Amplitude vs Frequency over k1", fontsize=15)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# ax.tick_params('z', labelsize=13)
# plt.savefig("freq_amp_over_k1.pdf")
# plt.show()

# uncomment for phase
ax.set_zlabel("Phase (degrees)", fontsize=15, labelpad=5)
ax.plot_surface(xx, yy, phases)
ax.view_init(elev=30., azim=-45)
plt.title("Phase vs Frequency over k1", fontsize=15)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
ax.tick_params('z', labelsize=13)
plt.savefig("freq_phase_over_k1.pdf")
plt.show()

quit()




