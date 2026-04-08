import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


caso_A = { #mW
	"I_total": 528,
	"I_v": 352,
	"I_h": 0.74,
	"I_-45": 167,
	"I_+45": 191,
	"I_lambda/4": 288,
	"-I_lambda/4": 240

}

caso_B = { #mW
	"I_total": 300,
	"I_v": 104,
	"I_h": 103,
	"I_-45": 200,
	"I_+45": 163,
	"I_lambda/4": 93,
	"-I_lambda/4": 100

}

caso_A_norm = {}
caso_B_norm = {}

for key in caso_A:
	caso_A_norm[key] = round(caso_A[key] / caso_A["I_total"],2)

for key in caso_B:
	caso_B_norm[key] = round(caso_B[key] / caso_B["I_total"],2)

print(caso_A_norm)
sa = np.array([caso_A_norm["I_total"], 
			  caso_A_norm["I_h"]-caso_A_norm["I_v"], 
			  caso_A_norm["I_+45"]-caso_A_norm["I_-45"], 
			  caso_A_norm["I_lambda/4"]-caso_A_norm["-I_lambda/4"]])

sb = np.array([caso_B_norm["I_total"], 
			  caso_B_norm["I_h"]-caso_B_norm["I_v"], 
			  caso_B_norm["I_+45"]-caso_B_norm["I_-45"], 
			  caso_B_norm["I_lambda/4"]-caso_B_norm["-I_lambda/4"]])

print(sa)
print(sb)

p1 = sa[1:]
p2 = sb[1:]

print(p1)
print(p2)

# Configuración de la esfera
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Dibujar superficie de la esfera (transparente)
u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]# lo hacemos con 30 y 30 puntos para no saturar el programa
ax.plot_wireframe(np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), np.cos(v), color="grey", alpha=0.1)

# Dibujar ejes principales, dejamos una separación con respecto a la esfera
ax.quiver([-1.2, 0, 0], [0, -1.2, 0], [0, 0, -1.2], [2.4, 0, 0], [0, 2.4, 0], [0, 0, 2.4], 
          color='black', lw=1, arrow_length_ratio=0.05)

# Etiquetas de ejes
ax.text(1.3, 0, 0, "S1 (H/V)"); ax.text(0, 1.3, 0, "S2 (+45/-45)"); ax.text(0, 0, 1.3, "S3 (R/L)")

# Graficar puntos medidos
origen = np.array([0, 0, 0])
ax.quiver(origen[0], origen[1], origen[2], p1[0], p1[1], p1[2], color='red', label='Medición A')
ax.quiver(origen[0], origen[1], origen[2], p2[0], p2[1], p2[2], color='blue', label='Medición B')

ax.scatter(*p1, color='red', s=100, label='Medición A')
ax.scatter(*p2, color='blue', s=100, label='Medición B')

ax.view_init(elev=20, azim=45)
plt.legend()
plt.show()
