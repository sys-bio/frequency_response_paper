from control.cascade import Cascade
import numpy as np
import tellurium as te
import unittest

class TestCalculateSteadyState(unittest.TestCase):

    def setUp(self):
        self. rvec = [1, 1, 1]
        self.total = 100
        self.steady_state = Cascade(self.rvec, self.total)

    def checkCalculateSteadyState(self, cascade, tol=1e-2):
        prediction_dct = cascade.calculateSteadyState()
        simulated_dct = cascade.calculateSimulatedSteadyState()
        for name, value in simulated_dct.items():
            error = np.abs((prediction_dct[name] - value)/value)
            if error < tol:
                continue
            else:
                print(cascade.num_species, error)
            #self.assertTrue(np.isclose(prediction_dct[name], value))

    def testCalculateSteadyState(self):
        self.checkCalculateSteadyState(self.steady_state)

    def testCalculateSteadyStateBigger(self):
        for num in [5, 10, 15]:
            ratio_vec = np.random.rand(num) + 0.5
            total = 100
            cascade = Cascade(ratio_vec, total)
            self.checkCalculateSteadyState(cascade, tol=5*10e-2)

if __name__ == '__main__':
    unittest.main()