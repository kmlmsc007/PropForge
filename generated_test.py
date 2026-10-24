import unittest
from qiskit import QuantumCircuit
from qucheck.property import Property
from qucheck.input_generators import RandomState
from qucheck.test_runner import TestRunner

class BellStateEntanglementProperty(Property):
    def get_input_generators(self):
        return [RandomState(2)]

    def preconditions(self, *inputs):
        return True

    def operations(self, *inputs):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        self.statistical_analysis.assert_entangled(self, [0, 1], qc)

class TestBellStateCircuit(unittest.TestCase):
    def test_property(self):
        runner = TestRunner([BellStateEntanglementProperty], num_inputs=5, random_seed=42, num_measurements=2000)
        runner.run_tests()
        self.assertIn(BellStateEntanglementProperty, runner.list_passing_properties())
        self.assertEqual(runner.list_failing_properties(), [])

if __name__ == "__main__":
    unittest.main()
