from control.cascade import Cascade

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import unittest

IGNORE_TEST = True
IS_PLOT = True

class TestCalculateSteadyState(unittest.TestCase):

    def setUp(self):
        if IGNORE_TEST:
            return
        self.init()

    def init(self):
        self. rvec = [1, 1, 1]
        self.total = 100
        self.cascade = Cascade(self.rvec, self.total)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        total = 100
        #
        rvec = [1, 2, 3]
        cascade = Cascade(rvec, total)
        for constant in ["k1", "k3", "k5"]:
            self.assertTrue("%s = 1" % constant in cascade.antimony)
        self.assertTrue("k4 = 2" in cascade.antimony)
        self.assertTrue("k6 = 3" in cascade.antimony)


    def checkCalculateSteadyState(self, cascade, tol=1e-2):
        prediction_dct = cascade.calculateSteadyState()
        simulated_dct = cascade.simulateSteadyState()
        for name, value in simulated_dct.items():
            error = np.abs((prediction_dct[name] - value)/value)
            if error < tol:
                continue
            else:
                print(cascade.num_species, error)
            #self.assertTrue(np.isclose(prediction_dct[name], value))

    def testCalculateSteadyState(self):
        if IGNORE_TEST:
            return
        if IGNORE_TEST:
            self.init()
        self.checkCalculateSteadyState(self.cascade)

    def testCalculateSteadyStateBigger(self):
        if IGNORE_TEST:
            return
        if IGNORE_TEST:
            self.init()
        for num in [5, 10, 15]:
            ratio_vec = np.random.rand(num) + 0.5
            total = 100
            cascade = Cascade(ratio_vec, total)
            self.checkCalculateSteadyState(cascade, tol=5*10e-2)

    def testSimulateFinalSteadyState1(self):
        if IGNORE_TEST:
            return
        result = self.cascade.simulateFinalSpeciesSteadyState()
        self.assertTrue(np.isclose(result, 25))

    def testSimulateFinalSteadyState2(self):
        # More extensive simulation test
        if IGNORE_TEST:
            return
        num_species = 10
        num_step = 5
        total = 100
        rv = np.repeat(1, num_species)
        Sn_ss = total
        for _ in range(num_step):
            rv = np.append([rv[0] + 0.1], rv[1:])
            cascade = Cascade(rv, total)
            new_Sn_ss = cascade.simulateFinalSpeciesSteadyState()
            self.assertLess(new_Sn_ss, Sn_ss)
            Sn_ss = new_Sn_ss

    def testSimulateLastControlCoefficient(self):
        if IGNORE_TEST:
            return
        rvec = [1, 1, 1]
        total = 100
        cascade = Cascade(rvec, total)
        cc_df = cascade.simulateControlCoefficient()
        self.assertTrue(isinstance(cc_df, pd.DataFrame))
        self.assertTrue(np.isclose(cc_df.loc[ 1, "r1"], -0.25))
        self.assertTrue(np.isclose(cc_df.loc[ 1, "r2"], -0.5))
        self.assertTrue(np.isclose(cc_df.loc[ 1, "r3"], -0.75))

    def testSet(self):
        if IGNORE_TEST:
            return
        if IGNORE_TEST:
            self.init()
        self.cascade.set({"k1": 100})
        self.assertTrue(self.cascade.roadrunner.k1 == 100)
        #
        self.cascade.set({1: 100})
        self.assertTrue(self.cascade.roadrunner.k1 == 100)

    def testPlotSimulatedControlCoefficient(self):
        #if IGNORE_TEST:
        #    return
        if IGNORE_TEST:
            self.init()
        size = 4
        rvec = np.repeat(1, size)
        total = 100
        cascade = Cascade(rvec, total)
        r_vals = [0.01, 0.1, 1, 10, 20, 50, 100, 500]
        ax = cascade.plotSimulatedControlCoefficient(species_idx=2, r_vals=r_vals)
        ax.set_xscale('log')
        cascade.writePlot("testPlotControlCoefficient.pdf")

    def testPlotConcentrations(self):
        if IGNORE_TEST:
            return
        if IGNORE_TEST:
            self.init()
        rvec = [1, 0.01]
        cascade = Cascade(rvec, self.total)
        k2_vals = [0.1, 1, 1.5, 2.0, 10, 20, 50, 100, 1000, 1e5]
        cascade.plotConcentrations(k2_vals)

    def testCalculateControlCoefficient(self):
        if IGNORE_TEST:
            return
        if IGNORE_TEST:
            self.init()
        rvec = [1, 1000]
        cascade = Cascade(rvec, self.total)
        r1_vals = np.array([10, 100, 1000, 10000, 100000])
        r1_vals = np.array([100000])
        calc_ser = cascade.calculateControlCoefficient(r1_vals=r1_vals)
        sim_ser = cascade.simulateControlCoefficient(r_vals=r1_vals)["r2"]
        rmse = np.sum((calc_ser - sim_ser).values**2)
        self.assertTrue(np.isclose(rmse, 0))

    def testIterateOnSpeciesNumber(self):
        if IGNORE_TEST:
            return
        if IGNORE_TEST:
            self.init()
        nums = list(self.cascade.iterateOnSpeciesNumber())
        self.assertEqual(set(nums), set(range(1, self.cascade.num_species)))


if __name__ == '__main__':
    unittest.main()