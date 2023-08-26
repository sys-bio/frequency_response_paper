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
z2 = []

for i in range(800):
    r.steadyState()
    x.append(r.S)
    y.append(r.AP)
    c1.append(r.getuCC('AP', 'S'))
    c2.append(r.getCC('AP', 'S'))
    z.append(r.getReducedJacobian()[0][0])
    # print(z[-1])
    z2.append(r.getNrMatrix())
    # print(z2)
    r.S = r.S + 0.01

# print(r.k1)
plt.plot(x, y, label=r"$AP_{ss}$")
# plt.plot(x, func_values, label="analytical AP")
# plt.plot(x, z, label="rJac")
plt.plot(x, c1, label=r"$\frac{dAP_{ss}}{dS}$")
plt.plot(x, c2, label=r"$\frac{dAP_{ss}}{dS}\frac{S}{AP_{ss}}$")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel("Signal S", fontsize=15)
plt.legend(fontsize=15)
plt.tight_layout()
plt.savefig("single_cycle_plot.pdf")
plt.savefig("single_cycle_plot")
plt.show()

quit()

# =========================================================

# r.conservedMoietyAnalysis = True
# r.steadyState()
#
# x = []
# AP = []
# Jac = []
# c1 = []
# c2 = []
# for i in range(800):
#     r.steadyState()
#     x.append(r.S)
#     AP.append(r.AP)
#     Jac.append(r.getReducedJacobian()[0][0])
#     r.S = r.S + 0.01
#
# fig, ax1 = plt.subplots()
# ax1.set_xlabel('Signal S', fontsize=15)
# ax1.set_ylabel('Jacobian', fontsize=15)
# plt.yticks(fontsize=15)
# plt.xticks(fontsize=15)
# JacPlot = ax1.plot(x, Jac, linewidth=2, label="Jacobian")
#
# # Plot second axis
# ax2 = ax1.twinx()
# ax2.tick_params(labelsize=16)
# APPlot = ax2.plot(x, AP, color='red', linewidth=2, label="AP", linestyle="dotted")
# ax2.set_ylabel('Sigmoid Response', fontsize=15)
#
# lns = JacPlot+APPlot
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc="upper left")
#
# fig.tight_layout()
# plt.savefig('Jacobian.pdf')
# # plt.savefig('Jacobian')
# plt.show()
#
#
# quit()

# =========================================================

# k1s = []
# BWs = []
#
# r.conservedMoietyAnalysis = True
# r.steadyState()
# #
# x = []
# AP = []
# # Jac = []
# # c1 = []
# # c2 = []
# # for i in range(800):
# #     r.steadyState()
# #     x.append(r.S)
# #     AP.append(r.AP)
# #     Jac.append(r.getReducedJacobian()[0][0])
# #     r.S = r.S + 0.01
#
# for i in range(800):
#     AP.append(r.AP)
#     r.steadyState()
#     x.append(r.S)
#     r.S = r.S + 0.01
#     BWs.append(r.getEE('v2', 'AP') + r.getEE('v1', 'A'))
#
# fig, ax1 = plt.subplots()
# BWPlot = ax1.plot(x, BWs, linewidth=2, label="bandwidth")
#
# ax1.set_xlabel('Signal S', fontsize=15)
# ax1.set_ylabel('Bandwidth ($\epsilon^{v2}_{AP} + \epsilon^{v1}_{A}$)', fontsize=15)
#
# # plt.xlabel('k1', fontsize=15)
# # plt.ylabel('Bandwidth ($\epsilon^{v2}_{AP} + \epsilon^{v1}_{A}$)', fontsize=15)
# # plt.title("Bandwidth vs k1", fontsize=15)
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.tight_layout()
#
# # Plot second axis
# ax2 = ax1.twinx()
# ax2.tick_params(labelsize=16)
# APPlot = ax2.plot(x, AP, color='red', linewidth=2, label="AP", linestyle="dotted")
# ax2.set_ylabel('Sigmoid Response', fontsize=15)
#
# lns = BWPlot+APPlot
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc="lower right")
#
# fig.tight_layout()
# plt.savefig("Bandwidth_vs_k1.pdf")
# # plt.savefig("Bandwidth_vs_k1")
# plt.show()
#
# quit()

# =========================================================

# r.conservedMoietyAnalysis = True
# r.steadyState()
#
# x = []
# freqs = []
# amps = []
# phases = []
# for i in range(801):
#     amps.append([])
#     phases.append([])
#     x.append(r.S)
#     fr = FreqencyResponse(r)
#     results = fr.getSpeciesFrequencyResponse(0.001, 3, 100, 'S', 'AP')
#     for each in results:
#         amps[-1].append(each[1])
#         phases[-1].append(each[2])
#     if i == 0:
#         for each in results:
#             freqs.append(np.log10(each[0]))
#     r.S = r.S + 0.01
#
# xx, yy = np.meshgrid(freqs, x)
#
# amps = np.array(amps)
# phases = np.array(phases)
#
# fig = plt.figure(figsize=(6, 6))
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel("Freq (log10)", fontsize=15, labelpad=10)
# ax.set_ylabel("Signal S", fontsize=15, labelpad=10)
#
# # uncomment for freq
# ax.set_zlabel("Amp (log10)", fontsize=15, labelpad=5)
# ax.plot_surface(xx, yy, amps)
# ax.view_init(elev=30., azim=-45)
# # plt.title("Amplitude vs Frequency over k1", fontsize=15)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# ax.tick_params('z', labelsize=13)
# plt.savefig("freq_amp_over_k1.pdf")
# plt.show()
#
# # uncomment for phase
# # ax.set_zlabel("Phase (degrees)", fontsize=15, labelpad=5)
# # ax.plot_surface(xx, yy, phases)
# # ax.view_init(elev=30., azim=-45)
# # # plt.title("Phase vs Frequency over k1", fontsize=15)
# # plt.xticks(fontsize=13)
# # plt.yticks(fontsize=13)
# # ax.tick_params('z', labelsize=13)
# # plt.savefig("freq_phase_over_k1.pdf")
# # plt.show()
#
# quit()

# =========================================================

r.conservedMoietyAnalysis = True
r.steadyState()

x = []
fig, ax1 = plt.subplots()
for i in range(17):
    freq = []
    amp = []
    phase = []

    x.append(r.S)
    fr = FreqencyResponse(r)
    results = fr.getSpeciesFrequencyResponse(0.001, 3, 100, 'S', 'AP')
    for each in results:
        freq.append(np.log10(each[0]))
        amp.append(each[1])
        phase.append(each[2])
    # ax1.plot(freq, amp)
    ax1.plot(freq, phase)
    r.S = r.S + 0.25
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.9, box.height])
ax1.legend(x, bbox_to_anchor=(1, 1.02), title="Signal S")
print(r.S)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
ax1.set_xlabel("Freq (log10)", fontsize=15)

# ax1.set_ylabel("Amp (log10)", fontsize=15)
# plt.savefig('bodeAmpSlices.pdf')
# plt.savefig('bodeAmpSlices')

ax1.set_ylabel("Phase (degrees)", fontsize=15)
plt.savefig('bodePhaseSlices.pdf')
# plt.savefig('bodePhaseSlices')
plt.show()



