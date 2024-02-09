
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

x = []
AP = []
Jac = []
c1 = []
c2 = []
for i in range(800):
    r.steadyState()
    x.append(r.S)
    AP.append(r.AP)
    Jac.append(r.getReducedJacobian()[0][0])
    r.S = r.S + 0.01

fig, ax1 = plt.subplots()
ax1.set_xlabel('Signal S', fontsize=15)
ax1.set_ylabel('Jacobian', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
JacPlot = ax1.plot(x, Jac, linewidth=2, label="Jacobian")

# Plot second axis
ax2 = ax1.twinx()
ax2.tick_params(labelsize=16)
APPlot = ax2.plot(x, AP, color='red', linewidth=2, label="AP")
ax2.set_ylabel('Sigmoid Response', fontsize=15)

lns = JacPlot+APPlot
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc="upper left")

fig.tight_layout()
plt.savefig('Jacobian.pdf')
plt.show()
