from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import numpy as np

pi = np.pi


theta = [0, pi/3, pi/2, pi]
shots = 100

# Creamos un simulador cu´antico
sim = AerSimulator()
# Creamos un circuito con 1 qubit y 1 bit cl´asico
qc = QuantumCircuit(1, 1)
# Aplicamos una rotaci´on Ry(theta) al qubit
qc.ry(theta[1], 0)
# Medimos el qubit en la base computacional (Z)
qc.measure(0, 0)
# Ejecutamos el circuito un n´umero finito de veces (shots)
job = sim.run(qc, shots=shots)
# Obtenemos el resultado de la simulaci´on
result = job.result()
# Extraemos los resultados de la medida
counts = result.get_counts(qc)

print(results)
print(counts)
qc.draw()