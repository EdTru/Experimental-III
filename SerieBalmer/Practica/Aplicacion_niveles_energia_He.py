import csv
import os
from tabulate import tabulate
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
import tkinter as tk
from PIL import Image

h = const.h
c = const.c
e = const.e

os.chdir(os.path.dirname(os.path.realpath(__file__)))

terminos_espectroscopicos = {
	"S":1,
	"P":2,
	"D":3,
	"F":4,
	"G":5
}


orb = []
term_espc = []
nombre_orb = []
J = []
L = []
S = []
E_n = []

with open("niveles_energia.csv", "r", newline='', encoding='utf-8') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		orb.append(row[0][2:4]+row[0][5:7])
		term_espc.append(row[1][2:4])


		J.append(row[2][2:3])
		L.append(terminos_espectroscopicos[row[1][3:4]])
		S.append(int((int(row[1][2:3])-1)/2))

		nombre_orb.append(row[0][2:4]+row[0][5:7]+"   "+row[1][2:4]+"   "+row[2][2:3])

		E_n.append(np.float64(row[4][2:-1]))


class GUI(ctk.CTk):

	def __init__(self):
		super().__init__()
		self.title("Niveles Energeticos del Helio - NIST")
		self.geometry("1500x1000")
		self.resizable(False, False)
		self.configure(fg_color="#0d0f1a")
		self.construir_interfaz()

	def construir_interfaz(self):
		self.grid_columnconfigure(0, minsize=250)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, minsize=210)
		self.grid_rowconfigure(0, weight=1)

		panel_izquierdo = ctk.CTkFrame(self, fg_color="#12152b", corner_radius=16,
										border_width=1, border_color="#2e3250")
		panel_izquierdo.grid(row=0, column=0, padx=(14, 7), pady=14, sticky="nsew")
		panel_izquierdo.grid_rowconfigure(5, weight=1)

		cuadro_selector = ctk.CTkFrame(panel_izquierdo, fg_color="transparent")
		cuadro_selector.grid(row=2, column=0, columnspan=2, padx=14, pady=(10, 4), sticky="ew")

		ctk.CTkLabel(cuadro_selector, text="Nivel superior (m)",
					 font=ctk.CTkFont("Courier", 10),
					 text_color="#9098c0").pack(anchor="w")

		self.seleccion_emisor = ctk.CTkOptionMenu(
			cuadro_selector, values=nombre_orb, width=220,
			font=ctk.CTkFont("Courier", 10),
			fg_color="#1e2240", button_color="#3a4070",
			text_color="#d0d8ff",
			command=self.cambiar_seleccion)

		self.seleccion_emisor.pack(anchor="w", pady=(2, 0))
		self.seleccion_emisor.set(nombre_orb[6])

		ctk.CTkLabel(cuadro_selector, text="Nivel inferior (n)",
					 font=ctk.CTkFont("Courier", 10),
					 text_color="#9098c0").pack(anchor="w")

		self.seleccion_receptor = ctk.CTkOptionMenu(
			cuadro_selector, values=nombre_orb, width=220,
			font=ctk.CTkFont("Courier", 10),
			fg_color="#1e2240", button_color="#3a4070",
			text_color="#d0d8ff",
			command=self.cambiar_seleccion)

		self.seleccion_receptor.pack(anchor="w", pady=(2, 0))
		self.seleccion_receptor.set(nombre_orb[0])

		self.btn = ctk.CTkButton(
			panel_izquierdo, text="CALCULAR",
			font=ctk.CTkFont("Courier", 12, "bold"),
			fg_color="#5060ee", hover_color="#3a4ac0",
			corner_radius=10, command=self.calcular)
		self.btn.grid(row=3, column=0, columnspan=2,
					  padx=14, pady=(6, 4), sticky="ew")

		self.validez = ctk.CTkLabel(panel_izquierdo, text="",
									  font=ctk.CTkFont("Courier", 10),
									  text_color="#ff6b6b", wraplength=210)
		self.validez.grid(row=4, column=0, columnspan=2,
							padx=14, pady=(0, 4), sticky="w")

		ctk.CTkFrame(panel_izquierdo, height=1, fg_color="#2e3250").grid(
			row=5, column=0, columnspan=2,
			sticky="ew", padx=10, pady=2)

		ctk.CTkLabel(panel_izquierdo, text="RESULTADOS",
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").grid(
			row=6, column=0, columnspan=2, pady=(14, 4), padx=14)

		cuadro_respuestas = ctk.CTkFrame(panel_izquierdo, fg_color="transparent")
		cuadro_respuestas.grid(row=7, column=0, columnspan=2, padx=14, pady=(4, 10), sticky="ew")


		for sym, unit, attr in [("dE", "eV",  "lbl_dE"),
								 ("λ",  "nm",  "lbl_lam"),
								 ("f",  "THz", "lbl_f")]:
			ctk.CTkLabel(cuadro_respuestas, text=f"{sym}  ({unit})",
						 font=ctk.CTkFont("Courier", 10),
						 text_color="#7880aa").pack(anchor="w", pady=(6, 0))
			lbl = ctk.CTkLabel(cuadro_respuestas, text="--",
							   font=ctk.CTkFont("Courier", 13, "bold"),
							   text_color="#e8eaff")
			lbl.pack(anchor="w")
			setattr(self, attr, lbl)

		centro = ctk.CTkFrame(self, fg_color="#101318", corner_radius=16,
							  border_width=1, border_color="#2e3250")
		centro.grid(row=0, column=1, padx=7, pady=14, sticky="nsew")

		my_image = ctk.CTkImage(
    light_image=Image.open("EspectroHelioTeo.png"),
    dark_image=Image.open("EspectroHelioTeo.png"),
    size=(1000, 1000)  # Ancho x Alto
)

		foto = ctk.CTkLabel(centro,text="",image=my_image)
		foto.pack()

		panel_derecho = ctk.CTkFrame(self, fg_color="#12152b", corner_radius=16,
							 border_width=1, border_color="#2e3250")
		panel_derecho.grid(row=0, column=2, padx=(7, 14), pady=14, sticky="nsew")
		panel_derecho.grid_rowconfigure(3, weight=1)

		ctk.CTkLabel(panel_derecho, text="COLOR",
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").grid(
			row=0, column=0, columnspan=2, pady=(14, 4), padx=14)
		ctk.CTkFrame(panel_derecho, height=1, fg_color="#2e3250").grid(
			row=1, column=0, columnspan=2,
			sticky="ew", padx=10, pady=2)

		self.color_canvas = tk.Canvas(panel_derecho, width=150, height=130,
									  bg="#0d0f1a", highlightthickness=0)
		self.color_canvas.grid(row=2, column=0, padx=28, pady=22)
		self.color_rect = self.color_canvas.create_rectangle(
			8, 8, 142, 122, fill="#1e2240", outline="#3a3e5c", width=2)

		self.lbl_hex = ctk.CTkLabel(panel_derecho, text="--",
									font=ctk.CTkFont("Courier", 11),
									text_color="#a0a8d0")
		self.lbl_hex.grid(row=3, column=0, pady=(0, 4))

		self.lbl_color_name = ctk.CTkLabel(panel_derecho, text="",
										   font=ctk.CTkFont("Courier", 10),
										   text_color="#6070a0")
		self.lbl_color_name.grid(row=4, column=0, pady=(0, 6))
		


	def cambiar_seleccion(self, _=None):
		pass

	def calcular(self):
		m_ind = nombre_orb.index(self.seleccion_emisor.get())
		n_ind = nombre_orb.index(self.seleccion_receptor.get())

		if self.comprobar_validez(m_ind=m_ind,n_ind=n_ind):
			deltaE = E_n[m_ind]-E_n[n_ind]
			lamd = h*c/(deltaE*e) * 10**9
			freq = c/lamd
			

			self.lbl_dE.configure(text=f"{deltaE:.4f} eV")
			self.lbl_lam.configure(text=f"{lamd:.3f} nm")
			self.lbl_f.configure(text=f"{freq:.4f} THz")

			self.cambiar_color(lamd)



	def comprobar_validez(self, m_ind, n_ind):
		razones = []
		if E_n[m_ind] -E_n[n_ind] <= 0:
			razones.append("El nivel superior debe tener mas energía")
		if S[m_ind] != S[n_ind]:
			razones.append("El espín total S no debe cambiar")
		if np.abs(L[m_ind]-L[n_ind]) != 1:
			razones.append("El cambio en L debe ser de +-1")

		if razones == []:
			self.validez.configure(
				text="OK  Transicion permitida", text_color="#6bff9e")
			return True

		self.validez.configure(
				text="X  " + " | ".join(razones), text_color="#ff6b6b")

		return False

	def cambiar_color(self, lamd):
		if 380 <= lamd <= 780:
			rgb = self.wavelength_to_rgb(lamd)
			hx  = self.rgb_to_hex(rgb)
			self.color_canvas.itemconfig(self.color_rect, fill=hx, outline=hx)
			self.lbl_hex.configure(text=hx)
		else:
			self.color_canvas.itemconfig(
				self.color_rect, fill="#1e2240", outline="#3a3e5c")
			self.lbl_hex.configure(text=f"{lamd:.2f} nm")

	def wavelength_to_rgb(self, lam_nm: float):
		if lam_nm < 380 or lam_nm > 780:
			return (160, 160, 160)
		if   lam_nm < 440: r, g, b = (440 - lam_nm) / 60, 0.0, 1.0
		elif lam_nm < 490: r, g, b = 0.0, (lam_nm - 440) / 50, 1.0
		elif lam_nm < 510: r, g, b = 0.0, 1.0, (510 - lam_nm) / 20
		elif lam_nm < 580: r, g, b = (lam_nm - 510) / 70, 1.0, 0.0
		elif lam_nm < 645: r, g, b = 1.0, (645 - lam_nm) / 65, 0.0
		else:              r, g, b = 1.0, 0.0, 0.0
		factor = (0.3 + 0.7*(lam_nm-380)/40 if lam_nm < 420 else
				  0.3 + 0.7*(780-lam_nm)/80 if lam_nm > 700 else 1.0)
		return (int(r*factor*255), int(g*factor*255), int(b*factor*255))

	def rgb_to_hex(self, rgb):
		return "#{:02x}{:02x}{:02x}".format(*rgb)





		

		



	

if __name__ == "__main__":
	app = GUI()
	app.mainloop()