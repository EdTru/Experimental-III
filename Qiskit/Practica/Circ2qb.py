from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib
from tabulate import tabulate


shots_L = [100, 1000, 2000, 5000]

baseZZ_prob = []
baseXX_prob = []
baseZZ_disp = []

for shots in shots_L:

	sim = AerSimulator()
	qc_ZZ = QuantumCircuit(2, 0)

	qc_ZZ.h(0)
	qc_ZZ.cx(0,1)

	qc_ZZ.measure_all()

	job = sim.run(qc_ZZ, shots=shots)

	result = job.result()
	counts_ZZ = result.get_counts(qc_ZZ)

	qc_XX = QuantumCircuit(2, 0)

	qc_XX.h(0)
	qc_XX.cx(0,1)

	qc_XX.h(0)
	qc_XX.h(1)

	qc_XX.measure_all()

	job = sim.run(qc_XX, shots=shots)

	result = job.result()
	counts_XX = result.get_counts(qc_XX)


	sigma = np.sqrt(0.5*(1-0.5)/shots)

	baseZZ_prob.append(["ZZ", shots, counts_ZZ["00"]/shots, 0, 0, counts_ZZ["11"]/shots, 1, counts_ZZ["11"]/shots + counts_ZZ["00"]/shots, np.abs(counts_ZZ["11"]/shots + counts_ZZ["00"]/shots -1)/(sigma)])
	baseXX_prob.append(["XX", shots, counts_XX["00"]/shots, 0, 0, counts_XX["11"]/shots, 1, counts_XX["11"]/shots + counts_XX["00"]/shots, np.abs(counts_XX["11"]/shots + counts_XX["00"]/shots -1)/(sigma)])

	
	baseZZ_disp.append(["ZZ", shots, sigma,0,0,sigma, np.abs(counts_ZZ["00"]/shots-0.5)/sigma, 0, 0, np.abs(counts_ZZ["00"]/shots-0.5)/sigma])



headsZZ_prob = ["Base","Shots", "f_{exp}(00)", "f_{exp}(01)", "f_{exp}(10)", "f_{exp}(11)", "<Z * Z>_{teo}", "<Z * Z>_{exp}", "z"]
headsXX_prob = ["Base","Shots", "f_{exp}(++)", "f_{exp}(-+)", "f_{exp}(+-)", "f_{exp}(--)", "<Z * Z>_{teo}", "<Z * Z>_{exp}", "z"]

heads_disp = ["Base", "Shots", "sigma_{teo}(00)", "sigma_{teo}(01)", "sigma_{teo}(10)", "sigma_{teo}(11)", "z(00)", "z(01)", "z(10)", "z(11)"]


tabla_latex_probZZ = tabulate(baseZZ_prob,headsZZ_prob,tablefmt="latex")
tabla_latex_probXX = tabulate(baseXX_prob,headsXX_prob,tablefmt="latex")
tabla_latex_disp = tabulate(baseZZ_disp, heads_disp,tablefmt="latex")

print(tabla_latex_probZZ)
print(tabla_latex_probXX)
print(tabla_latex_disp)