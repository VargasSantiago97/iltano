#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

#import ventanaIngreso
import PDF_catalogo
import tablaElegir

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Menu
import tkinter as tk
from tkinter import ttk

import os
import os.path

import sqlite3
from sqlite3 import Error

import shutil

import json

diccionario_textos = {}
diccionario_objetos = {}
diccionario_pinturas = {}
dicCat = {"asd":"asd"}
dicCatUbic = {}
dicProductores = {}

direccionBaseDeDatos = 'database/iltanohacienda.db'


dire = "C:/Users/Santiago/Desktop/mipdf2.pdf"

dicLotes = {}
dicLotesUbic = {}

remate = "remate1"

diccionarioObjetos = {
	"dicCatUbic" : dicCatUbic,
	"dicLotesUbic" : dicLotesUbic
}

def treeview_sort_column(tv, col, reverse):
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, command=lambda: \
	treeview_sort_column(tv, col, not reverse))

	tablaADicLotesUbic()

def sql_connection():
	try:
		con = sqlite3.connect(direccionBaseDeDatos)
		return con
	except Error:
		messagebox.showerror("ERROR", "Error conectando a la base de datos")
def actualizar_db(con, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows
def actualizar_db2(con, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT cantidad FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows


def buscar(selecBuscar):
	def funcsalirr(ssss):
		con = sql_connection()
		condiciones = " WHERE id = " + str(ssss)
		rows = actualizar_db(con, "remate", condiciones)

		diccionarioObjetos["entryRemate"].delete(0, tk.END)
		diccionarioObjetos["entryRemate"].insert(0, rows[0][1])

		activarCategoria()
	def funcsalirrcat(ssss):
		con = sql_connection()
		condiciones = " WHERE id = " + str(ssss)
		rows = actualizar_db(con, "catalogo", condiciones)

		diccionarioObjetos["entry_catalogo"].delete(0, tk.END)
		diccionarioObjetos["entry_catalogo"].insert(0, rows[0][1])

		categoriaCargada()

	#Buscar remate
	if(selecBuscar=="remate"):

		dicc_buscar = {"seleccionar" : "remate",
		"columnas" : {"0":{"id" : "nombre", "cabeza" : "Remate", "ancho" : 180, "row" : 1}, "1":{"id" : "fecha", "cabeza" : "Fecha", "ancho" : 60, "row" : 2}, "2":{"id" : "tipo", "cabeza" : "Tipo", "ancho" : 70, "row" : 3}},
		"db" : direccionBaseDeDatos,
		"tabla" : "remate",
		"condiciones" : ' WHERE nombre LIKE  "%' + str(diccionarioObjetos["entryRemate"].get()) + '%" AND estado = "activo"',
		"dimensionesVentana" : "336x400"}
		tablaElegir.tabla_elegir(dicc_buscar, funcsalirr)

	#Buscar catalogo
	if(selecBuscar=="catalogo"):
		dicc_buscar = {"seleccionar" : "catalogo",
		"columnas" : {"0":{"id" : "nombre", "cabeza" : "Catalogo", "ancho" : 180, "row" : 1}, "1":{"id" : "fecha", "cabeza" : "Nombre", "ancho" : 60, "row" : 2}, "2":{"id" : "tipo", "cabeza" : "Remate", "ancho" : 70, "row" : 3}},
		"db" : direccionBaseDeDatos,
		"tabla" : "catalogo",
		"condiciones" : ' WHERE (nombre LIKE  "%' + str(diccionarioObjetos["entry_catalogo"].get()) + '%" OR alias LIKE  "%' + str(diccionarioObjetos["entry_catalogo"].get()) + '%") AND remate = "' + str(diccionarioObjetos["entryRemate"].get()) + '" AND estado = "activo"',
		"dimensionesVentana" : "336x400"}
		tablaElegir.tabla_elegir(dicc_buscar, funcsalirrcat)

def activarCategoria():
	diccionarioObjetos["entry_catalogo"].configure(state="normal")
	diccionarioObjetos["entry_catalogo"].delete(0, tk.END)
	diccionarioObjetos["entry_catalogo"].focus()

	diccionarioObjetos["btn_nuevo"].configure(state="normal")
	diccionarioObjetos["btn_nuevo"].configure(backgroun="#d3ffba")
def categoriaCargada():
	diccionarioObjetos["btn_guardar"].configure(state="normal")
	diccionarioObjetos["btn_eliminar"].configure(state="normal")
	diccionarioObjetos["btn_pdf"].configure(state="normal")

	diccionarioObjetos["dicCatUbic"].clear()

	actualizarDicCat()

	#Leer diccionarios
	try:
		ubicGuardar = "../catalogos"

		nombreArchivoLotes = "remate_" + str(diccionarioObjetos["entryRemate"].get()) + "_-_catalogo_" + str(diccionarioObjetos["entry_catalogo"].get()) + "_lot.json"
		nombreArchivoCat = "remate_" + str(diccionarioObjetos["entryRemate"].get()) + "_-_catalogo_" + str(diccionarioObjetos["entry_catalogo"].get()) + "_cat.json"

		archivo = open(ubicGuardar + "/" + nombreArchivoLotes, "r")
		nuevoDicLotesUbic = json.loads(archivo.read())
		archivo.close()

		archivoCat = open(ubicGuardar + "/" + nombreArchivoCat, "r")
		nuevoDicCatUbic = json.loads(archivoCat.read())
		archivoCat.close()

		diccionarioObjetos["dicCatUbic"].update(nuevoDicCatUbic)

	except:
		messagebox.showerror("ERROR", "Error, no se pudo cargar")
		return 0

	actualizarLotes()
	actualizarTablaCategorias()

	diccionarioObjetos["dicLotesUbic"].clear()
	diccionarioObjetos["dicLotesUbic"].update(nuevoDicLotesUbic)




#Productores
def actualizarProductores():
	con = sql_connection()
	condiciones = ""
	rows = actualizar_db(con, "productores", condiciones)
	for row in rows:
		dicProductores[str(row[1])] = str(row[1])

#CATEGORIA
def actualizarDicCat():
	con = sql_connection()
	rows = actualizar_db(con, "catVenta", "")

	cantidadTotal = 0
	cabezasTotal = 0

	try:
		for row in rows:
			con = sql_connection()
			condiciones = " WHERE estado = 'activo' AND catVenta = '" + str(row[1]) + "' AND remate = '" + str(diccionarioObjetos["entryRemate"].get()) + "'"
			rows_lotes = actualizar_db2(con, "lotes", condiciones)

			cantidad = len(rows_lotes)
			if cantidad>0:
				cabezas = 0
				for row_lote in rows_lotes:
					try:
						num_cab = int(row_lote[0])
					except:
						num_cab = 0
					cabezas = cabezas + num_cab

				dicCat[str(row[0])] = {"cantidad" : cantidad, "cabezas" : cabezas,"alias" : str(row[1]), "nombre" : str(row[2])}

				cantidadTotal = cantidadTotal + cantidad
				cabezasTotal = cabezasTotal + cabezas
	except:
		messagebox.showerror("ERROR", "Error al cargar")
def actualizarDicCatUbic():
	cant = len(dicCat)
	llaves = list(dicCat.keys())

	try:
		for i in range(0, cant):
			dicCatUbic[str(i)] = llaves[i]
	except:
		messagebox.showerror("ERROR", "Error al ordenar")
def actualizarTablaCategorias():

	tabla = diccionario_objetos["tabla_catVenta"]

	try:
		for i in tabla.get_children():
			tabla.delete(i)

		cant = len(dicCatUbic)
		for i in range(0, cant):
			tabla.insert("", str(i), tags=str(i),text = str(dicCat[dicCatUbic[str(i)]]["cantidad"]), iid= i, values = (str(dicCat[dicCatUbic[str(i)]]["cabezas"]),
			str(dicCat[dicCatUbic[str(i)]]["alias"]), 
			str(dicCat[dicCatUbic[str(i)]]["nombre"])))
	except:
		messagebox.showerror("ERROR", "Error al cargar categorias de venta")

def actualizarDatosCatalogo():
	con = sql_connection()
	condiciones = " WHERE nombre = '" + remate + "'"
	rows = actualizar_db(con, "remate", condiciones)

	row = rows[0]

	diccionario_objetos["entry_datosFecha"].delete(0, tk.END)
	diccionario_objetos["entry_datosTitulo"].delete(0, tk.END)
	diccionario_objetos["entry_datosPredio"].delete(0, tk.END)
	diccionario_objetos["entry_datosLocalidad"].delete(0, tk.END)
	diccionario_objetos["entry_datosRemata"].delete(0, tk.END)

	diccionario_objetos["entry_datosFecha"].insert(0, str(row[2]))
	diccionario_objetos["entry_datosTitulo"].insert(0, str(row[1]))
	diccionario_objetos["entry_datosPredio"].insert(0, str(row[4]))
	diccionario_objetos["entry_datosLocalidad"].insert(0, str(row[5]))
	diccionario_objetos["entry_datosRemata"].insert(0, str(row[6]))

#LOTES
def actualizarLotes():
	cant_cats = len(dicCatUbic)

	for i in range(0, cant_cats):
		id_cateVenta = str(dicCatUbic[str(i)])
		cateVent = dicCat[id_cateVenta]["alias"]

		con = sql_connection()
		condiciones = " WHERE estado = 'activo' AND catVenta = '" + cateVent + "' AND remate = '" + str(diccionarioObjetos["entryRemate"].get()) + "'"

		rows = actualizar_db(con, "lotes", condiciones)

		cant_lotes = len(rows)

		dicLotes[id_cateVenta] = {}
		dicLotesUbic[id_cateVenta] = {}

		j=0

		for row in rows:
			dicLotes[id_cateVenta][str(row[0])] = {
			"corral" : str(row[4]),
			"productor" : str(row[2]),
			"cantidad" : str(row[3]),
			"categoria" : str(row[6]),
			"pintura" : str(row[7]),
			"peso" : str(row[12]),
			"promedio" : str(row[13]),
			}

			dicLotesUbic[id_cateVenta][str(j)] = str(row[0])
			j=j+1
def cargarDatosLotes():
	tabla = diccionario_objetos["tabla_lotesCargados"]

	id_cat = str(diccionario_objetos["texto_cat_id"].get())

	dicc = dicLotes[id_cat]
	diccUbic = dicLotesUbic[id_cat]

	cant_lotes = len(dicc)

	llaves = list(dicc.keys())
	#print(llaves)

	try:
		for i in tabla.get_children():
			tabla.delete(i)

		for i in range(0, cant_lotes):
			tabla.insert("", str(i), tags=diccUbic[str(i)], text = str(i), iid= diccUbic[str(i)], values = (str(dicc[diccUbic[str(i)]]["corral"]),
				str(dicc[diccUbic[str(i)]]["productor"]), 
				str(dicc[diccUbic[str(i)]]["cantidad"]),
				str(dicc[diccUbic[str(i)]]["categoria"]),
				str(dicc[diccUbic[str(i)]]["pintura"]),
				str(dicc[diccUbic[str(i)]]["peso"]),
				str(dicc[diccUbic[str(i)]]["promedio"]),
				"Mostrar",))
	except:
		messagebox.showerror("ERROR", "Error al cargar")



def tablaADicLotesUbic():
	#print(type(diccionario_objetos["tabla_lotesCargados"].get_children()))

	cat = diccionario_objetos["texto_cat_id"].get()
	nuevaPos = diccionario_objetos["tabla_lotesCargados"].get_children()

	#print(dicLotesUbic[cat])

	for i in range(0, len(dicLotesUbic[cat])):
		dicLotesUbic[cat][str(i)] = nuevaPos[i]

#MOVER EN TABLA CATEGORIA
def moverCatArriba():
	try:
		tabla = diccionario_objetos["tabla_catVenta"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = seleccion["tags"][0]
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		nuevoDic = {}
		nuevoDic[str(ubicacion-1)] = dicCatUbic[str(ubicacion)]
		nuevoDic[str(ubicacion)] = dicCatUbic[str(ubicacion-1)]

		dicCatUbic.update(nuevoDic)
		actualizarTablaCategorias()

		tabla.focus(ubicacion)
	except:
		messagebox.showerror("ERROR", "No se pudo mover")
def moverCatAbajo():
	try:
		tabla = diccionario_objetos["tabla_catVenta"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = seleccion["tags"][0]
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		nuevoDic = {}
		nuevoDic[str(ubicacion+1)] = dicCatUbic[str(ubicacion)]
		nuevoDic[str(ubicacion)] = dicCatUbic[str(ubicacion+1)]

		dicCatUbic.update(nuevoDic)
		actualizarTablaCategorias()
		tabla.focus(ubicacion)
	except:
		messagebox.showerror("ERROR", "No se pudo mover")
def moverCatArribaTODO():
	try:
		tabla = diccionario_objetos["tabla_catVenta"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = seleccion["tags"][0]
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		nuevoDic = {}
		nuevoDic[str(0)] = dicCatUbic[str(ubicacion)]

		for i in range(0, ubicacion):
			nuevoDic[str(i+1)] = dicCatUbic[str(i)]

		dicCatUbic.update(nuevoDic)
		actualizarTablaCategorias()

		tabla.focus(ubicacion)
	except:
		messagebox.showerror("ERROR", "No se pudo mover")
def moverCatAbajoTODO():
	try:
		tabla = diccionario_objetos["tabla_catVenta"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = seleccion["tags"][0]
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		ultimo = len(dicCatUbic)-1
		nuevoDic = {}
		nuevoDic[str(ultimo)] = dicCatUbic[str(ubicacion)]

		for i in range(0, ultimo-ubicacion):
			nuevoDic[str(ultimo-i-1)] = dicCatUbic[str(ultimo-i)]

		dicCatUbic.update(nuevoDic)
		actualizarTablaCategorias()

		tabla.focus(ubicacion)
	except:
		messagebox.showerror("ERROR", "No se pudo mover")

#MOVER EN TABLA LOTES
def moverLotArriba():
	try:
		cat = diccionario_objetos["texto_cat_id"].get()
		tabla = diccionario_objetos["tabla_lotesCargados"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = int(seleccion["text"])
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		nuevoDic = {}
		nuevoDic[str(ubicacion-1)] = dicLotesUbic[cat][str(ubicacion)]
		nuevoDic[str(ubicacion)] = dicLotesUbic[cat][str(ubicacion-1)]

		dicLotesUbic[cat].update(nuevoDic)
		cargarDatosLotes()

		tabla.focus(dicLotesUbic[cat][str(ubicacion)])
	except:
		messagebox.showerror("ERROR", "No se pudo mover")
def moverLotAbajo():
	try:
		cat = diccionario_objetos["texto_cat_id"].get()
		tabla = diccionario_objetos["tabla_lotesCargados"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = int(seleccion["text"])
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		nuevoDic = {}
		nuevoDic[str(ubicacion+1)] = dicLotesUbic[cat][str(ubicacion)]
		nuevoDic[str(ubicacion)] = dicLotesUbic[cat][str(ubicacion+1)]

		dicLotesUbic[cat].update(nuevoDic)
		cargarDatosLotes()

		tabla.focus(dicLotesUbic[cat][str(ubicacion)])
	except:
		messagebox.showerror("ERROR", "No se pudo mover")
def moverLotArribaTODO():
	try:
		cat = diccionario_objetos["texto_cat_id"].get()
		tabla = diccionario_objetos["tabla_lotesCargados"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = int(seleccion["text"])
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		nuevoDic = {}
		nuevoDic[str(0)] = dicLotesUbic[cat][str(ubicacion)]

		for i in range(0, ubicacion):
			nuevoDic[str(i+1)] = dicLotesUbic[cat][str(i)]

		dicLotesUbic[cat].update(nuevoDic)
		cargarDatosLotes()

		tabla.focus(dicLotesUbic[cat][str(ubicacion)])
	except:
		messagebox.showerror("ERROR", "No se pudo mover")
def moverLotAbajoTODO():
	try:
		cat = diccionario_objetos["texto_cat_id"].get()
		tabla = diccionario_objetos["tabla_lotesCargados"]
		seleccion = tabla.item(tabla.selection())
		ubicacion = int(seleccion["text"])
	except:
		messagebox.showerror("ERROR", "Por favor seleccione 1")
		return 0

	try:
		ultimo = len(dicLotesUbic[cat])-1
		nuevoDic = {}
		nuevoDic[str(ultimo)] = dicLotesUbic[cat][str(ubicacion)]

		for i in range(0, ultimo-ubicacion):
			nuevoDic[str(ultimo-i-1)] = dicLotesUbic[cat][str(ultimo-i)]

		dicLotesUbic[cat].update(nuevoDic)
		cargarDatosLotes()

		tabla.focus(dicLotesUbic[cat][str(ubicacion)])
	except:
		messagebox.showerror("ERROR", "No se pudo mover")

#SELECCIONAR
def seleccionarTablaCat():
	tabla = diccionario_objetos["tabla_catVenta"]
	seleccion = tabla.item(tabla.selection())
	ubicacion = seleccion["tags"][0]

	textoMostrar = str(dicCat[str(dicCatUbic[str(ubicacion)])]["alias"]) + " - " + str(dicCat[str(dicCatUbic[str(ubicacion)])]["nombre"])

	diccionario_objetos["texto_cat"].set(textoMostrar)
	diccionario_objetos["texto_cat_filtrar"].set(str(dicCat[str(dicCatUbic[str(ubicacion)])]["nombre"]))
	diccionario_objetos["texto_cat_id"].set(dicCatUbic[str(ubicacion)])

	#actualizarLotes()
	cargarDatosLotes()

	#print(ubicacion)
	#print(dicCatUbic[str(ubicacion)])
	#print(dicCat[str(dicCatUbic[str(ubicacion)])])
def seleccionarTablaLotes():
	tabla = diccionario_objetos["tabla_lotesCargados"]
	seleccion = tabla.item(tabla.selection())
	id_lote = seleccion["tags"][0]

#EXPORTAR
def crearDiccionarioExportar():
	dicc = {}

	name = str(time.strftime("%d-%m-%y")) + " " + remate + " creado a las " + str(time.strftime("%H-%M-%S")) + "hs.pdf"
	file = filedialog.askdirectory()

	if (file==""):
		return 0

	file = file + "/" + name



	dicc["datos"] = {
	"ruta":file,
	"fecha" : diccionario_objetos["entry_datosFecha"].get(),
	"titulo" : diccionario_objetos["entry_datosTitulo"].get(),
	"predio" : diccionario_objetos["entry_datosPredio"].get(),
	"lugar" : diccionario_objetos["entry_datosLocalidad"].get(),
	"remata" : diccionario_objetos["entry_datosRemata"].get(),
	"totalIngresados" : diccionario_objetos["entry_totalIngresados"].get(),
	"totalCorrales" : diccionario_objetos["entry_totalCorrales"].get(),
	}

	dicc["lotes"] = {}
	cant_cats = len(dicCatUbic)

	for i in range(0, cant_cats):
		dicc["lotes"][str(dicCat[dicCatUbic[str(i)]]["nombre"])] = {}

		cant_lotes = len(dicLotesUbic[str(dicCatUbic[str(i)])])

		for j in range(0, cant_lotes):
			dicc["lotes"][str(dicCat[dicCatUbic[str(i)]]["nombre"])][str(j)] = {
			"corral" : dicLotes[str(dicCatUbic[str(i)])][dicLotesUbic[str(dicCatUbic[str(i)])][str(j)]]["corral"],
			"vendedor" : dicLotes[str(dicCatUbic[str(i)])][dicLotesUbic[str(dicCatUbic[str(i)])][str(j)]]["productor"],
			"cantidad" : dicLotes[str(dicCatUbic[str(i)])][dicLotesUbic[str(dicCatUbic[str(i)])][str(j)]]["cantidad"],
			"categoria" : dicLotes[str(dicCatUbic[str(i)])][dicLotesUbic[str(dicCatUbic[str(i)])][str(j)]]["categoria"],
			"pintura" : dicLotes[str(dicCatUbic[str(i)])][dicLotesUbic[str(dicCatUbic[str(i)])][str(j)]]["pintura"],
			"peso" : dicLotes[str(dicCatUbic[str(i)])][dicLotesUbic[str(dicCatUbic[str(i)])][str(j)]]["peso"],
			"promedio" : dicLotes[str(dicCatUbic[str(i)])][dicLotesUbic[str(dicCatUbic[str(i)])][str(j)]]["promedio"],
			}

	return dicc
def exportar():
	dicc = crearDiccionarioExportar()
	if(dicc==0):
		messagebox.showerror("ERROR", "Seleccione un directorio.\nPDF NO EXPORTADO")
		return 0
	PDF_catalogo.preliquidacionPDF(dicc)

def guardar():
	try:
		ubicGuardar = "../catalogos"

		nombreArchivoLotes = "remate_" + str(diccionarioObjetos["entryRemate"].get()) + "_-_catalogo_" + str(diccionarioObjetos["entry_catalogo"].get()) + "_lot.json"
		nombreArchivoCat = "remate_" + str(diccionarioObjetos["entryRemate"].get()) + "_-_catalogo_" + str(diccionarioObjetos["entry_catalogo"].get()) + "_cat.json"

		archivo = open(ubicGuardar + "/" + nombreArchivoLotes, "w")
		diccLotes = json.dumps(dicLotesUbic, indent=4)
		archivo.write(diccLotes)
		archivo.close()

		archivoCat = open(ubicGuardar + "/" + nombreArchivoCat, "w")
		diccCat = json.dumps(dicCatUbic, indent=4)
		archivoCat.write(diccCat)
		archivoCat.close()

	except:
		messagebox.showerror("ERROR", "Error al guardar")


#NUEVO CATALOGO
def nuevoCatalogo(window, remate):
	def guardarCatalogo():
		try:
			x_alias = entry_alias.get()
			x_nombre = entry_nombre.get()
			x_remate = remate
			x_fecha = entry_fecha.get()
			x_observaciones = entry_observaciones.get()
			x_estado = "activo"

			entities = [str(x_alias), str(x_nombre), str(x_remate), str(x_fecha), str(x_observaciones), str(x_estado)]
		except:
			messagebox.showerror("ERROR", "No se pudo obtener los datos")
			return 0

		try:
			MsgBox = messagebox.askquestion('ATENCION', "¿Desea guardar?", icon = 'warning')
			if(MsgBox == 'yes'):
				con = sql_connection()
				cursorObj = con.cursor()
				cursorObj.execute("INSERT INTO catalogo VALUES(NULL, ?, ?, ?, ?, ?, ?)", entities)
				con.commit()
				messagebox.showinfo("Guardado", "Guardado con Éxito")
				diccionarioObjetos["entry_catalogo"].delete(0, tk.END)
				diccionarioObjetos["entry_catalogo"].insert(0, x_alias)
				winCat.destroy()

				actualizarDicCat()
				actualizarDicCatUbic()
				actualizarTablaCategorias()
				actualizarLotes()

				diccionarioObjetos["btn_guardar"].config(state="normal")
				diccionarioObjetos["btn_eliminar"].config(state="normal")
				diccionarioObjetos["btn_pdf"].config(state="normal")

		except:
			messagebox.showerror("ERROR", "No se pudo Guardar")


	winCat = Toplevel(window)
	winCat.title("Nuevo Catalogo")
	winCat.geometry("450x350")
	winCat.configure(backgroun="#E0F8F1") #E8F6FA

	sec1 = Label(winCat, backgroun="#E0F8F1")
	sec2 = Label(winCat, backgroun="#E0F8F1")
	sec3 = Label(winCat, backgroun="#E0F8F1")

	sec1.grid(column = 0, row = 0, padx = 10, pady = 10)
	sec2.grid(column = 0, row = 1, padx = 10, pady = 10)
	sec3.grid(column = 0, row = 2, padx = 10, pady = 10)

	Label(sec1, text="Crear catalogo en: " + str(remate), backgroun="#E0F8F1", font=("Helvetica", 15)).pack()

	Label(sec2, text="Alias:", backgroun="#E0F8F1", font=("Helvetica", 15)).grid(sticky=E, column = 0, row = 0, padx=10, pady=10)
	Label(sec2, text="Nombre:", backgroun="#E0F8F1", font=("Helvetica", 15)).grid(sticky=E, column = 0, row = 1, padx=10, pady=10)
	Label(sec2, text="Fecha:", backgroun="#E0F8F1", font=("Helvetica", 15)).grid(sticky=E, column = 0, row = 2, padx=10, pady=10)
	Label(sec2, text="Observaciones:", backgroun="#E0F8F1", font=("Helvetica", 15)).grid(sticky=E, column = 0, row = 3, padx=10, pady=10)

	entry_alias = Entry(sec2, font=("Helvetica", 15))
	entry_nombre = Entry(sec2, font=("Helvetica", 15))
	entry_fecha = Entry(sec2, font=("Helvetica", 15))
	entry_observaciones = Entry(sec2, font=("Helvetica", 15))

	entry_alias.grid(sticky=W, column = 1, row = 0, padx=10, pady=10)
	entry_nombre.grid(sticky=W, column = 1, row = 1, padx=10, pady=10)
	entry_fecha.grid(sticky=W, column = 1, row = 2, padx=10, pady=10)
	entry_observaciones.grid(sticky=W, column = 1, row = 3, padx=10, pady=10)

	btn_guardarCat = tk.Button(sec3, text="Guardar", font=("Helvetica", 15), command = guardarCatalogo, backgroun="#d3ffba")
	btn_guardarCat.pack()

def catalogo(idRemate):
	window = Tk()
	window.title("Catalogo")
	window.geometry("1024x600")
	window.configure(backgroun="#2C4D4F") #E8F6FA
	window.attributes('-fullscreen', True)

	padX = 5
	padY = 5

	lbl_datos = Label(window, backgroun="#E0F8F1")
	lbl_tablaCategorias = Label(window)
	lbl_tablaCategoriasMover = Label(window, backgroun="#E0F8F1")
	lbl_acciones = Label(window, backgroun="#E0F8F1")
	lbl_categoria = Label(window, backgroun="#E0F8F1")
	lbl_tablaCargados = Label(window)
	lbl_tablaCargadosMover = Label(window, backgroun="#E0F8F1")

	mod_alt = 0
	var_bajar = 50

	lbl_datos.place(x = 2, y = 2+mod_alt, width = 300, height = 170)
	lbl_tablaCategorias.place(x = 304, y = 2+mod_alt, width = 450, height = 170)
	lbl_tablaCategoriasMover.place(x = 756, y = 2+mod_alt, width = 100, height = 170)
	lbl_acciones.place(x = 858, y = 2+mod_alt, width = 164, height = 170)
	lbl_categoria.place(x = 2, y = 124+mod_alt+var_bajar, width = 1020, height = 48)
	lbl_tablaCargados.place(x = 2, y = 174+mod_alt+var_bajar, width = 918, height = 370)
	lbl_tablaCargadosMover.place(x = 922, y = 174+mod_alt+var_bajar, width = 100, height = 370)

	#DATOS DE CATALOGO
	if(True):	
		tk.Label(lbl_datos, text="Catálogo", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 2, width = 298)
	
		tk.Label(lbl_datos, text="Seleccionar Remate:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 50, width = 150)
		tk.Label(lbl_datos, text="Seleccionar Catalogo:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 80, width = 150)

		entry_remate = Entry(lbl_datos)
		entry_remate.place(x = 150, y = 50, width = 130)
		entry_remate.focus()

		entry_catalogo = Entry(lbl_datos, state="disabled")
		entry_catalogo.place(x = 150, y = 80, width = 130)

		btn_nuevo = tk.Button(lbl_datos, text="Nuevo catalogo", state="disabled", backgroun="#fffcbf", command=lambda: nuevoCatalogo(window, entry_remate.get()))
		btn_nuevo.place(x = 100, y = 120, width = 100)

		entry_remate.bind("<Return>", (lambda event: buscar("remate")))
		entry_catalogo.bind("<Return>", (lambda event: buscar("catalogo")))

		#tablaElegir

	#TABLA -> CATEGORIAS DE VENTA
	if(True):
		sbr_catVenta = Scrollbar(lbl_tablaCategorias)
		sbr_catVenta.pack(side=RIGHT, fill="y")

		tabla_catVenta = ttk.Treeview(lbl_tablaCategorias, columns=("cabezas", "alias", "nombre"), selectmode=tk.BROWSE) 
		tabla_catVenta.pack(side=LEFT, fill="both", expand=True)
		sbr_catVenta.config(command=tabla_catVenta.yview)
		tabla_catVenta.config(yscrollcommand=sbr_catVenta.set)

		tabla_catVenta.heading("#0", text="Lotes")
		tabla_catVenta.heading("cabezas", text="Cabezas")
		tabla_catVenta.heading("alias", text="Alias")
		tabla_catVenta.heading("nombre", text="Nombre")

		tabla_catVenta.column("#0", width=40)
		tabla_catVenta.column("cabezas", width=40)
		tabla_catVenta.column("alias", width=120)
		tabla_catVenta.column("nombre", width=120)

	#MOVER -> TABLA CATEGORIAS
	if(True):
		btn_moverArribaTodoCat = tk.Button(lbl_tablaCategoriasMover, text="↑↑↑", font=("verdana",15,"bold"), backgroun="#F5A9A9", command = moverCatArribaTODO)
		btn_moverArribaTodoCat.place(x = 25, y = 10, width=50, height=25)

		btn_moverArribaCat = tk.Button(lbl_tablaCategoriasMover, text="↑", font=("verdana",15,"bold"), backgroun="#F5D0A9", command = moverCatArriba)
		btn_moverArribaCat.place(x = 25, y = 50, width=50, height=25)

		btn_moverAbajoCat = tk.Button(lbl_tablaCategoriasMover, text="↓", font=("verdana",15,"bold"), backgroun="#F5D0A9", command = moverCatAbajo)
		btn_moverAbajoCat.place(x = 25, y = 90, width=50, height=25)

		btn_moverAbajoTodoCat = tk.Button(lbl_tablaCategoriasMover, text="↓↓↓", font=("verdana",15,"bold"), backgroun="#F5A9A9", command = moverCatAbajoTODO)
		btn_moverAbajoTodoCat.place(x = 25, y = 130, width=50, height=25)

	#ACCIONES
	if(True):

		btn_guardar = tk.Button(lbl_acciones, text="Guardar Catalogo", font=("verdana",10), backgroun="#F5D0A9", width=18, command=guardar, state = "disabled")
		btn_guardar.pack(pady=5)

		btn_eliminar = tk.Button(lbl_acciones, text="Eliminar Catalogo", font=("verdana",10), backgroun="#F5D0A9", width=18, command=exportar, state = "disabled")
		btn_eliminar.pack(pady=5)

		btn_pdf = tk.Button(lbl_acciones, text="Generar PDF", font=("verdana",10), backgroun="#F5D0A9", width=18, command=exportar, state = "disabled")
		btn_pdf.pack(pady=5)

	#CATEGORIA SELECCIONADA
	if(True):
		texto_cat = StringVar()
		texto_cat.set("Seleccione una categoria")
		texto_cat_filtrar = StringVar()
		texto_cat_filtrar.set("")
		texto_cat_id = StringVar()
		texto_cat_id.set("")

		tk.Label(lbl_categoria, text="Categoria: ", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 20+150, y = 10, width = 150)#E0F8F1

		lbl_cat = tk.Label(lbl_categoria, font=("verdana",16), anchor="w", backgroun="#E0F8F1")
		lbl_cat.place(x=175+150, y=8, width=700)
		lbl_cat.config(textvariable=texto_cat)

	#TABLA -> LOTES CARGADOS
	if(True):
		sbr_lotesCargados = Scrollbar(lbl_tablaCargados)
		sbr_lotesCargados.pack(side=RIGHT, fill="y")

		tabla_lotesCargados = ttk.Treeview(lbl_tablaCargados, columns=("corral", "productor", "cantidad", "categoria" , "pintura", "kg", "promedio", "estado"), selectmode=tk.BROWSE, height=7, show='headings') 
		tabla_lotesCargados.pack(side=LEFT, fill="both", expand=True)
		sbr_lotesCargados.config(command=tabla_lotesCargados.yview)
		tabla_lotesCargados.config(yscrollcommand=sbr_lotesCargados.set)

		tabla_lotesCargados.heading("corral", text="Corral", command=lambda: treeview_sort_column(tabla_lotesCargados, "corral", False))
		tabla_lotesCargados.heading("productor", text="Productor", command=lambda: treeview_sort_column(tabla_lotesCargados, "productor", False))
		tabla_lotesCargados.heading("cantidad", text="Cantidad", command=lambda: treeview_sort_column(tabla_lotesCargados, "cantidad", False))
		tabla_lotesCargados.heading("categoria", text="Categoria", command=lambda: treeview_sort_column(tabla_lotesCargados, "categoria", False))
		tabla_lotesCargados.heading("pintura", text="Pintura", command=lambda: treeview_sort_column(tabla_lotesCargados, "pintura", False))
		tabla_lotesCargados.heading("kg", text="Peso Kg", command=lambda: treeview_sort_column(tabla_lotesCargados, "kg", False))
		tabla_lotesCargados.heading("promedio", text="Promedio Kg", command=lambda: treeview_sort_column(tabla_lotesCargados, "promedio", False))
		tabla_lotesCargados.heading("estado", text="Estado", command=lambda: treeview_sort_column(tabla_lotesCargados, "estado", False))

		tabla_lotesCargados.column("corral", width=30)
		tabla_lotesCargados.column("productor", width=160)
		tabla_lotesCargados.column("cantidad", width=30)
		tabla_lotesCargados.column("categoria", width=160)
		tabla_lotesCargados.column("pintura", width=30)
		tabla_lotesCargados.column("kg", width=30)
		tabla_lotesCargados.column("promedio", width=30)
		tabla_lotesCargados.column("estado", width=30)

	#MOVER -> TABLA CARGADOS
	if(True):
		btn_moverArribaCargados = tk.Button(lbl_tablaCargadosMover, text="↑", font=("verdana",15,"bold"), backgroun="#F5D0A9", command = moverLotArriba)
		btn_moverArribaCargados.place(x = 25, y = 70, width=50, height=50)

		btn_moverAbajoCargados = tk.Button(lbl_tablaCargadosMover, text="↓", font=("verdana",15,"bold"), backgroun="#F5D0A9", command = moverLotAbajo)
		btn_moverAbajoCargados.place(x = 25, y = 130, width=50, height=50)

		btn_moverArribaTodoCargados = tk.Button(lbl_tablaCargadosMover, text="↑↑↑", font=("verdana",15,"bold"), backgroun="#F5A9A9", command = moverLotArribaTODO)
		btn_moverArribaTodoCargados.place(x = 25, y = 10, width=50, height=50)

		btn_moverAbajoTodoCargados = tk.Button(lbl_tablaCargadosMover, text="↓↓↓", font=("verdana",15,"bold"), backgroun="#F5A9A9", command = moverLotAbajoTODO)
		btn_moverAbajoTodoCargados.place(x = 25, y = 190, width=50, height=50)

	#ASIGNAR OBJETOS AL DICCIONARIOS:
	if(True):
		#Datos del catalogo
		diccionarioObjetos["entryRemate"] = entry_remate
		diccionarioObjetos["entry_catalogo"] = entry_catalogo

		diccionarioObjetos["btn_nuevo"] = btn_nuevo

		diccionarioObjetos["btn_guardar"] = btn_guardar
		diccionarioObjetos["btn_eliminar"] = btn_eliminar
		diccionarioObjetos["btn_pdf"] = btn_pdf
		



		#Tabla cat ventas
		diccionario_objetos["tabla_catVenta"] = tabla_catVenta

		#categoria seleccionada
		diccionario_objetos["texto_cat"] = texto_cat
		diccionario_objetos["texto_cat_filtrar"] = texto_cat_filtrar
		diccionario_objetos["texto_cat_id"] = texto_cat_id


		#Tabla lotes cargados
		diccionario_objetos["tabla_lotesCargados"] = tabla_lotesCargados

		"""
		diccionario_objetos[""] = 
		diccionario_objetos[""] = 
		diccionario_objetos[""] = 
		diccionario_objetos[""] = 
		"""

	#actualizarDicCat()
	#actualizarTablaCategorias()
	#actualizarProductores()
	#actualizarDatosCatalogo()

	entry_remate.insert(0, "remate1")
	#actualizarDicCat()

	#actualizarLotes()

	tabla_catVenta.bind('<Control-Up>', (lambda event: moverCatArriba()))
	tabla_catVenta.bind('<Control-Down>', (lambda event: moverCatAbajo()))
	tabla_catVenta.bind('<Double-1>', (lambda event: seleccionarTablaCat()))
	tabla_catVenta.bind('<Return>', (lambda event: seleccionarTablaCat()))

	tabla_lotesCargados.bind('<Double-1>', (lambda event: seleccionarTablaLotes()))
	tabla_lotesCargados.bind('<Control-Up>', (lambda event: moverLotArriba()))
	tabla_lotesCargados.bind('<Control-Down>', (lambda event: moverLotAbajo()))
	window.bind("<Control-s>", (lambda event: window.destroy()))
	window.mainloop()

catalogo("remate1")