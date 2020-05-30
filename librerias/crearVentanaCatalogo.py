#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

import ventanaIngreso
import PDF_catalogo

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

diccionario_textos = {}
diccionario_objetos = {}
diccionario_pinturas = {}
dicCat = {}
dicCatUbic = {}
dicProductores = {}

direccionBaseDeDatos = 'database/iltanohacienda.db'

dire = "C:/Users/Santiago/Desktop/mipdf2.pdf"

dicLotes = {}
dicLotesUbic = {}

remate = "remate1"


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

#Productores
def actualizarProductores():
	con = sql_connection()
	condiciones = ""
	rows = actualizar_db(con, "productores", condiciones)
	for row in rows:
		dicProductores[str(row[3])] = str(row[1])

#CATEGORIA
def actualizarDicCat():
	con = sql_connection()
	rows = actualizar_db(con, "catVenta", "")

	cantidadTotal = 0
	cabezasTotal = 0

	try:
		for row in rows:
			con = sql_connection()
			condiciones = " WHERE estado = 'activo' AND catVenta = '" + str(row[2]) + "'"
			rows_lotes = actualizar_db2(con, "lotes", condiciones)

			cantidad = len(rows_lotes)
			if cantidad>0:
				cabezas = 0
				for row_lote in rows_lotes:
					cabezas = cabezas + int(row_lote[0])
				dicCat[str(row[0])] = {"cantidad" : cantidad, "cabezas" : cabezas,"alias" : str(row[1]), "nombre" : str(row[2])}

				cantidadTotal = cantidadTotal + cantidad
				cabezasTotal = cabezasTotal + cabezas

		actualizarDicCatUbic()

		diccionario_objetos["entry_totalCorrales"].delete(0, tk.END)
		diccionario_objetos["entry_totalIngresados"].delete(0, tk.END)

		diccionario_objetos["entry_totalCorrales"].insert(0, cantidadTotal)
		diccionario_objetos["entry_totalIngresados"].insert(0, cabezasTotal)
		
	except:
		messagebox.showerror("ERROR", "Error al cargar")
def actualizarDicCatUbic():
	cant = len(dicCat)
	llaves = list(dicCat.keys())

	try:
		for i in range(0, cant):
			dicCatUbic[str(i)] = llaves[i]
		actualizarTablaCategorias()
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
		messagebox.showerror("ERROR", "Error al cargar los productores usados")
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
		con = sql_connection()
		cateVent = dicCat[str(dicCatUbic[str(i)])]["nombre"]
		condiciones = " WHERE estado = 'activo' AND catVenta = '" + cateVent + "'"

		rows = actualizar_db(con, "lotes", condiciones)

		cant_lotes = len(rows)

		id_cateVenta = str(dicCatUbic[str(i)])
		dicLotes[id_cateVenta] = {}
		dicLotesUbic[id_cateVenta] = {}

		j=0

		for row in rows:
			productor = dicProductores[str(row[2])]

			dicLotes[id_cateVenta][str(row[0])] = {
			"corral" : str(row[4]),
			"productor" : productor,
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






	#print(rows)

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


def catalogo(window):
	padX = 5
	padY = 5

	lbl_datos = Label(window, backgroun="#E0F8F1")
	lbl_tablaCategorias = Label(window)
	lbl_tablaCategoriasMover = Label(window, backgroun="#E0F8F1")
	lbl_acciones = Label(window, backgroun="#E0F8F1")
	lbl_categoria = Label(window, backgroun="#E0F8F1")
	lbl_filtrar = Label(window, backgroun="#E0F8F1")
	lbl_tabla = Label(window)
	lbl_cargar = Label(window, backgroun="#E0F8F1")
	lbl_tablaCargados = Label(window)
	lbl_tablaCargadosMover = Label(window, backgroun="#E0F8F1")

	mod_alt = 0
	var_bajar = 50

	lbl_datos.place(x = 2, y = 2+mod_alt, width = 300, height = 250)
	lbl_tablaCategorias.place(x = 304, y = 2+mod_alt, width = 450, height = 250)
	lbl_tablaCategoriasMover.place(x = 756, y = 2+mod_alt, width = 100, height = 250)
	lbl_acciones.place(x = 858, y = 2+mod_alt, width = 425, height = 250)
	lbl_categoria.place(x = 2, y = 204+mod_alt+var_bajar, width = 1281, height = 48)
	#lbl_filtrar.place(x = 2, y = 254+mod_alt+var_bajar, width = 150, height = 370)
	#lbl_tabla.place(x = 154, y = 254+mod_alt+var_bajar, width = 500, height = 370)
	#lbl_cargar.place(x = 2, y = 254+mod_alt+var_bajar, width = 100, height = 370)
	lbl_tablaCargados.place(x = 2, y = 254+mod_alt+var_bajar, width = 1179, height = 370)
	lbl_tablaCargadosMover.place(x = 1183, y = 254+mod_alt+var_bajar, width = 100, height = 370)

	#DATOS DE CATALOGO
	if(True):	
		tk.Label(lbl_datos, text="Datos catálogo", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 2, width = 298)
	
		tk.Label(lbl_datos, text="Fecha:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 50, width = 80)
		tk.Label(lbl_datos, text="Titulo:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 80, width = 80)
		tk.Label(lbl_datos, text="Predio:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 110, width = 80)
		tk.Label(lbl_datos, text="Localidad:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 140, width = 80)
		tk.Label(lbl_datos, text="Remata:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 170, width = 80)
		tk.Label(lbl_datos, text="Total ingresados", font=("Helvetica Neue",10), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 200, width = 150)
		tk.Label(lbl_datos, text="Total corrales", font=("Helvetica Neue",10), anchor="c", backgroun="#E0F8F1").place(x = 140, y = 200, width = 150)

		entry_datosFecha = Entry(lbl_datos)
		entry_datosFecha.place(x = 90, y = 50, width = 180)

		entry_datosTitulo = Entry(lbl_datos)
		entry_datosTitulo.place(x = 90, y = 80, width = 180)

		entry_datosPredio = Entry(lbl_datos)
		entry_datosPredio.place(x = 90, y = 110, width = 180)

		entry_datosLocalidad = Entry(lbl_datos)
		entry_datosLocalidad.place(x = 90, y = 140, width = 180)

		entry_datosRemata = Entry(lbl_datos)
		entry_datosRemata.place(x = 90, y = 170, width = 180)

		entry_totalIngresados = Entry(lbl_datos)
		entry_totalIngresados.place(x = 25, y = 220, width = 100)

		entry_totalCorrales = Entry(lbl_datos)
		entry_totalCorrales.place(x = 165, y = 220, width = 100)

	#TABLA -> CATEGORIAS DE VENTA
	if(True):
		sbr_catVenta = Scrollbar(lbl_tablaCategorias)
		sbr_catVenta.pack(side=RIGHT, fill="y")

		tabla_catVenta = ttk.Treeview(lbl_tablaCategorias, columns=("cabezas", "alias", "nombre"), selectmode=tk.BROWSE, height=7) 
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
		btn_moverArribaCat = tk.Button(lbl_tablaCategoriasMover, text="↑", font=("verdana",15,"bold"), backgroun="#F5D0A9", command = moverCatArriba)
		btn_moverArribaCat.place(x = 25, y = 70, width=50, height=50)

		btn_moverAbajoCat = tk.Button(lbl_tablaCategoriasMover, text="↓", font=("verdana",15,"bold"), backgroun="#F5D0A9", command = moverCatAbajo)
		btn_moverAbajoCat.place(x = 25, y = 130, width=50, height=50)

		btn_moverArribaTodoCat = tk.Button(lbl_tablaCategoriasMover, text="↑↑↑", font=("verdana",15,"bold"), backgroun="#F5A9A9", command = moverCatArribaTODO)
		btn_moverArribaTodoCat.place(x = 25, y = 10, width=50, height=50)

		btn_moverAbajoTodoCat = tk.Button(lbl_tablaCategoriasMover, text="↓↓↓", font=("verdana",15,"bold"), backgroun="#F5A9A9", command = moverCatAbajoTODO)
		btn_moverAbajoTodoCat.place(x = 25, y = 190, width=50, height=50)

	#ACCIONES
	if(True):
		btn_pdf = tk.Button(lbl_acciones, text="Generar PDF", font=("verdana",10), backgroun="#F5D0A9", command=exportar)
		btn_pdf.place(x = 20, y = 30, width=110, height=30)

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


	#FILTRAR
	if(True):
		tk.Label(lbl_filtrar, text="Filtrar", font=("Helvetica Neue",12, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 2, width = 149)

		tk.Label(lbl_filtrar, text="Productor", font=("Helvetica Neue",10), anchor="w", backgroun="#E0F8F1").place(x = 8, y = 30, width = 149)
		tk.Label(lbl_filtrar, text="Corral", font=("Helvetica Neue",10), anchor="w", backgroun="#E0F8F1").place(x = 8, y = 100, width = 149)
		tk.Label(lbl_filtrar, text="Cat. hacienda", font=("Helvetica Neue",10), anchor="w", backgroun="#E0F8F1").place(x = 8, y = 170, width = 149)

		entry_filtrarProductor = Entry(lbl_filtrar)
		entry_filtrarProductor.place(x = 10, y = 50, width = 130)

		entry_filtrarCorral = Entry(lbl_filtrar)
		entry_filtrarCorral.place(x = 10, y = 120, width = 130)

		entry_filtrarCat = Entry(lbl_filtrar)
		entry_filtrarCat.place(x = 10, y = 190, width = 130)


		btn_filtrar = tk.Button(lbl_filtrar, text="Filtrar", font=("verdana",10), backgroun="#F5D0A9")
		btn_filtrar.place(x = 20, y = 230, width=110, height=30)

		btn_filtrarMostrarTodo = tk.Button(lbl_filtrar, text="Mostrar Todo", font=("verdana",10), backgroun="#F5D0A9")
		btn_filtrarMostrarTodo.place(x = 20, y = 270, width=110, height=30)

	#TABLA -> LOTES
	#if(True):
		sbr_lotes = Scrollbar(lbl_tabla)
		sbr_lotes.pack(side=RIGHT, fill="y")

		tabla_lotes = ttk.Treeview(lbl_tabla, columns=("productor", "cantidad", "categoria" , "pintura", "kg", "promedio"), selectmode=tk.BROWSE, height=7) 
		tabla_lotes.pack(side=LEFT, fill="both", expand=True)
		sbr_lotes.config(command=tabla_lotes.yview)
		tabla_lotes.config(yscrollcommand=sbr_lotes.set)

		tabla_lotes.heading("#0", text="Corral")
		tabla_lotes.heading("productor", text="Productor")
		tabla_lotes.heading("cantidad", text="Cantidad")
		tabla_lotes.heading("categoria", text="Categoria Hacienda")
		tabla_lotes.heading("pintura", text="Pintura")
		tabla_lotes.heading("kg", text="Peso")
		tabla_lotes.heading("promedio", text="Promedio")

		tabla_lotes.column("#0", width=30)
		tabla_lotes.column("productor", width=50)
		tabla_lotes.column("cantidad", width=30)
		tabla_lotes.column("categoria", width=50)
		tabla_lotes.column("pintura", width=30)
		tabla_lotes.column("kg", width=30)
		tabla_lotes.column("promedio", width=30)

	#CARGAR
	#if(True):
		tk.Label(lbl_cargar, text="Cargar", font=("Helvetica Neue",12, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 2, width = 100)

		

		#select.get()
		select = IntVar()
		select.set(1)
		rad1 = tk.Radiobutton(lbl_cargar,text='Corral', value=1,variable = select, font=("verdana",10), anchor="w", bg='#E0F8F1')
		rad2 = tk.Radiobutton(lbl_cargar,text='Productor', value=2,variable = select, font=("verdana",10), anchor="w", bg='#E0F8F1')
		rad3 = tk.Radiobutton(lbl_cargar,text='Cat. Hac.', value=3,variable = select, font=("verdana",10), anchor="w", bg='#E0F8F1')
		rad4 = tk.Radiobutton(lbl_cargar,text='Kgs', value=4,variable = select, font=("verdana",10), anchor="w", bg='#E0F8F1')

		mod_alt = 30

		rad1.place(x=5, y=10+mod_alt, width = 95)
		rad2.place(x=5, y=30+mod_alt, width = 95)
		rad3.place(x=5, y=50+mod_alt, width = 95)
		rad4.place(x=5, y=70+mod_alt, width = 95)


		btn_cargarAscendente = tk.Button(lbl_cargar, text="Ascendente", font=("verdana",9, "bold"), backgroun="#CBF9E1")
		btn_cargarAscendente.place(x = 5, y = 140, width=90, height=25)

		btn_cargarDescendente = tk.Button(lbl_cargar, text="Descendente", font=("verdana",9, "bold"), backgroun="#CBF9E1")
		btn_cargarDescendente.place(x = 5, y = 170, width=90, height=25)

		btn_filtrarMostrarTodo = tk.Button(lbl_cargar, text="Borrar", font=("verdana",10, "bold"), backgroun="#EF9090")
		btn_filtrarMostrarTodo.place(x = 5, y = 230, width=90, height=35)

		btn_filtrarMostrarTodo = tk.Button(lbl_cargar, text="Borrar\nTodo", font=("verdana",10, "bold"), backgroun="#EF9090")
		btn_filtrarMostrarTodo.place(x = 5, y = 270, width=90, height=35)

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
		diccionario_objetos["entry_datosFecha"] = entry_datosFecha
		diccionario_objetos["entry_datosTitulo"] = entry_datosTitulo
		diccionario_objetos["entry_datosPredio"] = entry_datosPredio
		diccionario_objetos["entry_datosLocalidad"] = entry_datosLocalidad
		diccionario_objetos["entry_datosRemata"] = entry_datosRemata
		diccionario_objetos["entry_totalIngresados"] = entry_totalIngresados
		diccionario_objetos["entry_totalCorrales"] = entry_totalCorrales

		#Tabla cat ventas
		diccionario_objetos["tabla_catVenta"] = tabla_catVenta

		#categoria seleccionada
		diccionario_objetos["texto_cat"] = texto_cat
		diccionario_objetos["texto_cat_filtrar"] = texto_cat_filtrar
		diccionario_objetos["texto_cat_id"] = texto_cat_id

		#Filtrar
		diccionario_objetos["entry_filtrarProductor"] = entry_filtrarProductor
		diccionario_objetos["entry_filtrarCorral"] = entry_filtrarCorral
		diccionario_objetos["entry_filtrarCat"] = entry_filtrarCat

		#Tabla lotes cargados
		diccionario_objetos["tabla_lotesCargados"] = tabla_lotesCargados

		#CARGAR
		diccionario_objetos["select"] = select

		"""
		diccionario_objetos[""] = 
		diccionario_objetos[""] = 
		diccionario_objetos[""] = 
		diccionario_objetos[""] = 
		"""


	actualizarDicCat()
	#actualizarTablaCategorias()
	actualizarProductores()


	actualizarDatosCatalogo()
	actualizarLotes()

	tabla_catVenta.bind('<Control-Up>', (lambda event: moverCatArriba()))
	tabla_catVenta.bind('<Control-Down>', (lambda event: moverCatAbajo()))
	tabla_catVenta.bind('<Double-1>', (lambda event: seleccionarTablaCat()))
	tabla_catVenta.bind('<Return>', (lambda event: seleccionarTablaCat()))

	tabla_lotesCargados.bind('<Double-1>', (lambda event: seleccionarTablaLotes()))
	tabla_lotesCargados.bind('<Control-Up>', (lambda event: moverLotArriba()))
	tabla_lotesCargados.bind('<Control-Down>', (lambda event: moverLotAbajo()))




window1 = Tk()
window1.title("Catalogo")
window1.geometry("1285x728")
window1.configure(backgroun="#2C4D4F") #E8F6FA
catalogo(window1)
window1.mainloop()
