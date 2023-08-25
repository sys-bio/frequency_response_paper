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
     J1: A -> AP;  k1*S*A/(Km1 + A)
     J2: AP -> A;  k2*AP/(Km2 + AP)
     J3: B -> BP;  k3*AP*B/(Km3 + B)
     J4: BP -> B;  k4*BP/(Km4 + BP)

     k1 = 0.4
     k2 = 0.7
     k3 = 0.7
     // k4 = 3.5
     k4 = 0.7
     A = 10
     B = 10
     S = 1
     Km1 = 0.5
     Km2 = 0.5
     Km3 = 0.5
     Km4 = 0.5
""")

r1 = te.loada("""
     J1: A -> AP;  k1*S*A/(Km1 + A)
     J2: AP -> A;  k2*AP/(Km2 + AP)
     J3: B -> BP;  k3*AP*B/(Km3 + B)
     J4: BP -> B;  k4*BP/(Km4 + BP)

     k1 = 0.5
     k2 = 0.7
     k3 = 0.7
     // k4 = 0.7
     k4 = 3.5
     A = 10
     B = 10
     S = 1
     Km1 = 0.5
     Km2 = 0.5
     Km3 = 0.5
     Km4 = 0.5
""")

# print(r.getReducedStoichiometryMatrix())
# print(r.getLinkMatrix())
# quit()
#
# print(r.getFullJacobian())
# print(r.getReducedJacobian())
# print(r.getuCC('BP', 'k1'))
# quit()

# r.steadyState()
#
# x = []
# y1 = []
# y2 = []
# c1 = []
# c2 = []
# z = []
#
# for i in range(600):
#     r.steadyState()
#     x.append(r.k1)
#     y1.append(r.AP)
#     y2.append(r.BP)
#     c1.append(r.getuCC('BP', 'k1') / 20)
#     c2.append(r.getCC('BP', 'k1') / 4)
#     z.append(r.getReducedJacobian()[1][1])
#     r.k1 = r.k1 + 0.001
#
# plt.plot(x, y1, label="AP")
# plt.plot(x, y2, label="BP")
# # plt.plot(x, z, label="rJac")
# plt.plot(x, c1, label="CC/20")
# plt.plot(x, c2, label="scaled CC/4")
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.xlabel("k1", fontsize=15)
# plt.legend(fontsize=15)
# plt.tight_layout()
# # xticks = [0.4, 0.45, 0.5, 0.55, 0.6]
# # ticklabels = ['0.4', '0.45', '0.5', '0.55', '0.6']
# # plt.xticks(xticks, ticklabels)
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
# for i in np.arange(0.2, 1.2, .001):
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
# x = []
# BWs = []
# damps = []
# APs = []
# BPs = []
# uCCA = []
# CCA = []
# uCCB = []
# CCB = []
#
# for i in np.arange(1, 2, .001):
#     r.steadyState()
#     x.append(r.S)
#     r.S = i
#     APs.append(r.AP)
#     BPs.append(r.BP)
#     uCCB.append(r.getuCC('BP', 'S') / 10)
#     CCB.append(r.getCC('BP', 'S') / 2)
#     uCCA.append(r.getuCC('AP', 'S') / 2)
#     CCA.append(r.getCC('AP', 'S'))
#
#     omega_n = np.sqrt((r.getEE('J1', 'A') + r.getEE('J2', 'AP'))*(r.getEE('J3', 'B') + r.getEE('J4', 'BP')))
#     zeta = 0.5*(r.getEE('J1', 'A') + r.getEE('J2', 'AP') + r.getEE('J3', 'B') + r.getEE('J4', 'BP'))/omega_n
#     omega_c = omega_n*np.sqrt(1-2*zeta**2 + np.sqrt((2*zeta**2-1)**2) + 1)
#     damps.append(zeta)
#     BWs.append(omega_c)
#
# fig, axs = plt.subplots(4, figsize=(8, 10))
# # axs[0].plot(x, APs, label="AP", c="green")
# # axs[1].plot(x, BPs, label="BP", c="red")
#
# axs[0].plot(x, APs, label="$AP_{ss}$", c="green")
# axs[1].plot(x, BPs, label="$BP_{ss}$", c="red")
#
# # axs[0].plot(k1s, uCCA, label="AP CC/10", c="green", linestyle="dashed")
# # axs[0].plot(k1s, CCA, label="AP scaled CC", c="green", linestyle="dotted")
#
# axs[0].plot(x, uCCA, label=r"$\frac{dAP}{dS}\frac{1}{2}$", c="green", linestyle="dashed")
# axs[0].plot(x, CCA, label=r"$\frac{dAP}{dS}\frac{S}{AP}$", c="green", linestyle="dotted")
#
# # axs[1].plot(k1s, uCCB, label="BP CC/20", c="red", linestyle="dashed")
# # axs[1].plot(k1s, CCB, label="BP scaled CC/4", c="red", linestyle="dotted")
#
# axs[1].plot(x, uCCB, label=r"$\frac{dBP}{dS}\frac{1}{10}$", c="red", linestyle="dashed")
# axs[1].plot(x, CCB, label=r"$\frac{dBP}{dS}\frac{S}{BP}\frac{1}{2}$", c="red", linestyle="dotted")
#
# axs[2].plot(x, damps, label="damping ratio", c="blue")
# axs[3].plot(x, BWs, label="bandwidth", c="orange")
#
# axs[0].tick_params(axis='both', which='major', labelsize=15)
# axs[1].tick_params(axis='both', which='major', labelsize=15)
# axs[2].tick_params(axis='both', which='major', labelsize=15)
# axs[3].tick_params(axis='both', which='major', labelsize=15)
# plt.xlabel('k1', fontsize=15)
# # plt.title("Damping ratio (single-cycle two-layer system) vs k1")
# axs[0].legend(fontsize=15)
# axs[1].legend(fontsize=15, loc="center right")
# axs[2].legend(fontsize=15)
# axs[3].legend(fontsize=15)
# plt.tight_layout()
# plt.savefig("single_cycle_two_layer.pdf")
# # plt.savefig("single_cycle_two_layer")
# plt.show()
#
# quit()

# -------------------------------------------------------------

# r1.steadyState()
#
# x = []
# BWs = []
# damps = []
# APs = []
# BPs = []
# uCCA = []
# CCA = []
# uCCB = []
# CCB = []
#
# for i in np.arange(1, 1.8, .001):
#     r1.steadyState()
#     x.append(r1.S)
#     r1.S = i
#     APs.append(r1.AP)
#     BPs.append(r1.BP)
#     uCCB.append(r1.getuCC('BP', 'S') / 10)
#     CCB.append(r1.getCC('BP', 'S') / 4)
#     uCCA.append(r1.getuCC('AP', 'S') / 3)
#     CCA.append(r1.getCC('AP', 'S'))
#
#     omega_n = np.sqrt((r1.getEE('J1', 'A') + r1.getEE('J2', 'AP'))*(r1.getEE('J3', 'B') + r1.getEE('J4', 'BP')))
#     zeta = 0.5*(r1.getEE('J1', 'A') + r1.getEE('J2', 'AP') + r1.getEE('J3', 'B') + r1.getEE('J4', 'BP'))/omega_n
#     omega_c = omega_n*np.sqrt(1-2*zeta**2 + np.sqrt((2*zeta**2-1)**2) + 1)
#     damps.append(zeta)
#     BWs.append(omega_c)
#
# fig, axs = plt.subplots(4, figsize=(8, 10))
# # axs[0].plot(x, APs, label="AP", c="green")
# # axs[1].plot(x, BPs, label="BP", c="red")
#
# axs[0].plot(x, APs, label="$AP_{ss}$", c="green")
# axs[1].plot(x, BPs, label="$BP_{ss}$", c="red")
#
# # axs[0].plot(x, uCCA, label="AP CC/3", c="green", linestyle="dashed")
# # axs[0].plot(x, CCA, label="AP scaled CC", c="green", linestyle="dotted")
#
# axs[0].plot(x, uCCA, label=r"$\frac{dAP}{dS}\frac{1}{3}$", c="green", linestyle="dashed")
# axs[0].plot(x, CCA, label=r"$\frac{dAP}{dS}\frac{S}{AP}$", c="green", linestyle="dotted")
#
# # axs[1].plot(x, uCCB, label="BP CC/10", c="red", linestyle="dashed")
# # axs[1].plot(x, CCB, label="BP scaled CC/4", c="red", linestyle="dotted")
#
# axs[1].plot(x, uCCB, label=r"$\frac{dBP}{dS}\frac{1}{10}$", c="red", linestyle="dashed")
# axs[1].plot(x, CCB, label=r"$\frac{dBP}{dS}\frac{S}{BP}\frac{1}{4}$", c="red", linestyle="dotted")
#
# axs[2].plot(x, damps, label="damping ratio", c="blue")
# axs[3].plot(x, BWs, label="bandwidth", c="orange")
#
# axs[0].tick_params(axis='both', which='major', labelsize=15)
# axs[1].tick_params(axis='both', which='major', labelsize=15)
# axs[2].tick_params(axis='both', which='major', labelsize=15)
# axs[3].tick_params(axis='both', which='major', labelsize=15)
# plt.xlabel('Input signal S', fontsize=15)
# # plt.title("Damping ratio (single-cycle two-layer system) vs k1")
# axs[0].legend(fontsize=15)
# axs[1].legend(fontsize=15)
# axs[2].legend(fontsize=15)
# axs[3].legend(fontsize=15)
# plt.tight_layout()
# plt.savefig("single_cycle_two_layer_aligned.pdf")
# # plt.savefig("single_cycle_two_layer_aligned")
# plt.show()
#
# quit()

# =========================================================

x = []
freqs = []
amps = []
phases = []
for i in np.arange(1, 1.5, .001):
    amps.append([])
    phases.append([])
    x.append(i)
    r.S = i
    fr = FreqencyResponse(r)
    results = fr.getSpeciesFrequencyResponse(0.01, 3, 100, 'S', 'BP')
    for each in results:
        amps[-1].append(each[1])
        phases[-1].append(each[2])
    if i == 1:
        for each in results:
            freqs.append(np.log10(each[0]))

xx, yy = np.meshgrid(freqs, x)

amps = np.array(amps)
phases = np.array(phases)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Freq (log10)", fontsize=15, labelpad=10)
ax.set_ylabel("Input signal S", fontsize=15, labelpad=10)

# uncomment for freq
# ax.set_zlabel("Amp (log10)", fontsize=15, labelpad=5)
# ax.plot_surface(xx, yy, amps)
# ax.view_init(elev=30., azim=-45)
# # plt.title("Amplitude vs Frequency over k1", fontsize=15)
# # yticks = [0.4, 0.45, 0.5, 0.55, 0.6]
# # yicklabels = ['0.4', '0.45', '0.5', '0.55', '0.6']
# plt.xticks(fontsize=13)
# # plt.yticks(yticks, yicklabels, fontsize=13)
# plt.yticks(fontsize=13)
# ax.tick_params('z', labelsize=13)
# plt.savefig("two_layer_freq_amp_over_S.pdf")
# plt.show()

# uncomment for phase
ax.set_zlabel("Phase (degrees)", fontsize=15, labelpad=5)
ax.plot_surface(xx, yy, phases)
ax.view_init(elev=30., azim=-45)
# plt.title("Phase vs Frequency over k1", fontsize=15)
# yticks = [0.4, 0.45, 0.5, 0.55, 0.6]
# yicklabels = ['0.4', '0.45', '0.5', '0.55', '0.6']
plt.xticks(fontsize=13)
# plt.yticks(yticks, yicklabels, fontsize=13)
plt.yticks(fontsize=13)
ax.zaxis.set_ticks([-20, -40, -60, -80, -100, -120, -140, -160, -180])
ax.zaxis.set_ticklabels(["-20", "-40", "-60", "-80", "-100", "-120", "-140", "-160", "-180"])
ax.tick_params('z', labelsize=13)
plt.savefig("two_layer_freq_phase_over_S.pdf")
plt.show()

quit()




