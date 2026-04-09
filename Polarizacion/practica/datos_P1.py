import numpy as np
import matplotlib.pyplot as plt
import tabulate as tb

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


grados = np.transpose(pol_per)[0]

err_grados = [r"$\pm 0.5$"] * len(grados)

err_int = [r"$\pm 0.01$"] * len(grados)

intensidadv = np.transpose(pol_ver)[1]

intensidadp = np.transpose(pol_per)[1]

intensidadv_norm = intensidadv / np.max(intensidadv)

intensidadp_norm = intensidadp / np.max(intensidadp)

minv = min(intensidadv_norm)
minp = min(intensidadp_norm)

minimov = grados[np.argmin(intensidadv_norm)]
minimop = grados[np.argmin(intensidadp_norm)]


print(minimov)
print(minimop)


plt.scatter(grados, intensidadv_norm, label='Vertical')
plt.scatter(grados, intensidadp_norm, label='Horizontal')
plt.errorbar(grados, intensidadv_norm, xerr=0.5, yerr=0.01, fmt="o", ecolor="red", capsize=5)
plt.errorbar(grados, intensidadp_norm, xerr=0.5, yerr=0.01, fmt="o", ecolor="red", capsize=5)
plt.xlabel('Grados')
plt.ylabel('Intensidad')
plt.title('Ángulo -- Intensidad normalizada')
plt.legend()
plt.grid(True)
plt.show()


plt.show()

titulos = [r"$\theta (\degrees)$", r"I (mw)", r"$\delta \theta (\degrees)$", r"\delta I (mw)"]

tablav = tb.tabulate(np.transpose([grados, intensidadv, err_grados, err_int]), headers=titulos, tablefmt="latex_raw")

tablap = tb.tabulate(np.transpose([grados, intensidadp, err_grados, err_int]), headers=titulos, tablefmt="latex_raw")

print(tablav)

print(tablap)


