import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Difracción - Parte computacional")

#empezamos definiendo un ajuste lineal

def ajuste_lineal(x, y):
    resultado = linregress(x, y)
    return resultado.slope, resultado.intercept

#ventanas por las que podemos navegar
custom_font = ctk.CTkFont(family="Helvetica", size=24)

tab_pers = ctk.CTkTabview(
    app,
    width=600,
    height=250,
    corner_radius=10,
    fg_color="black",
    segmented_button_fg_color="blue",
    segmented_button_selected_color="#1892B0",
    segmented_button_selected_hover_color="red",
    segmented_button_unselected_color="#1892B0",
    text_color="white",
)
tab_pers.pack(fill="both", expand=True, padx=10, pady=10)

tab1 = tab_pers.add("Rendija")
tab2 = tab_pers.add("Red")
tab3 = tab_pers.add("Espectro")

#--------------------------------------------------------------------------------------------------------------
#ahora vamos a crear el contenido de la primera tab 
#--------------------------------------------------------------------------------------------------------------

frame_inputs = ctk.CTkFrame(tab1)
frame_inputs.pack(side="left", fill="y", padx=10, pady=10)

frame_plotear = ctk.CTkFrame(tab1)
frame_plotear.pack(side="right", fill="both", expand=True, padx=10, pady=10)



ctk.CTkLabel(frame_inputs, text="λ (m)", font=("Arial", 18)).pack()
entry_lambda = ctk.CTkEntry(frame_inputs, font=("Arial", 16)) # para introducir la longitud de onda por el teclado
entry_lambda.configure(width = 200, height = 30 )
entry_lambda.insert(0, "6.5e-7")
entry_lambda.pack()

ctk.CTkLabel(frame_inputs, text="2a (m)", font=("Arial", 18)).pack() #para introductir la distancia entre las rendijas por el teclado
entry_a = ctk.CTkEntry(frame_inputs, font=("Arial", 16))
entry_a.configure(width = 200, height = 30 )
entry_a.insert(0, "1e-4")
entry_a.pack()

fig = Figure(figsize=(5,4), dpi=100)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=frame_plotear) #creamos un canvas para dibujar la figura representada  ala derecha
canvas.get_tk_widget().pack(fill="both", expand=True)

def simular_rendija():
    lam = float(entry_lambda.get())
    a = float(entry_a.get())

    theta = np.linspace(-0.01, 0.01, 500)#límites de los ángulos a representar
    beta = np.pi * a * np.sin(theta) / lam
    I = (np.sin(beta)/beta)**2

    ax.clear()
    ax.plot(theta, I, linewidth=2, color="cyan")
    ax.set_title("Difracción rendija")
    ax.set_xlabel("θ")
    ax.set_ylabel("Intensidad")
    ax.set_facecolor("#484848")
    ax.grid()

    canvas.draw()

def representacion_lineal():
    D = np.array([float(x) for x in entry_D.get().split(",")])
    X = np.array([float(x) for x in entry_X.get().split(",")])

    ax.clear()
    ax.scatter(D, X, color="#2AC527", label="Datos experimentales")
    m, b = ajuste_lineal(D, X)
    ax.plot(D, m*D + b, color="#C52727", label=f"Ajuste lineal: X = {m:.2f}D + {b:.2e}")
    ax.set_title("Representación lineal")
    ax.set_xlabel("D (m)")
    ax.set_ylabel("X (m)")
    ax.set_facecolor("#484848")
    ax.grid()
    ax.legend()

    canvas.draw()

ctk.CTkButton(frame_inputs, text="Simular", command=simular_rendija).pack(pady=10)


# Datos experimentales
ctk.CTkLabel(frame_inputs, text="D (m)", font=("Arial", 18)).pack()
entry_D = ctk.CTkEntry(frame_inputs, font=("Arial", 16))
entry_D.configure(width = 200, height = 30 )
entry_D.insert(0, "1,1.5,2") #estos son un ejemplo
entry_D.pack()

ctk.CTkLabel(frame_inputs, text="Xmin (m)", font=("Arial", 18)).pack()
entry_X = ctk.CTkEntry(frame_inputs, font=("Arial", 16))
entry_X.configure(width = 200, height = 30 )
entry_X.insert(0, "0.005,0.007,0.01") #otro ejemplo de datos iniciales
entry_X.pack()

label_resultado = ctk.CTkLabel(frame_inputs, text="", font=("Arial", 18))
label_resultado.pack(pady=10)

def calcular_rendija():
    lam = float(entry_lambda.get())
    D = np.array([float(x) for x in entry_D.get().split(",")])
    X = np.array([float(x) for x in entry_X.get().split(",")])

    m, _ = ajuste_lineal(D, X)
    a = lam / m

    label_resultado.configure(text=f"2a = {a:.2e} m")

ctk.CTkButton(frame_inputs, text="Calcular 2a", command=calcular_rendija).pack()
ctk.CTkButton(frame_inputs, text="Mostrar representación lineal", command=representacion_lineal).pack(pady=10)

# --------------------------------------------------------------------------------------------------------------
#  pasamos a la segunda tab, la red de difracción
# --------------------------------------------------------------------------------------------------------------

frame_inputs_red = ctk.CTkFrame(tab2)
frame_inputs_red.pack(side="left", fill="y", padx=10, pady=10)

frame_plot_red = ctk.CTkFrame(tab2)
frame_plot_red.pack(side="right", fill="both", expand=True, padx=10, pady=10)

fig_red = Figure(figsize=(5,4), dpi=100)
ax_red = fig_red.add_subplot(111)

canvas_red = FigureCanvasTkAgg(fig_red, master=frame_plot_red) #reutilizamos el mismo canvas para la representación de la red
canvas_red.get_tk_widget().pack(fill="both", expand=True)

ctk.CTkLabel(frame_inputs_red, text="λ (m)", font=("Arial", 18)).pack()
entry_lambda2 = ctk.CTkEntry(frame_inputs_red, font=("Arial", 16))
entry_lambda2.configure(width = 200, height = 30 )
entry_lambda2.insert(0, "6.5e-7")
entry_lambda2.pack()

ctk.CTkLabel(frame_inputs_red, text="D (m)", font=("Arial", 18)).pack()
entry_D2 = ctk.CTkEntry(frame_inputs_red, font=("Arial", 16))
entry_D2.configure(width = 200, height = 30 )
entry_D2.insert(0, "1,1.5,2")
entry_D2.pack()

ctk.CTkLabel(frame_inputs_red, text="Xmax (m)", font=("Arial", 18)).pack()
entry_X2 = ctk.CTkEntry(frame_inputs_red, font=("Arial", 16))
entry_X2.configure(width = 200, height = 30)
entry_X2.insert(0, "0.01,0.015,0.02")
entry_X2.pack()

label_red = ctk.CTkLabel(frame_inputs_red, text="", font=("Arial", 18))
label_red.pack(pady=10)

# variable global simple
N_global = None

def calcular_red():
    global N_global

    lam = float(entry_lambda2.get())
    D = np.array([float(x) for x in entry_D2.get().split(",")])
    X = np.array([float(x) for x in entry_X2.get().split(",")])

    m, _ = ajuste_lineal(D, X)
    N = m / lam

    N_global = N
    label_red.configure(text=f"N = {N:.2e} líneas/m")

def representar_red():
    D = np.array([float(x) for x in entry_D2.get().split(",")])
    X = np.array([float(x) for x in entry_X2.get().split(",")])

    ax_red.clear()
    ax_red.scatter(D, X, color="#2AC527", label="Datos experimentales")
    m, b = ajuste_lineal(D, X)
    ax_red.plot(D, m*D + b, color="#00FBFF", label=f"Ajuste lineal: X = {m:.2f}D + {b:.2e}")
    ax_red.set_title("Red de difracción")
    ax_red.set_xlabel("D (m)")
    ax_red.set_ylabel("X (m)")
    ax_red.set_facecolor("#484848")
    ax_red.grid()
    ax_red.legend()

    canvas_red.draw()

ctk.CTkButton(frame_inputs_red, text="Calcular N", command=calcular_red).pack()
ctk.CTkButton(frame_inputs_red, text="Mostrar representación lineal", command=representar_red).pack(pady=10)

# --------------------------------------------------------------------------------------------------------------
# tercera tab, el espectro de difracción
# ---------------------------------------------------------------------------------------------------------------

frame_spec = ctk.CTkFrame(tab3)
frame_spec.pack(side="left", fill="y", padx=10, pady=10)

frame_spec_plot = ctk.CTkFrame(tab3)
frame_spec_plot.pack(side="right", fill="both", expand=True, padx=10, pady=10)

fig_spec = Figure(figsize=(5,4), dpi=100)
ax_spec = fig_spec.add_subplot(111)

canvas_spec = FigureCanvasTkAgg(fig_spec, master=frame_spec_plot) #reutilizamos el mismo canvas para la representación de la red
canvas_spec.get_tk_widget().pack(fill="both", expand=True)

ctk.CTkLabel(frame_spec, text="θ (rad)", font=("Arial", 18)).pack()
entry_theta = ctk.CTkEntry( frame_spec, font=("Arial", 16))
entry_theta.insert(0, "0.1,0.12,0.15")
entry_theta.pack()

label_spec = ctk.CTkLabel(frame_spec, text="", font=("Arial", 18))
label_spec.pack(pady=10)

def longitud_de_onda_a_rgb(lam, gamma=0.8):

    lam = float(lam) * 1e9 # Convertir a nanómetros para facilitar la asignación de colores

    if lam < 380:
        lam = 380
    if lam > 780:
        lam = 780
    
    # Determinar los valores RGB según la longitud de onda, aproximadamente
    if 380 <= lam <= 440:
        attenuation = 0.3 + 0.7 * (lam - 380) / (440 - 380)
        R = ((-(lam - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= lam <= 490:
        R = 0.0
        G = ((lam - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= lam <= 510:
        R = 0.0
        G = 1.0
        B = (-(lam - 510) / (510 - 490)) ** gamma
    elif 510 <= lam <= 580:
        R = ((lam - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= lam <= 645:
        R = 1.0
        G = (-(lam - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= lam <= 780:
        attenuation = 0.3 + 0.7 * (780 - lam) / (780 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    
    # Escalar a 0-255
    R = int(R * 255)
    G = int(G * 255)
    B = int(B * 255)
    
    return f'#{R:02X}{G:02X}{B:02X}'

def calcular_espectro():
    global N_global

    if N_global is None:
        label_spec.configure(text="Primero calcula N")
        return

    theta = np.array([float(x) for x in entry_theta.get().split(",")])
    d = 1/(2*N_global)

    lambdas = 2*d*np.abs(np.sin(theta))

    texto = "\n".join([f"{l:.2e} m" for l in lambdas])
    label_spec.configure(text=texto)
    print(lambdas)

    # gráfico simple
    ax_spec.clear()
    ax_spec.set_facecolor("#484848")
    ax_spec.grid()
    ax_spec.set_title("Espectro")
    ax_spec.set_xlabel("λ (m)")
    ax_spec.set_ylabel("Intensidad (u.a.)")
    
    if lambdas.size > 0:
        for l in lambdas:
            
            color = longitud_de_onda_a_rgb(l)

            ax_spec.axvline(x=l, color=color, linestyle="--", label=f"λ = {l:.2e} m")
        
        # Ajustamos los límites del eje X manualmente para que las líneas sean visibles
        margin = (np.max(lambdas) - np.min(lambdas)) * 0.2 if len(lambdas) > 1 else lambdas[0] * 0.1
        if margin == 0: margin = lambdas[0] * 0.1
        ax_spec.set_xlim(np.min(lambdas) - margin, np.max(lambdas) + margin)
        ax_spec.legend()

    canvas_spec.draw()

ctk.CTkButton(frame_spec, text="Calcular λ", command=calcular_espectro).pack()

# =========================

app.mainloop()