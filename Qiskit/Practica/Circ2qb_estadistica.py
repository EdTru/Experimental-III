from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np

def tirar():

	shots = 5000

	sim = AerSimulator()
	qc = QuantumCircuit(2,0)
	qc.h(0)
	qc.cx(0,1)
	qc.measure_all()

	job = sim.run(qc, shots=shots)
	result = job.result()
	counts = result.get_counts(qc)

	sigma = np.sqrt(0.5*(1-0.5)/shots)

	dispersion_00 = [(counts["00"]/shots-0.5)/sigma]
	dispersion_11 = [(counts["11"]/shots-0.5)/sigma]

	return dispersion_00, dispersion_11

N_exp = 300

dispersion_00, dispersion_11 = [], []

for i in range(N_exp):

	dispersion_00_nueva, dispersion_11_nueva = tirar()

	dispersion_00 += dispersion_00_nueva
	dispersion_11 += dispersion_11_nueva

print(dispersion_00)

datos = dispersion_00
plt.hist(datos, bins=20)  # Divide los datos en 5 intervalos
plt.xlabel("Desviación típica")
plt.ylabel("Frecuencia")
plt.title("Histograma por intervalos de la desviación típica del estado |00>")
plt.savefig("HistogramaCirc2qb.svg")
plt.show()