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
plt.style.use('ggplot')

def main():

	# ***** Constantes
	# límites del mapas
	LONG_MAX = -86.1010
	LONG_MIN = -118.2360
	LAT_MAX = 33.5791
	LAT_MIN = 12.37
	# read csv
	data = pd.read_csv('data/analisis_invierno_5.csv')

	# eliminar datos nulos
	data = data.dropna()

	# generer columna año
	data['Año'] = data.apply(lambda x: generarAnio(x['fecha']), axis=1)
	print("Columna Año")

	#generar columna mes
	data['Mes'] = data.apply(lambda x: generarMes(x['fecha']), axis=1)
	print("Columna Mes")

	# generar columna día
	data['Día'] = data.apply(lambda x: generarDia(x['fecha']), axis=1)
	print("Columna Día")

	# generar columna Estación
	data['Estación'] = data.apply(lambda x: generarEstacion(x['Mes'], x['Día']), axis=1)
	print("Columna Estación")
	# ***** Filtros de Información
	# Invierno
	data = data.loc[data['Estación'] == 'Invierno']
	print("Filtrar información (Invierno)")

	# información menor a -10 C
	data = data.loc[data['tmin'] >= -10]
	print("Filtrar información (tmin > -10)")

	# información aberrante tmin mayor a 15 C
	data = data.loc[data['tmin'] <= 15]
	print("Filtrar información (tmin < 15)")

	# ***** ANALISIS TMIN
	# agrupar información long, lat y año
	dataTmin = data.groupby(['longitud','latitud','Año']).mean()['tmin']

	# guardar información a csv
	dataTmin.to_csv('data/dataPorUbicacion_Anios_tmin.csv')
	print("Guardar información a CSV")

	# leer información del csv
	dataTmin = pd.read_csv('data/dataPorUbicacion_Anios_tmin.csv', header=None)
	print("Leer información agrupada del CSV")

	# columnas para el CSV
	cols = ['longitud','latitud','Año','Tmin']
	dataTmin.columns = cols

	# generar mapas Tmin
	for i in dataTmin['Año'].unique():
		# configuración del mapas
		plt.clf()
		fig = plt.figure(figsize=(6,4))
		m = Basemap(projection='mill',llcrnrlat=LAT_MIN,urcrnrlat=LAT_MAX,llcrnrlon=LONG_MIN,urcrnrlon=LONG_MAX,resolution='h')

		# filtrar información por años
		dataTemporal = dataTmin.loc[dataTmin['Año'] == i]
		x = np.array(dataTemporal['longitud'])
		y = np.array(dataTemporal['latitud'])
		z = np.array(dataTemporal['Tmin'])

		# agregar shapes
		m.readshapefile('shapes/Estados', 'Estados')

		# agregar puntos
		m.scatter(x,y, latlon=True, s=2,c=z, cmap='Blues_r')

		# crear anotación
		latitudAnotacion = (LAT_MAX + LAT_MIN) / 2
		longitudAnotacion = (LONG_MAX + LONG_MIN) / 2
		plt.annotate('@2018 INIFAP', xy=(longitudAnotacion,latitudAnotacion), xycoords='figure fraction', xytext=(0.25,0.55), color='g')
		plt.title("Temperatura Mínima Media\n registrada en el Invierno del {}".format(i))
		plt.colorbar()
		temp = "maps/Tmin_{}.png".format(i)
		print("Generar mapa: {}".format(i))
		plt.savefig(temp, dpi=300)

	# ***** ANALISIS TMAX
	# agrupar información long, lat y año
	dataTmax = data.groupby(['longitud','latitud','Año']).mean()['tmax']

	# guardar información a csv
	dataTmax.to_csv('data/dataPorUbicacion_Anios_tmax.csv')
	print("Guardar información a CSV")

	# leer información del csv
	dataTmax = pd.read_csv('data/dataPorUbicacion_Anios_tmax.csv', header=None)
	print("Leer información agrupada del CSV")

	# columnas para el CSV
	cols = ['longitud','latitud','Año','Tmax']
	dataTmax.columns = cols

	# generar mapas Tmin
	for i in dataTmax['Año'].unique():
		# configuración del mapas
		plt.clf()
		fig = plt.figure(figsize=(6,4))
		m = Basemap(projection='mill',llcrnrlat=LAT_MIN,urcrnrlat=LAT_MAX,llcrnrlon=LONG_MIN,urcrnrlon=LONG_MAX,resolution='h')

		# filtrar información por años
		dataTemporal = dataTmax.loc[dataTmax['Año'] == i]
		x = np.array(dataTemporal['longitud'])
		y = np.array(dataTemporal['latitud'])
		z = np.array(dataTemporal['Tmax'])

		# agregar shapes
		m.readshapefile('shapes/Estados', 'Estados')

		# agregar puntos
		m.scatter(x,y, latlon=True, s=2,c=z, cmap='Reds')

		# crear anotación
		latitudAnotacion = (LAT_MAX + LAT_MIN) / 2
		longitudAnotacion = (LONG_MAX + LONG_MIN) / 2
		plt.annotate('@2018 INIFAP', xy=(longitudAnotacion,latitudAnotacion), xycoords='figure fraction', xytext=(0.25,0.55), color='g')
		plt.title("Temperatura Máxima Media\n registrada en el Invierno del {}".format(i))
		plt.colorbar()
		temp = "maps/Tmax_{}.png".format(i)
		print("Generar mapa: {}".format(i))
		plt.savefig(temp, dpi=300)

	# ***** ANALISIS TMIN AñO-MES

	# generar columna año-mes
	data["AM"] = data["Año"] + "-" + data["Mes"]

	# agrupar información long, lat y año-mes
	dataAM = data.groupby(['longitud','latitud','AM']).mean()['tmin']

	# guardar información a csv
	dataAM.to_csv('data/dataPorUbicacion_AM_tmin.csv')
	print("Guardar información a CSV")

	# leer información del csv
	dataAM = pd.read_csv('data/dataPorUbicacion_AM_tmin.csv', header=None)
	print("Leer información agrupada del CSV")

	# columnas para el CSV
	cols = ['longitud','latitud','AM','Tmin']
	dataAM.columns = cols

	# generar mapas Tmin
	for i in dataAM['AM'].unique():
		# configuración del mapas
		plt.clf()
		fig = plt.figure(figsize=(6,4))
		m = Basemap(projection='mill',llcrnrlat=LAT_MIN,urcrnrlat=LAT_MAX,llcrnrlon=LONG_MIN,urcrnrlon=LONG_MAX,resolution='h')

		# filtrar información por años
		dataTemporal = dataAM.loc[dataAM['AM'] == i]
		x = np.array(dataTemporal['longitud'])
		y = np.array(dataTemporal['latitud'])
		z = np.array(dataTemporal['Tmin'])

		# agregar shapes
		m.readshapefile('shapes/Estados', 'Estados')

		# agregar puntos
		m.scatter(x,y, latlon=True, s=2,c=z, cmap='Blues_r')

		# crear anotación
		latitudAnotacion = (LAT_MAX + LAT_MIN) / 2
		longitudAnotacion = (LONG_MAX + LONG_MIN) / 2
		plt.annotate('@2018 INIFAP', xy=(longitudAnotacion,latitudAnotacion), xycoords='figure fraction', xytext=(0.25,0.55), color='g')
		plt.title("Temperatura Mínima Media\n registrada en {}".format(i))
		plt.colorbar()
		temp = "maps/Tmin_{}.png".format(i)
		print("Generar mapa: {}".format(i))
		plt.savefig(temp, dpi=300)

# funciones
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
