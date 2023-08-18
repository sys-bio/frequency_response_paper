
import tellurium as te
import matplotlib.pyplot as plt

r1 = te.loada("""
   # Ensures that AP is the first row of the stoichiometry matrix
   species AP, P
   A -> AP; k1*A/(Km + A)
   AP -> A; k2*AP/(Km + AP)
   k1 = 0.0; k2 = 0.7
   A = 10; Km = 0.5
   S = 1
""")

#Double Cycle model:

r2 = te.loada("""
     Ro -> R1; k1*S*Ro
     R1 -> Ro; k2*R1
     R1 -> R2; k3*S*R1
     R2 -> R1; k4*R2
     Ro = 10
     k1 = 0.72; //0.34
     k2 = 9.4; //0.23
     k3 = 8.73; //0.56
     k4 = 4.233; //0.45
     S = 0
     """)

# r1.steadyState()
#
# x = []
# y = []
# c1 = []
# c2 = []
# z = []
#
# for i in range(200):
#     r1.steadyState()
#     x.append(r1.k1)
#     y.append(r1.AP)
#     c1.append(r1.getuCC('AP', 'k1'))
#     c2.append(r1.getCC('AP', 'k1'))
#     z.append(r1.getReducedJacobian()[0][0])
#     r1.k1 = r1.k1 + 0.01
#
# plt.plot(x, y, label="AP")
# # plt.plot(x, func_values, label="analytical AP")
# # plt.plot(x, z, label="rJac")
# plt.plot(x, c1, label="CC")
# # plt.plot(x, c2, label="sCC")
# plt.xlabel("k1")
# plt.legend()
# plt.tight_layout()
# # plt.savefig("single_cycle_plot.pdf")
# plt.show()
#
# quit()

r2.steadyState()

x = []
y = []
c1 = []
c2 = []
z = []

for i in range(750):
    r2.steadyState()
    x.append(r2.S)
    y.append(r2.R2)
    c1.append(r2.getuCC('R2', 'S'))
    c2.append(r2.getCC('R2', 'S'))
    z.append(r2.getReducedJacobian()[0][0])
    r2.S = r2.S + 0.01

plt.plot(x, y, label="APP")
# plt.plot(x, func_values, label="analytical AP")
# plt.plot(x, z, label="rJac")
plt.plot(x, c1, label="CC")
# plt.plot(x, c2, label="sCC")
plt.xlabel("k1")
plt.legend()
plt.tight_layout()
# plt.savefig("single_cycle_plot.pdf")
plt.show()