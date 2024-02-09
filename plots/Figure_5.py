
import tellurium as te
from freqResponse import *

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

k1s = []
BWs = []
x = []
AP = []

for i in range(800):
    AP.append(r.AP)
    r.steadyState()
    x.append(r.S)
    r.S = r.S + 0.01
    BWs.append(r.getEE('v2', 'AP') + r.getEE('v1', 'A'))

fig, ax1 = plt.subplots()
BWPlot = ax1.plot(x, BWs, linewidth=2, label="bandwidth")

ax1.set_xlabel('Signal S', fontsize=15)
ax1.set_ylabel('Bandwidth ($\epsilon^{v2}_{AP} + \epsilon^{v1}_{A}$)', fontsize=15)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()

# Plot second axis
ax2 = ax1.twinx()
ax2.tick_params(labelsize=16)
APPlot = ax2.plot(x, AP, color='red', linewidth=2, label="AP")
ax2.set_ylabel('Sigmoid Response', fontsize=15)

lns = BWPlot+APPlot
labs = [k.get_label() for k in lns]
ax1.legend(lns, labs, loc="lower right")

fig.tight_layout()
plt.savefig("Bandwidth_vs_S.pdf")
plt.savefig("Bandwidth_vs_S")
plt.show()
