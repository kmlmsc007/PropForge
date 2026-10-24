import google.generativeai as genai
from google.api_core.exceptions import NotFound

API_KEY = "YOUR_API_KEY_HERE"

QUCHECK_API_SPEC = """
QuCheck Framework Architecture and Rules:
1. Core Imports:
   from qucheck.property import Property
   from qucheck.input_generators import RandomState
   from qucheck.test_runner import TestRunner

2. Property Class Definition:
   Each property must inherit from `Property`:
   class MyProperty(Property):
       def get_input_generators(self):
           # Must return a list containing at least one input generator (e.g., [RandomState(2)])
           return [RandomState(2)]

       def preconditions(self, *inputs):
           return True

       def operations(self, *inputs):
           # Build unmeasured quantum circuit (QuCheck handles measurements internally)
           qc = QuantumCircuit(2, 2)
           ...
           # Statistical assertions on self.statistical_analysis:
           # - self.statistical_analysis.assert_entangled(self, qubits, circuit, basis=["z"])
           # - self.statistical_analysis.assert_probability(self, qubits, circuit, probabilities, basis=["z"])
           # - self.statistical_analysis.assert_equal(self, qubits1, circ1, qubits2, circ2)
           # - self.statistical_analysis.assert_different(self, qubits1, circ1, qubits2, circ2)
           # - self.statistical_analysis.assert_separable(self, qubits, circuit, basis=["z"])

3. Execution with unittest:
   class TestMyCircuit(unittest.TestCase):
       def test_property(self):
           runner = TestRunner([MyProperty], num_inputs=5, random_seed=42, num_measurements=2000)
           runner.run_tests()
           self.assertIn(MyProperty, runner.list_passing_properties())
           self.assertEqual(runner.list_failing_properties(), [])
"""

def main():
    # Configure the Gemini API
    genai.configure(api_key=API_KEY)

    # 1) Read the contents of my_circuit.py
    with open("my_circuit.py", "r", encoding="utf-8") as f:
        circuit_code = f.read()

    # 2) Send code to the model with QuCheck API specifications
    prompt = (
        "You are an expert in quantum computing and the QuCheck testing framework.\n"
        f"API Reference:\n{QUCHECK_API_SPEC}\n\n"
        "Analyze this Qiskit circuit and write a valid QuCheck property-based test script for it. "
        "Output ONLY the raw Python code, no markdown.\n\n"
        f"Circuit:\n{circuit_code}"
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
    except NotFound:
        # Fallback to current active Flash model if gemini-1.5-flash is retired
        model = genai.GenerativeModel("gemini-3.8-flash")
        response = model.generate_content(prompt)

    generated_code = response.text.strip()

    # Clean markdown fences if present
    if generated_code.startswith("```"):
        lines = generated_code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        generated_code = "\n".join(lines).strip()

    # 3) Save AI response into generated_test.py
    with open("generated_test.py", "w", encoding="utf-8") as f:
        f.write(generated_code + "\n")

    # Print success message to terminal
    print("Success: Generated test saved to generated_test.py")

if __name__ == "__main__":
    main()
