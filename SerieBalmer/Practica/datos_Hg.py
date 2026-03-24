import numpy as np

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
d = 0.5
for ristra in tabla_d50:
	g = np.sqrt(d**2+float(ristra[3])**2)/(float(ristra[3])) *float(ristra[1])*10**(-9)
	tabla_g_d50.append(g)

amarilla1 = 0.276
verde1 = 0.287
azul1 = 0.323

azul2 = 0.570
verde2 = 0.603
amarilla2 = 0.612


tabla_d45 = np.array([
	["Amarillo", 578.0,0.336,0.191],
	["Verde",546.1,0.316,0.179],
	["Azul", 434.8,0.247,0.1395]
])

tabla_g_d45 = []
d = 0.5
for ristra in tabla_d45:
	g = np.sqrt(d**2+float(ristra[3])**2)/(float(ristra[3])) *float(ristra[1])*10**(-9)
	tabla_g_d45.append(g)

print(tabla_g_d50)