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

# k1s = []
# freqs = []
# amps = []
# phases = []
# for i in np.arange(0.14, 1.4, .01):
#     amps.append([])
#     phases.append([])
#     k1s.append(i)
#     r.k1 = i
#     fr = FreqencyResponse(r)
#     results = fr.getSpeciesFrequencyResponse(0.01, 3, 100, 'k1', 'AP')
#     for each in results:
#         amps[-1].append(each[1])
#         phases[-1].append(each[2])
#     if i == 0.14:
#         for each in results:
#             freqs.append(np.log10(each[0]))
#
# xx, yy = np.meshgrid(freqs, k1s)
#
# amps = np.array(amps)
# phases = np.array(phases)
#
# fig = plt.figure(figsize=(6,6))
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel("Freq")
# ax.set_ylabel("k1")

# uncomment for freq
# ax.set_zlabel("Amp")
# ax.plot_surface(xx, yy, amps)
# plt.savefig("freq_amp_over_k1")
# # plt.show()

# uncomment for phase
# ax.set_zlabel("Phase")
# ax.plot_surface(xx, yy, phases)
# # plt.savefig("freq_phase_over_k1")
# plt.show()

# quit()

r.steadyState()
print (r.A, r.AP)


x = []; y = []; c1 =[]; c2 = []; z = []
for i in range (100):
    r.steadyState()
    x.append (r.k1)
    y.append (r.AP)
    c1.append (r.getuCC ('AP', 'k1')/5)
    c2.append (r.getCC ('AP', 'k1'))
    z.append (r.getReducedJacobian()[0][0])
    r.k1 = r.k1 + 0.01

plt.plot (x, y, label="AP")
plt.plot (x, z, label="rJac")
plt.plot (x, c1, label="uCC")
plt.plot (x, c2, label="CC=uCC*k1/AP")
plt.legend()
plt.savefig("single_cycle_plot")
plt.show()
