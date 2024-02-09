
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
    z2.append(r.getNrMatrix())
    r.S = r.S + 0.01

plt.plot(x, y, label=r"$AP_{ss}$")
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
