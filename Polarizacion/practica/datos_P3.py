import numpy as np


caso_A = { #mW
	"I_total": 528,
	"I_v": 352,
	"I_h": 0.74,
	"I_-45": 167,
	"I_+45": 191,
	"I_lambda/4": 288,
	"-I_lambda/4": 240

}

caso_B = { #mW
	"I_total": 300,
	"I_v": 104,
	"I_h": 103,
	"I_-45": 200,
	"I_+45": 163,
	"I_lambda/4": 93,
	"-I_lambda/4": 100

}

caso_A_norm = {}
caso_B_norm = {}

for key in caso_A:
	caso_A_norm[key] = round(caso_A[key] / caso_A["I_total"],2)

for key in caso_B:
	caso_B_norm[key] = round(caso_B[key] / caso_B["I_total"],2)

print(caso_A_norm)
print(caso_B_norm)