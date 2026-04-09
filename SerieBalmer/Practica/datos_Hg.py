import numpy as np
from tabulate import tabulate

error_2l = 0.001
error_l = 0.0005
error_d = 0.0005


amarilla1 = 257
verde1 = 270
azul1 = 309

azul2 = 588
verde2 = 628
amarilla2 = 639

tabla_d50 = np.array([ #d = 0.50 m ["Color", "longitud_ref","2l","l","g"],
	["Amarillo", 578.0,0.382,0.191],
	["Verde",546.1,0.358,0.179],
	["Azul", 434.8,0.279,0.1395]
])

tabla_g_d50 = []

for ristra in tabla_d50:
	d = 0.5
	l = float(ristra[3])
	lamd = float(ristra[1])*10**(-9)

	g = np.sqrt(d**2+l**2)/(l) *lamd
	error_g = np.abs(lamd*(1/(np.sqrt(d**2+l**2))-np.sqrt(d**2+l**2)/l**2))*error_l + np.abs((lamd/l)*d/np.sqrt(d**2+l**2))*error_d

	tabla_g_d50.append([str(g),str(error_g)])

amarilla1 = 276
verde1 = 287
azul1 = 323

azul2 = 570
verde2 = 603
amarilla2 = 612


tabla_d45 = np.array([
	["Amarillo", 578.0,0.336,0.168],
	["Verde",546.1,0.316,0.158],
	["Azul", 434.8,0.247,0.1235]
])

tabla_g_d45 = []

for ristra in tabla_d45:
	d = 0.45
	l = float(ristra[3])
	lamd = float(ristra[1])*10**(-9)

	g = np.sqrt(d**2+float(ristra[3])**2)/(float(ristra[3])) *float(ristra[1])*10**(-9)
	error_g = np.abs(lamd*(1/(np.sqrt(d**2+l**2))-np.sqrt(d**2+l**2)/l**2))*error_l + np.abs((lamd/l)*d/np.sqrt(d**2+l**2))*error_d

	tabla_g_d45.append([str(g),str(error_g)])

#Unificamos las tablas

pie_tabla = []
gs = []
error_gs = []
for i in range(0,3):
	pie_tabla.append([0.5,tabla_d50[i][0],tabla_d50[i][1],tabla_d50[i][2],tabla_d50[i][3],tabla_g_d50[i][0],error_d,error_2l, error_l, tabla_g_d50[i][1]])
	pie_tabla.append([0.45,tabla_d45[i][0],tabla_d45[i][1],tabla_d45[i][2],tabla_d45[i][3],tabla_g_d45[i][0],error_d,error_2l, error_l, tabla_g_d45[i][1]])
	
	gs.append(float(tabla_g_d50[i][0]))
	gs.append(float(tabla_g_d45[i][0]))

	error_gs.append(float(tabla_g_d50[i][1]))
	error_gs.append(float(tabla_g_d45[i][1]))

cabezas = ["d (m)","Color","Lambda_ref (nm)","2l (m)","l (m)","g (m)","error d","error 2l","error l","error g"]

tabla = tabulate(pie_tabla,cabezas,tablefmt="latex")

print(tabla)
print(sum(gs)/len(gs))
print(sum(error_gs)/len(error_gs))