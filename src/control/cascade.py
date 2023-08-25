"""Analysis of biochemical cascades."""

import numpy as np
import os
import pandas as pd
import tellurium as te
import matplotlib.pyplot as plt

PLOT_DIR = os.path.join(os.path.dirname(__file__), "plots")
K2_NAME = "k2"
R1_POS = 0  # Position in ratio_vec for ratio 1
DEFAULT_RATIO = 0.01


class Cascade(object):

    def __init__(self, ratio_vec, total):
        """
        Args:
            ratio_vec: array-float (dimension N-1. ratio_vec[n] = r_n)
            total: float (T)
        """
        self.ratio_arr = np.array([float(r) for r in ratio_vec])
        self.total = total
        self.num_ratio_vec = len(self.ratio_arr)
        self.num_species = self.num_ratio_vec + 1
        self.antimony, self.species_names = self.makeAntimony()
        self.roadrunner = te.loada(self.antimony)

    def _calculateProductOfRatios(self, r1_val=None):
        """
        Calculate the product of ratios starting at various positions in the cascade
        and ending at the final species.

        Args:
            k2_val: float (k2 value to use)
        Returns:
            array-float
        """
        if r1_val is None:
            r1_val = self.ratio_arr[R1_POS]
        prods = []
        indices = list(range(self.num_species - 1))
        indices.reverse()
        #
        for pos in indices:
            if pos == R1_POS:
                ratio = r1_val
            else:
                ratio = self.ratio_arr[pos]
            prods.insert(0, ratio)
            if pos < self.num_ratio_vec - 1:
                prods[0] *= prods[1]
        #
        return prods

    def calculateSteadyState(self, r1_val=None):
        """ 
        Calculates the steady state value of each species.

        Args:
            r1_val: float (value of r1 to use)
        Returns
            dict
                key: species name
                value: steady state concentration
        """
        prods = self._calculateProductOfRatios(r1_val=r1_val)
        denominator = 1 + np.sum(prods)
        result_arr = self.total*np.append(prods, [1])/denominator
        result_dct = {self.species_names[n]: result_arr[n] for n in range(self.num_species)}
        return result_dct

    def makeAntimony(self):
        """Creates an antimony model for the cascade.

        Returns
            str (antimony model)
            str (list of species names)
        """
        constants = []
        species_names = []
        antimony = ""
        #
        def addSpecies(name):
            if not name in species_names:
                species_names.append(name)
        #
        def getConstantValue(constant):
            idx = self.getParameterNumber(constant)
            if idx % 2 == 1:
                return 1
            else:
                pos = idx % 2
                return self.ratio_arr[pos]
        #
        for idx in self.iterateOnSpeciesNumber():
            spc1 = self.makeSpeciesName(idx)
            addSpecies(spc1)
            spc2 = "S" + str(idx+1)
            addSpecies(spc2)
            constant_f = self.makeParameterName(2*(idx - 1) + 1)
            constant_b = self.makeParameterName(2*idx)
            constants.extend([constant_f, constant_b])
            forward_reaction = "J" + str(idx) + "f" + ": " + spc1 + " -> " + spc2 + "; " + spc1 + "*" + constant_f + ";\n"
            backward_reaction = "J" + str(idx) + "b" + ": " + spc2 + " -> " + spc1 + "; " + spc2 + "*" + constant_b + ";\n"
            antimony += forward_reaction + ";\n"
            antimony += backward_reaction + ";\n"
        # Create the constants
        for constant in constants:
            idx = self.getParameterNumber(constant)
            if idx % 2 == 1:
                value = 1
            else:
                pos = idx // 2 - 1
                value = self.ratio_arr[pos]
            antimony += constant + " = " + str(value) + ";\n"
        # Initialize species
        is_first = True
        for name in species_names:
            if is_first:
                antimony += name + " = " + str(self.total) + ";\n"
                is_first = False
            else:
                antimony += name + " = 0;\n"
        #
        return antimony, species_names
    
    def simulateSteadyState(self, parameter_dct=None):
        """
        Returns the steady state concentrations of the species from simulation.

        Returns
            dict (keys are species names, values are concentrations)
        """
        self.reset()
        if parameter_dct is not None:
            self.set(parameter_dct)
        self.roadrunner.steadyState()
        result_dct = {}
        for name in self.species_names:
            #result_dct[name] = data[column][-1]
            result_dct[name] = self.roadrunner[name]
        return result_dct
    
    def simulateFinalSpeciesSteadyState(self):
        """
        Returns the steady state concentrations of the final species
        in the cascade as obtained by simulation.

        Returns
            float
        """
        result_dct = self.simulateSteadyState()
        last_name = self.species_names[-1]
        return result_dct[last_name]

    @staticmethod 
    def makeParameterName(num):
        return "k" + str(num)
    
    @staticmethod 
    def makeRatioName(num):
        return "r" + str(num)
    
    @staticmethod 
    def makeSpeciesName(num):
        return "S" + str(num)

    @classmethod
    def makeControlCoefficient(cls, num):
        pname = cls.makeParameterName(2*num-1)
        return r'$\mathcal{C}^{S_N}_{%s}$' % pname
    
    @staticmethod
    def getParameterNumber(name):
        return int(name[1:])
    
    def set(self, parameter_dct):
        """
        Sets the parameters of the cascade.

        Args:
            parameter_dct: dict
                key: parameter name or number
                value: parameter value
        """
        for name, value in parameter_dct.items():
            if isinstance(name, int):
                name = self.makeParameterName(name)
            self.roadrunner[name] = value

    def reset(self):
        """
        Resets the cascade to its initial state.
        """
        self.roadrunner.reset()

    def simulateControlCoefficient(self, species_idx=1, r_vals=None, parameter_dct=None):
        """
        Gets control coefficient for SN relative to the even numbered kinetic constants.
        This will be the ratio r1 = k2/k1, etc. if the odd number constants are all 1.

        Args:
            species_idx: index of the species for which ratios are calculated
            r_vals: values of the ratio between the left-incoming arc to the species and the right out-going arc
            parameter_dct: values to set parameters to
        Returns:
            pd.DataFrame
                index: values of ratios
                columns: Species names
                values: control coefficient
        """
        k_name = self.makeParameterName(2*species_idx)
        if r_vals is None:
            r_vals = [self.roadrunner[k_name]]
        last_species_name = self.species_names[-1]
        result_dct = {self.makeRatioName(n): [] for n in self.iterateOnSpeciesNumber()}
        if parameter_dct is not None:
            self.set(parameter_dct)
        for val in r_vals:
            self.reset()
            dct = {k_name: float(val)}
            self.set(dct)
            self.roadrunner.steadyState()
            for n in self.iterateOnSpeciesNumber():
                parameter_name = self.makeParameterName(2*n)
                ratio_name = self.makeRatioName(n)
                cc = self.roadrunner.getCC(last_species_name, parameter_name)
                result_dct[ratio_name].append(cc)
        df = pd.DataFrame(result_dct, index=r_vals)
        return df
    
    def plotSimulatedControlCoefficient(self, species_idx=1, r_vals=None, ratio_dct=None,
                                        filename="control_coefficient.pdf", is_plot=True, is_forward_k=True,
                                        default_ratio=DEFAULT_RATIO, ax=None, **kwargs):
        """
        Plots the simulated control coefficient for S_N relative to k for the species_idx.

        Args:
            species_idx: index of the species for which ratios are calculated
            r_vals: values of the ratio of kinetic constants for a species
            ratio_dct (dict):
                key: ratio index
                value: value of the ratio
            default_ratio: value of a ratio if unspecified
            filename (str, optional): _description_. Defaults to "control_coefficient.pdf"
            is_forward_k (bool, optional): if True, calculates the control coefficient for the forward kinetic constant
        Returns:
            matplotlib.axes._subplots.AxesSubplot
        """
        # Construct the parameter dictionary
        if ratio_dct is None:
            ratio_dct = {}
        parameter_dct = {}
        for idx in self.iterateOnSpeciesNumber():
            parameter_dct[2*idx-1] = 1
            if idx in ratio_dct:
                parameter_dct[2*idx] = ratio_dct[idx]
            else:
                parameter_dct[2*idx] = self.ratio_arr[idx-1]
        cc_df = self.simulateControlCoefficient(species_idx=species_idx, r_vals=r_vals,
                                                   parameter_dct=parameter_dct)
        if is_forward_k:
            cc_df = -cc_df
        # Plot
        if ax is None:
             _, ax = plt.subplots(1)
        cc_df.plot(ax=ax)
        legends = [self.makeControlCoefficient(n) for n in self.iterateOnSpeciesNumber()]
        ax.legend(legends)
        titles = [r'$r_%d=%2.2f$' % (n, self.ratio_arr[n-1]) for n in self.iterateOnSpeciesNumber()
                 if n != species_idx]
        title = ", ".join(titles)
        ax.set_title(title)
        x_label = r'$r_%d$' % species_idx
        ax.set_xlabel(x_label)
        ax.set_ylabel("control coefficient")
        if is_plot:
            self.writePlot(filename, **kwargs)
        return ax

    def calculateControlCoefficient(self, r1_vals=None, parameter_dct=None):
        """
        Calculates the S_N control coefficient w.r.t. k2.

        Args:
            r1_vals: values of r1 to change
            kinetic_dct (dict):
                key: kinetic constant name
                value: kinetic constant values
        Returns:
            pd.Series
                index: k2 values
                value: control coefficient
        """
        if r1_vals is None:
            r1_vals = [self.ratio_arr[0]]
        cc_vals = []
        for r1_val in r1_vals:
            prods = self._calculateProductOfRatios(r1_val=r1_val)
            dSNdrm = -self.total*prods[0]/(r1_val*(1 + np.sum(prods))**2)
            ss_dct = self.calculateSteadyState(r1_val=r1_val)
            last_name = self.species_names[-1]
            cc_vals.append(dSNdrm*r1_val/ss_dct[last_name])
        ser = pd.Series(cc_vals, index=r1_vals)
        return ser

    def plotConcentrations(self, k2_vals, filename="concentration.pdf", **kwargs):
        """
        Plots the control coefficient for S_N relative to k_1 and optionally values of a second
        kinetic constant.

        Args:
            k2_vals: values of k2 to change
            filename (str, optional): _description_. Defaults to "control_coefficient.pdf".
        """
        def calculateSN():
            result_dct = {n: [] for n in self.species_names}
            for val in k2_vals:
                parameter_dct = {2: val}
                sim_dct = self.simulateSteadyState(parameter_dct=parameter_dct)
                for name, value in sim_dct.items():
                    result_dct[name].append(value)
            df = pd.DataFrame(result_dct)
            df.index = k2_vals
            return df

        #
        _, ax = plt.subplots(1)
        df = calculateSN()
        df.plot.bar(ax=ax, stacked=True)
        ax.set_xlabel(K2_NAME)
        ax.set_ylabel("concentration")
        ax.set_title("k4=%2.2f" % self.roadrunner.k4)
        self.writePlot(filename, **kwargs)

    def writePlot(self, filename, **kwargs):
        """
        Writes the current plot to a file.

        Args
            filename: str 
        """
        path = os.path.join(PLOT_DIR, filename)
        plt.savefig(path, **kwargs)

    def iterateOnSpeciesNumber(self):
        """
        Iterates on the species number, from 1 to N-1.

        yields: int
        """
        for idx in range(len(self.ratio_arr)):
            yield idx + 1