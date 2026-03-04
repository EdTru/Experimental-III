from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np

def tirar():
	pi = np.pi

	theta = [pi/3, pi/2]
	shots = 5000
	p_teo_0 = [0.75,0.5]
	p_teo_1 = [0.25,0.5]

	dispersion_pi3 = []
	dispersion_pi2 = []

	for theta_i in range(len(theta)):

		sim = AerSimulator()
		qc = QuantumCircuit(1, 1)
		qc.ry(theta[theta_i], 0)
		qc.measure(0, 0)
		job = sim.run(qc, shots=shots)
		result = job.result()
		counts = result.get_counts(qc)

		if theta_i == 0:
			dispersion_pi3.append((counts["0"] / shots - p_teo_0[theta_i] )/ np.sqrt((p_teo_0[theta_i] * (1 - p_teo_0[theta_i])) / shots))
		elif theta_i == 1:
			dispersion_pi2.append((counts["0"] / shots - p_teo_0[theta_i] )/ np.sqrt((p_teo_0[theta_i] * (1 - p_teo_0[theta_i])) / shots))


	return dispersion_pi3, dispersion_pi2

N_exp = 500

dispersion_pi3, dispersion_pi2 = [], []

for i in range(N_exp):

	dispersion_pi3_nueva, dispersion_pi2_nueva = tirar()

	dispersion_pi3 += dispersion_pi3_nueva
	dispersion_pi2 += dispersion_pi2_nueva

print(dispersion_pi2)

datos = dispersion_pi2
plt.hist(datos, bins=20)  # Divide los datos en 5 intervalos
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.title('Histograma por intervalos')
plt.show()