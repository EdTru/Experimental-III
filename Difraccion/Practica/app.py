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
app.title("Difracción - App sencilla")

# =========================
# FUNCIONES GENERALES
# =========================

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

#ahroa vamos a crear el contenido de la primera tab 

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

ctk.CTkButton(frame_inputs, text="Simular", command=simular_rendija).pack(pady=10)

# Datos experimentales
ctk.CTkLabel(frame_inputs, text="D (m)", font=("Arial", 18)).pack()
entry_D = ctk.CTkEntry(frame_inputs, font=("Arial", 16))
entry_D.insert(0, "1,1.5,2")
entry_D.pack()

ctk.CTkLabel(frame_inputs, text="Xmin (m)", font=("Arial", 18)).pack()
entry_X = ctk.CTkEntry(frame_inputs, font=("Arial", 16))
entry_X.insert(0, "0.005,0.007,0.01")
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

# =========================
# TAB 2: RED
# =========================

frame_red = ctk.CTkFrame(tab2)
frame_red.pack(padx=10, pady=10)

ctk.CTkLabel(frame_red, text="λ (m)").pack()
entry_lambda2 = ctk.CTkEntry(frame_red)
entry_lambda2.insert(0, "6.5e-7")
entry_lambda2.pack()

ctk.CTkLabel(frame_red, text="D (m)").pack()
entry_D2 = ctk.CTkEntry(frame_red)
entry_D2.insert(0, "1,1.5,2")
entry_D2.pack()

ctk.CTkLabel(frame_red, text="Xmax (m)").pack()
entry_X2 = ctk.CTkEntry(frame_red)
entry_X2.insert(0, "0.01,0.015,0.02")
entry_X2.pack()

label_red = ctk.CTkLabel(frame_red, text="")
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

ctk.CTkButton(frame_red, text="Calcular N", command=calcular_red).pack()

# =========================
# TAB 3: ESPECTRO
# =========================

frame_spec = ctk.CTkFrame(tab3)
frame_spec.pack(padx=10, pady=10)

ctk.CTkLabel(frame_spec, text="θ (rad)").pack()
entry_theta = ctk.CTkEntry(frame_spec)
entry_theta.insert(0, "0.1,0.12,0.15")
entry_theta.pack()

label_spec = ctk.CTkLabel(frame_spec, text="")
label_spec.pack(pady=10)

def calcular_espectro():
    global N_global

    if N_global is None:
        label_spec.configure(text="Primero calcula N")
        return

    theta = np.array([float(x) for x in entry_theta.get().split(",")])
    d = 1/(2*N_global)

    lambdas = 2*d*np.sin(theta)

    texto = "\n".join([f"{l:.2e} m" for l in lambdas])
    label_spec.configure(text=texto)

    # gráfico simple
    plt.figure()
    for l in lambdas:
        plt.axvline(l)
    plt.title("Espectro")
    plt.xlabel("λ (m)")
    plt.show()

ctk.CTkButton(frame_spec, text="Calcular λ", command=calcular_espectro).pack()

# =========================

app.mainloop()