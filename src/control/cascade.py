"""Analysis of biochemical cascades."""

import numpy as np
import os
import tellurium as te
import matplotlib.pyplot as plt

PLOT_DIR = os.path.join(os.path.dirname(__file__), "plots")


class Cascade(object):

    def __init__(self, ratio_vec, total):
        """
        Args:
            ratio_vec: array-float (dimension N-1. ratio_vec[n] = r_n)
            total: float (T)
        """
        self.ratio_vec = ratio_vec
        self.total = total
        self.num_ratio_vec = len(self.ratio_vec)
        self.num_species = self.num_ratio_vec + 1
        self.antimony, self.species_names = self.makeAntimony()
        self.roadrunner = te.loada(self.antimony)

    def calculateSteadyState(self):
        """ 
        Calculates the steady state value of each species.

        Args:
            ratio_vec: array-float (dimension N-1. ratio_vec[n] = r_n)
            total: float (T)
        Returns
            dict
                key: species name
                value: steady state concentration
        """
        prods = []
        indices = list(range(self.num_species - 1))
        indices.reverse()
        # Calculate the products for each position in the cascade
        for pos in indices:
            prods.insert(0, self.ratio_vec[pos])
            if pos < self.num_ratio_vec - 1:
                prods[0] *= prods[1]
        # 
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
                return self.ratio_vec[pos]
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
                value = self.ratio_vec[pos]
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
    
    def calculateSteadyState(self):
        """
        Returns the steady state concentrations of the species.

        Returns
            dict (keys are species names, values are concentrations)
        """
        self.roadrunner.reset()
        self.roadrunner.steadyState()
        result_dct = {}
        for name in self.species_names:
            #result_dct[name] = data[column][-1]
            result_dct[name] = self.roadrunner[name]
        return result_dct
    
    def simulateSteadyState(self):
        """
        Returns the steady state concentrations of the species from simulation.

        Returns
            dict (keys are species names, values are concentrations)
        """
        self.roadrunner.reset()
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

    def simulateControlCoefficient(self):
        """
        Gets control coefficient for S_N relative to k_1 from tellurium.

        Args:
            ratio_vec: array-float
            total: float
            ratio_idx: int (index of the ratio being changed)
            delta: float (amount by which the ratio is changed)
        """
        self.roadrunner.reset()
        self.roadrunner.steadyState()
        name = self.species_names[-1]
        return self.roadrunner.getCC(name, self.makeParameterName(1))
    
    def writePlot(self, filename, **kwargs):
        """
        Writes the current plot to a file.

        Args
            filename: str 
        """
        path = os.path.join(PLOT_DIR, filename)
        plt.savefig(path, **kwargs)