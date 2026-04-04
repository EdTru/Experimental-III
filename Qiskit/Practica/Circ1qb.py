from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
pi = np.pi

theta = [0, pi/3, pi/2, pi]

shots = [50, 100, 1000, 5000]
p_teo_0 = [1, 0.75,0.5,0]
p_teo_1 = [0, 0.25,0.5,1]

resultados_abs = [[],[],[],[]]
resultados_rel = [[],[],[],[]]

datos = []

dispersion_pi3 = []
dispersion_pi2 = []

for theta_i in range(len(theta)):

	for shot_i in range(len(shots)):

		sim = AerSimulator()
		qc = QuantumCircuit(1, 1)
		qc.ry(theta[theta_i], 0)
		qc.measure(0, 0)
		job = sim.run(qc, shots=shots[shot_i])
		result = job.result()
		counts = result.get_counts(qc)

		posibles_medidas = counts.keys()
		valores = list(counts.values())

		for i in range(len(valores)): valores[i] = valores[i]/shots[shot_i]

		resultados_abs[theta_i].append(counts)
		resultados_rel[theta_i].append(dict(zip(posibles_medidas,valores)))

		try:
			counts["0"] = counts["0"]
		except KeyError:
			counts["0"] = 0

		try:
			counts["1"] = counts["1"]
		except KeyError:
			counts["1"] = 0


		datos.append([theta[theta_i],
					  shots[shot_i],
					  counts["0"]/shots[shot_i],
					  counts["1"]/shots[shot_i],
					  p_teo_0[theta_i],
					  p_teo_1[theta_i],
					  np.sqrt((p_teo_0[theta_i]*(1-p_teo_0[theta_i]))/shots[shot_i]),
					  np.sqrt((p_teo_1[theta_i] * (1 - p_teo_1[theta_i])) / shots[shot_i]),
					  np.abs(counts["0"]/shots[shot_i]-p_teo_0[theta_i])/np.sqrt((p_teo_0[theta_i]*(1-p_teo_0[theta_i]))/shots[shot_i]),
					  np.abs(counts["1"]/shots[shot_i] - p_teo_1[theta_i]) / np.sqrt((p_teo_1[theta_i] * (1 - p_teo_1[theta_i])) / shots[shot_i])
					  ])

		if theta[theta_i] == 1:
			dispersion_pi3.append(np.abs(counts["0"]/shots[shot_i]-p_teo_0[theta_i])/np.sqrt((p_teo_0[theta_i]*(1-p_teo_0[theta_i]))/shots[shot_i]))
		elif theta[theta_i] == 2:
			dispersion_pi2.append(np.abs(counts["0"] / shots[shot_i] - p_teo_0[theta_i]) / np.sqrt((p_teo_0[theta_i] * (1 - p_teo_0[theta_i])) / shots[shot_i]))

#Analisis estadistico

heads = ["theta", "shots", "f_exp 0", "f_exp 1", "p_teo 0", "p_teo 1", "sigma_teo_0","sigma_teo_1","dif teo-exp 0","dif teo-exp 1"]

tabla_latex = tabulate(datos,heads,tablefmt="latex")

print(tabla_latex)