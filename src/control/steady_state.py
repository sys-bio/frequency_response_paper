#FXIME: Strange bug
import numpy as np
def calculateSteadyState(rvec, total):
    """ 
    Calculates the steady state value of each species.

    Args:
        rvec: array-float (dimension N-1. rvec[n] = r_n)
        total: float (T)
    Returns
        svec: array-float (dimension N)
    """
    num_r = len(rvec)
    num_species = num_r + 1 
    prods = []
    indices = list(range(num_r))
    # Calculate the products for each position in the cascade
    for idx in indices:
        pos = num_r - idx - 1
        prods.insert(0, rvec[pos])
        if pos < num_r - 1:
            prods[0] *= prods[1]
    # 
    denominator = 1 + np.sum(prods)
    result_arr = total*np.append(prods, [1])/denominator
    return result_arr

# TESTS
result = calculateSteadyState(np.array([17.0, 0.45, 1/3.]), 10) 
print(result)
