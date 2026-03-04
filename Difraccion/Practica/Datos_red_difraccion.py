import numpy as np

#Tablas de la forma [D (distancia rendija-caja), d(m=1 m=-1) (distancia entre m=-1 y m=1)]
#D en cm X_min cm
red600 = np.array([[35, 28],
					[30, 25.2],
					[25, 19.6],
					[20, 15.9],
					[15, 12]])

red300 = np.array([[70, 28.4],
					[60, 23.8],
					[50, 20.2],
					[40, 15],
					[30, 11.9]])

red100 = np.array([[70, 9.1],
					[60, 8.4],
					[50, 6.1],
					[40, 5],
					[30, 3.9]])


for i in red300:
	print(((i[1]/2)/((640*10**(-9))*i[0]))*10**(-3))

