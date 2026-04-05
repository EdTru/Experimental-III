import numpy as np
import tabulate


i = 323
g = np.float64(1.6336317230290944e-06) #Constante red apartado anterior

error_angulo = 0.05
error_angulo_rad = 0.0009
error_g = np.float64(6.254791388988623e-09) #Error medio apartado anterior
error_intensidad = 0.001

#error_lambd = error_g*np.abs(np.sin(angulo_rad))+np.abs(g*np.cos(angulo_rad))*error_angulo_rad

valores = np.array([#angulo º | voltaje mW/cm2

	[325-i, 5.65277301730027e-08,0.006 ],
	[326-i, 8.477007098601504e-08, 0.004],
	[327-i, 1.1298659001421894e-07, 0.009],
	[328-i, 1.4116869223257882e-07, 0.008],
	[329-i, 1.693077930997528e-07, 0.002],
	[330-i, 1.9739532117302723e-07, 0.008],
	[331-i, 2.254227207192609e-07, 0.013],
	[332-i, 2.533814543210446e-07, 0.006],
	[333-i, 2.812630054772808e-07, 0.003],
	[334-i, 3.090588811973927e-07, 0.001],
	[335-i, 3.367606145883713e-07, 0.004],
	[336-i, 3.6435976743387295e-07, 0.006],
	[337-i, 3.9184793276458193e-07, 0.005],
	[338-i, 4.1921673741905456e-07, 0.004],
	[339-i, 4.464578445942657e-07, 0.005],
	[340-i, 4.7356295638507927e-07, 0.001],
	[341-i, 5.005238163118703e-07, 0.013],
	[342-i, 5.273322118355299e-07, 0.013],
	[343-i, 5.539799768590825e-07, 0.018],
	[344-i, 5.804589942151593e-07, 0.013],
	[345-i, 6.067611981385656e-07, 0.025],
	[346-i, 6.328785767231911e-07, 0.006],
	[347-i, 6.588031743625143e-07, 0.016],
	[348-i, 6.845270941729572e-07, 0.009],
	[349-i, 7.10042500399352e-07, 0.004],
	[350-i, 7.35341620801789e-07, 0.002],
	[351-i, 7.604167490231157e-07, 0.002],
	[352-i, 7.852602469363674e-07, 0.003],
	[353-i, 8.098645469714153e-07, 0.002]
])

pies = []
dibujar = []
for i in valores:
	angulo = i[0]
	angulo_rad = np.float64(i[0]*2*np.pi/360)
	lambd = g*np.sin(angulo_rad)
	error_lambd = error_g*np.abs(np.sin(angulo_rad))+np.abs(g*np.cos(angulo_rad))*error_angulo_rad
	pies.append([angulo, angulo_rad.round(4), lambd.round(9),i[2],error_angulo,error_angulo_rad, error_lambd.round(9),error_intensidad])
	dibujar.append([lambd,i[2],error_lambd, error_intensidad])

cabezas = ["Ángulo (º)","Ángulo (rad)","lambda","Intensidad (mW/cm^2)","error angulo (º)","error angulo (rad)","error lamda", "error intensidad"]

tablaL = tabulate.tabulate(pies,cabezas,tablefmt="latex")

print(tablaL)




import matplotlib.pyplot as plt

val = np.transpose(dibujar)
plt.scatter(val[0], val[1])
plt.errorbar(val[0], val[1], yerr=val[3], xerr=val[2],fmt="o")
plt.title("Espectro de emisión visible del helio")
plt.xlabel("longitud de onda (m)")
plt.ylabel("Intensidad (mW/cm²)")
plt.savefig("Espectrohelio.svg")
plt.show()