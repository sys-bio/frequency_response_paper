from src.control.steady_state import SteadyState
import numpy as np
import tellurium as te
import unittest

class TestCalculateSteadyState(unittest.TestCase):

    def setUp(self):
        self. rvec = [1, 1, 1]
        self.total = 1
        self.steady_state = SteadyState(self.rvec, self.total)

    def checkCalculateSteadyState(self, steady_state):
        actuals = steady_state.calculateSteadyState()
        for name, value in steady_state.calculateSimulatedSteadyState().items():
            index = int(name[1])
            if not np.isclose(actuals[index], value):
                import pdb; pdb.set_trace()
            self.assertTrue(np.isclose(actuals[index], value))

    def testCalculateSteadyState(self):
        self.checkCalculateSteadyState(self.steady_state)

    def testCalculateSteadyStateBigger(self):
        for num in [5, 10, 15]:
            ratio_vec = np.random.rand(num)
            total = 1
            steady_state = SteadyState(ratio_vec, total)
            self.checkCalculateSteadyState(steady_state)

if __name__ == '__main__':
    unittest.main()