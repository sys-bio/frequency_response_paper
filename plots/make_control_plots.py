"""Constructs plots for the paper."""

from control.cascade import Cascade
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

PLOT_DIR = os.path.dirname(__file__)

def plotSingleControlCoefficientComparisons(species_idx, ax=None):
    size = 4
    rvec = np.repeat(1, size)
    total = 100
    cascade = Cascade(rvec, total)
    import pdb; pdb.set_trace()
    r_vals = np.array([])
    for bound in [1e-3, 1e-2, 0.1, 1, 10, 100]:
        r_vals = np.append(r_vals, np.linspace(bound, bound * 10, 20))
    cascade.plotSimulatedControlCoefficient(species_idx=species_idx, r_vals=r_vals, ax=ax)
    ax.set_xscale('log')
    ax.set_xlabel(r'$log r_{%d}$' % species_idx)
    writePlot("control_coefficient_comparisons.pdf")

def plotMultipleControlCoefficientComparisons():
    nrow = 2
    ncol = 2
    _, axes = plt.subplots(nrow, ncol, figsize=(10, 10))
    for irow in range(nrow):
        for icol in range(ncol):
            species_idx = irow * ncol + icol + 1
            ax = axes[irow][icol]
            plotSingleControlCoefficientComparisons(species_idx, ax=ax)

def writePlot(filename):
    """
    Writes the current plot to a file.

    Args
        filename: str 
    """
    path = os.path.join(PLOT_DIR, filename)
    plt.savefig(path)


if __name__ == "__main__":
    plotMultipleControlCoefficientComparisons()
    plt.show()