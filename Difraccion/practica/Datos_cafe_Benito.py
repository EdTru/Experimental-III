import numpy as np
import tabulate as tb
import matplotlib.pyplot as plt
from scipy.stats import linregress

#Tablas de la forma [D (distancia rendija-caja), d(m=1 m=-1) (distancia entre m=-1 y m=1)]
#D en cm X_min mm
red_distanciaG = np.array([[900, 9.4],
							[850, 8.11],
							[800, 5.03],
							[750, 5.64],
							[700, 4.43]])

red_distanciaP = np.array([[900, 3.62],
							[850, 3.71],
							[800, 2.01],
							[750, 2.12],
							[700, 2.81]])

red_radio = np.array([[900, 40.32],
						[850, 37.83],
						[800, 34.92],
						[750, 31.92],
						[700, 30.91]])

distancias = np.transpose(red_distanciaG)[0]


d_g = np.transpose(red_distanciaG)[1]
d_p = np.transpose(red_distanciaP)[1]
d_r = np.transpose(red_radio)[1]

D_error = [r"$\pm 0.02$"]*len(distancias)

d_error = [r"$\pm 0.01$"]*len(distancias)

indices_tabla1 = ["$D$ (mm)", "$d_{min}$", r"$\Delta D$ (mm)", r"$\Delta d_{min}$"]
indices_tabla2 = ["$D$ (mm)", "$d_{p}$", r"$\Delta D$ (mm)", r"$\Delta d_{max}$"]
indices_tabla3 = ["$D$ (mm)", "$d_{r}$", r"$\Delta D$ (mm)", r"$\Delta d_{max}$"]

tablad = tb.tabulate(np.transpose([distancias, d_g, D_error, d_error]), headers=indices_tabla1, tablefmt="latex_raw")
tablap = tb.tabulate(np.transpose([distancias, d_p, D_error, d_error]), headers=indices_tabla2, tablefmt="latex_raw")
tablar = tb.tabulate(np.transpose([distancias, d_r, D_error, d_error]), headers=indices_tabla3, tablefmt="latex_raw")
print(r"\begin{table}[H]")
print(r"\caption{Tabla para la toma 1 }")
print(r"\centering")
print(r"\small")
print(r"\setlength{\tabcolsep}{4pt}")
print(tablad)
print(r"\end{table}")
print("\n")

print("----------------------------------------")

print(r"\begin{table}[H]")
print(r"\caption{Tabla para la toma 1 }")
print(r"\centering")
print(r"\small")
print(r"\setlength{\tabcolsep}{4pt}")
print(tablap)
print(r"\end{table}")
print("\n")

print("----------------------------------------")


print(r"\begin{table}[H]")
print(r"\caption{Tabla para la toma 1 }")
print(r"\centering")
print(r"\small")
print(r"\setlength{\tabcolsep}{4pt}")
print(tablar)
print(r"\end{table}")

m, b, r_value, p_value, std_err = linregress(distancias, d_g)
plt.scatter(distancias, d_g, label="Distancias a primer mínimo", marker="o", s=15, zorder=3)
plt.plot(distancias, m*distancias + b, label="Ajuste lineal", color="red")
plt.errorbar(distancias, d_g, yerr=0.02, xerr=0.02, fmt='none', ecolor='black', elinewidth=1.2, capsize=5, zorder=2)
plt.xlabel("Distancia rendija-caja (mm)")
plt.ylabel("Distancia primer mínimo (mm)")
plt.title(f"Distancia rendija-caja vs Distancia primer mínimo, = {round(m,3)} ± {round(std_err,3)}")
plt.legend()
plt.grid()
plt.show()

m, b, r_value, p_value, std_err = linregress(distancias, d_p)
plt.scatter(distancias, d_p, label="Distancias entre puntos", marker="o", s=15, zorder=3)
plt.plot(distancias, m*distancias + b, label="Ajuste lineal", color="red")
plt.errorbar(distancias, d_p, yerr=0.02, xerr=0.02, fmt='none', ecolor='black', elinewidth=1.2, capsize=5, zorder=2)
plt.xlabel("Distancia rendija-caja (mm)")
plt.ylabel("Distancia entre puntos (mm)")
plt.title(f"Distancia rendija-caja vs Distancia entre puntos, = {round(m,3)} ± {round(std_err,3)}")
plt.legend()
plt.grid()
plt.show()

m, b, r_value, p_value, std_err = linregress(distancias, d_r)
plt.scatter(distancias, d_r, label="Distancias del radio completo", marker="o", s=15, zorder=3)
plt.plot(distancias, m*distancias + b, label="Ajuste lineal", color="red")
plt.errorbar(distancias, d_r, yerr=0.02, xerr=0.02, fmt='none', ecolor='black', elinewidth=1.2, capsize=5, zorder=2)
plt.xlabel("Distancia rendija-caja (mm)")
plt.ylabel("Distancia del radio completo (mm)")
plt.title(f"Distancia rendija-caja vs Distancia del radio complejo, = {round(m,3)} ± {round(std_err,3)}")
plt.legend()
plt.grid()
plt.show()