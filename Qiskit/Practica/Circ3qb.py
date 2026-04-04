from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

sim = AerSimulator()

qb0 = QuantumRegister(1, "qb0")
qb1 = QuantumRegister(1, "qb1")
qb2 = QuantumRegister(1, "qb2")

cr = ClassicalRegister(3, "c")

qc = QuantumCircuit(qb0,qb1,qb2, cr)

theta= np.pi/2
phi=0
lamd = 0

qc.u(theta=theta,phi=theta,lam=lamd,qubit=qb0) #El de inicio


qc.barrier()
qc.h(qb1)
qc.cx(qb1, qb2)


qc.barrier()
qc.cx(qb0, qb1)
qc.h(qb0)

qc.barrier()
qc.measure(qb0, cr[0])
qc.measure(qb1, cr[1])

with qc.if_test((cr[1], 1)):
	qc.x(qb2)
with qc.if_test((cr[0], 1)): 
	qc.z(qb2)

qc.measure(qb2, cr[2])

job = sim.run(qc, shots=1000)

counts = job.result().get_counts()

print("theta = ", theta, "phi = ",phi,"lambda = ", lamd)

matriz_U = np.array([
	[np.cos(theta/2), np.exp(-1j*lamd)*np.sin(theta/2)],
	[np.exp(1j*phi)*np.sin(theta/2),np.exp(1j*(phi+lamd))*np.cos(theta/2)]
])

vec_U = np.array([
	[1],[0]
])

inici = np.dot(matriz_U,vec_U)

print(inici)

print(counts)

qc.draw(output="mpl", filename="circ3qb.svg")