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
     J3: B -> BP;  k3*AP*B/(Km3 + B)
     J4: BP -> B;  k4*BP/(Km4 + BP)

     k1 = 0.4
     k2 = 0.7
     k3 = 0.7
     k4 = 0.7
     A = 10
     B = 10
     Km1 = 0.5
     Km2 = 0.5
     Km3 = 0.5
     Km4 = 0.5
""")

r.steadyState()

# print(r.getFullJacobian())
# print(r.getReducedJacobian())
# print(r.getuCC('BP', 'k1'))
# quit()

# x = []
# y = []
# c1 = []
# c2 = []
# z = []
#
# for i in range(200):
#     r.steadyState()
#     x.append(r.k1)
#     y.append(r.BP)
#     c1.append(r.getuCC('BP', 'k1') / 10)
#     c2.append(r.getCC('BP', 'k1'))
#     z.append(r.getReducedJacobian()[1][1])
#     r.k1 = r.k1 + 0.001
#
# plt.plot(x, y, label="BP")
# plt.plot(x, z, label="rJac")
# plt.plot(x, c1, label="CC/10")
# plt.plot(x, c2, label="sCC")
# plt.xlabel("k1")
# plt.legend()
# plt.tight_layout()
# plt.savefig("single_cycle_two_layer_plot.pdf")
# # plt.savefig("single_cycle_two_layer_plot")
# plt.show()
#
# quit()

# =========================================================

# r.steadyState()
#
# k1s = []
# BWs = []
#
# for i in np.arange(0.4, 0.6, .001):
#     r.steadyState()
#     k1s.append(r.k1)
#     r.k1 = i
#     omega_n = np.sqrt((r.getEE('J1', 'A') + r.getEE('J2', 'AP'))*(r.getEE('J3', 'B') + r.getEE('J4', 'BP')))
#     zeta = 0.5*(r.getEE('J1', 'A') + r.getEE('J2', 'AP') + r.getEE('J3', 'B') + r.getEE('J4', 'BP'))/omega_n
#     omega_c = omega_n*np.sqrt(1-2*zeta**2 + np.sqrt((2*zeta**2-1)**2) + 1)
#     BWs.append(omega_c)
# #
# plt.plot(k1s, BWs)
# plt.xlabel('k1')
# plt.ylabel('Bandwidth')
# plt.title("Bandwidth (single-cycle two-layer system) vs k1")
# plt.tight_layout()
# plt.savefig("single_cycle_two_layer_bandwidth_vs_k1.pdf")
# plt.show()
#
# quit()

# =========================================================

# r.steadyState()
#
# k1s = []
# BWs = []
# damps = []
#
# for i in np.arange(0.4, 0.6, .001):
#     r.steadyState()
#     k1s.append(r.k1)
#     r.k1 = i
#     omega_n = np.sqrt((r.getEE('J1', 'A') + r.getEE('J2', 'AP'))*(r.getEE('J3', 'B') + r.getEE('J4', 'BP')))
#     zeta = 0.5*(r.getEE('J1', 'A') + r.getEE('J2', 'AP') + r.getEE('J3', 'B') + r.getEE('J4', 'BP'))/omega_n
#     omega_c = omega_n*np.sqrt(1-2*zeta**2 + np.sqrt((2*zeta**2-1)**2) + 1)
#     damps.append(zeta)
#     # BWs.append(omega_c)
# #
# plt.plot(k1s, damps)
# plt.xlabel('k1')
# plt.ylabel('Damping ratio')
# plt.title("Damping ratio (single-cycle two-layer system) vs k1")
# plt.tight_layout()
# plt.savefig("single_cycle_two_layer_damping_ratio_vs_k1.pdf")
# plt.show()
#
# quit()

# =========================================================

k1s = []
freqs = []
amps = []
phases = []
for i in np.arange(0.4, 0.6, .001):
    amps.append([])
    phases.append([])
    k1s.append(i)
    r.k1 = i
    fr = FreqencyResponse(r)
    results = fr.getSpeciesFrequencyResponse(0.01, 3, 100, 'k1', 'BP')
    for each in results:
        amps[-1].append(each[1])
        phases[-1].append(each[2])
    if i == 0.4:
        for each in results:
            freqs.append(np.log10(each[0]))

xx, yy = np.meshgrid(freqs, k1s)

amps = np.array(amps)
phases = np.array(phases)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Freq (log10)")
ax.set_ylabel("k1")

# uncomment for freq
# ax.set_zlabel("Amp (log10)")
# ax.plot_surface(xx, yy, amps)
# ax.view_init(elev=30., azim=-45)
# plt.title("Amplitude vs Frequency over a range of k1 values")
# # plt.savefig("two_layer_freq_amp_over_k1.pdf")
# plt.savefig("two_layer_freq_amp_over_k1.pdf")
# plt.show()

# uncomment for phase
ax.set_zlabel("Phase (degrees)")
ax.plot_surface(xx, yy, phases)
ax.view_init(elev=30., azim=-45)
plt.title("Phase vs Frequency over a range of k1 values")
# plt.savefig("freq_phase_over_k1.pdf")
plt.savefig("two_layer_freq_phase_over_k1.pdf")
plt.show()

quit()




