from control.cascade import Cascade
import numpy as np
import tellurium as te
import unittest

IGNORE_TEST = False
IS_PLOT = False

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
        if IGNORE_TEST:
            return
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
        self.checkCalculateSteadyState(self.cascade)

    def testCalculateSteadyStateBigger(self):
        if IGNORE_TEST:
            return
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
        num_species = 10
        num_step = 5
        total = 100
        rv = np.repeat(2, num_species)
        cc = self.cascade.simulateControlCoefficient()

if __name__ == '__main__':
    unittest.main()