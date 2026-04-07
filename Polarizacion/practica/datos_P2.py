import numpy as np
import matplotlib.pyplot as plt
import tabulate as tb

#lambd = 635nm
datos_malus = np.array([
	[0  ,145],
	[5  ,143],
	[10 ,140],
	[15 ,133],
	[20 ,125],
	[25 ,115],
	[30, 103],
	[35 ,89],
	[40 ,78],
	[45 ,67],
	[50 ,55],
	[55 ,44],
	[60 ,33],
	[65 ,23],
	[70 ,15],
	[75 ,9],
	[80 ,4.72],
	[85 ,2.66],
	[90 ,2.78],
	[95 ,5.1],
	[100,9.53],
	[105,16],
	[110  ,24],
	[115 ,34],
	[120 ,45],
	[125 ,57],
	[130,70],
	[135,82],
	[140,95],
	[145,107],
	[150,117],
	[160,127],
	[165 ,134],
	[170 ,135],
	[175, 136],
	[180 ,136]
])

dati = np.transpose(datos_malus)
print(dati[0])

plt.scatter(dati[0],dati[1])


plt.show()

titulos = [r"$\theta$ (º)", r"$I$ (mw)", r"$\Delta \theta$ (º)", r"$\Delta I$ (mw)"]

err_grados = [r"$\pm 0.5$"] * len(dati[0])

err_int = [r"$\pm 0.01$"] * len(dati[0])

tabla = tb.tabulate(np.transpose([dati[0], dati[1], err_grados, err_int]), headers=titulos, tablefmt="latex_raw")

print(tabla)