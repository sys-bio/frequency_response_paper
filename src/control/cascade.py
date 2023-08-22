"""Analysis of biochemical cascades."""

import numpy as np
import os
import pandas as pd
import tellurium as te
import matplotlib.pyplot as plt

PLOT_DIR = os.path.join(os.path.dirname(__file__), "plots")
K2_NAME = "k2"
R1_POS = 0  # Position in ratio_vec for ratio 1


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
        for idx in range(1, self.num_species):
            spc1 = "S" + str(idx)
            addSpecies(spc1)
            spc2 = "S" + str(idx+1)
            addSpecies(spc2)
            constant_f = self.makeParameterName(str(2*(idx - 1) + 1))
            constant_b = self.makeParameterName(str(2*idx))
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

    def simulateControlCoefficient(self, k2_vals=None, parameter_dct=None):
        """
        Gets control coefficient for S_N relative to k_1 from tellurium.

        Args:
            k2_vals: values of k2 to change
            parameter_dct: values to set parameters to
        Returns:
            pd.Series
                index: k2 values
                values: control coefficient
        """
        if k2_vals is None:
            k2_vals = [self.roadrunner[K2_NAME]]
        if parameter_dct is None:
            parameter_dct = {}
        last_species_name = self.species_names[-1]
        results = []
        dct = dict(parameter_dct)
        for val in k2_vals:
            self.reset()
            dct[K2_NAME] = float(val)
            self.set(dct)
            self.roadrunner.steadyState()
            results.append(self.roadrunner.getCC(last_species_name, K2_NAME))
        ser = pd.Series(results, index=k2_vals)
        return ser 
    
    def plotSimulatedControlCoefficient(self, k2_vals, parameter_dct=None, filename="control_coefficient.pdf", **kwargs):
        """
        Plots the simulated control coefficient for S_N relative to k_2 and optionally values of a second
        kinetic constant.

        Args:
            k2_vas: values of k2
            kinetic_dct (dict):
                key: kinetic constant name
                value: kinetic constant values
            filename (str, optional): _description_. Defaults to "control_coefficient.pdf".
        Returns:
            pd.Series
                index: k2 values
                value: control coefficient
        """
        cc_vals = self.simulateControlCoefficient(k2_vals, parameter_dct=parameter_dct).values
        # Plot
        _, ax = plt.subplots(1)
        ax.plot(k2_vals, cc_vals)
        ax.set_xlabel(K2_NAME)
        ax.set_ylabel("control coefficient")
        self.writePlot(filename, **kwargs)

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