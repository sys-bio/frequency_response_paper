
import random
import matplotlib.pyplot as plt
import numpy as np
import math


def single(sm1, sm2, se12, se21):
    return sm2/(se12 * sm1 + se21 * sm2)


def double(m1, m2, m3, e32, e22, e11, e43, e33):
    return (m1 * (e32 + e22) + m2 * e11)/(e22 * e43 * m1 + e11 * e43 * m2 + e11 * e33 * m3)


singles = []
doubles = []

for i in range(25000000):
    if i % 100000 == 0:
        print(i)
    SM1 = random.uniform(0.1, 1.0)
    SM2 = random.uniform(0.1, 1.0)
    SE12 = random.uniform(0.1, 1.0)
    SE21 = random.uniform(0.1, 1.0)

    SM1t = SM1/(SM1 + SM2)
    SM2t = SM2/(SM1 + SM2)

    M1 = random.uniform(0.1, 1.0)
    M2 = random.uniform(0.1, 1.0)
    M3 = random.uniform(0.1, 1.0)
    E32 = random.uniform(0.1, 1.0)
    E22 = random.uniform(0.1, 1.0)
    E11 = random.uniform(0.1, 1.0)
    E43 = random.uniform(0.1, 1.0)
    E33 = random.uniform(0.1, 1.0)

    M1t = M1/(M1 + M2 + M3)
    M2t = M2/(M1 + M2 + M3)
    M3t = M3/(M1 + M2 + M3)

    singles.append(single(SM1t, SM2t, SE12, SE21))
    doubles.append(double(M1t, M2t, M3t, E32, E22, E11, E43, E33))

plt.xlim(xmin=0, xmax=10)
single_counts = plt.hist(singles, alpha=0.5, bins=np.arange(0, math.ceil(max(doubles)) + 1, .01), label='single cycle')
double_counts = plt.hist(doubles, alpha=0.5, bins=np.arange(0, math.ceil(max(doubles)) + 1, .01), label='double cycle')

max_s = max(single_counts[0])
max_si = np.where(single_counts[0] == max_s)[0]

max_d = max(double_counts[0])
max_di = np.where(double_counts[0] == max_d)[0]

s_avg = np.average(singles)
d_avg = np.average(doubles)
s_med = np.median(singles)
d_med = np.median(doubles)

plt.legend(loc='upper right')
plt.xlabel('Sensitivity')
# plt.title('Single vs Double cycle sensitivities')
plt.show()
# plt.savefig('compareSensitivitySingleDouble.pdf')
