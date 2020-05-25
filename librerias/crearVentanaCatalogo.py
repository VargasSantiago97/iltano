#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

import ventanaIngreso

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

direccionBaseDeDatos = 'database/iltanohacienda.db'

remate = "remate1"


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
	cursorObj.execute("SELECT productor FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows

def actualizarPinturas():
	con = sql_connection()
	condiciones = " WHERE estado = 'activo'"
	rows = actualizar_db(con, "productores", condiciones)
	for row in rows:
		diccionario_pinturas[str(row[3])] = "-"

	con = sql_connection()
	condiciones = " WHERE remate = '" + remate + "'"
	rows = actualizar_db(con, "pintura", condiciones)
	for row in rows:
		diccionario_pinturas[str(row[3])] = str(row[2])
	return diccionario_pinturas

def productFiltrar(entrada, tabla_productor):
	pal_clave = str(entrada)
	con = sql_connection()
	condiciones =  ' WHERE (nombre LIKE "%' + pal_clave + '%" OR razon LIKE "%' + pal_clave + '%" OR ndoc LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%" OR con_iva LIKE "%' + pal_clave + '%" OR localidad LIKE "%' + pal_clave + '%" OR provincia LIKE "%' + pal_clave + '%" OR ruca LIKE "%' + pal_clave + '%" OR establecimiento LIKE "%' + pal_clave + '%") AND estado = "activo"'
	rows = actualizar_db(con, "productores", condiciones)
	cargarTabla2(rows, tabla_productor)

def cargarTabla2(rows, tabla_productor):
	pinturas = actualizarPinturas()

	for i in tabla_productor.get_children():
		tabla_productor.delete(i)
	i=0

	for row in rows:
		tabla_productor.insert("", tk.END, text = pinturas[str(row[3])], iid=i, values = (str(row[1]), 
			str(row[3])))
		i = i + 1

def cargarTabla():
	tabla_productor = diccionario_objetos["tabla_productor"]
	tabla_productor_cargado = diccionario_objetos["tabla_productor_cargado"]

	#Todos los productores
	try:
		con = sql_connection()
		condiciones = " WHERE estado = 'activo'"
		rows = actualizar_db(con, "productores", condiciones)
	except:
		messagebox.showerror("ERROR", "Error al leer base de datos")
		rows = []
	try:
		pinturas = actualizarPinturas()
		for i in tabla_productor.get_children():
			tabla_productor.delete(i)
		i=0
		for row in rows:
			tabla_productor.insert("", tk.END, text = pinturas[str(row[3])], iid=i, values = (str(row[1]), 
			str(row[3])))
			i = i + 1
	except:
		messagebox.showerror("ERROR", "Error al cargar los productores")

	#Productores usados obtener
	try:
		con = sql_connection()
		condiciones = " WHERE estado = 'activo'"
		rows = actualizar_db2(con, "lotes", condiciones)

		lista = []
		for i in range(0, len(rows)):
			lista.append(rows[i][0])

		listaCuitsUsados = list(set(lista))

		if (len(listaCuitsUsados)>0):
			condiciones = " WHERE ndoc ='" + listaCuitsUsados[0] + "'"
			for i in range(1, len(listaCuitsUsados)):
				condiciones = condiciones + " OR ndoc = '" + listaCuitsUsados[i] + "'"

		con = sql_connection()
		rows = actualizar_db(con, "productores", condiciones)
	except:
		messagebox.showerror("ERROR", "Error al leer base de datos")
		rows = []

	#Productores usados cargar
	try:
		for i in tabla_productor_cargado.get_children():
			tabla_productor_cargado.delete(i)
		i=0
		for row in rows:
			tabla_productor_cargado.insert("", tk.END, text = pinturas[str(row[3])], iid=i, values = (str(row[1]), 
			str(row[3])))
			i = i + 1
	except:
		messagebox.showerror("ERROR", "Error al cargar los productores usados")


def cargarProductor(tabla_productor):
	try:
		entrada = tabla_productor.item(tabla_productor.selection()[0])
		cuit = str(entrada["values"][1])
		pintura = tabla_productor.item(tabla_productor.selection())["text"]

		con = sql_connection()
		condiciones = " WHERE ndoc = '" + cuit + "' AND estado = 'activo'"
		rows = actualizar_db(con, "productores", condiciones)

		row = rows[0]

		diccionario_textos["alias"].set(row[1])
		diccionario_textos["razon"].set(row[2])
		diccionario_textos["cuit"].set(row[3])
		diccionario_textos["ruca"].set(row[19])
		diccionario_textos["pintura_inic"].set(pintura)
		cargarTablaLotes(cuit)
		limpiarLote()
	except:
		inneserario = 0
	

def cargarTablaLotes(cuit):
	try:
		con = sql_connection()
		condiciones = " WHERE remate = '" + remate + "' AND productor = '" + cuit + "' AND estado = 'activo'"
		rows = actualizar_db(con, "lotes", condiciones)
	except:
		messagebox.showerror("ERROR", "Error al leer la base de datos")
		rows = []

	try:
		tabla = diccionario_objetos["tabla_lotes"]

		for i in tabla.get_children():
			tabla.delete(i)
		i=0

		varLocal_corrales = 0
		varLocar_animales = 0
		varLocar_kg = 0.0

		for row in rows:
			id_Lote = int(row[0])
			varLocal_corral = row[4]
			varLocal_catVenta = row[5]
			varLocal_catHacienda = row[6]
			varLocal_cantidad = row[3]
			varLocal_kgs = row[12]
			varLocal_kgsProm = row[13]
			varLocal_observaciones = row[14]

			varLocal_corrales = varLocal_corrales + 1
			varLocar_animales = varLocar_animales + int(varLocal_cantidad)
			varLocar_kg = varLocar_kg + float(varLocal_kgs)

			tabla.insert("", tk.END, text = varLocal_corral, iid=id_Lote, values = (varLocal_catVenta,
				varLocal_catHacienda,
				varLocal_cantidad,
				varLocal_kgs,
				varLocal_kgsProm,
				varLocal_observaciones))
			i = i + 1

		diccionario_textos["corrales"].set(str(varLocal_corrales))
		diccionario_textos["animales"].set(str(varLocar_animales))
		diccionario_textos["kg"].set(str(varLocar_kg))

	except:
		messagebox.showerror("ERROR", "Error al cargar los lotes")
def cargarLote(tabla):
	try:
		id_Lote = tabla.selection()[0]
		con = sql_connection()
		condiciones = " WHERE id = " + id_Lote + " AND estado = 'activo'"
		rows = actualizar_db(con, "lotes", condiciones)

		row = rows[0]

		diccionario_textos["cantidad"].set(row[3])
		diccionario_textos["corral"].set(row[4])
		diccionario_textos["catVenta"].set(row[5])
		diccionario_textos["catHacienda"].set(row[6])
		diccionario_textos["pintura"].set(row[7])
		diccionario_textos["kgBruto"].set(row[8])
		diccionario_textos["kgPromedio"].set(row[9])
		diccionario_textos["desbastePorcentaje"].set(row[10])
		diccionario_textos["desbasteKg"].set(row[11])
		diccionario_textos["neto"].set(row[12])
		diccionario_textos["promedio"].set(row[13])
		diccionario_textos["observaciones"].set(row[14])
		diccionario_objetos["txt_observaciones"].config(state="normal")
		diccionario_objetos["txt_observaciones"].delete("1.0", tk.END)
		diccionario_objetos["txt_observaciones"].insert("1.0", row[15])
		diccionario_objetos["txt_observaciones"].config(state="disabled")
		diccionario_textos["dte"].set(row[16])

		diccionario_textos["id"].set(row[0])
	except:
		messagebox.showerror("ERROR", "Error al cargar el lote")

def eliminarLote(cuit, lote):
	if (cuit == "     -"):
		messagebox.showerror("ERROR", "Primero seleccione un productor con doble click en la lista")
	else:
		if(lote == ""):
			messagebox.showerror("ERROR", "Primero seleccione un lote con doble click en la lista")
		else:
			respuesta = messagebox.askquestion("ATENCION", "¿Desea eliminar esta tropa?")
			if respuesta == 'yes':
				try:
					con = sql_connection()
					cursorObj = con.cursor()
					cursorObj.execute('UPDATE lotes SET estado = "borrado" WHERE id = ' + str(lote))
					con.commit()
					messagebox.showinfo("Éxito", "Lote eliminado con éxito")
					cargarTablaLotes(cuit)
					limpiarLote()
				except:
					messagebox.showerror("ERROR", "Error al borrar")

def limpiarLote():
	diccionario_textos["cantidad"].set("     -")
	diccionario_textos["corral"].set("     -")
	diccionario_textos["catVenta"].set("     -")
	diccionario_textos["catHacienda"].set("     -")
	diccionario_textos["pintura"].set("     -")
	diccionario_textos["kgBruto"].set("     -")
	diccionario_textos["kgPromedio"].set("     -")
	diccionario_textos["desbastePorcentaje"].set("     -")
	diccionario_textos["desbasteKg"].set("     -")
	diccionario_textos["neto"].set("     -")
	diccionario_textos["promedio"].set("     -")
	diccionario_textos["id"].set("")
	diccionario_textos["observaciones"].set("")
	diccionario_objetos["txt_observaciones"].config(state="normal")
	diccionario_objetos["txt_observaciones"].delete("1.0", tk.END)
	diccionario_objetos["txt_observaciones"].config(state="disabled")
	diccionario_textos["dte"].set("")
	diccionario_textos["flete"].set("")
	diccionario_textos["fletePrecio"].set("")

def pinturaSet(entry):
	mandar = "-"
	try:
		if(entry==""):
			messagebox.showerror("ERROR", "Ingresar una pintura válida")
		else:
			diccionario_textos["pintura_inic"].set(entry)
			mandar = entry
	except:
		messagebox.showerror("ERROR", "Error al cargar la pintura del productor")

	cuit = diccionario_textos["cuit"].get()

	pinturas = actualizarPinturas()
	pintura = pinturas[cuit]

	if(pintura!='-'):
		try:
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE pintura SET pintura = "' + mandar + '" where (remate = "' + remate + '" AND productor = "' + cuit + '")')
			con.commit()
			cargarTabla()
		except:
			messagebox.showerror("ERROR", "Error al editar pintura en base de datos")
	else:
		try:
			entities = [remate, mandar, cuit]

			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO pintura VALUES(NULL, ?, ?, ?)", entities)
			con.commit()
			cargarTabla()
		except:
			messagebox.showerror("ERROR", "Error al guardar pintura en base de datos")

def abrirLote(cuit, accion):
	if (cuit == "     -"):
		messagebox.showerror("ERROR", "Primero seleccione un productor con doble click en la lista")
	else:
		if(accion == "nuevo"):
			try:
				ventanaIngreso.ingreso(cuit, accion, remate, cargarTablaLotes, limpiarLote, cargarTabla)
			except:
				messagebox.showerror("ERROR", "Error al abrir la ventana")
		else:
			if(diccionario_textos["id"].get() == ""):
				messagebox.showerror("ERROR", "Primero seleccione un lote con doble click en la lista")
			else:
				try:
					ventanaIngreso.ingreso(cuit, diccionario_textos["id"].get(), remate, cargarTablaLotes, limpiarLote, cargarTabla)
				except:
					messagebox.showerror("ERROR", "Error al abrir la ventana")



def catalogo(window):
	padX = 5
	padY = 5

	lbl_datos = Label(window, backgroun="#E0F8F1")
	lbl_tablaCategorias = Label(window)
	lbl_tablaCategoriasMover = Label(window, backgroun="#E0F8F1")
	lbl_acciones = Label(window, backgroun="#E0F8F1")
	lbl_filtrar = Label(window, backgroun="#E0F8F1")
	lbl_tabla = Label(window)
	lbl_cargar = Label(window, backgroun="#E0F8F1")
	lbl_tablaCargados = Label(window)
	lbl_tablaCargadosMover = Label(window, backgroun="#E0F8F1")

	mod_alt = 0

	lbl_datos.place(x = 2, y = 2+mod_alt, width = 300, height = 250)
	lbl_tablaCategorias.place(x = 304, y = 2+mod_alt, width = 450, height = 250)
	lbl_tablaCategoriasMover.place(x = 756, y = 2+mod_alt, width = 100, height = 250)
	lbl_acciones.place(x = 858, y = 2+mod_alt, width = 425, height = 250)
	lbl_filtrar.place(x = 2, y = 254+mod_alt, width = 150, height = 370)
	lbl_tabla.place(x = 154, y = 254+mod_alt, width = 500, height = 370)
	lbl_cargar.place(x = 656, y = 254+mod_alt, width = 100, height = 370)
	lbl_tablaCargados.place(x = 758, y = 254+mod_alt, width = 423, height = 370)
	lbl_tablaCargadosMover.place(x = 1183, y = 254+mod_alt, width = 100, height = 370)

	#DATOS DE CATALOGO
	if(True):	
		tk.Label(lbl_datos, text="Datos catálogo", font=("Helvetica Neue",14, "bold"), anchor="c", backgroun="#E0F8F1").place(x = 0, y = 2, width = 298)
	
		tk.Label(lbl_datos, text="Fecha:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 50, width = 80)
		tk.Label(lbl_datos, text="Titulo:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 80, width = 80)
		tk.Label(lbl_datos, text="Predio:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 110, width = 80)
		tk.Label(lbl_datos, text="Localidad:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 140, width = 80)
		tk.Label(lbl_datos, text="Remata:", font=("Helvetica Neue",10), anchor="e", backgroun="#E0F8F1").place(x = 0, y = 170, width = 80)

		entry_datosFecha = Entry(lbl_datos)
		entry_datosFecha.place(x = 90, y = 50, width = 180)

		entry_datosFecha = Entry(lbl_datos)
		entry_datosFecha.place(x = 90, y = 80, width = 180)

		entry_datosFecha = Entry(lbl_datos)
		entry_datosFecha.place(x = 90, y = 110, width = 180)

		entry_datosFecha = Entry(lbl_datos)
		entry_datosFecha.place(x = 90, y = 140, width = 180)

		entry_datosFecha = Entry(lbl_datos)
		entry_datosFecha.place(x = 90, y = 170, width = 180)

	#TABLA -> CATEGORIAS DE VENTA
	if(True):
		sbr_catVenta = Scrollbar(lbl_tablaCategorias)
		sbr_catVenta.pack(side=RIGHT, fill="y")

		tabla_catVenta = ttk.Treeview(lbl_tablaCategorias, columns=("alias", "nombre"), selectmode=tk.BROWSE, height=7) 
		tabla_catVenta.pack(side=LEFT, fill="both", expand=True)
		sbr_catVenta.config(command=tabla_catVenta.yview)
		tabla_catVenta.config(yscrollcommand=sbr_catVenta.set)

		tabla_catVenta.heading("#0", text="Cant.")
		tabla_catVenta.heading("alias", text="Alias")
		tabla_catVenta.heading("nombre", text="Nombre")

		tabla_catVenta.column("#0", width=40)
		tabla_catVenta.column("alias", width=120)
		tabla_catVenta.column("nombre", width=120)

	#MOVER -> TABLA CATEGORIAS
	if(True):
		btn_moverArribaCat = tk.Button(lbl_tablaCategoriasMover, text="↑", font=("verdana",15,"bold"), backgroun="#F5D0A9")
		btn_moverArribaCat.place(x = 25, y = 70, width=50, height=50)

		btn_moverAbajoCat = tk.Button(lbl_tablaCategoriasMover, text="↓", font=("verdana",15,"bold"), backgroun="#F5D0A9")
		btn_moverAbajoCat.place(x = 25, y = 130, width=50, height=50)

		btn_moverArribaTodoCat = tk.Button(lbl_tablaCategoriasMover, text="↑↑↑", font=("verdana",15,"bold"), backgroun="#F5A9A9")
		btn_moverArribaTodoCat.place(x = 25, y = 10, width=50, height=50)

		btn_moverAbajoTodoCat = tk.Button(lbl_tablaCategoriasMover, text="↓↓↓", font=("verdana",15,"bold"), backgroun="#F5A9A9")
		btn_moverAbajoTodoCat.place(x = 25, y = 190, width=50, height=50)

	#ACCIONES


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
	if(True):
		sbr_lotes = Scrollbar(lbl_tabla)
		sbr_lotes.pack(side=RIGHT, fill="y")

		tabla_lotes = ttk.Treeview(lbl_tabla, columns=("productor", "cantidad", "categoria" , "pintura", "kg"), selectmode=tk.BROWSE, height=7) 
		tabla_lotes.pack(side=LEFT, fill="both", expand=True)
		sbr_lotes.config(command=tabla_lotes.yview)
		tabla_lotes.config(yscrollcommand=sbr_lotes.set)

		tabla_lotes.heading("#0", text="Corral")
		tabla_lotes.heading("productor", text="Productor")
		tabla_lotes.heading("cantidad", text="Cantidad")
		tabla_lotes.heading("categoria", text="Categoria")
		tabla_lotes.heading("pintura", text="Pintura")
		tabla_lotes.heading("kg", text="Peso")

		tabla_lotes.column("#0", width=30)
		tabla_lotes.column("productor", width=50)
		tabla_lotes.column("cantidad", width=30)
		tabla_lotes.column("categoria", width=50)
		tabla_lotes.column("pintura", width=30)
		tabla_lotes.column("kg", width=30)

	#CARGAR
	if(True):
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

		tabla_lotesCargados = ttk.Treeview(lbl_tablaCargados, columns=("productor", "cantidad", "categoria" , "pintura", "kg"), selectmode=tk.BROWSE, height=7) 
		tabla_lotesCargados.pack(side=LEFT, fill="both", expand=True)
		sbr_lotesCargados.config(command=tabla_lotesCargados.yview)
		tabla_lotesCargados.config(yscrollcommand=sbr_lotesCargados.set)

		tabla_lotesCargados.heading("#0", text="Corral")
		tabla_lotesCargados.heading("productor", text="Productor")
		tabla_lotesCargados.heading("cantidad", text="Cantidad")
		tabla_lotesCargados.heading("categoria", text="Categoria")
		tabla_lotesCargados.heading("pintura", text="Pintura")
		tabla_lotesCargados.heading("kg", text="Peso")

		tabla_lotesCargados.column("#0", width=30)
		tabla_lotesCargados.column("productor", width=50)
		tabla_lotesCargados.column("cantidad", width=30)
		tabla_lotesCargados.column("categoria", width=50)
		tabla_lotesCargados.column("pintura", width=30)
		tabla_lotesCargados.column("kg", width=30)

	#MOVER -> TABLA CARGADOS
	if(True):
		btn_moverArribaCargados = tk.Button(lbl_tablaCargadosMover, text="↑", font=("verdana",15,"bold"), backgroun="#F5D0A9")
		btn_moverArribaCargados.place(x = 25, y = 70, width=50, height=50)

		btn_moverAbajoCargados = tk.Button(lbl_tablaCargadosMover, text="↓", font=("verdana",15,"bold"), backgroun="#F5D0A9")
		btn_moverAbajoCargados.place(x = 25, y = 130, width=50, height=50)

		btn_moverArribaTodoCargados = tk.Button(lbl_tablaCargadosMover, text="↑↑↑", font=("verdana",15,"bold"), backgroun="#F5A9A9")
		btn_moverArribaTodoCargados.place(x = 25, y = 10, width=50, height=50)

		btn_moverAbajoTodoCargados = tk.Button(lbl_tablaCargadosMover, text="↓↓↓", font=("verdana",15,"bold"), backgroun="#F5A9A9")
		btn_moverAbajoTodoCargados.place(x = 25, y = 190, width=50, height=50)



	#--Buscador
	lbl_ventana_productor_buscador_entry = LabelFrame(lbl_ventana_productor_buscador, text="Filtrar")
	lbl_ventana_productor_buscador_tabla = LabelFrame(lbl_ventana_productor_buscador, text="Productores")
	lbl_ventana_productor = LabelFrame(lbl_ventana_productor_buscador, text="Productores usados")

	lbl_ventana_productor_buscador_entry.grid(column = 0, row = 0, padx = 2, pady = 2)
	lbl_ventana_productor_buscador_tabla.grid(column = 0, row = 1, padx = 10, pady = 5)
	lbl_ventana_productor.grid(column = 0, row = 2, padx = 10, pady = 5)

	#--
	entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="43")
	entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = padY)

	btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar", command= lambda: productFiltrar(entry_filtrar_productor.get(), tabla_productor))
	btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 5)

	sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
	sbr_productor.pack(side=RIGHT, fill="y")

	tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("cliente", "doc"), selectmode=tk.BROWSE, height=7) 
	tabla_productor.pack(side=LEFT, fill="both", expand=True)
	sbr_productor.config(command=tabla_productor.yview)
	tabla_productor.config(yscrollcommand=sbr_productor.set)

	tabla_productor.heading("#0", text="Pint.")
	tabla_productor.heading("cliente", text="Productor")
	tabla_productor.heading("doc", text="CUIT/DNI")

	tabla_productor.column("#0", width=40)
	tabla_productor.column("cliente", width=180)
	tabla_productor.column("doc", width=120)

	#CARGADOS
	sbr_productor_cargado = Scrollbar(lbl_ventana_productor)
	sbr_productor_cargado.pack(side=RIGHT, fill="y")

	tabla_productor_cargado = ttk.Treeview(lbl_ventana_productor, columns=("cliente", "doc"), selectmode=tk.BROWSE, height=18) 
	tabla_productor_cargado.pack(side=LEFT, fill="both", expand=True)
	sbr_productor_cargado.config(command=tabla_productor_cargado.yview)
	tabla_productor_cargado.config(yscrollcommand=sbr_productor_cargado.set)

	tabla_productor_cargado.heading("#0", text="Pint.")
	tabla_productor_cargado.heading("cliente", text="Productor")
	tabla_productor_cargado.heading("doc", text="CUIT/DNI")

	tabla_productor_cargado.column("#0", width=40)
	tabla_productor_cargado.column("cliente", width=180)
	tabla_productor_cargado.column("doc", width=120)

	entry_filtrar_productor.bind("<Return>", (lambda event: productFiltrar(entry_filtrar_productor.get(), tabla_productor)))
	tabla_productor.bind("<Double-1>", (lambda event: cargarProductor(tabla_productor)))
	tabla_productor.bind("<Return>", (lambda event: cargarProductor(tabla_productor)))
	tabla_productor_cargado.bind("<Double-1>", (lambda event: cargarProductor(tabla_productor_cargado)))
	tabla_productor_cargado.bind("<Return>", (lambda event: cargarProductor(tabla_productor_cargado)))
	
	#Informacion
	texto_alias = StringVar()
	texto_alias.set("") # Caso 1
	texto_razon = StringVar()
	texto_razon.set("")
	texto_cuit = StringVar()
	texto_cuit.set("     -")
	texto_ruca = StringVar()
	texto_ruca.set("     -")
	texto_corrales = StringVar()
	texto_corrales.set("     -")
	texto_animales = StringVar()
	texto_animales.set("     -")
	texto_kg = StringVar()
	texto_kg.set("     -")
	texto_id_lote = StringVar()
	texto_id_lote.set("")

	diccionario_textos["alias"] = texto_alias
	diccionario_textos["razon"] = texto_razon
	diccionario_textos["cuit"] = texto_cuit
	diccionario_textos["ruca"] = texto_ruca
	diccionario_textos["corrales"] = texto_corrales
	diccionario_textos["animales"] = texto_animales
	diccionario_textos["kg"] = texto_kg

	lbl_alias = tk.Label(lbl_ventana_productor_informacion, font=("Helvetica Neue",14,"bold"), anchor="w")
	lbl_alias.place(x=0, y=0, width=350)
	lbl_alias.config(textvariable=texto_alias)

	lbl_razon = tk.Label(lbl_ventana_productor_informacion, font=("Helvetica Neue",10), anchor="w")
	lbl_razon.place(x=0, y=30, width=350)
	lbl_razon.config(textvariable=texto_razon)

	lbl_cuit = tk.Label(lbl_ventana_productor_informacion, font=("verdana",12), anchor="w")
	lbl_cuit.place(x=40, y=67, width=140)
	lbl_cuit.config(textvariable=texto_cuit)

	lbl_ruca = tk.Label(lbl_ventana_productor_informacion, font=("verdana",12), anchor="w")
	lbl_ruca.place(x=245, y=67, width=100)
	lbl_ruca.config(textvariable=texto_ruca)


	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="CUIT:").place(x=0, y=70)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="RUCA:").place(x=200, y=70)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Total Corrales:").place(x=0, y=110)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Total Animales:").place(x=0, y=130)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Total Kilogramos:").place(x=0, y=150)

	lbl_corrales = tk.Label(lbl_ventana_productor_informacion, font=("verdana",10,"bold"), anchor="w")
	lbl_corrales.place(x=115, y=110, width=100)
	lbl_corrales.config(textvariable=texto_corrales)

	lbl_animales = tk.Label(lbl_ventana_productor_informacion, font=("verdana",10,"bold"), anchor="w")
	lbl_animales.place(x=115, y=130, width=100)
	lbl_animales.config(textvariable=texto_animales)

	lbl_kg = tk.Label(lbl_ventana_productor_informacion, font=("verdana",10,"bold"), anchor="w")
	lbl_kg.place(x=115, y=150, width=100)
	lbl_kg.config(textvariable=texto_kg)


	texto_pintura_inic = StringVar()
	texto_pintura_inic.set("-")

	lbl_pintura = tk.Label(lbl_ventana_productor_pintura, font=("Helvetica Neue",40,"bold"), anchor="center", backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_pintura.place(x=6, y=15, width=108)
	lbl_pintura.config(textvariable=texto_pintura_inic)

	entry_pintura = Entry(lbl_ventana_productor_pintura)
	entry_pintura.place(x=32, y=120, width=50)

	btn_pintura = tk.Button(lbl_ventana_productor_pintura, text="Setear", backgroun="#D6F4F8", font=("Helvetica Neue",8), command= lambda: pinturaSet(entry_pintura.get()))
	btn_pintura.place(x=32, y = 145, width = 50)

	entry_pintura.bind("<Return>", (lambda event: pinturaSet(entry_pintura.get())))

	#Acciones:
	btn_nuevo_lote = tk.Button(lbl_ventana_acciones, text="NUEVO\n(F1)", backgroun="#CBF9E1", font=("Helvetica Neue",12,"bold"), command= lambda: abrirLote(str(texto_cuit.get()),"nuevo"))
	btn_nuevo_lote.place(x=30-10, y = 20, width = 100, height = 60)

	btn_editar_lote = tk.Button(lbl_ventana_acciones, text="EDITAR", backgroun="#D6F4F8", font=("Helvetica Neue",12,"bold"), command= lambda: abrirLote(str(texto_cuit.get()), str(texto_id_lote.get())))
	btn_editar_lote.place(x=145-10, y = 20, width = 100, height = 60)

	btn_eliminar_lote = tk.Button(lbl_ventana_acciones, text="ELIMINAR", backgroun="#EF9090", font=("Helvetica Neue",12,"bold"), command= lambda: eliminarLote(str(texto_cuit.get()), str(texto_id_lote.get()))) 
	btn_eliminar_lote.place(x=257-10, y = 20, width = 100, height = 60)



	btn_exportar_corral = tk.Button(lbl_ventana_acciones, text="Imprimir\nCorral", backgroun="#D6F4F8", font=("Helvetica Neue",10,"bold"))
	btn_exportar_corral.place(x=30-10, y = 100, width = 100, height = 60)

	btn_exportar_tabla = tk.Button(lbl_ventana_acciones, text="Imprimir\nTabla", backgroun="#D6F4F8", font=("Helvetica Neue",10,"bold"))
	btn_exportar_tabla.place(x=145-10, y = 100, width = 100, height = 60)

	btn_exportar_todo = tk.Button(lbl_ventana_acciones, text="Imprimir\nTodo", backgroun="#D6F4F8", font=("Helvetica Neue",10,"bold"))
	btn_exportar_todo.place(x=257-10, y = 100, width = 100, height = 60)

	#VENTANA LOTE
	lbl_hacienda = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_peso = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_obs = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_dte = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")

	lbl_hacienda.place(x = 2, y = 2, width = 216, height = 180)
	lbl_peso.place(x = 222, y = 2, width = 216, height = 180)
	lbl_obs.place(x = 442, y = 2, width = 216, height = 180)
	lbl_dte.place(x = 662, y = 2, width = 210, height = 180)

	texto_cantidad = StringVar()
	texto_corral = StringVar()
	texto_catVenta = StringVar()
	texto_catHacienda = StringVar()
	texto_pintura = StringVar()
	texto_kgBruto = StringVar()
	texto_kgPromedio = StringVar()
	texto_desbastePorcentaje = StringVar()
	texto_desbasteKg = StringVar()
	texto_neto = StringVar()
	texto_promedio = StringVar()
	texto_observaciones = StringVar()
	texto_dte = StringVar()
	texto_flete = StringVar()
	texto_fletePrecio = StringVar()


	texto_cantidad.set("     -")
	texto_corral.set("     -")
	texto_catVenta.set("     -")
	texto_catHacienda.set("     -")
	texto_pintura.set("     -")
	texto_kgBruto.set("     -")
	texto_kgPromedio.set("     -")
	texto_desbastePorcentaje.set("     -")
	texto_desbasteKg.set("     -")
	texto_neto.set("     -")
	texto_promedio.set("     -")
	texto_observaciones.set("")
	texto_dte.set("")
	texto_flete.set("Propio")
	texto_fletePrecio.set("$999.999")

	diccionario_textos["cantidad"] = texto_cantidad
	diccionario_textos["corral"] = texto_corral
	diccionario_textos["catVenta"] = texto_catVenta
	diccionario_textos["catHacienda"] = texto_catHacienda
	diccionario_textos["pintura"] = texto_pintura
	diccionario_textos["kgBruto"] = texto_kgBruto
	diccionario_textos["kgPromedio"] = texto_kgPromedio
	diccionario_textos["desbastePorcentaje"] = texto_desbastePorcentaje
	diccionario_textos["desbasteKg"] = texto_desbasteKg
	diccionario_textos["neto"] = texto_neto
	diccionario_textos["promedio"] = texto_promedio
	diccionario_textos["id"] = texto_id_lote
	diccionario_textos["observaciones"] = texto_observaciones
	diccionario_textos["dte"] = texto_dte
	diccionario_textos["flete"] = texto_flete
	diccionario_textos["fletePrecio"] = texto_fletePrecio


	diccionario_textos["pintura_inic"] = texto_pintura_inic

	Label(lbl_hacienda, font=("verdana",10), text="Cantidad:", anchor="e", backgroun="#FFFFFF").place(x=2, y=20, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Corral:", anchor="e", backgroun="#FFFFFF").place(x=2, y=50, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Cat. venta:", anchor="e", backgroun="#FFFFFF").place(x=2, y=80, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Cat. hacienda:", anchor="e", backgroun="#FFFFFF").place(x=2, y=110, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Pintura:", anchor="e", backgroun="#FFFFFF").place(x=2, y=140, width=100)


	lbl_cantidad = tk.Label(lbl_hacienda, font=("verdana",12,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_cantidad.place(x=100, y=16, width=100)
	lbl_cantidad.config(textvariable=texto_cantidad)

	lbl_corral = tk.Label(lbl_hacienda, font=("verdana",12,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_corral.place(x=100, y=46, width=100)
	lbl_corral.config(textvariable=texto_corral)

	lbl_catVenta = tk.Label(lbl_hacienda, font=("verdana",8,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_catVenta.place(x=100, y=80, width=100)
	lbl_catVenta.config(textvariable=texto_catVenta)

	lbl_catHacienda = tk.Label(lbl_hacienda, font=("verdana",8,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_catHacienda.place(x=100, y=110, width=100)
	lbl_catHacienda.config(textvariable=texto_catHacienda)

	lbl_pintura = tk.Label(lbl_hacienda, font=("verdana",12,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_pintura.place(x=100, y=138, width=100)
	lbl_pintura.config(textvariable=texto_pintura)

	Label(lbl_peso, font=("verdana",10), text="Kg bruto:", anchor="e", backgroun="#FFFFFF").place(x=22, y=20, width=90)
	Label(lbl_peso, font=("verdana",10), text="Kg prom:", anchor="e", backgroun="#FFFFFF").place(x=22, y=50, width=90)
	Label(lbl_peso, font=("verdana",10), text="Desbaste %:", anchor="e", backgroun="#FFFFFF").place(x=22, y=80, width=90)
	Label(lbl_peso, font=("verdana",10), text="Desbaste kg:", anchor="e", backgroun="#FFFFFF").place(x=22, y=110, width=90)
	Label(lbl_peso, font=("verdana",10), text="NETO:", anchor="e", backgroun="#FFFFFF").place(x=2, y=140, width=50)
	Label(lbl_peso, font=("verdana",10), text="Prom:", anchor="e", backgroun="#FFFFFF").place(x=100, y=140, width=50)


	lbl_kgBruto = tk.Label(lbl_peso, font=("verdana",10,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_kgBruto.place(x=120, y=16, width=100)
	lbl_kgBruto.config(textvariable=texto_kgBruto)

	lbl_kgPromedio = tk.Label(lbl_peso, font=("verdana",10,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_kgPromedio.place(x=120, y=46, width=100)
	lbl_kgPromedio.config(textvariable=texto_kgPromedio)

	lbl_desbasteProcentaje = tk.Label(lbl_peso, font=("verdana",10,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_desbasteProcentaje.place(x=120, y=76, width=100)
	lbl_desbasteProcentaje.config(textvariable=texto_desbastePorcentaje)

	lbl_desbasteKg = tk.Label(lbl_peso, font=("verdana",10,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_desbasteKg.place(x=120, y=106, width=100)
	lbl_desbasteKg.config(textvariable=texto_desbasteKg)

	lbl_neto = tk.Label(lbl_peso, font=("verdana",10,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_neto.place(x=48, y=138, width=58)
	lbl_neto.config(textvariable=texto_neto)

	lbl_promedio = tk.Label(lbl_peso, font=("verdana",10,"bold"), anchor="w", backgroun="#FFFFFF")
	lbl_promedio.place(x=148, y=138, width=60)
	lbl_promedio.config(textvariable=texto_promedio)

	#OBSERVACIONES
	lbl_observaciones = tk.Label(lbl_obs, font=("verdana",10,"bold"), anchor="w", backgroun="#D6F4F8")
	lbl_observaciones.place(x=2, y=2, width=212)
	lbl_observaciones.config(textvariable=texto_observaciones)

	txt_observaciones = scrolledtext.ScrolledText(lbl_obs)
	txt_observaciones.place(x = 2, y = 25, width = 212, height = 152)
	txt_observaciones.config(state="disabled")
	diccionario_objetos["txt_observaciones"] = txt_observaciones


	#DTE
	tk.Label(lbl_dte, text="DTE", font=("verdana",10,"bold"), anchor="w", backgroun="#D6F4F8").place(x=2, y=2, width=212)

	lbl_numDte = tk.Label(lbl_dte, font=("verdana",10,"bold"), anchor="c", backgroun="#D6F4F8")
	lbl_numDte.place(x=42, y=2, width=168)
	lbl_numDte.config(textvariable=texto_dte)

	tk.Label(lbl_dte, text="Flete:", font=("verdana",10,"bold"), anchor="w", backgroun="#D6F4F8").place(x=2, y=70, width=212)

	lbl_flete = tk.Label(lbl_dte, font=("verdana",10,"bold"), anchor="c", backgroun="#D6F4F8")
	lbl_flete.place(x=42, y=70, width=168)
	lbl_flete.config(textvariable=texto_flete)

	lbl_fletePrecio = tk.Label(lbl_dte, font=("verdana",10,"bold"), anchor="c", backgroun="#D6F4F8")
	lbl_fletePrecio.place(x=2, y=100, width=212)
	lbl_fletePrecio.config(textvariable=texto_fletePrecio)


	#LOTES DEL PRODUCTOR
	sbr_lotes = Scrollbar(lbl_ventana_lotes)
	sbr_lotes.pack(side=RIGHT, fill="y")

	tabla_lotes = ttk.Treeview(lbl_ventana_lotes, columns=("catVenta", "catHacienda", "cantidad", "kg", "kgProm", "observaciones"), selectmode=tk.BROWSE, height=18) 
	tabla_lotes.pack(side=LEFT, fill="both", expand=True)
	sbr_lotes.config(command=tabla_lotes.yview)
	tabla_lotes.config(yscrollcommand=sbr_lotes.set)

	tabla_lotes.heading("#0", text="Corral")
	tabla_lotes.heading("catVenta", text="Categoría Venta")
	tabla_lotes.heading("catHacienda", text="Caategoría Hacienda")
	tabla_lotes.heading("cantidad", text="Cantidad")
	tabla_lotes.heading("kg", text="Kgs")
	tabla_lotes.heading("kgProm", text="Kgs prom.")
	tabla_lotes.heading("observaciones", text="Observaciones")

	tabla_lotes.column("#0", width=40)
	tabla_lotes.column("catVenta", width=150)
	tabla_lotes.column("catHacienda", width=150)
	tabla_lotes.column("cantidad", width=60)
	tabla_lotes.column("kg", width=60)
	tabla_lotes.column("kgProm", width=60)
	tabla_lotes.column("observaciones", width=250)

	diccionario_objetos["tabla_lotes"] = tabla_lotes
	diccionario_objetos["tabla_productor"] = tabla_productor
	diccionario_objetos["tabla_productor_cargado"] = tabla_productor_cargado

	cargarTabla()

	tabla_lotes.bind("<Double-1>", (lambda event: cargarLote(tabla_lotes)))
	tabla_lotes.bind("<Return>", (lambda event: cargarLote(tabla_lotes)))


window1 = Tk()
window1.title("Catalogo")
window1.geometry("1285x728")
window1.configure(backgroun="#2C4D4F") #E8F6FA
catalogo(window1)
window1.mainloop()
