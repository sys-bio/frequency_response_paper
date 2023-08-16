"""Calculates steady state concentrations for an N cycle cascade."""

import numpy as np
import tellurium as te


class SteadyState(object):

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
            svec: array-float (dimension N)
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
        return result_arr

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
            idx1 = int(constant[2])
            idx2 = int(constant[3])
            if idx1 < idx2:
                return 1
            else:
                return self.ratio_vec[idx2]
        #
        for idx in range(self.num_species-1):
            spc1 = "S" + str(idx)
            addSpecies(spc1)
            spc2 = "S" + str(idx+1)
            addSpecies(spc2)
            constant_f = "k_" + str(idx) + str(idx+1)
            constant_b = "k_" + str(idx+1) + str(idx)
            constants.extend([constant_f, constant_b])
            forward_reaction = "J" + str(idx) + "f" + ": " + spc1 + " -> " + spc2 + "; " + spc1 + "*" + constant_f + ";\n"
            backward_reaction = "J" + str(idx) + "b" + ": " + spc2 + " -> " + spc1 + "; " + spc2 + "*" + constant_b + ";\n"
            antimony += forward_reaction + ";\n"
            antimony += backward_reaction + ";\n"
        # Create the constants
        for constant in constants:
            antimony += "const " + constant + " = " + str(getConstantValue(constant)) + ";\n"
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
    
    def calculateSimulatedSteadyState(self):
        """
        Returns the steady state concentrations of the species.

        Returns
            dict (keys are species names, values are concentrations)
        """
        self.roadrunner.steadyState()
        result_dct = {}
        for name in self.species_names:
            result_dct[name] = self.roadrunner[name]
        return result_dct