import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class SimuladorPolarizacion(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de la Elipse de Polarización")
        self.geometry("900x550")
        
        self.t_val = 0.0 #tiempo usado para el giro constante 

        self.crear_interfaz()
        self.actualizar_stokes()
        self.animar_grafico()

    def crear_interfaz(self):
        # Creamos un panel izquierdo que llene todo el espacio y que va a albergar los botones
        self.panel_controles = ctk.CTkFrame(self, width=300)
        self.panel_controles.pack(side="left", fill="y", padx=20, pady=20)

        ctk.CTkLabel(self.panel_controles, text="Controles de Entrada", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))

        # Variables de entrada, campos de entrada y el ángulo de giro
        self.e0x = ctk.DoubleVar(value=1.0)
        self.e0y = ctk.DoubleVar(value=1.0)
        self.delta = ctk.DoubleVar(value=np.pi / 2) # Empieza en pi/2 (polarización circular)

        # E0x
        ctk.CTkLabel(self.panel_controles, text="Amplitud E0x (0 a 1)").pack(anchor="w", padx=10)
        self.slider_e0x = ctk.CTkSlider(self.panel_controles, from_=0, to=1, variable=self.e0x, command=self.actualizar_stokes)
        self.slider_e0x.pack(fill="x", padx=10, pady=(0, 15))

        # Slider E0y
        ctk.CTkLabel(self.panel_controles, text="Amplitud E0y (0 a 1)").pack(anchor="w", padx=10)
        self.slider_e0y = ctk.CTkSlider(self.panel_controles, from_=0, to=1, variable=self.e0y, command=self.actualizar_stokes)
        self.slider_e0y.pack(fill="x", padx=10, pady=(0, 15))

        # Slider Desfase (Delta)
        ctk.CTkLabel(self.panel_controles, text="Desfase δ (0 a 2π rad)").pack(anchor="w", padx=10)
        self.slider_delta = ctk.CTkSlider(self.panel_controles, from_=0, to=2*np.pi, variable=self.delta, command=self.actualizar_stokes)
        self.slider_delta.pack(fill="x", padx=10, pady=(0, 25))

        # Panel para Parámetros de Stokes
        self.panel_stokes = ctk.CTkFrame(self.panel_controles)
        self.panel_stokes.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.panel_stokes, text="Parámetros de Stokes", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        self.lbl_stokes = ctk.CTkLabel(self.panel_stokes, text="", justify="left", font=ctk.CTkFont(family="monospace", size=20))
        self.lbl_stokes.pack(pady=5, padx=10, anchor="w")

        # HAcemos un panel donde estará el canvas que estará dibujando todo el rato la animación
        self.panel_grafico = ctk.CTkFrame(self)
        self.panel_grafico.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        # Configuración de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 5), facecolor="#FFFFFF")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_stokes(self, event=None):
        """Calcula y actualiza los parámetros de Stokes en la interfaz."""
        e0x_val = self.e0x.get()
        e0y_val = self.e0y.get()
        delta_val = self.delta.get()

        s0 = e0x_val**2 + e0y_val**2
        s1 = e0x_val**2 - e0y_val**2
        s2 = 2 * e0x_val * e0y_val * np.cos(delta_val)
        s3 = 2 * e0x_val * e0y_val * np.sin(delta_val)

        texto_stokes = f"S0 = {s0:.3f}\nS1 = {s1:.3f}\nS2 = {s2:.3f}\nS3 = {s3:.3f}"
        self.lbl_stokes.configure(text=texto_stokes)

    def animar_grafico(self):
        """Dibuja la elipse y el punto animado en tiempo real."""
        e0x_val = self.e0x.get()
        e0y_val = self.e0y.get()
        delta_val = self.delta.get()

        # Dibujamos la trayectoria completa (la elipse estática de fondo)
        t_completo = np.linspace(0, 2*np.pi, 100)
        ex_completo = e0x_val * np.cos(t_completo)
        ey_completo = e0y_val * np.cos(t_completo + delta_val)

        # Calculamos la posición del punto en el instante actual t_val
        ex_punto = e0x_val * np.cos(self.t_val)
        ey_punto = e0y_val * np.cos(self.t_val + delta_val)

        self.ax.clear()
        
        # Plot de la elipse (línea punteada azul) y el punto actual (rojo)
        self.ax.plot(ex_completo, ey_completo, 'b--', alpha=0.5, label='Trayectoria')
        self.ax.plot(ex_punto, ey_punto, 'ro', markersize=8, label='Vector $\\vec{E}$')
        
        # Dibujar el vector desde el origen hasta el punto
        self.ax.arrow(0, 0, ex_punto, ey_punto, head_width=0.05, head_length=0.08, fc='red', ec='red', alpha=0.7)

        # Configuración estética del gráfico
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.set_aspect('equal')
        self.ax.set_title("Plano Transversal a la Propagación")
        self.ax.set_xlabel("$E_x$")
        self.ax.set_ylabel("$E_y$")
        self.ax.grid(True, linestyle=':', alpha=0.6)

        self.canvas.draw()

        # Avanzar el tiempo
        self.t_val += 0.1
        if self.t_val > 2*np.pi:
            self.t_val = 0

        # Programar el próximo frame en 50 milisegundos (20 FPS aprox)
        self.after(50, self.animar_grafico)

if __name__ == "__main__":
    app = SimuladorPolarizacion()
    app.mainloop()