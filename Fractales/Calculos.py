import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from Datos_practica import *

masa_relativa = np.transpose(papel_suave[0])[0]
log_masa_relativa = np.log(masa_relativa)

diametros = np.transpose(np.transpose(papel_suave)[1])
log_diametros = np.log(diametros)


for i in range(7):

	def test_function(x,a,b):
		return a*x+b

	param, param_cov = curve_fit(test_function, log_masa_relativa, log_diametros[i])

	fit_f = param[0]* log_masa_relativa +param[1]

	print(param[0])

	# Graficar la señal original y la reconstruida

	plt.subplot(1, 1, 1)
	plt.scatter(log_masa_relativa, log_diametros[i])
	plt.plot(log_masa_relativa, fit_f)
	plt.xlabel("log(masa relativa)")
	plt.ylabel("log(diametros)")
	plt.title("Scatter Plot m=")

	plt.show()