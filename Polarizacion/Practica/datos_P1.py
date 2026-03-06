import numpy as np
import matplotlib.pyplot as plt

#lambd = 635nm

pol_ver = np.array([ #Intensidad del rayo reflejado
	#[ 0, 389 ],#microw
	[ 5, 7.45],
	[10, 7.56],
	[15, 7.84],
	[20, 8.72],
	[25, 9.77],
	[30, 10],
	[35, 12],
	[40, 14],
	[45, 16],
	[50, 19],
	[55, 25],
	[60, 32],
	[65, 44],
	[70, 61],
	[75, 83],
	[80, 116],
	[85, 161]
])

pol_per = np.array([
	#[ 0, 33],#microw
	[ 5, 0.77],
	[10, 0.72],
	[15, 0.66],
	[20, 0.61],
	[25, 0.52],
	[30, 0.48],
	[35, 0.39],
	[40, 0.33],
	[45, 0.26],
	[50, 0.14],
	[55, 0.14],
	[60, 0.18],
	[65, 0.41],
	[70, 0.93],
	[75, 2.06],
	[80, 4.79],
	[85, 9.62]
])

"""
grados = []

intensidad1 = []

intensidad2 = []

for i in pol_ver:
	grados.append(i[0])

for i in pol_ver:
	intensidad1.append(i[1]/161)

for i in pol_per:
	intensidad2.append(i[1]/9.62)


plt.plot(grados, intensidad1, label='Datos')
plt.plot(grados, intensidad2, label='Datos')
plt.xlabel('Grados')
plt.ylabel('Intensidad')
plt.title('Gráfico de ejemplo')
plt.legend()
plt.grid(True)
plt.show()


plt.show()
"""