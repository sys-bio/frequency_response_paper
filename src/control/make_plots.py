"""Constructs plots for the paper."""

from control.cascade import Cascade

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plotSingleControlCoefficientComparisons(species_idx, ax=None):
    size = 4
    rvec = np.repeat(1, size)
    total = 100
    cascade = Cascade(rvec, total)
    r_vals = [0.01, 0.05, 0.1, 0.5, 1, 5, 10, 15, 20, 50, 100, 200, 300, 400, 500]
    cascade.plotSimulatedControlCoefficient(species_idx=species_idx, r_vals=r_vals, ax=ax)
    ax.set_xscale('log')
    cascade.writePlot("plotControlCoefficientComparisons.pdf")

def plotMultipleControlCoefficientComparisons():
    nrow = 2
    ncol = 2
    _, axes = plt.subplots(nrow, ncol, figsize=(10, 10))
    for irow in range(nrow):
        for icol in range(ncol):
            species_idx = irow * ncol + icol + 1
            ax = axes[irow][icol]
            plotSingleControlCoefficientComparisons(species_idx, ax=ax)


if __name__ == "__main__":
    plotMultipleControlCoefficientComparisons()
    plt.show()