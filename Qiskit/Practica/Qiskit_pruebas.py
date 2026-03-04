from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib

pi = np.pi

theta = [0, pi/3, pi/2, pi]
shots = 100

sim = AerSimulator()
qc = QuantumCircuit(1, 1)
qc.ry(theta[2], 0)
qc.measure(0, 0)
job = sim.run(qc, shots=shots)
result = job.result()
counts = result.get_counts(qc)


