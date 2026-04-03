from qiskit import QuantumCircuit
from qiskit._accelerate import results
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Define registers
qb0 = QuantumRegister(1, "qb0")
qb1 = QuantumRegister(1, "qb1")
qb2 = QuantumRegister(1, "qb2")

cr = ClassicalRegister(3, "c")

qc = QuantumCircuit(qb0,qb1,qb2, cr)

qc.x(qb0)


qc.barrier()
qc.h(qb1)
qc.cx(qb1, qb2)


# Now we will use random variables to create the secret state. Don't worry about the "u" gate and the details.
np.random.seed(42)  # fixing seed for repeatability
theta = np.random.uniform(0.0, 1.0) * np.pi  # from 0 to pi
varphi = np.random.uniform(0.0, 2.0) * np.pi  # from 0 to 2*pi

# Assign the secret state to the qubit on the other side of Alice's (qubit 0), labeled Q
#qc.u(theta, varphi, 0.0, qb0)
qc.barrier()

# Now entangle Q and Alice's qubits as in the discussion above.
qc.cx(qb0, qb1)
qc.h(qb0)
qc.barrier()

# Now Alice measures her qubits, and stores the outcomes in the "classical registers" cr[]
qc.measure(qb0, cr[0])
qc.measure(qb1, cr[1])



# Now we insert some conditional logic. If Alice measures Q in a "1" we need a Z gate, and if Alice measures A in a "1" we need an X gate (see the table).
with qc.if_test((cr[1], 1)):
	qc.x(qb2)
with qc.if_test((cr[0], 1)): 
	qc.z(qb2)

qc.measure(qb2, cr[2])

counts = job.result().get_counts()

print(counts)

qc.draw(output="mpl")