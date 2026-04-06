import numpy as np
from tabulate import tabulate
from scipy.stats import linregress # parahacer el ajuste lineal 
import matplotlib.pyplot as plt 


#en mm, error = 0,02mm
m_error = np.array([[0,0.2],
                    [0,0.2],
                    [0,0.2],
                    [0,0.2],
                    [0,0.2],
                    [0,0.2],
                    [0, 0.2]])

papel_suave_1 = np.array([[1,14.7],
                        [2, 17.9],
                        [4, 23.2],
                        [8, 33],
                        [16, 37.3],
                        [32, 61.4],
                        [64, 73.7]])

papel_suave_2 = np.array([[1,14.6],
                        [2, 22.2],
                        [4, 35.8],
                        [8, 38.5],
                        [16, 54.8],
                        [32, 78.2],
                        [64, 119.2]])

papel_suave_3 = np.array([[1,17.7],
                            [2, 27.4],
                            [4, 32.1],
                            [8, 39.6],
                            [16, 47.7],
                            [32, 72.5],
                            [64, 115.3]])

papel_suave_4 = np.array([[1,18.6],
                            [2, 30.1],
                            [4, 33],
                            [8, 43.1],
                            [16, 46.9],
                            [32, 73.7],
                            [64, 113.1]])

papel_suave_5 = np.array([[1,17.3],
                            [2, 24.6],
                            [4, 36.2],
                            [8, 47.8],
                            [16, 51.5],
                            [32, 72.2],
                            [64, 110.4]])

papel_suave_6 = np.array([[1,14.7],
                            [2, 23.3],
                            [4, 31.1],
                            [8, 45.4],
                            [16, 52.7],
                            [32, 80.6],
                            [64, 110.1]])

papel_suave_7 = np.array([[1,15.4],
                            [2, 22.2],
                            [4, 30.2],
                            [8, 43.1],
                            [16, 51.2],
                            [32, 80.7],
                            [64, 117]])


papel_aluminio_1 = np.array([[1, 10.1],
                        [2, 12.4],
                        [4, 18.1],
                        [8, 21.3],
                        [16, 28.1],
                        [32, 35.6],
                        [64, 52.6]])

papel_aluminio_2 =np.array([[1,10.4],
                        [2, 11.6],
                        [4, 16.5],
                        [8, 22.1],
                        [16, 28],
                        [32, 37.1],
                        [64, 50.5]])

papel_aluminio_3 = np.array([[1,9.8],
                        [2, 11.5],
                        [4, 16.2],
                        [8, 22],
                        [16, 27.9],
                        [32, 36.7],
                        [64, 56]])

papel_aluminio_4 = np.array([[1,10],
                        [2, 11.2],
                        [4, 15.9],
                        [8, 21.1],
                        [16, 24.3],
                        [32, 32.4],
                        [64, 51.7]])


papel_aluminio_4 = np.array([[1,8.2],
                        [2, 11.2],
                        [4, 16.7],
                        [8, 18.2],
                        [16, 25.3],
                        [32, 35.3],
                        [64, 56.2]])

papel_aluminio_5 = np.array([[1,10.6],
                        [2, 12.3],
                        [4, 16.9],
                        [8, 18.9],
                        [16, 28.6],
                        [32, 32.6],
                        [64, 57.3]])

papel_aluminio_6 = np.array([[1,10.5],
                        [2, 11.5],
                        [4, 17.6],
                        [8, 21.9],
                        [16, 25.9],
                        [32, 35.7],
                        [64, 52.1]])

papel_aluminio_7 = np.array([[1,10.8],
                        [2, 12.9],
                        [4, 17],
                        [8, 20.5],
                        [16, 25.6],
                        [32, 38.1],
                        [64, 50.1]])

papel_comprimido_1 = np.array([[1, 10.2],
                        [2, 15.4],
                        [4, 22.5],
                        [8, 24.1],
                        [16, 36.2],
                        [32, 50.4],
                        [64, 66.6]])

papel_comprimido_2 = np.array([[1, 11.3],
                        [2, 14.4],
                        [4, 29.5],
                        [8, 29.6],
                        [16, 36],
                        [32, 49.4],
                        [64, 55.8]])

papel_comprimido_3 = np.array([[1, 10],
                        [2, 16.5],
                        [4, 25.1],
                        [8, 30.7],
                        [16, 33.5],
                        [32, 51.9],
                        [64, 65.6]])

papel_comprimido_4 = np.array([[1, 10.1],
                        [2, 14.3],
                        [4, 22.2],
                        [8, 29.5],
                        [16, 35.7],
                        [32, 49.6],
                        [64, 63.7]])

papel_comprimido_5 = np.array([[1, 10.4],
                        [2, 15.6],
                        [4, 24.8],
                        [8, 29.7],
                        [16, 36.5],
                        [32, 50.2],
                        [64, 65.2]])

papel_comprimido_6 = np.array([[1, 11.1],
                        [2, 16.7],
                        [4, 20.3],
                        [8, 26.1],
                        [16, 33.4],
                        [32, 48.2],
                        [64, 60.6]])

papel_comprimido_7 = np.array([[1, 12.4],
                        [2, 14.1],
                        [4, 21.4],
                        [8, 23],
                        [16, 38.4],
                        [32, 44.5],
                        [64, 57.5]])

papel_suave = [papel_suave_1, papel_suave_2, papel_suave_3, papel_suave_4, papel_suave_5, papel_suave_6, papel_suave_7]
papel_aluminio = [papel_aluminio_1, papel_aluminio_2, papel_aluminio_3, papel_aluminio_4, papel_aluminio_5, papel_aluminio_6,papel_aluminio_7]
papel_comprimido = [papel_comprimido_1, papel_comprimido_2, papel_comprimido_3, papel_comprimido_4, papel_comprimido_5, papel_comprimido_6,papel_comprimido_7]

papel_comprimido_img= np.array([[1,126.061],
                        [2, 338.813],
                        [4, 411.11],
                        [8, 722.904],
                        [16, 1276.177],
                        [32, 2305.782],
                        [64, 3905.996]])

papel_aluminio_img = np.array([[1, 68.578],
                           [2, 102.184],
                           [4, 188.383],
                           [8, 422.367],
                           [16, 615.74],
                           [32, 1066.163],
                           [64, 3125.95]])

papel_suave_img = np.array([[1, 270.303],
                        [2, 737.06],
                        [4, 956.744],
                        [8, 2163.926],
                        [16, 2461.446],
                        [32, 6372.170],
                        [64, 13444.336]])


masas = np.transpose(papel_comprimido_img)[0].astype(int)

areas_comprimido_img = np.transpose(papel_comprimido_img)[1].astype(float)
areas_aluminio_img = np.transpose(papel_aluminio_img)[1].astype(float)
areas_suave_img = np.transpose(papel_suave_img)[1].astype(float)



d_comprimido = [ round(float(np.sqrt(i/np.pi) *2), 2) for i in areas_comprimido_img]
d_aluminio = [ round(float(np.sqrt(i/np.pi) *2), 2) for i in areas_aluminio_img]
d_suave = [ round(float(np.sqrt(i/np.pi) *2), 2) for i in areas_suave_img]


for i in papel_suave:
    valores_d_exp = np.transpose(i)[1].astype(float)
    print("Los valores de imagej son:", d_suave)
    print("Los valores experimentales son:", valores_d_exp)
    #print(np.subtract(np.array(valores_d_exp), np.array(d_suave)))

log_masas = np.log(masas)
log_d_comprimido = np.log(d_comprimido)
log_d_aluminio = np.log(d_aluminio)
log_d_suave = np.log(d_suave)

m_comprimido, b_comprimido, r_value, p_value, std_err_comprimido = linregress(log_masas, log_d_comprimido)
m_aluminio, b_aluminio, r_value, p_value, std_err_aluminio = linregress(log_masas, log_d_aluminio)
m_suave, b_suave, r_value, p_value, std_err_suave = linregress(log_masas, log_d_suave)


print(f"\n--- Análisis Serie A (Papel Suave) con ImageJ ---")
print(f"Pendiente (m): {m_suave:.5f}")
print(f"Error de la pendiente (Δm_imagen): {std_err_suave:.5f}")
print(f"Dimensión fractal (d = 1/m): {1/m_suave:.3f}")

print(f"\n--- Análisis Serie B (Papel Comprimido) con ImageJ ---")
print(f"Pendiente (m): {m_comprimido:.5f}")
print(f"Error de la pendiente (Δm_imagen): {std_err_comprimido:.5f}")
print(f"Dimensión fractal (d = 1/m): {1/m_comprimido:.3f}")

print(f"\n--- Análisis Serie C (Papel Aluminio) con ImageJ ---")
print(f"Pendiente (m): {m_aluminio:.5f}")
print(f"Error de la pendiente (Δm_imagen): {std_err_aluminio:.5f}")
print(f"Dimensión fractal (d = 1/m): {1/m_aluminio:.3f}")

d_suave_exp = np.mean([np.transpose(p)[1] for p in papel_suave], axis=0)
d_aluminio_exp = np.mean([np.transpose(p)[1] for p in papel_aluminio], axis=0)
d_comprimido_exp = np.mean([np.transpose(p)[1] for p in papel_comprimido], axis=0)

m_suave_exp, _, _, _, std_err_suave_exp = linregress(log_masas, np.log(d_suave_exp))
m_alum_exp, _, _, _, std_err_alum_exp = linregress(log_masas, np.log(d_aluminio_exp))
m_comp_exp, _, _, _, std_err_comp_exp = linregress(log_masas, np.log(d_comprimido_exp))

# Agrupamos los datos en una lista de listas (3 filas)
filas_resultados = [
    ["Papel Suave", round(m_suave_exp, 5), round(m_suave, 5), round(std_err_suave_exp, 5), round(std_err_suave, 5)],
    ["Papel Aluminio", round(m_alum_exp, 5), round(m_aluminio, 5), round(std_err_alum_exp, 5), round(std_err_aluminio, 5)],
    ["Papel Comprimido", round(m_comp_exp, 5), round(m_comprimido, 5), round(std_err_comp_exp, 5), round(std_err_comprimido, 5)]
]

# Definimos los headers tal como pediste (con el formato correcto para LaTeX)
headers = [r"\textbf{Papel}", r"$m_{exp}$", r"$m_{img}$", r"$\Delta m_{exp}$", r"$\Delta m_{img}$"]

print("\n" + "="*70)
print("CÓDIGO LATEX GENERADO PARA LA MEMORIA (Copia y pega en fractales.tex):")
print("="*70)

# Usamos tablefmt="latex_booktabs" que queda mucho más elegante sin líneas verticales
tabla_latex = tabulate(filas_resultados, headers=headers, tablefmt="latex_booktabs")

# Añadimos el entorno de tabla y el caption
print(r"\begin{table}[h]")
print(r"\centering")
print(tabla_latex)
print(r"\caption{Comparativa de la pendiente $m$ y su error estándar $\Delta m$ obtenidos experimentalmente frente al análisis de imagen.}")
print(r"\label{tab:comparativa_errores}")
print(r"\end{table}")