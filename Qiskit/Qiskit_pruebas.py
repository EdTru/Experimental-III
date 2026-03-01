from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile
import matplotlib.pyplot as plt
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
# Inicializar el simulador
simulator = AerSimulator()
# Transpilar el circuito
transpiled_qc = transpile(qc, simulator)
# Ejecutar el circuito
result = simulator.run(transpiled_qc, shots=1024).result()
# Obtener los resultados
counts = result.get_counts()
print(counts)
# Dibujar el circuito
qc.draw(output='mpl')
# Mostrar la gráfica del circuito
plt.show()