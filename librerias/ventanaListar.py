#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

import tablaElegir
#from librerias import tablaElegir
#import ventanaProductor2

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Menu
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

from PIL import Image,ImageTk

import os
import os.path

import sqlite3
from sqlite3 import Error

import shutil

diccionarioObjetos = {}
dicFiltrar = {}
direccionBaseDeDatos = 'database/iltanohacienda.db'

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

def treeview_sort_column(tv, col, reverse):
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, command=lambda: \
	treeview_sort_column(tv, col, not reverse))


def ayuda():
	messagebox.showinfo("Atencion", "Ayuda no disponible")
	pass
def buscar():
	dicc = {}
	dicc.update(dicFiltrar)
	tabla = diccionarioObjetos["tabla"]

	for i in tabla.get_children():
		tabla.delete(i)

	try:
		con = sqlite3.connect(dicc["consulta"]["db"])
	except Error:
		messagebox.showerror("ERROR", "Error conectando a la base de datos")
		return 0

	cantidadFiltros = len(dicc["filtros"])
	condiciones = " WHERE "

	for i in range(0, cantidadFiltros):

		columna = str(dicc["filtros"][str(i)]["id"])
		frase = str(diccionarioObjetos["entry_" + dicc["filtros"][str(i)]["id"]].get())

		condiciones = condiciones + columna + ' LIKE "%' + frase + '%"'
		if(i < cantidadFiltros-1):
			condiciones = condiciones + " AND "


	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + dicc["consulta"]["tabla"] + condiciones + " AND estado = 'activo'")
	rows = cursorObj.fetchall()

	for row in rows:
		entities = []
		for j in range(0, len(dicc["columnas"])):
			entities.append(row[dicc["columnas"][str(j)]["row"]])
		entities = tuple(entities)

		tabla.insert("", tk.END, iid=str(row[0]), values = entities)


def imprimir():
	for i in diccionarioObjetos["tabla"].get_children():
		print (diccionarioObjetos["tabla"].item(i))
def excel():
	arch = open("cat.csv", "w")

	arch.write("CUIT;PRODUCTOR;FECHA DE CREACION\n")
	
	for i in diccionarioObjetos["tabla"].get_children():
		cuit = str(diccionarioObjetos["tabla"].item(i)["values"][0])
		nombre = str(diccionarioObjetos["tabla"].item(i)["values"][1])
		fecha = str(diccionarioObjetos["tabla"].item(i)["values"][2])
		arch.write(cuit + ";" + nombre + ";" + fecha + "\n")

	arch.close()

def filtrar(dicc):
	tabla = diccionarioObjetos["tabla"]

	for i in tabla.get_children():
		tabla.delete(i)

	try:
		con = sqlite3.connect(dicc["consulta"]["db"])
	except Error:
		messagebox.showerror("ERROR", "Error conectando a la base de datos")
		return 0

	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + dicc["consulta"]["tabla"] + dicc["consulta"]["condiciones"])
	rows = cursorObj.fetchall()

	for row in rows:
		entities = []
		for j in range(0, len(dicc["columnas"])):
			entities.append(row[dicc["columnas"][str(j)]["row"]])
		entities = tuple(entities)

		tabla.insert("", tk.END, iid=str(row[0]), values = entities)

def elegir(asdd):
	ventanaProductor2.ventana1(asdd["values"][0])

def bodyListar(window, dicc):

	dicFiltrar.update(dicc)

	lbl_filtros = tk.LabelFrame(window, backgroun="#d2e9f7")
	lbl_filtros.place(x=0, y=0, width = 976, height = 150)

	lbl_tabla = tk.LabelFrame(window, backgroun="#d2e9f7")
	lbl_tabla.place(x=0, y=152, width = 976, height = 439)

	#FILTROS
	if(True):
		#label contenedores:
		lbl_filtros_2 = Label(lbl_filtros, backgroun="#d2e9f7")
		lbl_filtros_2.grid(sticky = "e", column = 0, row=0,pady=0, padx=50)

		if(True):
			d_lbl = {}
			for i in range(0, 3):
				d_lbl[str(i)] = Label(lbl_filtros_2, backgroun="#d2e9f7")
				d_lbl[str(i)].grid(sticky = "n", column = i, row=0,pady=20, padx=20)

		seccion = 0
		varSecc = 0

		cantidadFiltros = len(dicc["filtros"])

		for i in range(0, cantidadFiltros):

			Label(d_lbl[str(seccion)], text=dicc["filtros"][str(i)]["cabeza"], backgroun="#d2e9f7").grid(sticky = "e", column = 0, row = i, padx=5, pady=6)

			diccionarioObjetos["entry_" + dicc["filtros"][str(i)]["id"]] = Entry(d_lbl[str(seccion)])
			diccionarioObjetos["entry_" + dicc["filtros"][str(i)]["id"]].grid(column = 1, row = i)
			diccionarioObjetos["entry_" + dicc["filtros"][str(i)]["id"]].bind("<Return>", (lambda event: buscar()))

			varSecc += 1
			if varSecc==3:
				seccion += 1
				varSecc = 0

	#TABLA
	if(True):
		sbr = Scrollbar(lbl_tabla)
		sbr.pack(side=RIGHT, fill="y")

		columnas = []
		for i in range(0, len(dicc["columnas"])):
			columnas.append(dicc["columnas"][str(i)]["id"])
		columnas = tuple(columnas)

		tabla = ttk.Treeview(lbl_tabla, columns=columnas, selectmode=tk.BROWSE, show='headings') 
		tabla.pack(side=LEFT, fill="both", expand=True)
		sbr.config(command=tabla.yview)
		tabla.config(yscrollcommand=sbr.set)


		for i in range(0, len(dicc["columnas"])):
			tabla.heading(dicc["columnas"][str(i)]["id"], text=dicc["columnas"][str(i)]["cabeza"], command=lambda: treeview_sort_column(tabla, dicc["columnas"][str(i)]["id"], False))
			tabla.column(dicc["columnas"][str(i)]["id"], width=dicc["columnas"][str(i)]["ancho"])


		diccionarioObjetos["tabla"] = tabla

		filtrar(dicc)

		tabla.bind("<Double-1>", (lambda event: elegir(tabla.item(tabla.selection()))))
		tabla.bind("<Return>", (lambda event: elegir(tabla.item(tabla.selection()))))



	"""
	tk.Label(windo, text = "Alias", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 1, padx=10, pady=10)
	tk.Label(windo, text = "Nombre", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)
	tk.Label(windo, text = "Descripcion", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 3, padx=10, pady=10)

	entryAlias = Entry(windo, font=("Helvetica Neue",14))
	entryRazon = Entry(windo, font=("Helvetica Neue",14), state="disabled")
	entryDescripcion = Entry(windo, font=("Helvetica Neue",14), state="disabled")

	entryAlias.grid(sticky = "w", column = 1, row = 1, padx=0, pady=10)
	entryRazon.grid(sticky = "w", column = 1, row = 2, padx=0, pady=10)
	entryDescripcion.grid(sticky = "w", column = 1, row = 3, padx=0, pady=10)

	diccionarioObjetos["entryAlias"] = entryAlias
	diccionarioObjetos["entryRazon"] = entryRazon
	diccionarioObjetos["entryDescripcion"] = entryDescripcion

	diccionarioObjetos["botBuscar"]["state"] = "normal"

	entryAlias.focus()
	entryAlias.bind('<Return>', (lambda event: verificar()))
	entryAlias.bind('<Button-1>', (lambda event: activarBuscar()))
	entryAlias.bind('<F5>', (lambda event: buscar()))

	entryRazon.bind('<Button-1>', (lambda event: desactivarBuscar()))
	entryDescripcion.bind('<Button-1>', (lambda event: desactivarBuscar()))

	entryRazon.bind('<Return>', (lambda event: entryDescripcion.focus()))
	"""

def ventana1(dicc):

	def cerrarVentana():
		window.destroy()

	dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}

	window = Tk()
	window.title("LISTAR " + dicc["seleccionar"])
	window.geometry("1000x700+200+50")
	window.configure(backgroun="#E6F5FF") #E8F6FA
	window.resizable(0,0)


	iconBuscar = Image.open('iconos/buscar.png')
	iconAyuda = Image.open('iconos/ayuda.png')
	iconCerrar = Image.open('iconos/cerrar.png')
	iconImprimir = Image.open('iconos/imprimir.png')
	iconExcel = Image.open('iconos/excel.png')


	iconBuscar = ImageTk.PhotoImage(iconBuscar)
	iconAyuda = ImageTk.PhotoImage(iconAyuda)
	iconCerrar = ImageTk.PhotoImage(iconCerrar)
	iconImprimir = ImageTk.PhotoImage(iconImprimir)
	iconExcel = ImageTk.PhotoImage(iconExcel)

	barraherr = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraherr.pack(side=TOP, fill=X, pady = 2)

	barraTitulo = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraTitulo.pack(side=TOP, fill=X)

	lblBody = tk.Label(window, backgroun="#3f7599")
	lblBody.pack(side=TOP, fill=BOTH, padx=10, pady=10)
	lblBody.config(width="1", height="100")

	botBuscar = tk.Button(barraherr, image=iconBuscar, compound="top", backgroun="#b3f2bc", command=buscar)
	botImprimir = tk.Button(barraherr, image=iconImprimir, compound="top", backgroun="#f2f0b3", command = imprimir)
	botExcel = tk.Button(barraherr, image=iconExcel, compound="top", backgroun="#f2f0b3", command = excel)
	botAyuda = tk.Button(barraherr, image=iconAyuda, compound="top", command=ayuda, backgroun="#f2f0b3")
	botCerrar = tk.Button(barraherr, image=iconCerrar, compound="top", command=cerrarVentana, backgroun="#FF6E6E")

	padX=3
	padY=2

	botBuscar.pack(side=LEFT, padx=padX+20, pady=padY)
	botImprimir.pack(side=LEFT, padx=padX, pady=padY)
	botExcel.pack(side=LEFT, padx=padX, pady=padY)
	botAyuda.pack(side=LEFT, padx=padX+20, pady=padY)
	botCerrar.pack(side=LEFT, padx=padX, pady=padY)


	textTitulo = StringVar()
	textTitulo.set(dicc["seleccionar"])
	textID = StringVar()
	textID.set("")

	lbl_titulo = tk.Label(barraTitulo, font=("Helvetica Neue",10,"bold"), anchor="n", backgroun="#BAE7FF")
	lbl_titulo.pack()
	lbl_titulo.config(textvariable=textTitulo)

	diccionarioObjetos["botBuscar"] = botBuscar

	diccionarioObjetos["textTitulo"] = textTitulo
	diccionarioObjetos["textID"] = textID
	

	window.bind("<Control-s>", (lambda event: cerrarVentana()))

	bodyListar(lblBody, dicc)

	window.mainloop()

dicProd = {
	"seleccionar" : "PRODUCTORES",
	
	"columnas" : {
		"0":{
			"id" : "num1", 
			"cabeza" : "ALIAS", 
			"ancho" : 100, 
			"row" : 1}, 
		"1":{
			"id" : "num2", 
			"cabeza" : "RAZON SOCIAL", 
			"ancho" : 100, 
			"row" : 2},
		"2":{
			"id" : "num3", 
			"cabeza" : "CUIT", 
			"ancho" : 30, 
			"row" : 3},
		"3":{
			"id" : "num4", 
			"cabeza" : "COND. IVA", 
			"ancho" : 30, 
			"row" : 6},
		"4":{
			"id" : "num5", 
			"cabeza" : "LOCALIDAD", 
			"ancho" : 30, 
			"row" : 8},
		"5":{
			"id" : "num6", 
			"cabeza" : "OBSERVACIONES", 
			"ancho" : 100, 
			"row" : 13}},
	
	"consulta": {
		"db" : 'database/iltanohacienda.db',
		"tabla" : "productores",
		"condiciones" : ''},
	"filtros" : {
		"0" : {
			"id": "nombre",
			"cabeza":"Alias",
		},
		"1" : {
			"id": "razon",
			"cabeza":"Razon Social",
		},
		"2" : {
			"id": "ndoc",
			"cabeza":"N° doc",
		},
		"3" : {
			"id": "con_iva",
			"cabeza":"Cond. IVA",
		},
		"4" : {
			"id": "localidad",
			"cabeza":"Localidad",
		},
		"5" : {
			"id": "provincia",
			"cabeza":"Provincia",
		},
	},
	}
dicRemates = {
	"seleccionar" : "REMATES",
	
	"columnas" : {
		"0":{
			"id" : "num1", 
			"cabeza" : "ALIAS", 
			"ancho" : 100, 
			"row" : 1}, 
		"1":{
			"id" : "num2", 
			"cabeza" : "FECHA", 
			"ancho" : 20, 
			"row" : 2},
		"2":{
			"id" : "num3", 
			"cabeza" : "PREDIO", 
			"ancho" : 100, 
			"row" : 4},
		"3":{
			"id" : "num4", 
			"cabeza" : "MARTILLO", 
			"ancho" : 100, 
			"row" : 6},
		"4":{
			"id" : "num5", 
			"cabeza" : "OBSERVACIONES", 
			"ancho" : 100, 
			"row" : 7},
		},
	
	"consulta": {
		"db" : 'database/iltanohacienda.db',
		"tabla" : "remate",
		"condiciones" : ' WHERE estado = "activo"'},
	"filtros" : {
		"0" : {
			"id": "nombre",
			"cabeza":"Alias",
		},
		"1" : {
			"id": "fecha",
			"cabeza":"Fecha",
		},
		"2" : {
			"id": "tipo",
			"cabeza":"Tipo",
		},
		"3" : {
			"id": "predio",
			"cabeza":"Predio",
		},
		"4" : {
			"id": "localidad",
			"cabeza":"Localidad",
		},
		"5" : {
			"id": "martillo",
			"cabeza":"Martillo",
		},
	},
	}
dicLotes = {
	"seleccionar" : "LOTES",
	
	"columnas" : {
		"0":{
			"id" : "num1", 
			"cabeza" : "CORRAL", 
			"ancho" : 20, 
			"row" : 4}, 
		"1":{
			"id" : "num2", 
			"cabeza" : "VENDEDOR", 
			"ancho" : 200, 
			"row" : 2},
		"2":{
			"id" : "num3", 
			"cabeza" : "CANTIDAD", 
			"ancho" : 20, 
			"row" : 3},
		"3":{
			"id" : "num4", 
			"cabeza" : "CATEGORIA", 
			"ancho" : 200, 
			"row" : 6},
		"4":{
			"id" : "num5", 
			"cabeza" : "KGs", 
			"ancho" : 20, 
			"row" : 12},
		"5":{
			"id" : "num6", 
			"cabeza" : "Promedio", 
			"ancho" : 20, 
			"row" : 13},
		},
	
	"consulta": {
		"db" : 'database/iltanohacienda.db',
		"tabla" : "lotes",
		"condiciones" : ' WHERE estado = "activo"'},
	"filtros" : {
		"0" : {
			"id": "remate",
			"cabeza":"Remate",
		},
		"1" : {
			"id": "productor",
			"cabeza":"Vendedor",
		},
		"2" : {
			"id": "cantidad",
			"cabeza":"Cantidad",
		},
		"3" : {
			"id": "corral",
			"cabeza":"Corral",
		},
		"4" : {
			"id": "catVenta",
			"cabeza":"Categoria Venta",
		},
		"5" : {
			"id": "catHacienda",
			"cabeza":"Categoria Hacienda",
		},
	},
	}
ventana1(dicRemates)