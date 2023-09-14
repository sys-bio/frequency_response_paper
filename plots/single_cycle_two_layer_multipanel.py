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
from matplotlib.ticker import EngFormatter, StrMethodFormatter
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

# r.conservedMoietyAnalysis = True
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
#     r.S = i
#     r.steadyState()
#     x.append(r.S)
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
# axs[0].plot(x, APs, label="$AP$", c="green")
# axs[1].plot(x, BPs, label="$BP$", c="red")
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
# plt.xlabel('Signal S', fontsize=15)
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

# r.conservedMoietyAnalysis = True
# r1.steadyState()
#
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
#     r1.S = i
#     r1.steadyState()
#     x.append(r1.S)
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
# plt.xlabel('Signal S', fontsize=15)
# # plt.title("Damping ratio (single-cycle two-layer system) vs k1")
# axs[0].legend(fontsize=15)
# axs[1].legend(fontsize=15)
# axs[2].legend(fontsize=15)
# axs[3].legend(fontsize=15)
# plt.tight_layout()
# plt.savefig("single_cycle_two_layer_aligned.pdf")
# plt.savefig("single_cycle_two_layer_aligned")
# plt.show()
#
# quit()

# -------------------------------------------------------------

# r.conservedMoietyAnalysis = True
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
# EE1A = []
# EE2AP = []
# EE3B = []
# EE4BP = []
#
# for i in np.arange(1, 2, .001):
#     r.S = i
#     r.steadyState()
#     x.append(r.S)
#     APs.append(r.AP)
#     BPs.append(r.BP)
#     uCCB.append(r.getuCC('BP', 'S') / 10)
#     CCB.append(r.getCC('BP', 'S') / 2)
#     uCCA.append(r.getuCC('AP', 'S') / 2)
#     CCA.append(r.getCC('AP', 'S'))
#     EE1A.append(r.getuEE('J1', 'A'))
#     EE2AP.append(r.getuEE('J2', 'AP'))
#     EE3B.append(r.getuEE('J3', 'B'))
#     EE4BP.append(r.getuEE('J4', 'BP'))
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
# # axs[0].plot(x, APs, label="$AP$", c="green")
# # axs[1].plot(x, BPs, label="$BP$", c="red")
#
# # axs[0].plot(k1s, uCCA, label="AP CC/10", c="green", linestyle="dashed")
# # axs[0].plot(k1s, CCA, label="AP scaled CC", c="green", linestyle="dotted")
#
# # axs[0].plot(x, uCCA, label=r"$\frac{dAP}{dS}\frac{1}{2}$", c="green", linestyle="dashed")
# # axs[0].plot(x, CCA, label=r"$\frac{dAP}{dS}\frac{S}{AP}$", c="green", linestyle="dotted")
#
# # axs[1].plot(k1s, uCCB, label="BP CC/20", c="red", linestyle="dashed")
# # axs[1].plot(k1s, CCB, label="BP scaled CC/4", c="red", linestyle="dotted")
#
# # axs[1].plot(x, uCCB, label=r"$\frac{dBP}{dS}\frac{1}{10}$", c="red", linestyle="dashed")
# # axs[1].plot(x, CCB, label=r"$\frac{dBP}{dS}\frac{S}{BP}\frac{1}{2}$", c="red", linestyle="dotted")
#
# # axs[2].plot(x, damps, label="damping ratio", c="blue")
# # axs[3].plot(x, BWs, label="bandwidth", c="orange")
#
# axs[0].plot(x, EE1A, label="$\epsilon^{v1}_{A}$")
# axs[1].plot(x, EE2AP, label="$\epsilon^{v2}_{AP}$")
# axs[2].plot(x, EE3B, label="$\epsilon^{v3}_{B}$")
# axs[3].plot(x, EE4BP, label="$\epsilon^{v4}_{BP}$")
#
# axs[0].tick_params(axis='both', which='major', labelsize=15)
# axs[1].tick_params(axis='both', which='major', labelsize=15)
# axs[2].tick_params(axis='both', which='major', labelsize=15)
# axs[3].tick_params(axis='both', which='major', labelsize=15)
# # axs[4].tick_params(axis='both', which='major', labelsize=15)
# # axs[5].tick_params(axis='both', which='major', labelsize=15)
# # axs[6].tick_params(axis='both', which='major', labelsize=15)
# # axs[7].tick_params(axis='both', which='major', labelsize=15)
# plt.xlabel('Signal S', fontsize=15)
# # plt.title("Damping ratio (single-cycle two-layer system) vs k1")
# axs[0].legend(fontsize=15)
# axs[1].legend(fontsize=15)
# axs[2].legend(fontsize=15)
# axs[3].legend(fontsize=15)
# # axs[4].legend(fontsize=15)
# # axs[5].legend(fontsize=15)
# # axs[6].legend(fontsize=15)
# # axs[7].legend(fontsize=15)
# plt.tight_layout()
# plt.savefig("A1.pdf")
# plt.savefig("A1")
# plt.show()
#
# quit()

# -------------------------------------------------------------

r1.conservedMoietyAnalysis = True
r1.steadyState()

x = []
BWs = []
damps = []
APs = []
BPs = []
uCCA = []
CCA = []
uCCB = []
CCB = []
EE1A = []
EE2AP = []
EE3B = []
EE4BP = []

for i in np.arange(1, 2, .001):
    r1.S = i
    r1.steadyState()
    x.append(r1.S)
    APs.append(r1.AP)
    BPs.append(r1.BP)
    uCCB.append(r1.getuCC('BP', 'S') / 10)
    CCB.append(r1.getCC('BP', 'S') / 2)
    uCCA.append(r1.getuCC('AP', 'S') / 2)
    CCA.append(r1.getCC('AP', 'S'))
    EE1A.append(r1.getuEE('J1', 'A'))
    EE2AP.append(r1.getuEE('J2', 'AP'))
    EE3B.append(r1.getuEE('J3', 'B'))
    EE4BP.append(r1.getuEE('J4', 'BP'))

    omega_n = np.sqrt((r1.getEE('J1', 'A') + r1.getEE('J2', 'AP'))*(r1.getEE('J3', 'B') + r1.getEE('J4', 'BP')))
    zeta = 0.5*(r1.getEE('J1', 'A') + r1.getEE('J2', 'AP') + r1.getEE('J3', 'B') + r1.getEE('J4', 'BP'))/omega_n
    omega_c = omega_n*np.sqrt(1-2*zeta**2 + np.sqrt((2*zeta**2-1)**2) + 1)
    damps.append(zeta)
    BWs.append(omega_c)

fig, axs = plt.subplots(4, figsize=(8, 10))
# axs[0].plot(x, APs, label="AP", c="green")
# axs[1].plot(x, BPs, label="BP", c="red")

# axs[0].plot(x, APs, label="$AP$", c="green")
# axs[1].plot(x, BPs, label="$BP$", c="red")

# axs[0].plot(k1s, uCCA, label="AP CC/10", c="green", linestyle="dashed")
# axs[0].plot(k1s, CCA, label="AP scaled CC", c="green", linestyle="dotted")

# axs[0].plot(x, uCCA, label=r"$\frac{dAP}{dS}\frac{1}{2}$", c="green", linestyle="dashed")
# axs[0].plot(x, CCA, label=r"$\frac{dAP}{dS}\frac{S}{AP}$", c="green", linestyle="dotted")

# axs[1].plot(k1s, uCCB, label="BP CC/20", c="red", linestyle="dashed")
# axs[1].plot(k1s, CCB, label="BP scaled CC/4", c="red", linestyle="dotted")

# axs[1].plot(x, uCCB, label=r"$\frac{dBP}{dS}\frac{1}{10}$", c="red", linestyle="dashed")
# axs[1].plot(x, CCB, label=r"$\frac{dBP}{dS}\frac{S}{BP}\frac{1}{2}$", c="red", linestyle="dotted")

# axs[2].plot(x, damps, label="damping ratio", c="blue")
# axs[3].plot(x, BWs, label="bandwidth", c="orange")

axs[0].plot(x, EE1A, label="EE1A")
axs[1].plot(x, EE2AP, label="EE2AP")
axs[2].plot(x, EE3B, label="EE3B")
axs[3].plot(x, EE4BP, label="EE4BP")

axs[0].tick_params(axis='both', which='major', labelsize=15)
axs[1].tick_params(axis='both', which='major', labelsize=15)
axs[2].tick_params(axis='both', which='major', labelsize=15)
axs[3].tick_params(axis='both', which='major', labelsize=15)
# axs[4].tick_params(axis='both', which='major', labelsize=15)
# axs[5].tick_params(axis='both', which='major', labelsize=15)
# axs[6].tick_params(axis='both', which='major', labelsize=15)
# axs[7].tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('Signal S', fontsize=15)
# plt.title("Damping ratio (single-cycle two-layer system) vs k1")
axs[0].legend(fontsize=15)
axs[1].legend(fontsize=15, loc="center right")
axs[2].legend(fontsize=15)
axs[3].legend(fontsize=15)
# axs[4].legend(fontsize=15)
# axs[5].legend(fontsize=15)
# axs[6].legend(fontsize=15)
# axs[7].legend(fontsize=15)
plt.tight_layout()
plt.savefig("A2.pdf")
plt.savefig("A2")
plt.show()

quit()

# --------------------------------------------------

r.conservedMoietyAnalysis = True
r.steadyState()

x = []
BWs = []
damps = []
APs = []
BPs = []
uCCA = []
CCA = []
uCCB = []
CCB = []
EE1A = []
EE2AP = []
EE3B = []
EE4BP = []
EAadds = []
EBadds = []

for i in np.arange(1, 2, .001):
    r.S = i
    r.steadyState()
    x.append(r.S)
    APs.append(r.AP)
    BPs.append(r.BP)
    uCCB.append(r.getuCC('BP', 'S') / 10)
    CCB.append(r.getCC('BP', 'S') / 2)
    uCCA.append(r.getuCC('AP', 'S') / 2)
    CCA.append(r.getCC('AP', 'S'))
    EE1A.append(r.getuEE('J1', 'A'))
    EE2AP.append(r.getuEE('J2', 'AP'))
    EE3B.append(r.getuEE('J3', 'B'))
    EE4BP.append(r.getuEE('J4', 'BP'))

    omega_n = np.sqrt((r.getEE('J1', 'A') + r.getEE('J2', 'AP'))*(r.getEE('J3', 'B') + r.getEE('J4', 'BP')))
    EAadds.append(r.getEE('J1', 'A') + r.getEE('J2', 'AP'))
    EBadds.append(r.getEE('J3', 'B') + r.getEE('J4', 'BP'))
    zeta = 0.5*(r.getEE('J1', 'A') + r.getEE('J2', 'AP') + r.getEE('J3', 'B') + r.getEE('J4', 'BP'))/omega_n
    omega_c = omega_n*np.sqrt(1-2*zeta**2 + np.sqrt((2*zeta**2-1)**2) + 1)
    damps.append(zeta)
    BWs.append(omega_c)
# print(min(damps))
# for i, each in enumerate(damps):
    # print(x[i], APs[i], uCCA[i], BPs[i], uCCB[i], damps[i])
for i, each in enumerate(EAadds):
    print(x[i], BWs[i], damps[i], EAadds[i], EBadds[i])
fig, axs = plt.subplots(4, figsize=(8, 10))

# axs[0].plot(x, APs, label="AP", c="green")
# axs[1].plot(x, BPs, label="BP", c="red")

axs[0].plot(x, APs, label="$AP$", c="green")
axs[1].plot(x, BPs, label="$BP$", c="red")

# axs[0].plot(k1s, uCCA, label="AP CC/10", c="green", linestyle="dashed")
# axs[0].plot(k1s, CCA, label="AP scaled CC", c="green", linestyle="dotted")

axs[0].plot(x, uCCA, label=r"$\frac{dAP}{dS}\frac{1}{2}$", c="green", linestyle="dashed")
axs[0].plot(x, CCA, label=r"$\frac{dAP}{dS}\frac{S}{AP}$", c="green", linestyle="dotted")

# axs[1].plot(k1s, uCCB, label="BP CC/20", c="red", linestyle="dashed")
# axs[1].plot(k1s, CCB, label="BP scaled CC/4", c="red", linestyle="dotted")

axs[1].plot(x, uCCB, label=r"$\frac{dBP}{dS}\frac{1}{10}$", c="red", linestyle="dashed")
axs[1].plot(x, CCB, label=r"$\frac{dBP}{dS}\frac{S}{BP}\frac{1}{2}$", c="red", linestyle="dotted")

axs[2].plot(x, damps, label="damping ratio", c="blue")
axs[3].plot(x, BWs, label="bandwidth", c="orange")

# axs[4].plot(x, EE1A, label="EE1A")
# axs[5].plot(x, EE2AP, label="EE2AP")
# axs[6].plot(x, EE3B, label="EE3B")
# axs[7].plot(x, EE4BP, label="EE4BP")

axs[0].tick_params(axis='both', which='major', labelsize=15)
axs[1].tick_params(axis='both', which='major', labelsize=15)
axs[2].tick_params(axis='both', which='major', labelsize=15)
axs[3].tick_params(axis='both', which='major', labelsize=15)
# axs[4].tick_params(axis='both', which='major', labelsize=15)
# axs[5].tick_params(axis='both', which='major', labelsize=15)
# axs[6].tick_params(axis='both', which='major', labelsize=15)
# axs[7].tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('Signal S', fontsize=15)
# plt.title("Damping ratio (single-cycle two-layer system) vs k1")
axs[0].legend(fontsize=15)
axs[1].legend(fontsize=15, loc="center right")
axs[2].legend(fontsize=15)
axs[3].legend(fontsize=15)
# axs[4].legend(fontsize=15)
# axs[5].legend(fontsize=15)
# axs[6].legend(fontsize=15)
# axs[7].legend(fontsize=15)
plt.tight_layout()
# plt.savefig("single_cycle_two_layer.pdf")
# plt.savefig("single_cycle_two_layer")
# plt.show()

quit()
