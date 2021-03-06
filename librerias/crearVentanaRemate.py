#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

#import ventanaIngreso
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
diccionario_objetos["ID_LOTE_A_EDITAR"] = "NULL"

direccionBaseDeDatos = 'database/iltanohacienda.db'

dire = "C:/Users/Santiago/Desktop/mipdf2.pdf"

dicLotes = {}
dicLotesUbic = {}

rematename = "remate1"

padX = 5
padY = 5

def treeview_sort_column(tv, col, reverse):
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, command=lambda: \
	treeview_sort_column(tv, col, not reverse))

	#tablaADicLotesUbic()

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

def actualizarProductores():
	con = sql_connection()
	condiciones = ""
	rows = actualizar_db(con, "productores", condiciones)
	for row in rows:
		dicProductores[str(row[3])] = str(row[1])

#Tabla lotes
def lotesFiltrar():
	pal_claveCorral = str(diccionario_objetos["entry_corralVendedor"].get())
	pal_clavePintura = str(diccionario_objetos["entry_pinturaVendedor"].get())
	pal_claveVendedor = str(diccionario_objetos["entry_vendedorVendedor"].get())

	con = sql_connection()
	condiciones =  ' WHERE corral LIKE "%' + pal_claveCorral + '%" AND pintura LIKE "%' + pal_clavePintura + '%" AND productor LIKE "%' + pal_claveVendedor + '%" AND estado = "activo" AND remate = "' + rematename + '"'
	rows = actualizar_db(con, "lotes", condiciones)

	dicAux = {}

	if(len(rows)==0):
		messagebox.showerror("ERROR", "No se encontro en la base de datos")
		return 0

	i = 0
	for row in rows:
		dicAux[str(i)] = {
		"id" : str(row[0]),
		"corral" : str(row[4]),
		"productor" : dicProductores[str(row[2])],
		"cantidad" : str(row[3]),
		"categoria" : str(row[6]),
		"pintura" : str(row[7]),
		"peso" : str(row[12]),
		"promedio" : str(row[13]),
		"cuit" : str(str(row[2])),
		}
		i+=1

	if(len(rows)==1):
		cargarDatosVendedor(rows[0][2])
		cargarDatosLotes(rows[0][0])

		diccionario_objetos["entry_corralVendedor"].delete(0, tk.END)
		diccionario_objetos["entry_pinturaVendedor"].delete(0, tk.END)
		diccionario_objetos["entry_vendedorVendedor"].delete(0, tk.END)

		diccionario_objetos["entry_comprador"].focus()
		return 0

	cargarTablaLotes(dicAux)
	borrarDatosLoteComprador()

def actualizarTablaLotes():
	con = sql_connection()
	condiciones = " WHERE remate = '" + rematename + "' AND estado = 'activo'"
	rows = actualizar_db(con, "lotes", condiciones)

	i=0
	for row in rows:
		dicLotes[str(i)] = {
		"id" : str(row[0]),
		"corral" : str(row[4]),
		"productor" : dicProductores[str(row[2])],
		"cantidad" : str(row[3]),
		"categoria" : str(row[6]),
		"pintura" : str(row[7]),
		"peso" : str(row[12]),
		"promedio" : str(row[13]),
		"cuit" : str(str(row[2])),
		}
		i+=1
	cargarTablaLotes(dicLotes)
def cargarTablaLotes(dicLotesCargar):
	tabla = diccionario_objetos["tabla_lotesCargados"]

	cant_lotes = len(dicLotesCargar)

	try:
		for i in tabla.get_children():
			tabla.delete(i)

		for i in range(0, cant_lotes):
			tabla.insert("", str(i), tags=(str(dicLotesCargar[str(i)]["id"]), str(dicLotesCargar[str(i)]["cuit"])), text = str(i), iid= str(i), values = (str(dicLotesCargar[str(i)]["corral"]),
				str(dicLotesCargar[str(i)]["productor"]),
				str(dicLotesCargar[str(i)]["cantidad"]),
				str(dicLotesCargar[str(i)]["categoria"]),
				str(dicLotesCargar[str(i)]["pintura"]),
				str(dicLotesCargar[str(i)]["peso"]),
				str(dicLotesCargar[str(i)]["promedio"]),))
	except:
		messagebox.showerror("ERROR", "Error al cargar")






	#print(rows)

def seleccionarTablaLote():
	tabla = diccionario_objetos["tabla_lotesCargados"]

	seleccion = tabla.item(tabla.selection())

	lote = seleccion["tags"][0]
	productor = seleccion["tags"][1]

	borrarDatosMontosCalculos()
	cargarDatosVendedor(productor)
	cargarDatosLotes(lote)
def cargarDatosVendedor(productor):
	con = sql_connection()
	condiciones = " WHERE ndoc = '" + str(productor) + "'"
	rows = actualizar_db(con, "productores", condiciones)

	row = rows[0]

	texto_alias = str(row[1])
	texto_razon = str(row[2])
	texto_cuit = str(row[3])
	texto_ruca = str(row[19])
	texto_observaciones = str(row[13])

	diccionario_objetos["texto_aliasVendedor"].set(texto_alias)
	diccionario_objetos["texto_razonVendedor"].set(texto_razon)
	diccionario_objetos["texto_cuitVendedor"].set(texto_cuit)
	diccionario_objetos["texto_rucaVendedor"].set(texto_ruca)

	diccionario_objetos["txt_observacionesVendedor"].configure(state="normal")
	diccionario_objetos["txt_observacionesVendedor"].delete("1.0", tk.END)
	diccionario_objetos["txt_observacionesVendedor"].insert("1.0", texto_observaciones)
	diccionario_objetos["txt_observacionesVendedor"].configure(state="disabled")
def cargarDatosLotes(lote):
	con = sql_connection()
	condiciones = " WHERE estado = 'activo' AND remate = '" + rematename + "' AND lote = '" + str(lote) + "'"
	rows = actualizar_db(con, "compraventa", condiciones)

	if(len(rows)==1):
		MsgBox = messagebox.askquestion('ATENCION', 'Este lote ya ha sido cargado ¿Desea cargarlo?', icon = 'warning')
		if(MsgBox == 'yes'):
			id_compraventa = rows[0][0]
			id_comprador = rows[0][2]
			precio = rows[0][3]

			con = sql_connection()
			condiciones = " WHERE id = '" + str(lote) + "'"
			rows = actualizar_db(con, "lotes", condiciones)
			row = rows[0]
			diccionario_objetos["ID_LOTE_A_EDITAR"] = str(id_compraventa)
			diccionario_objetos["ID_LOTE"] = lote
			diccionario_objetos["datosLote_texto_catHacienda"].set(str(row[6]))
			diccionario_objetos["datosLote_texto_catVenta"].set(str(row[5]))
			diccionario_objetos["datosLote_texto_corral"].set(str(row[4]))
			diccionario_objetos["datosLote_texto_cantidad"].set(str(row[3]))
			diccionario_objetos["datosLote_texto_neto"].set(str(row[12]))
			diccionario_objetos["datosLote_texto_promedio"].set(str(row[13]))

			diccionario_objetos["datosLote_txt_observaciones"].configure(state="normal")
			diccionario_objetos["datosLote_txt_observaciones"].delete("1.0", tk.END)
			diccionario_objetos["datosLote_txt_observaciones"].insert("1.0", (str(row[14])) + " - " + (str(row[15])))
			diccionario_objetos["datosLote_txt_observaciones"].configure(state="disabled")

			cargarDatosComprador(id_comprador)
			diccionario_objetos["entry_kilo"].delete(0, tk.END)
			diccionario_objetos["entry_kilo"].insert(0, precio)
			calcularKilo(precio)


		
	else:
		con = sql_connection()
		condiciones = " WHERE id = '" + str(lote) + "'"
		rows = actualizar_db(con, "lotes", condiciones)

		row = rows[0]

		diccionario_objetos["ID_LOTE_A_EDITAR"] = "NULL"
		diccionario_objetos["ID_LOTE"] = lote
		diccionario_objetos["datosLote_texto_catHacienda"].set(str(row[6]))
		diccionario_objetos["datosLote_texto_catVenta"].set(str(row[5]))
		diccionario_objetos["datosLote_texto_corral"].set(str(row[4]))
		diccionario_objetos["datosLote_texto_cantidad"].set(str(row[3]))
		diccionario_objetos["datosLote_texto_neto"].set(str(row[12]))
		diccionario_objetos["datosLote_texto_promedio"].set(str(row[13]))

		diccionario_objetos["datosLote_txt_observaciones"].configure(state="normal")
		diccionario_objetos["datosLote_txt_observaciones"].delete("1.0", tk.END)
		diccionario_objetos["datosLote_txt_observaciones"].insert("1.0", (str(row[14])) + " - " + (str(row[15])))
		diccionario_objetos["datosLote_txt_observaciones"].configure(state="disabled")



#Tabla Compradores
def compradorFiltrar():
	pal_clave = str(diccionario_objetos["entry_comprador"].get())

	con = sql_connection()
	condiciones =  ' WHERE (nombre LIKE "%' + pal_clave + '%" OR razon LIKE "%' + pal_clave + '%" OR ndoc LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%" OR con_iva LIKE "%' + pal_clave + '%" OR localidad LIKE "%' + pal_clave + '%" OR provincia LIKE "%' + pal_clave + '%" OR ruca LIKE "%' + pal_clave + '%" OR establecimiento LIKE "%' + pal_clave + '%") AND estado = "activo"'
	rows = actualizar_db(con, "productores", condiciones)
	if(len(rows)==1):
		cargarDatosComprador(rows[0][3])
		cargarTablaCompradores([])
	else:
		cargarTablaCompradores(rows)
def cargarTablaCompradores(rows):
	tabla = diccionario_objetos["tabla_compradores"]

	for j in tabla.get_children():
		tabla.delete(j)

	try:
		for row in rows:
			texto_alias = str(row[1])
			texto_cuit = str(row[3])

			tabla.insert("", tk.END, tags=(str(row[0]), str(row[3])), values = (texto_alias,
				texto_cuit,))
	except:
		messagebox.showerror("ERROR", "Error al cargar")

def seleccionarTablaComprador():
	tabla = diccionario_objetos["tabla_compradores"]

	seleccion = tabla.item(tabla.selection())

	productor = seleccion["tags"][1]

	cargarDatosComprador(productor)
def cargarDatosComprador(productor):
	con = sql_connection()
	condiciones = " WHERE ndoc = '" + str(productor) + "'"
	rows = actualizar_db(con, "productores", condiciones)

	row = rows[0]

	texto_alias = str(row[1])
	texto_razon = str(row[2])
	texto_cuit = str(row[3])
	texto_ruca = str(row[19])
	texto_observaciones = str(row[13])

	diccionario_objetos["texto_aliasComprador"].set(texto_alias)
	diccionario_objetos["texto_razonComprador"].set(texto_razon)
	diccionario_objetos["texto_cuitComprador"].set(texto_cuit)
	diccionario_objetos["texto_rucaComprador"].set(texto_ruca)

	diccionario_objetos["txt_observacionesComprador"].configure(state="normal")
	diccionario_objetos["txt_observacionesComprador"].delete("1.0", tk.END)
	diccionario_objetos["txt_observacionesComprador"].insert("1.0", texto_observaciones)
	diccionario_objetos["txt_observacionesComprador"].configure(state="disabled")

#CONSTRUCTORES
def labelLoteBuscar(lbl_lote):
	lbl_buscar = tk.LabelFrame(lbl_lote, text="Buscar LOTE", backgroun="#E0F8F1")
	lbl_buscar.place(x = 30, y = 0, width = 260, height = 198)

	tk.Label(lbl_buscar, text="Corral:", font=("Helvetica Neue",20, "bold"), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 0, width = 120)
	tk.Label(lbl_buscar, text="Pintura:", font=("Helvetica Neue",20, "bold"), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 50, width = 120)
	tk.Label(lbl_buscar, text="Vendedor:", font=("Helvetica Neue",10, "bold"), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 100, width = 120)

	entry_corral = Entry(lbl_buscar, font=("verdana",20))
	entry_pintura = Entry(lbl_buscar, font=("verdana",20))
	entry_vendedor = Entry(lbl_buscar, font=("verdana",10))

	entry_corral.place(x = 130, y = 0, width = 100)
	entry_pintura.place(x = 130, y = 50, width = 100)
	entry_vendedor.place(x = 130, y = 100, width = 100)

	btn_buscar = tk.Button(lbl_buscar, text="Buscar", font=("verdana",12, "bold"), backgroun="#CBF9E1", command = lotesFiltrar)
	btn_buscar.place(x = 60, y = 135, width=140, height=40)


	diccionario_objetos["entry_corralVendedor"] = entry_corral
	diccionario_objetos["entry_pinturaVendedor"] = entry_pintura
	diccionario_objetos["entry_vendedorVendedor"] = entry_vendedor

	def entryCorral():
		entry_pintura.focus()
		lotesFiltrar()
	def entryPintura():
		entry_vendedor.focus()
		lotesFiltrar()
	def entryVendedor():
		diccionario_objetos["entry_comprador"].focus()
		lotesFiltrar()

	entry_corral.bind("<Return>", (lambda event: entryCorral()))
	entry_pintura.bind("<Return>", (lambda event: entryPintura()))
	entry_vendedor.bind("<Return>", (lambda event: entryVendedor()))
def labelLoteTabla(lbl_lote):
	lbl_tabla = Label(lbl_lote)
	lbl_tabla.place(x = 300, y = 2, width = 600, height = 196)

	sbr_lotesCargados = Scrollbar(lbl_tabla)
	sbr_lotesCargados.pack(side=RIGHT, fill="y")

	tabla_lotesCargados = ttk.Treeview(lbl_tabla, columns=("corral", "productor", "cantidad", "categoria" , "pintura", "kg", "promedio"), selectmode=tk.BROWSE, height=7, show='headings') 
	tabla_lotesCargados.pack(side=LEFT, fill="both", expand=True)
	sbr_lotesCargados.config(command=tabla_lotesCargados.yview)
	tabla_lotesCargados.config(yscrollcommand=sbr_lotesCargados.set)

	tabla_lotesCargados.heading("corral", text="Corral", command=lambda: treeview_sort_column(tabla_lotesCargados, "corral", False))
	tabla_lotesCargados.heading("productor", text="Productor", command=lambda: treeview_sort_column(tabla_lotesCargados, "productor", False))
	tabla_lotesCargados.heading("cantidad", text="Cant", command=lambda: treeview_sort_column(tabla_lotesCargados, "cantidad", False))
	tabla_lotesCargados.heading("categoria", text="Categoria", command=lambda: treeview_sort_column(tabla_lotesCargados, "categoria", False))
	tabla_lotesCargados.heading("pintura", text="Pint", command=lambda: treeview_sort_column(tabla_lotesCargados, "pintura", False))
	tabla_lotesCargados.heading("kg", text="Peso", command=lambda: treeview_sort_column(tabla_lotesCargados, "kg", False))
	tabla_lotesCargados.heading("promedio", text="Prom", command=lambda: treeview_sort_column(tabla_lotesCargados, "promedio", False))

	tabla_lotesCargados.column("corral", width=30)
	tabla_lotesCargados.column("productor", width=160)
	tabla_lotesCargados.column("cantidad", width=30)
	tabla_lotesCargados.column("categoria", width=100)
	tabla_lotesCargados.column("pintura", width=30)
	tabla_lotesCargados.column("kg", width=30)
	tabla_lotesCargados.column("promedio", width=30)

	diccionario_objetos["tabla_lotesCargados"] = tabla_lotesCargados

	tabla_lotesCargados.bind('<Double-1>', (lambda event: seleccionarTablaLote()))
	tabla_lotesCargados.bind('<Return>', (lambda event: seleccionarTablaLote()))
def labelLoteInfor(lbl_lote):
	lbl_info = tk.LabelFrame(lbl_lote, text="VENDEDOR", backgroun="#E0F8F1")
	lbl_info.place(x = 910, y = 0, width = 368, height = 198)

	texto_alias = StringVar()
	texto_alias.set("") # Caso 1
	texto_razon = StringVar()
	texto_razon.set("")
	texto_cuit = StringVar()
	texto_cuit.set("     -")
	texto_ruca = StringVar()
	texto_ruca.set("     -")


	lbl_alias = tk.Label(lbl_info, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_alias.place(x=0, y=0, width=350)
	lbl_alias.config(textvariable=texto_alias)

	lbl_razon = tk.Label(lbl_info, font=("Helvetica Neue",10), anchor="w", backgroun="#E0F8F1")
	lbl_razon.place(x=0, y=30, width=350)
	lbl_razon.config(textvariable=texto_razon)

	lbl_cuit = tk.Label(lbl_info, font=("verdana",12), anchor="w", backgroun="#E0F8F1")
	lbl_cuit.place(x=40, y=63, width=140)
	lbl_cuit.config(textvariable=texto_cuit)

	lbl_ruca = tk.Label(lbl_info, font=("verdana",12), anchor="w", backgroun="#E0F8F1")
	lbl_ruca.place(x=245, y=63, width=100)
	lbl_ruca.config(textvariable=texto_ruca)


	Label(lbl_info, font=("verdana",10), text="CUIT:", backgroun="#E0F8F1").place(x=0, y=65)
	Label(lbl_info, font=("verdana",10), text="RUCA:", backgroun="#E0F8F1").place(x=200, y=65)

	txt_observaciones = scrolledtext.ScrolledText(lbl_info, backgroun="#edfffa")
	txt_observaciones.place(x = 0, y = 95, width = 362, height = 80)
	txt_observaciones.config(state="disabled")

	diccionario_objetos["texto_aliasVendedor"] = texto_alias
	diccionario_objetos["texto_razonVendedor"] = texto_razon
	diccionario_objetos["texto_cuitVendedor"] = texto_cuit
	diccionario_objetos["texto_rucaVendedor"] = texto_ruca
	diccionario_objetos["txt_observacionesVendedor"] = txt_observaciones

def labelCompradorBuscador(lbl_comprador):
	#--Buscador
	lbl_comprador_aux = Label(lbl_comprador, backgroun="#E0F8F1")
	lbl_comprador_aux.place(x = 30, y = 0, width = 365, height = 198)

	lbl_ventana_productor_buscador_entry = tk.LabelFrame(lbl_comprador_aux, text="Filtrar", backgroun="#E0F8F1")
	lbl_ventana_productor_buscador_tabla = tk.LabelFrame(lbl_comprador_aux, text="Productores", backgroun="#E0F8F1")

	lbl_ventana_productor_buscador_entry.grid(column = 0, row = 0)
	lbl_ventana_productor_buscador_tabla.grid(column = 0, row = 1)

	#--
	entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="43")
	entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = 5)

	btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar", command= lambda: compradorFiltrar())
	btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 0)

	sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
	sbr_productor.pack(side=RIGHT, fill="y")

	tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("cliente", "doc"), selectmode=tk.BROWSE, height=5, show='headings') 
	tabla_productor.pack(side=LEFT, fill="both", expand=True)
	sbr_productor.config(command=tabla_productor.yview)
	tabla_productor.config(yscrollcommand=sbr_productor.set)

	tabla_productor.heading("cliente", text="Productor")
	tabla_productor.heading("doc", text="CUIT/DNI")

	tabla_productor.column("cliente", width=240)
	tabla_productor.column("doc", width=100)

	diccionario_objetos["entry_comprador"] = entry_filtrar_productor
	diccionario_objetos["tabla_compradores"] = tabla_productor

	entry_filtrar_productor.bind("<Return>", (lambda event: compradorFiltrar()))
	tabla_productor.bind('<Double-1>', (lambda event: seleccionarTablaComprador()))
	tabla_productor.bind('<Return>', (lambda event: seleccionarTablaComprador()))
def labelLoteDatos(lbl_comprador):
	lbl_info = tk.LabelFrame(lbl_comprador, text="LOTE SELECCIONADO", backgroun="#E0F8F1")
	lbl_info.place(x = 400, y = 0, width = 505, height = 198)

	texto_catHacienda = StringVar()
	texto_catHacienda.set("") # Caso 1
	texto_catVenta = StringVar()
	texto_catVenta.set("")

	lbl_catVenta = tk.Label(lbl_info, font=("Helvetica Neue",12, "bold"), anchor="w", backgroun="#E0F8F1")
	lbl_catVenta.place(x=0, y=0, width=500)
	lbl_catVenta.config(textvariable=texto_catVenta)

	lbl_catHacienda = tk.Label(lbl_info, font=("Helvetica Neue",10,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_catHacienda.place(x=0, y=20, width=500)
	lbl_catHacienda.config(textvariable=texto_catHacienda)

	tk.Label(lbl_info, text="Corral", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=0, y=42, width=125, height=13)
	tk.Label(lbl_info, text="Cantidad", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=125, y=42, width=125, height=13)
	tk.Label(lbl_info, text="Peso Neto", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=250, y=42, width=125, height=13)
	tk.Label(lbl_info, text="Peso Prom", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=375, y=42, width=125, height=13)


	texto_corral = StringVar()
	texto_corral.set("")
	texto_cantidad = StringVar()
	texto_cantidad.set("")
	texto_neto = StringVar()
	texto_neto.set("")
	texto_promedio = StringVar()
	texto_promedio.set("")


	lbl_corral = tk.Label(lbl_info, font=("Helvetica Neue",25,"bold"), anchor="c", backgroun="#E0F8F1")
	lbl_corral.place(x=0, y=55, width=125)
	lbl_corral.config(textvariable=texto_corral)

	lbl_cantidad = tk.Label(lbl_info, font=("Helvetica Neue",25,"bold"), anchor="c", backgroun="#E0F8F1")
	lbl_cantidad.place(x=125, y=55, width=125)
	lbl_cantidad.config(textvariable=texto_cantidad)

	lbl_neto = tk.Label(lbl_info, font=("Helvetica Neue",25,"bold"), anchor="c", backgroun="#E0F8F1")
	lbl_neto.place(x=250, y=55, width=125)
	lbl_neto.config(textvariable=texto_neto)

	lbl_promedio = tk.Label(lbl_info, font=("Helvetica Neue",25,"bold"), anchor="c", backgroun="#E0F8F1")
	lbl_promedio.place(x=375, y=55, width=125)
	lbl_promedio.config(textvariable=texto_promedio)

	txt_observaciones = scrolledtext.ScrolledText(lbl_info, backgroun="#edfffa")
	txt_observaciones.place(x = 0, y = 110, width = 500, height = 68)
	txt_observaciones.insert("1.0", "ASDASDASD")
	txt_observaciones.config(state="disabled")

	diccionario_objetos["datosLote_texto_catHacienda"] = texto_catHacienda
	diccionario_objetos["datosLote_texto_catVenta"] = texto_catVenta
	diccionario_objetos["datosLote_texto_corral"] = texto_corral
	diccionario_objetos["datosLote_texto_cantidad"] = texto_cantidad
	diccionario_objetos["datosLote_texto_neto"] = texto_neto
	diccionario_objetos["datosLote_texto_promedio"] = texto_promedio
	diccionario_objetos["datosLote_txt_observaciones"] = txt_observaciones
def labelCompradorInfor(lbl_comprador):
	lbl_info = tk.LabelFrame(lbl_comprador, text="COMPRADOR", backgroun="#E0F8F1")
	lbl_info.place(x = 910, y = 0, width = 368, height = 198)

	texto_alias = StringVar()
	texto_alias.set("Seleccione un comprador de la lista") # Caso 1
	texto_razon = StringVar()
	texto_razon.set("")
	texto_cuit = StringVar()
	texto_cuit.set("     -")
	texto_ruca = StringVar()
	texto_ruca.set("     -")

	lbl_alias = tk.Label(lbl_info, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_alias.place(x=0, y=0, width=350)
	lbl_alias.config(textvariable=texto_alias)

	lbl_razon = tk.Label(lbl_info, font=("Helvetica Neue",10), anchor="w", backgroun="#E0F8F1")
	lbl_razon.place(x=0, y=30, width=350)
	lbl_razon.config(textvariable=texto_razon)

	lbl_cuit = tk.Label(lbl_info, font=("verdana",12), anchor="w", backgroun="#E0F8F1")
	lbl_cuit.place(x=40, y=63, width=140)
	lbl_cuit.config(textvariable=texto_cuit)

	lbl_ruca = tk.Label(lbl_info, font=("verdana",12), anchor="w", backgroun="#E0F8F1")
	lbl_ruca.place(x=245, y=63, width=100)
	lbl_ruca.config(textvariable=texto_ruca)

	Label(lbl_info, font=("verdana",10), text="CUIT:", backgroun="#E0F8F1").place(x=0, y=65)
	Label(lbl_info, font=("verdana",10), text="RUCA:", backgroun="#E0F8F1").place(x=200, y=65)

	txt_observaciones = scrolledtext.ScrolledText(lbl_info, backgroun="#edfffa")
	txt_observaciones.place(x = 0, y = 95, width = 362, height = 80)
	txt_observaciones.config(state="disabled")

	diccionario_objetos["texto_aliasComprador"] = texto_alias
	diccionario_objetos["texto_razonComprador"] = texto_razon
	diccionario_objetos["texto_cuitComprador"] = texto_cuit
	diccionario_objetos["texto_rucaComprador"] = texto_ruca

	diccionario_objetos["txt_observacionesComprador"] = txt_observaciones

def labelCompradorMontos(lbl_montos):
	lbl_montos = tk.LabelFrame(lbl_montos, text="Montos", backgroun="#E0F8F1")
	lbl_montos.place(x = 40, y = 10, width = 200, height = 220)

	tk.Label(lbl_montos, text="$/kg", font=("Helvetica Neue",20, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 0, width = 190)
	tk.Label(lbl_montos, text="$/Lote", font=("Helvetica Neue",20, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 100, width = 190)

	entry_kilo = Entry(lbl_montos, font=("verdana",20))
	entry_lote = Entry(lbl_montos, font=("verdana",20))

	entry_kilo.place(x = 20, y = 35, width = 150)
	entry_lote.place(x = 20, y = 135, width = 150)

	entry_lote.bind("<Return>", (lambda event: calcularLote(entry_lote.get())))
	entry_kilo.bind("<Return>", (lambda event: calcularKilo(entry_kilo.get())))

	diccionario_objetos["entry_kilo"] = entry_kilo
	diccionario_objetos["entry_lote"] = entry_lote
def labelCalculosLote(lbl_montos):
	lbl_calculos = tk.LabelFrame(lbl_montos, text="Calculos Aproximados", backgroun="#E0F8F1")
	lbl_calculos.place(x = 260, y = 10, width = 830, height = 220)

	mod_alt = -20
	tk.Label(lbl_calculos, text="Martillo", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 20+mod_alt, width = 280)

	tk.Label(lbl_calculos, text="Precio por KG $", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 60+mod_alt, width = 160)
	tk.Label(lbl_calculos, text="Precio por Cabeza $", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 90+mod_alt, width = 160)
	tk.Label(lbl_calculos, text="Precio de Lote $", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 120+mod_alt, width = 160)
	
	tk.Label(lbl_calculos, text="Comision", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 280, y = 20+mod_alt, width = 280)
	tk.Label(lbl_calculos, text="Impuestos", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 280, y = 100+mod_alt, width = 280)

	tk.Label(lbl_calculos, text="Porcen. %", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 280, y = 60+mod_alt, width = 100)
	tk.Label(lbl_calculos, text="$", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 430, y = 60+mod_alt, width = 20)

	tk.Label(lbl_calculos, text="IVA Hac. %", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 280, y = 140+mod_alt, width = 100)
	tk.Label(lbl_calculos, text="IVA Com. %", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 280, y = 170+mod_alt, width = 100)
	tk.Label(lbl_calculos, text="$", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 430, y = 140+mod_alt, width = 20)
	tk.Label(lbl_calculos, text="$", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 430, y = 170+mod_alt, width = 20)

	tk.Label(lbl_calculos, text="Otros", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 570, y = 20+mod_alt, width = 250)
	tk.Label(lbl_calculos, text="Total aprox. a liquidar $:", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 570, y = 140+mod_alt, width = 250)

	tk.Label(lbl_calculos, text="Otros $", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 570, y = 60+mod_alt, width = 100)
	tk.Label(lbl_calculos, text="Otros $", font=("Helvetica Neue",12), anchor="e", backgroun="#E0F8F1").place(x = 570, y = 90+mod_alt, width = 100)

	texto_kg = StringVar()
	texto_kg.set("")
	texto_cabeza = StringVar()
	texto_cabeza.set("")
	texto_lote = StringVar()
	texto_lote.set("")
	texto_comision = StringVar()
	texto_comision.set("")
	texto_ivaHacienda = StringVar()
	texto_ivaHacienda.set("")
	texto_ivaComision = StringVar()
	texto_ivaComision.set("")
	texto_total = StringVar()
	texto_total.set("")

	arregloY=-2

	lbl_kg = tk.Label(lbl_calculos, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_kg.place(x=160, y=60+mod_alt+arregloY, width=120)
	lbl_kg.config(textvariable=texto_kg)

	lbl_cabeza = tk.Label(lbl_calculos, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_cabeza.place(x=160, y=90+mod_alt+arregloY, width=120)
	lbl_cabeza.config(textvariable=texto_cabeza)

	lbl_lote = tk.Label(lbl_calculos, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_lote.place(x=160, y=120+mod_alt+arregloY, width=120)
	lbl_lote.config(textvariable=texto_lote)

	lbl_comision = tk.Label(lbl_calculos, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_comision.place(x=450, y=60+mod_alt+arregloY, width=120)
	lbl_comision.config(textvariable=texto_comision)

	lbl_ivaHacienda = tk.Label(lbl_calculos, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_ivaHacienda.place(x=450, y=170+mod_alt+arregloY, width=120)
	lbl_ivaHacienda.config(textvariable=texto_ivaHacienda)

	lbl_ivaComision = tk.Label(lbl_calculos, font=("Helvetica Neue",14,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_ivaComision.place(x=450, y=140+mod_alt+arregloY, width=120)
	lbl_ivaComision.config(textvariable=texto_ivaComision)

	lbl_total = tk.Label(lbl_calculos, font=("Helvetica Neue",22,"bold"), anchor="c", backgroun="#E0F8F1")
	lbl_total.place(x=570, y=170+mod_alt+arregloY, width=250)
	lbl_total.config(textvariable=texto_total)


	entry_comisionPorcentaje = Entry(lbl_calculos, font=("verdana",12))
	entry_comisionPorcentaje.place(x = 380, y = 60+mod_alt, width = 50)	

	entry_ivaHaciendaPorcentaje = Entry(lbl_calculos, font=("verdana",12))
	entry_ivaHaciendaPorcentaje.place(x = 380, y = 140+mod_alt, width = 50)	

	entry_ivaComisionPorcentaje = Entry(lbl_calculos, font=("verdana",12))
	entry_ivaComisionPorcentaje.place(x = 380, y = 170+mod_alt, width = 50)

	entry_ivaHaciendaPorcentaje.insert(0, 10.5)
	entry_ivaComisionPorcentaje.insert(0, 10.5)
	entry_comisionPorcentaje.insert(0, 4.5)

	entry_otros1 = Entry(lbl_calculos, font=("verdana",12))
	entry_otros1.place(x = 680, y = 60+mod_alt, width = 130)
	entry_otros2 = Entry(lbl_calculos, font=("verdana",12))
	entry_otros2.place(x = 680, y = 90+mod_alt, width = 130)

	diccionario_objetos["calculos_texto_kg"] = texto_kg
	diccionario_objetos["calculos_texto_cabeza"] = texto_cabeza
	diccionario_objetos["calculos_texto_lote"] = texto_lote
	diccionario_objetos["calculos_texto_comision"] = texto_comision
	diccionario_objetos["calculos_texto_ivaHacienda"] = texto_ivaHacienda
	diccionario_objetos["calculos_texto_ivaComision"] = texto_ivaComision
	diccionario_objetos["calculos_texto_total"] = texto_total
	diccionario_objetos["calculos_entry_comisionPorcentaje"] = entry_comisionPorcentaje
	diccionario_objetos["calculos_entry_ivaHaciendaPorcentaje"] = entry_ivaHaciendaPorcentaje
	diccionario_objetos["calculos_entry_ivaComisionPorcentaje"] = entry_ivaComisionPorcentaje
	diccionario_objetos["calculos_entry_otros1"] = entry_otros1
	diccionario_objetos["calculos_entry_otros2"] = entry_otros2

	entry_comisionPorcentaje.bind("<Return>", (lambda event: calcularComision()))

	entry_ivaHaciendaPorcentaje.bind("<Return>", (lambda event: calcularImpuestos()))
	entry_ivaComisionPorcentaje.bind("<Return>", (lambda event: calcularImpuestos()))

	entry_otros1.bind("<Return>", (lambda event: calcularFinal()))
	entry_otros2.bind("<Return>", (lambda event: calcularFinal()))
def labelAcciones(lbl_montos):
	lbl_acciones = tk.LabelFrame(lbl_montos, text="Acciones", backgroun="#E0F8F1")
	lbl_acciones.place(x = 1110, y = 10, width = 150, height = 220)

	btn_guardar = tk.Button(lbl_acciones, text="GUARDAR", font=("verdana",15, "bold"), backgroun="#76f5b7", command=guardar)
	btn_guardar.place(x = 10, y = 10, width=130, height=90)

	btn_borrar = tk.Button(lbl_acciones, text="BORRAR", font=("verdana",12, "bold"), backgroun="#e3876d", command=borrarLote)
	btn_borrar.place(x = 10, y = 105, width=130, height=40)


	btn_imprimir = tk.Button(lbl_acciones, text="IMPRIMIR", font=("verdana",12, "bold"), backgroun="#cce388")
	btn_imprimir.place(x = 10, y = 150, width=130, height=40)


#OTROS
def borrarDatosLoteComprador():
	#Borrar Lote
	diccionario_objetos["datosLote_texto_catHacienda"].set("")
	diccionario_objetos["datosLote_texto_catVenta"].set("")
	diccionario_objetos["datosLote_texto_corral"].set("")
	diccionario_objetos["datosLote_texto_cantidad"].set("")
	diccionario_objetos["datosLote_texto_neto"].set("")
	diccionario_objetos["datosLote_texto_promedio"].set("")

	diccionario_objetos["datosLote_txt_observaciones"].configure(state="normal")
	diccionario_objetos["datosLote_txt_observaciones"].delete("1.0", tk.END)
	diccionario_objetos["datosLote_txt_observaciones"].configure(state="disabled")

	#Borrar Vendedor
	diccionario_objetos["texto_aliasVendedor"].set("")
	diccionario_objetos["texto_razonVendedor"].set("")
	diccionario_objetos["texto_cuitVendedor"].set("")
	diccionario_objetos["texto_rucaVendedor"].set("")
	diccionario_objetos["txt_observacionesVendedor"].configure(state="normal")
	diccionario_objetos["txt_observacionesVendedor"].delete("1.0", tk.END)
	diccionario_objetos["txt_observacionesVendedor"].configure(state="disabled")
def borrarDatosComprador():
	#Borrar Comprador
	diccionario_objetos["texto_aliasComprador"].set("")
	diccionario_objetos["texto_razonComprador"].set("")
	diccionario_objetos["texto_cuitComprador"].set("")
	diccionario_objetos["texto_rucaComprador"].set("")
	diccionario_objetos["txt_observacionesComprador"].configure(state="normal")
	diccionario_objetos["txt_observacionesComprador"].delete("1.0", tk.END)
	diccionario_objetos["txt_observacionesComprador"].configure(state="disabled")
def borrarDatosMontosCalculos():
	diccionario_objetos["calculos_texto_kg"].set("")
	diccionario_objetos["calculos_texto_cabeza"].set("")
	diccionario_objetos["calculos_texto_lote"].set("")
	diccionario_objetos["calculos_texto_comision"].set("")
	diccionario_objetos["calculos_texto_ivaHacienda"].set("")
	diccionario_objetos["calculos_texto_ivaComision"].set("")
	diccionario_objetos["calculos_texto_total"].set("")

	diccionario_objetos["entry_kilo"].delete(0, tk.END)
	diccionario_objetos["entry_lote"].delete(0, tk.END)

def guardar():
	lote = diccionario_objetos["ID_LOTE"]
	con = sql_connection()
	condiciones = " WHERE lote = '" + str(lote) + "' AND estado='activo'"
	rows = actualizar_db(con, "compraventa", condiciones)

	if(len(rows) == 1):
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea editar este lote?', icon = 'warning')
		if(MsgBox == 'yes'):
			editarLote()
	else:
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea guardar?', icon = 'warning')
		if(MsgBox == 'yes'):
			guardarLote()

def editarLote():
	lote = diccionario_objetos["ID_LOTE"]
	try:
		x_lote = diccionario_objetos["ID_LOTE_A_EDITAR"]
		x_comprador = str(diccionario_objetos["texto_cuitComprador"].get())
		x_precio = str(float(diccionario_objetos["calculos_texto_kg"].get()))


		entities = [x_comprador,
		x_precio,
		x_lote]

		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute('UPDATE compraventa SET comprador = ?, precio = ? where id = ?', entities)
		con.commit()

		messagebox.showinfo("Éxito", "Lote EDITADO con éxito!")
		diccionario_objetos["ID_LOTE_A_EDITAR"] = "NULL"
		borrarDatosComprador()
		borrarDatosLoteComprador()
		borrarDatosMontosCalculos()

	except:
		messagebox.showerror("ERROR", "Error al cargar a la base de datos")
def guardarLote():
	lote = diccionario_objetos["ID_LOTE"]
	try:
		x_lote = str(lote)
		x_comprador = str(diccionario_objetos["texto_cuitComprador"].get())
		x_precio = str(float(diccionario_objetos["calculos_texto_kg"].get()))
		x_estado = "activo"
		x_remate = rematename
		x_vendedor = str(diccionario_objetos["texto_cuitVendedor"].get())

		entities = [x_lote,
		x_comprador,
		x_precio,
		x_remate,
		x_estado,
		x_vendedor]

		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO compraventa VALUES(NULL, ?, ?, ?, ?, ?, ?)", entities)
		con.commit()
		messagebox.showinfo("Éxito", "Productor ingresado con éxito!")
		borrarDatosComprador()
		borrarDatosLoteComprador()
		borrarDatosMontosCalculos()
	except:
		messagebox.showerror("ERROR", "Error al cargar a la base de datos")

def borrarLote():
	lote = diccionario_objetos["ID_LOTE_A_EDITAR"]
	if(lote=="NULL"):
		messagebox.showerror("ERROR", "Primero selecciones un lote cargado para borrar")
		return 0
	else:
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea eliminar los datos de compra de este lote?', icon = 'warning')
		if(MsgBox == 'yes'):
			entities = [lote]
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE compraventa SET estado = "borrado" where id = ?', entities)
			con.commit()

			messagebox.showinfo("Éxito", "Lote BORRADO con éxito!")
			diccionario_objetos["ID_LOTE_A_EDITAR"] = "NULL"
			borrarDatosComprador()
			borrarDatosLoteComprador()
			borrarDatosMontosCalculos()

#CALCULOS
def calcularKilo(entry_kilo):
	try:
		precio_kilo = float(entry_kilo)
		peso_neto = float(diccionario_objetos["datosLote_texto_neto"].get())
		cantidad_cabezas = float(diccionario_objetos["datosLote_texto_cantidad"].get())
	except:
		messagebox.showerror("ERROR", 'Pruebe seleccionar un lote\nIngresar numeros sin separador de millares\nEl separador decimal es un punto "."')
		return 0
	precioKilo = str(round(precio_kilo, 2))
	precioLote = str(round(precio_kilo*peso_neto, 2))
	precioCabeza = str(round((precio_kilo*peso_neto)/cantidad_cabezas, 2))

	diccionario_objetos["calculos_texto_kg"].set(precioKilo)
	diccionario_objetos["calculos_texto_cabeza"].set(precioCabeza)
	diccionario_objetos["calculos_texto_lote"].set(precioLote)

	calcularComision()
def calcularLote(entry_lote):
	try:
		precio_lote = float(entry_lote)
		peso_neto = float(diccionario_objetos["datosLote_texto_neto"].get())
		cantidad_cabezas = float(diccionario_objetos["datosLote_texto_cantidad"].get())
	except:
		messagebox.showerror("ERROR", 'Pruebe seleccionar un lote\nIngresar numeros sin separador de millares\nEl separador decimal es un punto "."')
		return 0
	precioKilo = str(round(precio_lote/peso_neto, 2))
	precioLote = str(round(precio_lote, 2))
	precioCabeza = str(round(precio_lote/cantidad_cabezas, 2))

	diccionario_objetos["calculos_texto_kg"].set(precioKilo)
	diccionario_objetos["calculos_texto_cabeza"].set(precioCabeza)
	diccionario_objetos["calculos_texto_lote"].set(precioLote)

	calcularComision()
def calcularComision():
	try:
		porcentaje_comision = float(diccionario_objetos["calculos_entry_comisionPorcentaje"].get())
		precio_subtotal = float(diccionario_objetos["calculos_texto_lote"].get())
	except:
		messagebox.showerror("ERROR", 'Pruebe seleccionar un lote\nIngresar numeros sin separador de millares\nEl separador decimal es un punto "."')
		return 0
	comision = str(round(precio_subtotal*porcentaje_comision/100, 2))

	diccionario_objetos["calculos_texto_comision"].set(comision)

	calcularImpuestos()

def calcularImpuestos():
	try:
		porcentaje_comision = float(diccionario_objetos["calculos_entry_ivaComisionPorcentaje"].get())
		porcentaje_hacienda = float(diccionario_objetos["calculos_entry_ivaHaciendaPorcentaje"].get())
	except:
		messagebox.showerror("ERROR", 'Pruebe seleccionar un lote\nIngresar numeros sin separador de millares\nEl separador decimal es un punto "."')
		return 0
	precio_comision = float(diccionario_objetos["calculos_texto_comision"].get())
	precio_subtotal = float(diccionario_objetos["calculos_texto_lote"].get())

	ivaHacienda = str(round(precio_comision*porcentaje_comision/100, 2))
	ivaComision = str(round(precio_subtotal*porcentaje_hacienda/100, 2))

	diccionario_objetos["calculos_texto_ivaHacienda"].set(ivaHacienda)
	diccionario_objetos["calculos_texto_ivaComision"].set(ivaComision)

	calcularFinal()

def calcularFinal():
	precio_subtotal = float(diccionario_objetos["calculos_texto_lote"].get())
	precio_comision = float(diccionario_objetos["calculos_texto_comision"].get())
	precio_ivaHacienda = float(diccionario_objetos["calculos_texto_ivaHacienda"].get())
	precio_ivaComision = float(diccionario_objetos["calculos_texto_ivaComision"].get())

	try:	
		otro1 = float(diccionario_objetos["calculos_entry_otros1"].get())
	except:
		otro1 = 0.0
	try:	
		otro2 = float(diccionario_objetos["calculos_entry_otros2"].get())
	except:
		otro2 = 0.0

	precio_total = str(round(precio_subtotal + precio_comision + precio_ivaHacienda + precio_ivaComision + otro1 + otro2, 2))

	diccionario_objetos["calculos_texto_total"].set(precio_total)


def remate(window):
	lbl_lote = Label(window, backgroun="#E0F8F1")
	lbl_comprador = Label(window, backgroun="#E0F8F1")
	lbl_montos = Label(window, backgroun="#E0F8F1")

	mod_alt = 0
	var_bajar = 0

	lbl_lote.place(x = 2, y = 2+mod_alt, width = 1281, height = 200)
	lbl_comprador.place(x = 2, y = 204+mod_alt, width = 1281, height = 200)
	lbl_montos.place(x = 2, y = 406+mod_alt, width = 1281, height = 250)

	#EN LOTE:
	if(True):
		tk.Label(lbl_lote, text="LOTES", font=("Helvetica Neue",15, "bold"), anchor="c", backgroun="#E0F8F1", wraplength=1).place(x = 5, y = 0, width = 15, height = 200)
		labelLoteBuscar(lbl_lote)
		labelLoteTabla(lbl_lote)
		labelLoteInfor(lbl_lote)

	#EN COMPRADOR:
	if(True):
		tk.Label(lbl_comprador, text="COMPRADOR", font=("Helvetica Neue",10, "bold"), anchor="c", backgroun="#E0F8F1", wraplength=1).place(x = 5, y = 0, width = 15, height = 200)
		labelCompradorBuscador(lbl_comprador)
		labelLoteDatos(lbl_comprador)
		labelCompradorInfor(lbl_comprador)

	#EN MONTOS:
	if(True):
		tk.Label(lbl_montos, text="MONTOS", font=("Helvetica Neue",15, "bold"), anchor="c", backgroun="#E0F8F1", wraplength=1).place(x = 5, y = 25, width = 25, height = 200)
		labelCompradorMontos(lbl_montos)
		labelCalculosLote(lbl_montos)
		labelAcciones(lbl_montos)

	actualizarProductores()
	actualizarTablaLotes()

window1 = Tk()
window1.title("Remate")
window1.geometry("1285x728")
window1.configure(backgroun="#2C4D4F") #E8F6FA
remate(window1)
window1.mainloop()
