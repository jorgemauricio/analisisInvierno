#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite el análisis del
dato de temperatura mínima de la RNEAA
# Author: Jorge Mauricio
# Email: jorge.ernesto.mauricio@gmail.com
# Date: 2018-02-01
# Version: 1.0
#######################################
"""
# librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def main():
	# read csv
	data = pd.read_csv('data/analisis_invierno_3.csv')
	# crear columna año
	data['Año'] = data.apply(lambda x: generarAnio(x['fecha']), axis=1)

	# crear columna mes
	data['Mes'] = data.apply(lambda x: generarMes(x['fecha']), axis=1)

	# crear columna día
	data['Día'] = data.apply(lambda x: generarDia(x['fecha']), axis=1)

	# crear columna estación
	data['Estación'] = data.apply(lambda x: generarEstacion(x['Mes'], x['Día']), axis=1)

	# filtrar información
	data = data.loc[data['Estación'] == 'Invierno']

	# media de tmin anual
	plt.style.use('ggplot')
	data.groupby('Año').mean()['tmin']

	# generar datos agrupados por años
	dataAnio = data.groupby(['longitud','latitud','Año']).mean()['tmin']

	# guardar datos a csv
	dataAnio.to_csv('data/dataPorUbicacion_Anios.csv')

	# leer datos del csv
	data = pd.read_csv('data/dataPorUbicacion_Anios.csv', header=None)

	# crear columnas
	cols = ['longitud','latitud','Año','Tmin']

	# agregar columnas
	data.columns = cols

	# límites del mapas
	LONG_MAX = -86.1010
	LONG_MIN = -118.2360
	LAT_MAX = 33.5791
	LAT_MIN = 12.37

	for i in data['Año'].unique():
		# configuración del mapas
		plt.clf()
		fig = plt.figure(figsize=(8,4))
		m = Basemap(projection='mill',llcrnrlat=LAT_MIN,urcrnrlat=LAT_MAX,llcrnrlon=LONG_MIN,urcrnrlon=LONG_MAX,resolution='h')

		# filtrar información por años
		dataTemporal = dataA.loc[dataA['Año'] == i]
		x = np.array(dataTemporal['longitud'])
		y = np.array(dataTemporal['latitud'])
		z = np.array(dataTemporal['Tmin'])

		# agregar shapes
		m.readshapefile('shapes/Estados', 'Estados')

		# agregar puntos
		m.scatter(x,y, latlon=True, c=z, cmap='Blues_r')

		# crear anotación
		latitudAnotacion = (LAT_MAX + LAT_MIN) / 2
		longitudAnotacion = (LONG_MAX + LONG_MIN) / 2
		plt.annotate('@2018 INIFAP', xy=(longitudAnotacion,latitudAnotacion), xycoords='figure fraction', xytext=(0.45,0.45), color='g')
		plt.colorbar()
		temp = f"data/maps/Tmin_{i}.png"
		plt.savefig(temp, dpi=300)

def generarAnio(f):
	return f.split()[0].split('-')[0]

# crear columna mes
def generarMes(f):
	return f.split()[0].split('-')[1]

# crear columna dia
def generarDia(f):
	return f.split()[0].split('-')[2]

# funcion para generar estación meteorologica
def generarEstacion(m,d):
	m = int(m)
	d = int(d)
	if m == 12:
		if d >=21:
			return 'Invierno'
		else:
			return 'Otoño'
	if m == 1:
		return 'Invierno'
	if m == 2:
		return 'Invierno'
	if m == 3:
		if d <= 15:
			return 'Invierno'
		else:
			return 'Primavera'


if __name__== "__main__":
	main()
