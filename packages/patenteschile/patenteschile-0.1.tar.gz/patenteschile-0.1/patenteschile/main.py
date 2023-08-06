# patentevalida.py
# Autor: Alejandro (farias@8loop.cl)
# Esta librería genera patentes vehículares válidas
"""
for patentevalida import *
patentes = Patente(10)
print(patentes)
"""

import sys
import rstr
import re

class Patente:
	def calculate_patente(self):
		words = rstr.xeger(r"[B-Z]{4}\d")
		number = rstr.xeger(r"[10-99]{1}")
		filter = ['A','E','I','M','N','Ñ','O','Q','U']
		return words + number # concat letras y numeros

	def generate(self, num: int):
		patentes = []

		for i in range(0, num):
			patente = self.calculate_patente()
			patentes.append(patente)
		return patentes
