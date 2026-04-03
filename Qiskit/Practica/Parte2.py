from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib
from tabulate import tabulate


shots_L = [100, 1000, 2000, 5000]

baseZZ_prob = []
baseZZ_disp = []

for shots in shots_L:

	sim = AerSimulator()
	qc = QuantumCircuit(2, 0)

	qc.h(0)
	qc.cx(0,1)

	qc.measure_all()

	job = sim.run(qc, shots=shots)

	result = job.result()
	counts = result.get_counts(qc)

	baseZZ_prob.append(["ZZ", shots, counts["00"]/shots, 0, 0, counts["11"]/shots, 0.5, 0, 0, 0.5])
	sigma = np.sqrt(0.5*(1-0.5)/shots)
	baseZZ_disp.append(["ZZ", shots, sigma,0,0,sigma, np.abs(counts["00"]/shots-0.5)/sigma, 0, 0, np.abs(counts["00"]/shots-0.5)/sigma])



heads_prob = ["Base","Shots", "f_{exp}(00)", "f_{exp}(01)", "f_{exp}(10)", "f_{exp}(11)", "p_{teo}(00)", "p_{teo}(01)", "p_{teo}(10)", "p_{teo}(11)"]
heads_disp = ["Base", "Shots", "sigma_{teo}(00)", "sigma_{teo}(01)", "sigma_{teo}(10)", "sigma_{teo}(11)", "z(00)", "z(01)", "z(10)", "z(11)"]


tabla_latex_prob = tabulate(baseZZ_prob,heads_prob,tablefmt="latex")
tabla_latex_disp = tabulate(baseZZ_disp, heads_disp,tablefmt="latex")

print(tabla_latex_prob)
print(tabla_latex_disp)