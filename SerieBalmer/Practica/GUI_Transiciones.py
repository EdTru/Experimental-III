"""
GUI de niveles energéticos del Helio
=====================================
Niveles: valores espectroscópicos reales (NIST ASD, energías en eV respecto
		 al estado fundamental del He neutro).
Sistemas: Parahelio (singletes, S=0) y Ortohelio (tripletes, S=1).
Transiciones: solo EMISIÓN, con reglas de selección dipolar eléctrica:
			  ΔL = ±1,  ΔS = 0  (no hay mezcla singlete-triplete).
"""

import customtkinter as ctk
import tkinter as tk

# ── Apariencia ─────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Constantes físicas ──────────────────────────────────────────────────────
H_PLANCK = 6.62607015e-34   # J·s
C_LIGHT  = 2.99792458e8     # m/s
EV_TO_J  = 1.602176634e-19  # 1 eV en Julios

# ── Niveles energéticos reales del He (NIST ASD) ────────────────────────────
# Energías en eV respecto al estado fundamental 1s² ¹S₀  (E=0).
# Clave: (config, término)  →  valor: energía en eV
# Fuente: https://physics.nist.gov/PhysRefData/ASD/levels_form.html
#
# PARAHELIO  (S=0, singletes): 1s ns ¹S, 1s np ¹P°, 1s nd ¹D
# ORTOHELIO  (S=1, tripletes): 1s ns ³S, 1s np ³P°, 1s nd ³D
#
# Cada nivel: {"label": str, "E": float(eV), "n": int, "L": int, "S": int, "system": str}

LEVELS = [
	# ── PARAHELIO ────────────────────────────────────────────────────────────
	# 1s²  estado fundamental
	{"label": "1s2 1S0",    "E":  0.000,  "n": 1, "L": 0, "S": 0, "system": "Para"},

	# 1s 2s 1S
	{"label": "1s2s 1S0",   "E": 20.616,  "n": 2, "L": 0, "S": 0, "system": "Para"},
	# 1s 2p 1P
	{"label": "1s2p 1P1",   "E": 21.218,  "n": 2, "L": 1, "S": 0, "system": "Para"},

	# 1s 3s 1S
	{"label": "1s3s 1S0",   "E": 22.920,  "n": 3, "L": 0, "S": 0, "system": "Para"},
	# 1s 3p 1P
	{"label": "1s3p 1P1",   "E": 23.087,  "n": 3, "L": 1, "S": 0, "system": "Para"},
	# 1s 3d 1D
	{"label": "1s3d 1D2",   "E": 23.074,  "n": 3, "L": 2, "S": 0, "system": "Para"},

	# 1s 4s 1S
	{"label": "1s4s 1S0",   "E": 23.593,  "n": 4, "L": 0, "S": 0, "system": "Para"},
	# 1s 4p 1P
	{"label": "1s4p 1P1",   "E": 23.673,  "n": 4, "L": 1, "S": 0, "system": "Para"},
	# 1s 4d 1D
	{"label": "1s4d 1D2",   "E": 23.668,  "n": 4, "L": 2, "S": 0, "system": "Para"},

	# ── ORTOHELIO ────────────────────────────────────────────────────────────
	# 1s 2s 3S  (metaestable)
	{"label": "1s2s 3S1",   "E": 19.820,  "n": 2, "L": 0, "S": 1, "system": "Orto"},
	# 1s 2p 3P
	{"label": "1s2p 3P",    "E": 20.964,  "n": 2, "L": 1, "S": 1, "system": "Orto"},

	# 1s 3s 3S
	{"label": "1s3s 3S1",   "E": 22.718,  "n": 3, "L": 0, "S": 1, "system": "Orto"},
	# 1s 3p 3P
	{"label": "1s3p 3P",    "E": 23.007,  "n": 3, "L": 1, "S": 1, "system": "Orto"},
	# 1s 3d 3D
	{"label": "1s3d 3D",    "E": 23.007,  "n": 3, "L": 2, "S": 1, "system": "Orto"},

	# 1s 4s 3S
	{"label": "1s4s 3S1",   "E": 23.474,  "n": 4, "L": 0, "S": 1, "system": "Orto"},
	# 1s 4p 3P
	{"label": "1s4p 3P",    "E": 23.592,  "n": 4, "L": 1, "S": 1, "system": "Orto"},
	# 1s 4d 3D
	{"label": "1s4d 3D",    "E": 23.594,  "n": 4, "L": 2, "S": 1, "system": "Orto"},
]

LEVEL_LABELS = [lv["label"] for lv in LEVELS]


# ── Reglas de seleccion dipolar electrica ───────────────────────────────────
def allowed_transition(upper: dict, lower: dict) -> bool:
	"""
	True si upper->lower esta permitida:
		ΔS = 0   (no intercombinacion singlete-triplete)
		ΔL = ±1  (regla de paridad)
	Solo emision: E_upper > E_lower.
	"""
	if upper["E"] <= lower["E"]:
		return False
	if upper["S"] != lower["S"]:
		return False
	if abs(upper["L"] - lower["L"]) != 1:
		return False
	return True


# ── Calculo espectroscopico ──────────────────────────────────────────────────
def compute_transition(upper: dict, lower: dict):
	if not allowed_transition(upper, lower):
		return None, None, None
	dE_eV = upper["E"] - lower["E"]
	dE_J  = dE_eV * EV_TO_J
	lam_m = H_PLANCK * C_LIGHT / dE_J
	lam_nm = lam_m * 1e9
	freq   = C_LIGHT / lam_m
	return dE_eV, lam_nm, freq


# ── Conversion longitud de onda → color ─────────────────────────────────────
def wavelength_to_rgb(lam_nm: float):
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


def rgb_to_hex(rgb):
	return "#{:02x}{:02x}{:02x}".format(*rgb)


def color_name(lam_nm):
	if   lam_nm < 380: return "Ultravioleta"
	elif lam_nm < 420: return "Violeta"
	elif lam_nm < 450: return "Violeta-Azul"
	elif lam_nm < 490: return "Azul"
	elif lam_nm < 510: return "Cyan"
	elif lam_nm < 560: return "Verde"
	elif lam_nm < 590: return "Amarillo"
	elif lam_nm < 620: return "Naranja"
	elif lam_nm < 780: return "Rojo"
	else:              return "Infrarrojo"


# ── Aplicacion ───────────────────────────────────────────────────────────────
class HeliumApp(ctk.CTk):

	COLOR_PARA = "#6c9fff"
	COLOR_ORTO = "#ff7f7f"
	COLOR_DIM  = "#3a3e5c"
	COLOR_SEL  = "#ffd966"

	def __init__(self):
		super().__init__()
		self.title("Niveles Energeticos del Helio - NIST")
		self.geometry("980x640")
		self.resizable(False, False)
		self.configure(fg_color="#0d0f1a")
		self._build_layout()

	def _build_layout(self):
		self.grid_columnconfigure(0, minsize=250)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, minsize=210)
		self.grid_rowconfigure(0, weight=1)
		self._build_left_panel()
		self._build_center_panel()
		self._build_right_panel()

	# ── Panel izquierdo ──────────────────────────────────────────────────────
	def _build_left_panel(self):
		left = ctk.CTkFrame(self, fg_color="#12152b", corner_radius=16,
							border_width=1, border_color="#2e3250")
		left.grid(row=0, column=0, padx=(14, 7), pady=14, sticky="nsew")
		left.grid_rowconfigure(5, weight=1)

		self._section_label(left, "TRANSICION", row=0)
		self._separator(left, row=1)

		sel_frame = ctk.CTkFrame(left, fg_color="transparent")
		sel_frame.grid(row=2, column=0, columnspan=2, padx=14, pady=(10, 4), sticky="ew")

		ctk.CTkLabel(sel_frame, text="Nivel superior (emisor)",
					 font=ctk.CTkFont("Courier", 10),
					 text_color="#9098c0").pack(anchor="w")
		self.combo_upper = ctk.CTkOptionMenu(
			sel_frame, values=LEVEL_LABELS, width=220,
			font=ctk.CTkFont("Courier", 10),
			fg_color="#1e2240", button_color="#3a4070",
			text_color="#d0d8ff",
			command=self._on_combo_change)
		self.combo_upper.pack(anchor="w", pady=(2, 0))
		self.combo_upper.set(LEVEL_LABELS[4])   # 1s3p 1P1

		ctk.CTkLabel(sel_frame, text="Nivel inferior (destino)",
					 font=ctk.CTkFont("Courier", 10),
					 text_color="#9098c0").pack(anchor="w", pady=(10, 0))
		self.combo_lower = ctk.CTkOptionMenu(
			sel_frame, values=LEVEL_LABELS, width=220,
			font=ctk.CTkFont("Courier", 10),
			fg_color="#1e2240", button_color="#3a4070",
			text_color="#d0d8ff",
			command=self._on_combo_change)
		self.combo_lower.pack(anchor="w", pady=(2, 0))
		self.combo_lower.set(LEVEL_LABELS[2])   # 1s2p 1P1

		self.btn = ctk.CTkButton(
			left, text="CALCULAR",
			font=ctk.CTkFont("Courier", 12, "bold"),
			fg_color="#5060ee", hover_color="#3a4ac0",
			corner_radius=10, command=self.calcular)
		self.btn.grid(row=3, column=0, columnspan=2,
					  padx=14, pady=(6, 4), sticky="ew")

		self.lbl_valid = ctk.CTkLabel(left, text="",
									  font=ctk.CTkFont("Courier", 10),
									  text_color="#ff6b6b", wraplength=210)
		self.lbl_valid.grid(row=4, column=0, columnspan=2,
							padx=14, pady=(0, 4), sticky="w")

		self._separator(left, row=5)
		self._section_label(left, "RESULTADOS", row=6)

		res = ctk.CTkFrame(left, fg_color="transparent")
		res.grid(row=7, column=0, columnspan=2, padx=14, pady=(4, 10), sticky="ew")

		for sym, unit, attr in [("dE", "eV",  "lbl_dE"),
								 ("lam",  "nm",  "lbl_lam"),
								 ("f",  "THz", "lbl_f")]:
			ctk.CTkLabel(res, text=f"{sym}  ({unit})",
						 font=ctk.CTkFont("Courier", 10),
						 text_color="#7880aa").pack(anchor="w", pady=(6, 0))
			lbl = ctk.CTkLabel(res, text="--",
							   font=ctk.CTkFont("Courier", 13, "bold"),
							   text_color="#e8eaff")
			lbl.pack(anchor="w")
			setattr(self, attr, lbl)

		self._separator(left, row=8)
		leg = ctk.CTkFrame(left, fg_color="transparent")
		leg.grid(row=9, column=0, columnspan=2, padx=14, pady=(6, 14), sticky="ew")
		for color, text in [(self.COLOR_PARA, "Parahelio  (S=0, singletes)"),
							 (self.COLOR_ORTO, "Ortohelio  (S=1, tripletes)")]:
			row_f = ctk.CTkFrame(leg, fg_color="transparent")
			row_f.pack(anchor="w", pady=2)
			ctk.CTkFrame(row_f, width=12, height=12,
						 fg_color=color, corner_radius=3).pack(side="left", padx=(0, 6))
			ctk.CTkLabel(row_f, text=text,
						 font=ctk.CTkFont("Courier", 9),
						 text_color="#8090b0").pack(side="left")

	# ── Panel central ────────────────────────────────────────────────────────
	def _build_center_panel(self):
		center = ctk.CTkFrame(self, fg_color="#10132a", corner_radius=16,
							  border_width=1, border_color="#2e3250")
		center.grid(row=0, column=1, padx=7, pady=14, sticky="nsew")

		ctk.CTkLabel(center, text="DIAGRAMA DE NIVELES - He (NIST)",
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").pack(pady=(12, 4))

		self.canvas = tk.Canvas(center, bg="#10132a",
								highlightthickness=0, width=460, height=560)
		self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
		self._draw_diagram()

	# ── Panel derecho ────────────────────────────────────────────────────────
	def _build_right_panel(self):
		right = ctk.CTkFrame(self, fg_color="#12152b", corner_radius=16,
							 border_width=1, border_color="#2e3250")
		right.grid(row=0, column=2, padx=(7, 14), pady=14, sticky="nsew")
		right.grid_rowconfigure(3, weight=1)

		self._section_label(right, "COLOR", row=0)
		self._separator(right, row=1)

		self.color_canvas = tk.Canvas(right, width=150, height=130,
									  bg="#0d0f1a", highlightthickness=0)
		self.color_canvas.grid(row=2, column=0, padx=28, pady=22)
		self.color_rect = self.color_canvas.create_rectangle(
			8, 8, 142, 122, fill="#1e2240", outline="#3a3e5c", width=2)

		self.lbl_hex = ctk.CTkLabel(right, text="--",
									font=ctk.CTkFont("Courier", 11),
									text_color="#a0a8d0")
		self.lbl_hex.grid(row=3, column=0, pady=(0, 4))

		self.lbl_color_name = ctk.CTkLabel(right, text="",
										   font=ctk.CTkFont("Courier", 10),
										   text_color="#6070a0")
		self.lbl_color_name.grid(row=4, column=0, pady=(0, 6))

		self._separator(right, row=5)
		self._section_label(right, "REGLAS DE\nSELECCION", row=6)

		rules = ctk.CTkFrame(right, fg_color="transparent")
		rules.grid(row=7, column=0, padx=14, pady=(6, 14), sticky="ew")
		for rule in ["dS = 0  (no intercomb.)",
					 "dL = +/-1  (dipolar)",
					 "Solo emision  (E-alto -> E-bajo)"]:
			ctk.CTkLabel(rules, text=f"* {rule}",
						 font=ctk.CTkFont("Courier", 9),
						 text_color="#7080a0").pack(anchor="w", pady=1)

	# ── Helpers ──────────────────────────────────────────────────────────────
	def _section_label(self, parent, text, row):
		ctk.CTkLabel(parent, text=text,
					 font=ctk.CTkFont("Courier", 11, "bold"),
					 text_color="#6c7aff").grid(
			row=row, column=0, columnspan=2, pady=(14, 4), padx=14)

	def _separator(self, parent, row):
		ctk.CTkFrame(parent, height=1, fg_color="#2e3250").grid(
			row=row, column=0, columnspan=2,
			sticky="ew", padx=10, pady=2)

	# ── Diagrama ─────────────────────────────────────────────────────────────
	def _draw_diagram(self, upper=None, lower=None, lam_nm=None):
		cv = self.canvas
		cv.delete("all")

		W, H = 460, 560
		lm, rm, tm, bm = 60, 20, 40, 30

		col_para_x = lm + (W - lm - rm) * 0.28
		col_orto_x = lm + (W - lm - rm) * 0.72
		level_w = 75

		e_min = 0.0
		e_max = 24.8
		e_range = e_max - e_min

		def e_to_y(e):
			frac = (e - e_min) / e_range
			return H - bm - frac * (H - tm - bm)

		# Eje Y
		cv.create_line(lm, tm, lm, H - bm, fill="#3a3e5c", width=1)
		for ev_tick in range(0, 26, 2):
			y = e_to_y(ev_tick)
			cv.create_line(lm - 4, y, lm, y, fill="#4a5070", width=1)
			cv.create_text(lm - 6, y, text=str(ev_tick),
						   fill="#505870", font=("Courier", 7), anchor="e")
		cv.create_text(18, H // 2, text="E (eV)",
					   fill="#5a6080", font=("Courier", 8), angle=90)

		# Cabeceras
		cv.create_text(col_para_x, tm - 22, text="PARAHELIO",
					   fill=self.COLOR_PARA, font=("Courier", 8, "bold"))
		cv.create_text(col_orto_x, tm - 22, text="ORTOHELIO",
					   fill=self.COLOR_ORTO, font=("Courier", 8, "bold"))

		# Linea de ionizacion
		y_ion = e_to_y(24.587)
		cv.create_line(lm, y_ion, W - rm, y_ion,
					   fill="#777777", width=1, dash=(4, 4))
		cv.create_text(W - rm - 2, y_ion - 7, text="ioniz. 24.59 eV",
					   fill="#666666", font=("Courier", 7), anchor="e")

		# Niveles
		for lv in LEVELS:
			cx = col_para_x if lv["system"] == "Para" else col_orto_x
			y  = e_to_y(lv["E"])
			x1, x2 = cx - level_w/2, cx + level_w/2

			if lv is upper or lv is lower:
				col, wd = self.COLOR_SEL, 2
			elif lv["system"] == "Para":
				col, wd = self.COLOR_PARA, 1
			else:
				col, wd = self.COLOR_ORTO, 1

			dash = (4, 3) if "3S" in lv["label"] and lv["n"] == 2 else ()
			cv.create_line(x1, y, x2, y, fill=col, width=wd, dash=dash)

			cv.create_text(x2 + 3, y, text=lv["label"],
						   fill=col if lv in (upper, lower) else "#4a5270",
						   font=("Courier", 7), anchor="w")

		# Flecha
		if upper and lower and allowed_transition(upper, lower):
			y_up = e_to_y(upper["E"])
			y_lo = e_to_y(lower["E"])
			cx_u = col_para_x if upper["system"] == "Para" else col_orto_x
			xc   = cx_u

			arr_col = (rgb_to_hex(wavelength_to_rgb(lam_nm))
					   if lam_nm else "#ffffff")

			cv.create_line(xc, y_up, xc, y_lo,
						   fill=arr_col, width=3, arrow="last")

			mid_y = (y_up + y_lo) / 2
			txt = f"lam={lam_nm:.1f} nm" if lam_nm and lam_nm < 5000 else "UV/IR"
			cv.create_text(xc + 4, mid_y, text=txt,
						   fill=arr_col, font=("Courier", 8), anchor="w")

	# ── Callbacks ────────────────────────────────────────────────────────────
	def _on_combo_change(self, _=None):
		u = self._get_level(self.combo_upper.get())
		l = self._get_level(self.combo_lower.get())
		if u is None or l is None:
			return
		if not allowed_transition(u, l):
			reasons = []
			if u["E"] <= l["E"]:
				reasons.append("El nivel superior debe tener mas energia")
			if u["S"] != l["S"]:
				reasons.append("dS != 0: intercombinacion prohibida")
			if abs(u["L"] - l["L"]) != 1:
				reasons.append("dL != +/-1: transicion prohibida")
			self.lbl_valid.configure(
				text="X  " + " | ".join(reasons), text_color="#ff6b6b")
		else:
			self.lbl_valid.configure(
				text="OK  Transicion permitida", text_color="#6bff9e")

	def calcular(self):
		u = self._get_level(self.combo_upper.get())
		l = self._get_level(self.combo_lower.get())

		if u is None or l is None:
			self.lbl_valid.configure(
				text="X  Nivel no encontrado", text_color="#ff6b6b")
			return

		dE, lam, freq = compute_transition(u, l)

		if dE is None:
			self._on_combo_change()
			self._reset_results()
			self._draw_diagram()
			return

		self.lbl_dE.configure(text=f"{dE:.4f} eV")
		self.lbl_lam.configure(text=f"{lam:.3f} nm")
		self.lbl_f.configure(text=f"{freq/1e12:.4f} THz")

		self._draw_diagram(upper=u, lower=l, lam_nm=lam)
		self._update_color(lam)

	def _get_level(self, label: str):
		for lv in LEVELS:
			if lv["label"] == label:
				return lv
		return None

	def _update_color(self, lam_nm):
		if 380 <= lam_nm <= 780:
			rgb = wavelength_to_rgb(lam_nm)
			hx  = rgb_to_hex(rgb)
			self.color_canvas.itemconfig(self.color_rect, fill=hx, outline=hx)
			self.lbl_hex.configure(text=hx)
			self.lbl_color_name.configure(text=color_name(lam_nm))
		else:
			self.color_canvas.itemconfig(
				self.color_rect, fill="#1e2240", outline="#3a3e5c")
			self.lbl_hex.configure(text=f"{lam_nm:.2f} nm")
			self.lbl_color_name.configure(text=color_name(lam_nm))

	def _reset_results(self):
		for lbl in (self.lbl_dE, self.lbl_lam, self.lbl_f):
			lbl.configure(text="--")
		self.color_canvas.itemconfig(
			self.color_rect, fill="#1e2240", outline="#ff4444")
		self.lbl_hex.configure(text="--")
		self.lbl_color_name.configure(text="")


# ── Punto de entrada ─────────────────────────────────────────────────────────
if __name__ == "__main__":
	app = HeliumApp()
	app.mainloop()