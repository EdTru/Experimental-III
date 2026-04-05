import customtkinter as ctk
import scipy.constants as const
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

h = const.h
c = const.c
e = const.e

niveles_helio = {
	1: -54.418,   # 1s  (estado fundamental He)
	2: -13.604,    # 2s
	3: -6.046,    # 3s
	4: -3.401,    # 4s
	5: -2.176,    # 5s
	6: -1.511,    # 6s
	7: -1.110,
	8: -0.850,
	9: -0.671
}

def energy_jump(n: int, m: int):
	"""Devuelve ΔE (eV), λ (nm) y frecuencia (Hz). n > m → emisión."""
	if n not in niveles_helio or m not in niveles_helio:
		return None, None, None
	dE_eV = niveles_helio[m] - niveles_helio[n]   # negativo → emisión
	dE_J  = abs(dE_eV) * e
	if dE_J == 0:
		return 0.0, float("inf"), 0.0
	lam_m = h * c / dE_J
	lam_nm = lam_m * 1e9
	freq   = c / lam_m
	return dE_eV, lam_nm, freq


def wavelength_to_rgb(lam_nm: float):
	"""Convierte longitud de onda visible (nm) a color RGB (0-255)."""
	if lam_nm < 380 or lam_nm > 780:
		return (180, 180, 180)  # gris si fuera del visible
	if   lam_nm < 440:
		r, g, b = (440 - lam_nm) / 60, 0, 1
	elif lam_nm < 490:
		r, g, b = 0, (lam_nm - 440) / 50, 1
	elif lam_nm < 510:
		r, g, b = 0, 1, (510 - lam_nm) / 20
	elif lam_nm < 580:
		r, g, b = (lam_nm - 510) / 70, 1, 0
	elif lam_nm < 645:
		r, g, b = 1, (645 - lam_nm) / 65, 0
	else:
		r, g, b = 1, 0, 0
	# Atenuación en extremos
	if   lam_nm < 420:  factor = 0.3 + 0.7 * (lam_nm - 380) / 40
	elif lam_nm > 700:  factor = 0.3 + 0.7 * (780 - lam_nm) / 80
	else:               factor = 1.0
	return (int(r * factor * 255), int(g * factor * 255), int(b * factor * 255))


def rgb_to_hex(rgb):
	return "#{:02x}{:02x}{:02x}".format(*rgb)

class espectroHelio(ctk.CTk):

	def __init__(self):
		super().__init__() #Ejecutamos primero el init de custom tkinter
		self.title("Espectro energético del Helio")
		self.geometry("900x580")
		self.resizable(False, False)
		self.configure(fg_color="#0f1117")

		self.interfaz()

	def interfaz(self):
		self.grid_columnconfigure(0, minsize=220)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, minsize=220)
		self.grid_rowconfigure(0, weight=1)


		#Todo lo relativo al panel izquierdo
		panel_izq = ctk.CTkFrame(self, fg_color="#1a1d2e", corner_radius=16,
							border_width=1, border_color="#2e3250")
		panel_izq.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="nsew")
		panel_izq.grid_rowconfigure(3, weight=1)

		ctk.CTkLabel(panel_izq, text="PARÁMETROS",
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").grid(row=0, column=0, columnspan=2,
											   pady=(18, 6), padx=16)

		inp_frame = ctk.CTkFrame(panel_izq, fg_color="transparent")
		inp_frame.grid(row=2, column=0, columnspan=2, pady=12, padx=16, sticky="ew")

		for i, (label, attr) in enumerate([("n (nivel superior)", "entry_n"),
											("m (nivel inferior)", "entry_m")]):
			ctk.CTkLabel(inp_frame, text=label,
						 font=ctk.CTkFont("Courier", 11),
						 text_color="#a0a8d0").grid(row=i*2, column=0,
													sticky="w", pady=(8, 2))
			entry = ctk.CTkEntry(inp_frame, width=80,
								 font=ctk.CTkFont("Courier", 14, "bold"),
								 justify="center",
								 fg_color="#0f1117", border_color="#6c7aff",
								 text_color="#e8eaff")
			entry.grid(row=i*2+1, column=0, sticky="w")
			setattr(self, attr, entry)
		
		self.btn = ctk.CTkButton(panel_izq, text="CALCULAR",
								 font=ctk.CTkFont("Courier", 12, "bold"),
								 fg_color="#6c7aff", hover_color="#4a58dd",
								 corner_radius=10, command=self.calcular,width=200)
		self.btn.grid(row=3, column=0, columnspan=2, padx=16, pady=(4, 12), sticky="sew")


		ctk.CTkLabel(panel_izq, text="RESULTADOS",
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").grid(row=5, column=0, columnspan=2,
											   pady=(10, 6), padx=16)

		res_frame = ctk.CTkFrame(panel_izq, fg_color="transparent")
		res_frame.grid(row=6, column=0, columnspan=2, padx=16, pady=(0, 18), sticky="ew")

		labels = [("ΔE", "eV", "lbl_dE"), ("λ", "nm", "lbl_lam"), ("f", "Hz", "lbl_f")]
		for i, (sym, unit, attr) in enumerate(labels):
			ctk.CTkLabel(res_frame,
						 text=f"{sym}  ({unit})",
						 font=ctk.CTkFont("Courier", 10),
						 text_color="#7880aa").grid(row=i*2, column=0, sticky="w", pady=(6, 0))
			lbl = ctk.CTkLabel(res_frame, text="—",
							   font=ctk.CTkFont("Courier", 13, "bold"),
							   text_color="#e8eaff")
			lbl.grid(row=i*2+1, column=0, sticky="w")
			setattr(self, attr, lbl)

		#Todo lo relativo al panel central
		panel_centro = ctk.CTkFrame(self, fg_color="#13162b", corner_radius=16,
							  border_width=1, border_color="#2e3250")
		panel_centro.grid(row=0, column=1, padx=8, pady=16, sticky="nsew")

		ctk.CTkLabel(panel_centro, text="Niveles energéticos del helio",
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").pack(pady=(14, 4))

		
		self.canvas = tk.Canvas(panel_centro, bg="#13162b", highlightthickness=0,
								width=420, height=480)
		self.canvas.pack(fill="both", expand=True, padx=12, pady=(0, 12))
		self.dibujar_diagrama()

		#Todo lo relativo al panel derecho
		panel_der = ctk.CTkFrame(self, fg_color="#1a1d2e", corner_radius=16,
							 border_width=1, border_color="#2e3250")
		panel_der.grid(row=0, column=2, padx=(8, 16), pady=16, sticky="nsew")
		panel_der.grid_rowconfigure(2, weight=1)

		ctk.CTkLabel(panel_der, text="COLOR",
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").grid(row=0, column=0, pady=(18, 6), padx=16)

		self.color_canvas = tk.Canvas(panel_der, width=140, height=120,
									  bg="#0f1117", highlightthickness=0)
		self.color_canvas.grid(row=2, column=0, padx=20, pady=20)
		self.color_rect = self.color_canvas.create_rectangle(
			10, 10, 130, 110, fill="#2a2d3e", outline="#3a3e5c", width=2)

		self.lbl_color_hex = ctk.CTkLabel(panel_der, text="—",
										   font=ctk.CTkFont("Courier", 11),
										   text_color="#a0a8d0")
		self.lbl_color_hex.grid(row=3, column=0, pady=(0, 8))

		self.lbl_color_desc = ctk.CTkLabel(panel_der, text="",
											font=ctk.CTkFont("Courier", 10),
											text_color="#6070a0",
											wraplength=160)
		self.lbl_color_desc.grid(row=4, column=0, pady=(0, 18), padx=10)

	def dibujar_diagrama(self, valor_n=None,valor_m=None,lamd=None):
		cv = self.canvas
		cv.delete("all")

		W, H = 420, 480
		left_margin = 60
		right_margin = 40
		top_margin = 30
		bottom_margin = 30

		# Rango energético para escalar
		e_min = min(niveles_helio.values())
		e_max = max(niveles_helio.values())
		e_range = e_max - e_min

		def e_to_y(e):
			frac = (e - e_min) / e_range
			return H - bottom_margin - frac * (H - top_margin - bottom_margin)

		# Eje Y
		cv.create_line(left_margin, top_margin, left_margin, H - bottom_margin,
					   fill="#3a3e5c", width=1)
		cv.create_text(left_margin - 12, H // 2, text="E (eV)", fill="#5a6080",
					   font=("Courier", 9), angle=90)

		# Niveles
		for n, e in niveles_helio.items():
			y = e_to_y(e)
			x1, x2 = left_margin + 20, W - right_margin - 20

			# Color del nivel
			if n == valor_n:
				color, width = "#ff6b6b", 2
			elif n == valor_m:
				color, width = "#6bffb8", 2
			else:
				color, width = "#4a5080", 1

			cv.create_line(x1, y, x2, y, fill=color, width=width)

			# Etiqueta n=
			cv.create_text(left_margin + 8, y, text=f"n={n}",
						   fill=color if n in (valor_n, valor_m) else "#606880",
						   font=("Courier", 9), anchor="e")
			# Etiqueta energía
			cv.create_text(W - right_margin - 8, y, text=f"{e:.2f}",
						   fill="#505870", font=("Courier", 8), anchor="w")

		# Flecha de transición
		if valor_n != valor_m:
			y_n = e_to_y(niveles_helio[valor_n])
			y_m = e_to_y(niveles_helio[valor_m])
			xc = (left_margin + W - right_margin) // 2

			# Color de la flecha según λ
			if lamd and 380 <= lamd <= 780:
				arrow_color = rgb_to_hex(wavelength_to_rgb(lamd))
			else:
				arrow_color = "#ffffff"

			cv.create_line(xc, y_n, xc, y_m, fill=arrow_color, width=3,
						   arrow="last" if niveles_helio[valor_n] > niveles_helio[valor_m] else "first")

			# Etiqueta λ
			mid_y = (y_n + y_m) / 2
			txt = f"λ = {lamd:.1f} nm" if lamd < 1e4 else "UV/IR"
			cv.create_text(xc + 30, mid_y, text=txt,
							   fill=arrow_color, font=("Courier", 9), anchor="w")


		

	def calcular(self):
		try:
			n = int(self.entry_n.get())
			m = int(self.entry_m.get())
		except ValueError:
			self.mostrar_error("Introduce números enteros válidos para n y m.")
			return

		if n == m:
			self.mostrar_error("n y m deben ser distintos.")
			return

		if n not in niveles_helio or m not in niveles_helio:
			self.mostrar_error(f"Niveles válidos: {list(niveles_helio.keys())}")
			return

		dE, lam, freq = energy_jump(n, m)

		# Actualizar etiquetas
		self.lbl_dE.configure(text=f"{dE:.4f} eV")
		self.lbl_lam.configure(text=f"{lam:.2f} nm" if lam < 1e6 else "IR/UV lejano")
		self.lbl_f.configure(text=f"{freq:.4e} Hz")

		# Actualizar diagrama
		self.dibujar_diagrama(valor_n=n, valor_m=m, lamd=lam)

		# Actualizar color
		self.actualiza_color(lam)

	def actualiza_color(self, lam_nm):
		if 380 <= lam_nm <= 780:
			rgb = wavelength_to_rgb(lam_nm)
			hex_col = rgb_to_hex(rgb)
			self.color_canvas.itemconfig(self.color_rect, fill=hex_col, outline=hex_col)
			self.lbl_color_hex.configure(text=hex_col)
			desc = self.descripcion_color(lam_nm)
			self.lbl_color_desc.configure(text=desc)
		else:
			self.color_canvas.itemconfig(self.color_rect, fill="#2a2d3e", outline="#3a3e5c")
			region = "Ultravioleta" if lam_nm < 380 else "Infrarrojo"
			self.lbl_color_hex.configure(text=f"{lam_nm:.1f} nm")
			self.lbl_color_desc.configure(text=f"Fuera del visible\n({region})")

	def descripcion_color(self, lam):
		if lam < 420:   return "Violeta"
		elif lam < 450: return "Violeta-Azul"
		elif lam < 490: return "Azul"
		elif lam < 510: return "Cyan"
		elif lam < 560: return "Verde"
		elif lam < 590: return "Amarillo-Verde"
		elif lam < 620: return "Naranja"
		else:           return "Rojo"


	def mostrar_error(self, msg):
		for lbl in (self.lbl_dE, self.lbl_lam, self.lbl_f):
			lbl.configure(text="—")
		self.lbl_color_hex.configure(text=msg)
		self.lbl_color_desc.configure(text="")
		self.color_canvas.itemconfig(self.color_rect, fill="#2a2d3e", outline="#ff4444")
		self.dibujar_diagrama()

if __name__ == "__main__":
	app = espectroHelio()
	app.mainloop()