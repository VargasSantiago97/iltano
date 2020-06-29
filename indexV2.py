#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

from librerias import tablaElegir
from librerias import pdf_ordenDeCarga
from librerias import ventanaRemates
#from librerias import ventanaIngreso2

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

dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : False}
diccionario_objetos = {"id_remate_alias" : "NULL", "id_catalogo_alias" : "NULL"}

diccionarioLotes = {}

direccionBaseDeDatos = "librerias/database/iltanohacienda.db"

ubicLiquidaciones = "C:/Users/Santiago/Desktop/exportaciones/liquidaciones"

window = Tk()
window.title("IL TANO HACIENDA SAS")
window.geometry("1024x600")
window.resizable(0,0)
window.configure(backgroun="#000000") #E8F6FA
window.attributes('-fullscreen', dicc_objetos["varFullScreen"])

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
def actualizar_db_selec(con, seleccionar, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT " + str(seleccionar) + " FROM " + str(tabla) + condiciones)
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

#PRODUCTORES
def compradorFiltrar():
	pal_clave = str(diccionario_objetos["entry_comprador"].get())

	con = sql_connection()
	condiciones =  ' WHERE (nombre LIKE "%' + pal_clave + '%" OR razon LIKE "%' + pal_clave + '%" OR ndoc LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%" OR con_iva LIKE "%' + pal_clave + '%" OR localidad LIKE "%' + pal_clave + '%" OR provincia LIKE "%' + pal_clave + '%" OR ruca LIKE "%' + pal_clave + '%" OR establecimiento LIKE "%' + pal_clave + '%") AND estado = "activo"'
	rows = actualizar_db(con, "productores", condiciones)

	try:
		remate = diccionario_objetos["id_remate_alias"]
		catalogo = diccionario_objetos["id_catalogo_alias"]
		con = sql_connection()
		condiciones = ' WHERE alias LIKE "%' + pal_clave + '%" AND estado = "activo" AND remate = "' + remate + '" AND catalogo = "' + catalogo + '"'
		rows_aux = actualizar_db(con, "productoresAuxiliares", condiciones)

		for row in rows_aux:
			rows.append(row)

	except:
		pass

	if(len(rows)==1):
		cargarDatosComprador(rows[0][1])
		cargarTablaCompradores([])
	else:
		cargarTablaCompradores(rows)
def compradorFiltrarUsados():
	try:
		tabla = diccionario_objetos["tabla"]

		productores = []

		for i in tabla.get_children():
			productorsss = tabla.item(i)["values"][8]
			if productorsss != "":
				productor = productorsss
				total = 0
				for j in tabla.get_children():
					if tabla.item(j)["values"][8] == productor:
						try:
							tot = float(tabla.item(j)["values"][9])
						except:
							tot = 0
						total = total + tot
				tupla = ("x", productor, "", total)
				if tupla not in productores:
					productores.append(tupla)

		cargarTablaCompradores(productores)

	except:
		pass

def cargarTablaCompradores(rows):

	tabla = diccionario_objetos["tabla_compradores"]

	for j in tabla.get_children():
		tabla.delete(j)

	try:
		for row in rows:
			texto_alias = str(row[1])
			texto_cuit = str(row[3])

			tabla.insert("", tk.END, tags=(str(row[0]), str(row[1])), values = (texto_alias,
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
	condiciones = " WHERE nombre = '" + str(productor) + "'"
	rows = actualizar_db(con, "productores", condiciones)

	if(len(rows)==0):
		remate = diccionario_objetos["id_remate_alias"]
		catalogo = diccionario_objetos["id_catalogo_alias"]

		con = sql_connection()
		condiciones = " WHERE alias = '" + str(productor) + "' AND remate = '" + remate + "' AND catalogo = '" + catalogo + "'"
		rows_aux = actualizar_db(con, "productoresAuxiliares", condiciones)

		if(len(rows_aux)==0):
			messagebox.showerror("ERROR", "No se pudo encontrar productor auxiliar, seleccione un catalogo")
			return 0
		else:
			texto_alias = rows_aux[0][1]
			texto_razon = "productor auxiliar"
			texto_cuit = ""

	else:
		row = rows[0]

		texto_alias = str(row[1])
		texto_razon = str(row[2])
		texto_cuit = str(row[3])


	tabla = diccionario_objetos["tabla"]
	kilogramos = 0
	cabezas = 0
	total = 0

	for i in tabla.get_children():
		if(tabla.item(i)["values"][8])==texto_alias:
			kilogramos = kilogramos + float(tabla.item(i)["values"][5])
			cabezas = cabezas + int(tabla.item(i)["values"][2])
			total = total + float(tabla.item(i)["values"][9])

			kilogramos = round(kilogramos, 2)
			cabezas = round(cabezas, 2)
			total = round(total, 2)

	texto_kgs = str(kilogramos)
	texto_total = str(total)
	texto_cabezas = str(cabezas)

	diccionario_objetos["texto_alias"].set(texto_alias)
	diccionario_objetos["texto_razon"].set(texto_razon)
	diccionario_objetos["texto_cuit"].set(texto_cuit)
	diccionario_objetos["texto_kgs"].set(texto_kgs)
	diccionario_objetos["texto_total"].set(texto_total)
	diccionario_objetos["texto_cabezas"].set(texto_cabezas)

	diccionario_objetos["btn_guardar"].config(state="normal")
#prod. auxiliars
def nuevoProductorAuxiliar():

	def guardarProductorAuxiliar():
		try:
			remate = str(diccionario_objetos["id_remate_alias"])
			catalogo = str(diccionario_objetos["id_catalogo_alias"])
			alias = str(entry_prodAuxiliar.get())

			con = sql_connection()
			condiciones = " WHERE alias = '" + alias + "' AND remate = '" + remate + "' AND catalogo = '" + catalogo + "' AND estado='activo'"
			rows = actualizar_db(con, "productoresAuxiliares", condiciones)

			entities = [alias, remate, catalogo, "", "activo"]

			con = sql_connection()
			condiciones = " WHERE nombre = '" + alias + "' AND estado='activo'"
			rows_verif = actualizar_db(con, "productores", condiciones)
			if len(rows_verif) != 0:
				messagebox.showerror("ERROR", "Este alias ya existe en base de datos 'Productores'")
				return 0

		except:
			messagebox.showerror("ERROR", "Error al leer datos")
			return 0

		if len(rows)==0:
			try:
				con = sql_connection()
				cursorObj = con.cursor()
				cursorObj.execute("INSERT INTO productoresAuxiliares VALUES(NULL, ?, ?, ?, ?, ?)", entities)
				con.commit()
				messagebox.showinfo("Éxito", "Productor ingresado con éxito!")

				winProd.destroy()

				diccionario_objetos["texto_alias"].set(alias)
				diccionario_objetos["texto_razon"].set("productor auxiliar")
				diccionario_objetos["texto_cuit"].set("")
				diccionario_objetos["texto_kgs"].set("")
				diccionario_objetos["texto_total"].set("")
				diccionario_objetos["texto_cabezas"].set("")

				diccionario_objetos["btn_guardar"].configure(state="normal")
			except:
				messagebox.showerror("ERROR", "Error al guardar")
		else:
			messagebox.showerror("ERROR", "Ya existe un productor auxiliar con ese alias")

	winProd = Toplevel(window)
	winProd.title("NUEVO PRODUCTOR AUXILIAR")
	winProd.geometry("350x200")
	winProd.configure(backgroun="#E8F6FA") #E8F6FA

	winProd1 = Label(winProd, backgroun="#E8F6FA")
	winProd2 = Label(winProd, backgroun="#E8F6FA")

	winProd1.grid(column=0, row=0, pady = 10, padx = 10)
	winProd2.grid(column=0, row=1, pady = 10, padx = 10)

	tk.Label(winProd1, text="Alias", font=("Helvetica", 15), backgroun="#E8F6FA").grid(column=0, row=0, padx=20, pady=20)


	entry_prodAuxiliar = Entry(winProd1, font=("Helvetica", 15))
	entry_prodAuxiliar.grid(column=1, row=0)
	entry_prodAuxiliar.focus()
	entry_prodAuxiliar.bind("<Return>", (lambda event: guardarProductorAuxiliar()))

	btn_guardarProdAux = tk.Button(winProd2, text="GUARDAR", font=("Helvetica", 15, "bold"), command=guardarProductorAuxiliar, backgroun="#b3f2bc")
	btn_guardarProdAux.grid(column=0, row=0)

	winProd.mainloop()
def asignarProductoresAuxiliares():
	try:
		remate = diccionario_objetos["id_remate_alias"]
		catalogo = diccionario_objetos["id_catalogo_alias"]
	except:
		messagebox.showinfo("ATENCION", "Primero seleccione remate y catalogo")
		return 0

	def asignarProductor():
		prodAux = texto_prodAux.get()
		prodOrigin = entry_productor.get()

		#verif prod aux
		con = sql_connection()
		condiciones =  " WHERE estado = 'activo' AND remate = '" + remate + "' AND catalogo = '" + catalogo + "' AND alias = '" + prodAux + "'"
		rows = actualizar_db(con, "productoresAuxiliares", condiciones)

		if (len(rows)==0):
			messagebox.showerror("ERROR", "Productor auxiliar invalido")
			return 0
		else:
			id_prod_aux = rows[0][0]

		#verif prod
		con = sql_connection()
		condiciones =  " WHERE estado = 'activo' AND nombre = '" + prodOrigin + "'"
		rows = actualizar_db(con, "productores", condiciones)

		if (len(rows)==0):
			messagebox.showerror("ERROR", "Productor invalido")
			return 0

		#cargar
		try:
			entities = [prodOrigin, str(id_prod_aux)]
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE productoresAuxiliares SET productor = ? where id = ?', entities)
			con.commit()
			messagebox.showinfo("Éxito", "Productor cargado con éxito!")
		except:
			messagebox.showerror("ERROR", "ERROR al cargar en la base de datos")
			return 0

		actualizarTablaProductoresAuxiliares()

	def buscarProductorAuxiliar():
		def funcSalirAux(ssss):
			con = sql_connection()
			condiciones = " WHERE id = " + str(ssss)
			rows = actualizar_db(con, "productores", condiciones)

			entry_productor.delete(0, tk.END)
			entry_productor.insert(0, rows[0][1])

		dicc_buscar = {"seleccionar" : "productor",
		"columnas" : {"0":{"id" : "alias", "cabeza" : "Alias", "ancho" : 180, "row" : 1}, "1":{"id" : "razon", "cabeza" : "Razon Social", "ancho" : 180, "row" : 2}, "2":{"id" : "cuit", "cabeza" : "CUIT", "ancho" : 110, "row" : 3}},
		"db" : direccionBaseDeDatos,
		"tabla" : "productores",
		"condiciones" : ' WHERE (nombre LIKE  "%' + str(entry_productor.get()) + '%" OR razon LIKE "%' + str(entry_productor.get()) + '%" OR ndoc LIKE "%' + str(entry_productor.get()) + '%") AND estado = "activo"',
		"dimensionesVentana" : "500x400"}
		tablaElegir.tabla_elegir(dicc_buscar, funcSalirAux)

	def actualizarTablaProductoresAuxiliares():
		try:
			con = sql_connection()
			condiciones = " WHERE estado = 'activo' AND remate = '" + remate + "' AND catalogo = '" + catalogo + "'"
			rows = actualizar_db(con, "productoresAuxiliares", condiciones)
		except:
			messagebox.showinfo("No se puedo actualizar la base de datos","No se puedo actualizar la base de datos")
			return 0

		try:
			for i in tabla_aux.get_children():
				tabla_aux.delete(i)

			for row in rows:
				textoProdAux = str(row[1])
				textoProd = str(row[4])

				tabla_aux.insert("", tk.END, tags=(str(row[0]), str(row[1])), values = (textoProdAux, textoProd,))
		except:
			messagebox.showinfo("ERROR", "No se pudo cargar la tabla")

	def elegirItemAux(seleccion):
		prodSelec = str(seleccion["values"][0])
		texto_prodAux.set(prodSelec)

		entry_productor.delete(0, tk.END)

	window_asignar = Toplevel(window)
	window_asignar.title("Asignar productores auxiliares  - " + remate + " - " + catalogo)
	window_asignar.geometry("520x500")
	window_asignar.configure(backgroun="#E8F6FA")

	lbl_tablaAux = tk.Label(window_asignar, backgroun="#E8F6FA")
	lbl_tablaAux.place(x = 10, y = 10, width = 500, height = 300)

	lbl_prodAux = tk.Label(window_asignar, backgroun="#c7e5ed")
	lbl_prodAux.place(x = 10, y = 320, width = 500, height = 50)

	lbl_entry = tk.Label(window_asignar, backgroun="#c7e5ed")
	lbl_entry.place(x = 10, y = 380, width = 500, height = 50)

	lbl_btnAsignar = tk.Label(window_asignar, backgroun="#E8F6FA")
	lbl_btnAsignar.place(x = 10, y = 440, width = 500, height = 50)


	#tabla productores auxiliares
	if(True):
		sbr_aux = Scrollbar(lbl_tablaAux)
		sbr_aux.pack(side=RIGHT, fill="y")


		tabla_aux = ttk.Treeview(lbl_tablaAux, columns=["AUX", "PRODUCTOR"], selectmode=tk.BROWSE, show='headings') 
		tabla_aux.pack(side=LEFT, fill="both", expand=True)
		sbr_aux.config(command=tabla_aux.yview)
		tabla_aux.config(yscrollcommand=sbr_aux.set)


		tabla_aux.heading("AUX", text="PRODUCTOR AUX", command=lambda: treeview_sort_column(tabla_aux, "AUX", False))
		tabla_aux.heading("PRODUCTOR", text="PRODUCTOR", command=lambda: treeview_sort_column(tabla_aux, "PRODUCTOR", False))
		
		tabla_aux.column("AUX", width=100)
		tabla_aux.column("PRODUCTOR", width=100)


		tabla_aux.bind("<Double-1>", (lambda event: elegirItemAux(tabla_aux.item(tabla_aux.selection()))))
		tabla_aux.bind("<Return>", (lambda event: elegirItemAux(tabla_aux.item(tabla_aux.selection()))))

	#prod aux
	if(True):
		tk.Label(lbl_prodAux, backgroun="#c7e5ed", text = "Prod. auxiliar:", font=("Helvetica", 15, "bold"), anchor = "e").place(x = 5, y = 5, width = 150, height = 35)

		texto_prodAux = StringVar()
		texto_prodAux.set("")

		lbl_prodAux_text = tk.Label(lbl_prodAux, font=("Helvetica Neue",15), anchor="c", backgroun="#c7e5ed")
		lbl_prodAux_text.place(x=160, y=5, width=330, height = 35)
		lbl_prodAux_text.config(textvariable=texto_prodAux)

	#prod
	if(True):
		tk.Label(lbl_entry, backgroun="#c7e5ed", text = "Productor:", font=("Helvetica", 15, "bold"), anchor = "e").place(x = 5, y = 5, width = 150, height = 35)

		entry_productor = Entry(lbl_entry, font=("Helvetica Neue",15,"bold"))
		entry_productor.place(x = 160, y = 5, width=330, height = 35)
		entry_productor.bind("<Return>", (lambda event: buscarProductorAuxiliar()))
		entry_productor.bind("<Control-s>", (lambda event: remateSeleccionador()))
		entry_productor.bind("<F1>", (lambda event: remateSeleccionador()))
		entry_productor.focus()

	#btn
	if(True):
		btn_buscar = tk.Button(lbl_btnAsignar, text="GUARDAR", compound="top", backgroun="#b3f2bc", font=("Helvetica", 20, "bold"), command=asignarProductor)
		btn_buscar.pack()


	actualizarTablaProductoresAuxiliares()




	window_asignar.mainloop()


#Pantalla detalles
def pantallaDetalles():
	def pantCompletaDetalles():
		windowDetalles.attributes('-fullscreen', dicc_objetos["varFullScreenDetalles"])
		dicc_objetos["varFullScreenDetalles"] = not dicc_objetos["varFullScreenDetalles"]

	windowDetalles = Toplevel()
	windowDetalles.geometry("700x700")
	windowDetalles.configure(backgroun="#000000")

	texto_alias = StringVar(windowDetalles)
	texto_alias.set("asd") # Caso 1

	lbl_alias = tk.Label(windowDetalles, font=("Helvetica Neue",100,"bold"), anchor="n", backgroun="#000000", foreground = "#FFFFFF") 
	lbl_alias.place(x=0, y=0, width = 700)
	lbl_alias.config(textvariable=texto_alias)

	dicc_objetos["texto_alias"] = texto_alias




	windowDetalles.bind('<F11>', (lambda event: pantCompletaDetalles()))
	windowDetalles.mainloop()


#CARGAR LOTES
def crearDiccionarioLotes():
	remate = str(diccionario_objetos["id_remate_alias"])
	catalogo = str(diccionario_objetos["id_catalogo_alias"])

	#Leer diccionarios
	try:
		ubicGuardar = "catalogos"

		nombreArchivoLotes = "remate_" + remate + "_-_catalogo_" + catalogo + "_lot.json"
		nombreArchivoCat = "remate_" + remate + "_-_catalogo_" + catalogo + "_cat.json"

		archivo = open(ubicGuardar + "/" + nombreArchivoLotes, "r")
		dicLotes = json.loads(archivo.read())
		archivo.close()

		archivoCat = open(ubicGuardar + "/" + nombreArchivoCat, "r")
		dicCat = json.loads(archivoCat.read())
		archivoCat.close()

	except:
		messagebox.showerror("ERROR", "Error, no se pudo cargar")
		return 0

	k = 0
	diccionarioLotes.clear()
	for i in range(0, len(dicCat)):
		id_cat = dicCat[str(i)]
		for j in range(0, len(dicLotes[id_cat])):
			id_lote = dicLotes[id_cat][str(j)]

			con = sql_connection()
			condiciones = " WHERE id = " + str(id_lote)
			rows = actualizar_db(con, "lotes", condiciones)

			con = sql_connection()
			condiciones = " WHERE remate = '" + remate + "' AND productor = '" + str(rows[0][2]) + "'"
			rows_pintura = actualizar_db_selec(con, "pintura", "pintura", condiciones)
			if(len(rows_pintura) > 0):
				x_pintura = rows_pintura[0][0]
			else:
				x_pintura = ""

			con = sql_connection()
			condiciones = " WHERE lote = '" + str(rows[0][0]) + "' AND estado = 'activo'"
			rows_compraventa = actualizar_db(con, "compraventa", condiciones)

			if(len(rows_compraventa) > 0):
				x_precio = rows_compraventa[0][3]
				x_comprador = rows_compraventa[0][2]
				x_precioCalculo = rows_compraventa[0][3]
			else:
				x_precio = ""
				x_comprador = ""
				x_precioCalculo = 0

			x_id = rows[0][0]
			x_corral = rows[0][4]
			x_vendedor = rows[0][2]
			x_cantidad = rows[0][3]
			x_categoriaVenta = rows[0][5]
			x_categoria = rows[0][6]
			x_kilogramos = rows[0][12]
			x_promedio = rows[0][13]
			x_total = round(float(x_kilogramos) * float(x_precioCalculo), 2)


			diccionarioLotes[str(k)] = {
			"id" : str(x_id),
			"corral" : str(x_corral),
			"vendedor" : str(x_vendedor),
			"cantidad" : str(x_cantidad),
			"categoria" : str(x_categoria),
			"categoriaVenta" : str(x_categoriaVenta),
			"pintura" : str(x_pintura),
			"kilogramos" : str(x_kilogramos),
			"promedio" : str(x_promedio),
			"precio" : str(x_precio),
			"comprador" : str(x_comprador),
			"total" : str(x_total)
			}
			k += 1
def cargarTablaLotes():

	tabla = diccionario_objetos["tabla"]

	for i in tabla.get_children():
		tabla.delete(i)


	cant_lotes = len(diccionarioLotes)

	for i in range(0, cant_lotes):
		tabla.insert("", str(i), tags=str(i), text = diccionarioLotes[str(i)]["id"], iid= diccionarioLotes[str(i)]["id"], values = (diccionarioLotes[str(i)]["corral"],
			diccionarioLotes[str(i)]["vendedor"],
			diccionarioLotes[str(i)]["cantidad"],
			diccionarioLotes[str(i)]["categoria"],
			diccionarioLotes[str(i)]["pintura"],
			diccionarioLotes[str(i)]["kilogramos"],
			diccionarioLotes[str(i)]["promedio"],
			diccionarioLotes[str(i)]["precio"],
			diccionarioLotes[str(i)]["comprador"],
			diccionarioLotes[str(i)]["total"]))
def elegirItem(loteseleccion):
	diccionario_objetos["btn_productorAuxiliar"].configure(state="normal")
	diccionario_objetos["btn_editarLote"].configure(state="normal")

	#DATOS DEL LOTE
	id_lote = str(loteseleccion["text"])
	diccionario_objetos["id_lote"] = id_lote

	con = sql_connection()
	condiciones = " WHERE id = " + id_lote
	rows = actualizar_db(con, "lotes", condiciones)

	row = rows[0]

	texto_catHacienda = str(row[6])
	texto_catVenta = str(row[5])
	texto_corral = str(row[4])
	texto_cantidad = str(row[3])
	texto_neto = str(row[12])
	texto_promedio = str(row[13])
	txt_observaciones = str(row[14]) + "  -  " + str(row[15])

	diccionario_objetos["datosLote_texto_catHacienda"].set(texto_catHacienda)
	diccionario_objetos["datosLote_texto_catVenta"].set(texto_catVenta)
	diccionario_objetos["datosLote_texto_corral"].set(texto_corral)
	diccionario_objetos["datosLote_texto_cantidad"].set(texto_cantidad)
	diccionario_objetos["datosLote_texto_neto"].set(texto_neto)
	diccionario_objetos["datosLote_texto_promedio"].set(texto_promedio)

	diccionario_objetos["datosLote_txt_observaciones"].config(state="normal")
	diccionario_objetos["datosLote_txt_observaciones"].delete("1.0", tk.END)
	diccionario_objetos["datosLote_txt_observaciones"].insert("1.0", txt_observaciones)
	diccionario_objetos["datosLote_txt_observaciones"].config(state="disabled")

	#DATOS DE LA COMPRA
	id_remate_alias = str(diccionario_objetos["id_remate_alias"])

	con = sql_connection()
	condiciones = " WHERE estado = 'activo' AND lote = '" + id_lote + "' AND remate = '" + id_remate_alias + "'"
	rows = actualizar_db(con, "compraventa", condiciones)

	if(len(rows)==0):
		diccionario_objetos["texto_alias"].set("")
		diccionario_objetos["texto_razon"].set("")
		diccionario_objetos["texto_cuit"].set("")
		diccionario_objetos["texto_kgs"].set(0)
		diccionario_objetos["texto_total"].set(0)
		diccionario_objetos["texto_cabezas"].set(0)

		diccionario_objetos["entry_precio"].delete(0, tk.END)
		diccionario_objetos["btn_guardar"].configure(text="GUARDAR", state="disabled", command=guardarCompraventa)
		diccionario_objetos["btn_eliminar"].configure(state="disabled")

		diccionario_objetos["id_compraventa"] = ""
	else:
		diccionario_objetos["id_compraventa"] = str(rows[0][0])

		#verificar productor
		if(rows[0][2]!=""):
			cargarDatosComprador(rows[0][2])
		else:
			diccionario_objetos["texto_alias"].set("")
			diccionario_objetos["texto_razon"].set("")
			diccionario_objetos["texto_cuit"].set("")
			diccionario_objetos["texto_kgs"].set(0)
			diccionario_objetos["texto_total"].set(0)
			diccionario_objetos["texto_cabezas"].set(0)

		#verificar precio
		diccionario_objetos["entry_precio"].delete(0, tk.END)
		if(rows[0][3]!=""):
			diccionario_objetos["entry_precio"].insert(0, rows[0][3])

		#Cambiar botones
		diccionario_objetos["btn_guardar"].configure(text="EDITAR", state="normal", command=editarCompraventa)
		diccionario_objetos["btn_eliminar"].configure(state="normal")


#COMPRAVENTA
def eliminarCompraventa():
	try:
		id_compraventa = diccionario_objetos["id_compraventa"]

		MsgBox = messagebox.askquestion('ATENCION', '¿Desea BORRAR?', icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE compraventa SET estado = "borrado" where id = ' + id_compraventa)
			con.commit()
			messagebox.showinfo("Borrado", "Borrado con Éxito")
			crearDiccionarioLotes()
			cargarTablaLotes()
			
	except:
		messagebox.showerror("ERROR", "No se pudo borrar")
def guardarCompraventa():
	try:
		x_lote = diccionario_objetos["id_lote"]
		x_comprador = diccionario_objetos["texto_alias"].get()
		x_precio = diccionario_objetos["entry_precio"].get()
		x_estado = "activo"
		x_remate = str(diccionario_objetos["id_remate_alias"])
		x_vendedor = ""

		entities = [x_lote,
		x_comprador,
		x_precio,
		x_remate,
		x_estado,
		x_vendedor]

	except:
		messagebox.showerror("ERROR", "Error al obtener los datos")
		return 0

	try:
		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO compraventa VALUES(NULL, ?, ?, ?, ?, ?, ?)", entities)
		con.commit()
		messagebox.showinfo("Éxito", "Productor ingresado con éxito!")
		crearDiccionarioLotes()
		cargarTablaLotes()
	except:
		messagebox.showerror("ERROR", "Error al guardar")
def editarCompraventa():
	try:
		x_idCompraventa = diccionario_objetos["id_compraventa"]
		x_comprador = diccionario_objetos["texto_alias"].get()
		x_precio = diccionario_objetos["entry_precio"].get()

		entities = [str(x_comprador),
		str(x_precio),
		str(x_idCompraventa)]

	except:
		messagebox.showerror("ERROR", "Error al obtener los datos")
		return 0

	try:
		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute('UPDATE compraventa SET comprador = ?, precio = ? where id = ?', entities)
		con.commit()
		messagebox.showinfo("Éxito", "Lote EDITADO con éxito!")
		crearDiccionarioLotes()
		cargarTablaLotes()
	except:
		messagebox.showerror("ERROR", "Error al guardar")


#SELECCIONAR REMATE Y CATALOGO
def seleccionarRemate():

	def buscarRemate():
		def funcsalirr(ssss):
			con = sql_connection()
			condiciones = " WHERE id = " + str(ssss)
			rows = actualizar_db(con, "remate", condiciones)

			entryRemate.delete(0, tk.END)
			entryRemate.insert(0, rows[0][1])

		dicc_buscar = {"seleccionar" : "remate",
		"columnas" : {"0":{"id" : "nombre", "cabeza" : "Remate", "ancho" : 180, "row" : 1}, "1":{"id" : "fecha", "cabeza" : "Fecha", "ancho" : 60, "row" : 2}, "2":{"id" : "tipo", "cabeza" : "Tipo", "ancho" : 70, "row" : 3}},
		"db" : direccionBaseDeDatos,
		"tabla" : "remate",
		"condiciones" : ' WHERE nombre LIKE  "%' + str(entryRemate.get()) + '%" AND estado = "activo"',
		"dimensionesVentana" : "336x400"}
		tablaElegir.tabla_elegir(dicc_buscar, funcsalirr)

	def remateSeleccionador():
		con = sql_connection()
		condiciones = " WHERE nombre = '" + str(entryRemate.get()) + "' AND estado = 'activo'"
		rows = actualizar_db(con, "remate", condiciones)

		if (len(rows)==0):
			messagebox.showerror("ERROR", "ERROR, ese remate no existe o está borrado")
			return 0
		else:
			diccionario_objetos["textID"].set(rows[0][0])
			diccionario_objetos["id_remate_alias"] = rows[0][1]
			diccionario_objetos["textTitulo"].set("REMATE: " + str(rows[0][1]))
			wind_select.destroy()

	wind_select = Toplevel(window)
	wind_select.title("SELECCIONAR REMATE")
	wind_select.geometry("400x200")
	wind_select.configure(backgroun="#E8F6FA") #E8F6FA

	tk.Label(wind_select, text="REMATE", font=("Helvetica Neue",12,"bold"), anchor="n", backgroun="#E8F6FA", foreground = "#000000").grid(column=0, row=0, padx=10, pady=10)

	entryRemate = Entry(wind_select, font=("Helvetica Neue",12,"bold"))
	entryRemate.grid(column = 1, row = 0, padx = 10, pady = 10)
	entryRemate.bind("<Return>", (lambda event: buscarRemate()))
	entryRemate.bind("<Control-s>", (lambda event: remateSeleccionador()))
	entryRemate.bind("<F1>", (lambda event: remateSeleccionador()))
	entryRemate.focus()


	btn_buscar = Button(wind_select, text="Buscar", command=buscarRemate)
	btn_buscar.grid(column = 1, row = 1, padx = 10, pady = 10)

	btn_seleccionar = Button(wind_select, text="Seleccionar", command= lambda: remateSeleccionador())
	btn_seleccionar.grid(column = 1, row = 2, padx = 10, pady = 10)

	wind_select.mainloop()
def seleccionarCatalogo():
	remateName = diccionario_objetos["textID"].get()

	if remateName == "":
		messagebox.showerror("ERROR", "Primero debe seleccionar un remate")
		return 0

	def buscarCatalogo():
		def funcsalirCat(ssss):
			con = sql_connection()
			condiciones = " WHERE id = " + str(ssss)
			rows = actualizar_db(con, "catalogo", condiciones)

			entryCatalogo.delete(0, tk.END)
			entryCatalogo.insert(0, rows[0][1])

		dicc_buscar = {"seleccionar" : "catalogo",
		"columnas" : {"0":{"id" : "nombre", "cabeza" : "Catalogo", "ancho" : 180, "row" : 1}, "1":{"id" : "nombre", "cabeza" : "Nombre", "ancho" : 60, "row" : 2}, "2":{"id" : "fecha", "cabeza" : "Fecha", "ancho" : 70, "row" : 4}},
		"db" : direccionBaseDeDatos,
		"tabla" : "catalogo",
		"condiciones" : ' WHERE (nombre LIKE  "%' + str(entryCatalogo.get()) + '%" OR alias LIKE  "%' + str(entryCatalogo.get()) + '%") AND estado = "activo"',
		"dimensionesVentana" : "336x400"}
		tablaElegir.tabla_elegir(dicc_buscar, funcsalirCat)

	def catalogoSeleccionador():
		con = sql_connection()
		condiciones = " WHERE alias = '" + str(entryCatalogo.get()) + "' AND estado = 'activo'"
		rows = actualizar_db(con, "catalogo", condiciones)

		if (len(rows)==0):
			messagebox.showerror("ERROR", "ERROR, ese catalogo no existe o está borrado")
			return 0
		else:
			diccionario_objetos["id_catalogo_id"] = rows[0][0]
			diccionario_objetos["id_catalogo_alias"] = rows[0][1]
			diccionario_objetos["textTitulo"].set("REMATE: " + str(diccionario_objetos["id_remate_alias"]) + "    -    CATALOGO: " + rows[0][1])
			wind_select.destroy()
			crearDiccionarioLotes()
			cargarTablaLotes()

	wind_select = Toplevel(window)
	wind_select.title("SELECCIONAR CATALOGO EN REMATE: " + str(diccionario_objetos["id_remate_alias"]))
	wind_select.geometry("400x200")
	wind_select.configure(backgroun="#E8F6FA") #E8F6FA

	tk.Label(wind_select, text="CATALOGO", font=("Helvetica Neue",12,"bold"), anchor="n", backgroun="#E8F6FA", foreground = "#000000").grid(column=0, row=0, padx=10, pady=10)

	entryCatalogo = Entry(wind_select, font=("Helvetica Neue",12,"bold"))
	entryCatalogo.grid(column = 1, row = 0, padx = 10, pady = 10)
	entryCatalogo.bind("<Return>", (lambda event: buscarCatalogo()))
	entryCatalogo.bind("<Control-s>", (lambda event: catalogoSeleccionador()))
	entryCatalogo.bind("<F1>", (lambda event: catalogoSeleccionador()))
	entryCatalogo.focus()


	btn_buscar = Button(wind_select, text="Buscar", command=buscarCatalogo)
	btn_buscar.grid(column = 1, row = 1, padx = 10, pady = 10)

	btn_seleccionar = Button(wind_select, text="Seleccionar", command= lambda: catalogoSeleccionador())
	btn_seleccionar.grid(column = 1, row = 2, padx = 10, pady = 10)

	wind_select.mainloop()

def cargarTodosLosLotes():
	remate = str(diccionario_objetos["id_remate_alias"])

	diccionarioLotes.clear()

	con = sql_connection()
	condiciones = " WHERE remate = '" + str(remate) + "' AND estado = 'activo'"
	rows = actualizar_db(con, "lotes", condiciones)

	k=0
	for row in rows:
		con = sql_connection()
		condiciones = " WHERE remate = '" + remate + "' AND productor = '" + str(row[2]) + "'"
		rows_pintura = actualizar_db_selec(con, "pintura", "pintura", condiciones)

		if(len(rows_pintura) > 0):
			x_pintura = rows_pintura[0][0]
		else:
			x_pintura = ""

		con = sql_connection()
		condiciones = " WHERE lote = '" + str(row[0]) + "' AND estado = 'activo'"
		rows_compraventa = actualizar_db(con, "compraventa", condiciones)

		if(len(rows_compraventa) > 0):
			x_precio = rows_compraventa[0][3]
			x_comprador = rows_compraventa[0][2]
			x_precioCalculo = rows_compraventa[0][3]
		else:
			x_precio = ""
			x_comprador = ""
			x_precioCalculo = 0

		x_id = row[0]
		x_corral = row[4]
		x_vendedor = row[2]
		x_cantidad = row[3]
		x_categoriaVenta = row[5]
		x_categoria = row[6]
		x_kilogramos = row[12]
		x_promedio = row[13]
		x_total = round(float(x_kilogramos) * float(x_precioCalculo), 2)


		diccionarioLotes[str(k)] = {
		"id" : str(x_id),
		"corral" : str(x_corral),
		"vendedor" : str(x_vendedor),
		"cantidad" : str(x_cantidad),
		"categoria" : str(x_categoria),
		"categoriaVenta" : str(x_categoriaVenta),
		"pintura" : str(x_pintura),
		"kilogramos" : str(x_kilogramos),
		"promedio" : str(x_promedio),
		"precio" : str(x_precio),
		"comprador" : str(x_comprador),
		"total" : str(x_total)
		}
		k += 1

	cargarTablaLotes()

#EXPORTAR
def exportarExcel():
	tabla = diccionario_objetos["tabla"]

	dire = filedialog.askdirectory()

	if dire == () or dire == "":
		messagebox.showinfo("Atencion", "El archivo no se exportó")
		return 0

	fileName = dire + "/Catalogo cargado - " + diccionario_objetos["id_remate_alias"] + " - " + diccionario_objetos["id_catalogo_alias"] + " --- " + str(time.strftime("%d-%m-%y")) + " - " + str(time.strftime("%H-%M-%S")) + "hs.csv"

	archivoExportar = open(fileName, "w")

	texto = "CORRAL;VENDEDOR;CANT;CATEGORIA;PINT;KG;PROM;PRECIO;COMPRADOR;TOTAL\n"

	for i in tabla.get_children():
		info = tabla.item(i)["values"]

		x_corral = str(info[0])
		x_vendedor = str(info[1])
		x_cantidad = str(info[2])
		x_categoria = str(info[3])
		x_pintura = str(info[4])
		x_kilogramos = str(info[5])
		x_promedio = str(info[6]).replace(".", ",")
		x_precio = str(info[7]).replace(".", ",")
		x_comprador = str(info[8])
		x_total = str(info[9]).replace(".", ",")

		texto = texto + x_corral + ";" + x_vendedor + ";" + x_cantidad + ";" + x_categoria + ";" + x_pintura + ";" + x_kilogramos + ";" + x_promedio + ";" + x_precio + ";" + x_comprador + ";" + x_total + "\n"

	archivoExportar.write(texto)
	archivoExportar.close()
def exportarExcelTotales():

	dire = filedialog.askdirectory()
	if dire == () or dire == "":
		messagebox.showinfo("Atencion", "El archivo no se exportó")
		return 0

	fileName = dire + "/TOTALES COMPRAS - " + diccionario_objetos["id_remate_alias"] + " --- " + str(time.strftime("%d-%m-%y")) + " - " + str(time.strftime("%H-%M-%S")) + "hs.csv"

	archivoExportar = open(fileName, "w")

	texto = "LIQUIDACION;COMPRADOR;CABEZAS;SUBTOTAL;COMISION;IVA HACIENDA; IVA COMISION; TOTAL LIQUIDACION\n"

	con = sql_connection()
	condiciones = " WHERE remate = '" + diccionario_objetos["id_remate_alias"] + "'"
	rows = actualizar_db(con, "liquidacionesCompraGuardadas", condiciones)

	for row in rows:
		direArchivo = ubicLiquidaciones + "/" + str(row[4])

		archivo = open(direArchivo, "r")
		dicc = json.loads(archivo.read())
		archivo.close()

		x_liquidacion = str(row[3])
		x_comprador = str(row[2])
		x_cabezas = str(dicc["totales"]["totalCabezas"])
		x_subtotal = str(dicc["totales"]["subtotalMartillo"]).replace(".", ",")
		x_comision = str(dicc["gastos"]["0"]["importe"]).replace(".", ",")
		x_ivaHacienda = str(dicc["totales"]["ivaHacienda"]).replace(".", ",")
		x_ivaComision = str(dicc["gastos"]["0"]["$iva"]).replace(".", ",")
		x_total = str(dicc["totales"]["total"]).replace(".", ",")

		texto = texto + x_liquidacion + ";" + x_comprador + ";" + x_cabezas + ";" + x_subtotal + ";" + x_comision + ";" + x_ivaHacienda + ";" + x_ivaComision + ";" + x_total + "\n"

	archivoExportar.write(texto)
	archivoExportar.close()
def exportarExcelTotalesVentas():

	dire = filedialog.askdirectory()
	if dire == () or dire == "":
		messagebox.showinfo("Atencion", "El archivo no se exportó")
		return 0

	fileName = dire + "/TOTALES VENTAS - " + diccionario_objetos["id_remate_alias"] + " --- " + str(time.strftime("%d-%m-%y")) + " - " + str(time.strftime("%H-%M-%S")) + "hs.csv"

	archivoExportar = open(fileName, "w")

	texto = "LIQUIDACION;VENDEDOR;CABEZAS;SUBTOTAL;COMISION;IVA HACIENDA; IVA COMISION; RETENCION IIBB;TOTAL LIQUIDACION\n"

	con = sql_connection()
	condiciones = " WHERE remate = '" + diccionario_objetos["id_remate_alias"] + "'"
	rows = actualizar_db(con, "liquidacionesVentaGuardadas", condiciones)

	for row in rows:
		direArchivo = ubicLiquidaciones + "/" + str(row[4])

		archivo = open(direArchivo, "r")
		dicc = json.loads(archivo.read())
		archivo.close()

		x_liquidacion = str(row[3])
		x_comprador = str(row[2])
		x_cabezas = str(dicc["totales"]["totalCabezas"])
		x_subtotal = str(dicc["totales"]["subtotalMartillo"]).replace(".", ",")
		x_comision = str(dicc["gastos"]["0"]["importe"]).replace(".", ",")
		x_ivaHacienda = str(dicc["totales"]["ivaHacienda"]).replace(".", ",")
		x_ivaComision = str(dicc["gastos"]["0"]["$iva"]).replace(".", ",")
		x_retencion = str(dicc["totales"]["retencion"]).replace(".", ",")
		x_total = str(dicc["totales"]["total"]).replace(".", ",")

		texto = texto + x_liquidacion + ";" + x_comprador + ";" + x_cabezas + ";" + x_subtotal + ";" + x_comision + ";" + x_ivaHacienda + ";" + x_ivaComision + ";" + x_retencion + ";" + x_total + "\n"

	archivoExportar.write(texto)
	archivoExportar.close()

#ORDENES DE CARGA
def ordenesDeCarga():

	def exportarOrdenesTodas():
		for i in tablaOrdenes.get_children():
			id_preliq = tablaOrdenes.item(i)["text"]

			con = sql_connection()
			condiciones = " WHERE id = " + str(id_preliq)
			row_dat = actualizar_db(con, "liquidacionesCompraGuardadas", condiciones)

			direArchivo = ubicLiquidaciones + "/" + str(row_dat[0][4])

			archivo = open(direArchivo, "r")
			dicc = json.loads(archivo.read())
			archivo.close()

			pdf_ordenDeCarga.preliquidacionPDF(dicc)

	def exportarOrden(entrada):
		id_preliq = entrada["text"]

		con = sql_connection()
		condiciones = " WHERE id = " + str(id_preliq)
		row_dat = actualizar_db(con, "liquidacionesCompraGuardadas", condiciones)

		direArchivo = ubicLiquidaciones + "/" + str(row_dat[0][4])

		archivo = open(direArchivo, "r")
		dicc = json.loads(archivo.read())
		archivo.close()

		pdf_ordenDeCarga.preliquidacionPDF(dicc)


	remate = diccionario_objetos["id_remate_alias"]
	wind_ordenes = Toplevel(window)
	wind_ordenes.title("ORDENES DE CARGA")
	wind_ordenes.geometry("500x400")
	wind_ordenes.configure(backgroun="#E8F6FA") #E8F6FA

	lbl_tablaOrdenes = Label(wind_ordenes, backgroun="#d1f5ff")
	lbl_tablaOrdenes.place(x = 5, y = 5, width=490, height=200)

	sbrOrdenes = Scrollbar(lbl_tablaOrdenes)
	sbrOrdenes.pack(side=RIGHT, fill="y")

	tablaOrdenes = ttk.Treeview(lbl_tablaOrdenes, columns=["PRODUCTOR", "LIQUIDACION"], selectmode=tk.BROWSE, show='headings') 
	tablaOrdenes.pack(side=LEFT, fill="both", expand=True)
	sbrOrdenes.config(command=tablaOrdenes.yview)
	tablaOrdenes.config(yscrollcommand=sbrOrdenes.set)

	tablaOrdenes.heading("PRODUCTOR", text="PRODUCTOR", command=lambda: treeview_sort_column(tablaOrdenes, "PRODUCTOR", False))
	tablaOrdenes.heading("LIQUIDACION", text="LIQUIDACION", command=lambda: treeview_sort_column(tablaOrdenes, "LIQUIDACION", False))

	tablaOrdenes.column("PRODUCTOR", width=150)
	tablaOrdenes.column("LIQUIDACION", width=30)

	tablaOrdenes.bind("<Double-1>", (lambda event: exportarOrden(tablaOrdenes.item(tablaOrdenes.selection()))))
	tablaOrdenes.bind("<Return>", (lambda event: exportarOrden(tablaOrdenes.item(tablaOrdenes.selection()))))

	for i in tablaOrdenes.get_children():
		tablaOrdenes.delete(i)

	con = sql_connection()
	condiciones = " WHERE remate = '" + remate + "'"
	rows = actualizar_db(con, "liquidacionesCompraGuardadas", condiciones)

	for row in rows:
		tablaOrdenes.insert("", tk.END, tags=str(row[0]), text = str(row[0]), iid= str(row[0]), values = (str(row[2]),
		str(row[3])))

	btn_todas = tk.Button(wind_ordenes, text="Exportar todas", command=exportarOrdenesTodas, font=("Helvetica Neue",12, "bold"), backgroun="#b3f2bc")
	btn_todas.place(x = 200, y = 250, width=130, height=40)

	wind_ordenes.mainloop()


#BARRA DE MENU
if(True):
	def pantCompleta():
		dicc_objetos["varFullScreen"] = not dicc_objetos["varFullScreen"]
		window.attributes('-fullscreen', dicc_objetos["varFullScreen"])
	
	def salirWindow():
		window.destroy()

	barraMenu = Menu(window)
	barraMenu.option_add('*tearOff', False)


	mnuRemate = Menu(barraMenu)
	mnuRemate.add_command(label="Remate", command = lambda: ventanaRemates.ventana1("NULL", window))
	mnuRemate.add_command(label="Listado de remates")
	mnuRemate.add_separator()
	mnuRemate.add_command(label="Seleccionar remate", command = lambda: seleccionarRemate())

	mnuCategorias = Menu(barraMenu)
	mnuCategorias.add_command(label="Cat. Venta")
	mnuCategorias.add_command(label="Listado cat. venta")
	mnuCategorias.add_separator()
	mnuCategorias.add_command(label="Cat. Hacienda")
	mnuCategorias.add_command(label="Listado cat. hacienda")

	mnuProductores = Menu(barraMenu)
	mnuProductores.add_command(label="Productor")
	mnuProductores.add_command(label="Listado productores")
	mnuProductores.add_separator()
	mnuProductores.add_command(label="Nuevo productor AUX", command = nuevoProductorAuxiliar)
	mnuProductores.add_command(label="Listar productores AUX")
	mnuProductores.add_command(label="Asignar productores AUX", command = asignarProductoresAuxiliares)
	mnuProductores.add_separator()
	mnuProductores.add_command(label="Productores usados", command = compradorFiltrarUsados)


	mnuLiquidaciones = Menu(barraMenu)
	mnuLiquidaciones.add_command(label="Liq. Compras")
	mnuLiquidaciones.add_command(label="Liq. Ventas")
	mnuLiquidaciones.add_separator()
	mnuLiquidaciones.add_command(label="Configuracion liq. compras")
	mnuLiquidaciones.add_command(label="Configuracion liq. ventas")
	mnuLiquidaciones.add_separator()
	mnuLiquidaciones.add_command(label="Lote")
	mnuLiquidaciones.add_command(label="Listado de lotes")
	mnuLiquidaciones.add_separator()
	mnuLiquidaciones.add_command(label="Alicuotas")
	mnuLiquidaciones.add_separator()
	mnuLiquidaciones.add_command(label="Ordenes de carga", command = ordenesDeCarga)
	mnuLiquidaciones.add_separator()
	mnuLiquidaciones.add_command(label="Exportar .csv compras totales", command=exportarExcelTotales)
	mnuLiquidaciones.add_command(label="Exportar .csv ventas totales", command=exportarExcelTotalesVentas)

	mnuCatalogo = Menu(barraMenu)
	mnuCatalogo.add_command(label="Catalogo")
	mnuCatalogo.add_separator()
	mnuCatalogo.add_command(label="Seleccionar Catalogo", command= lambda: seleccionarCatalogo())
	mnuCatalogo.add_command(label="Cargar todos los lotes", command= lambda: cargarTodosLosLotes())
	mnuCatalogo.add_command(label="Exportar .csv catalogo cargado", command= lambda: exportarExcel())

	mnuConfiguracion = Menu(barraMenu)
	mnuConfiguracion.add_command(label="Administrar Empresa")
	mnuConfiguracion.add_separator()
	mnuConfiguracion.add_command(label="Sincronizacion en la NUBE")
	mnuConfiguracion.add_separator()
	mnuConfiguracion.add_command(label="Copia de seguridad")
	#mnuConfiguracion.add_command(label="RESTAURAR copia de seguridad")
	#mnuConfiguracion.add_separator()
	#mnuConfiguracion.add_command(label="Pantalla detalles", command = pantallaDetalles)
	mnuConfiguracion.add_separator()
	mnuConfiguracion.add_command(label="Pantalla completa", command = pantCompleta)
	mnuConfiguracion.add_command(label="Salir", command = salirWindow)

	barraMenu.add_cascade(label="Remate", menu = mnuRemate)
	barraMenu.add_cascade(label="Categorias", menu = mnuCategorias)
	barraMenu.add_cascade(label="Productores", menu = mnuProductores)
	barraMenu.add_cascade(label="Liquidaciones", menu = mnuLiquidaciones)
	barraMenu.add_cascade(label="Catalogo", menu = mnuCatalogo)
	barraMenu.add_cascade(label="Configuracion", menu = mnuConfiguracion)
	window.config(menu = barraMenu)

	window.bind('<F11>', (lambda event: pantCompleta()))

#BARRA DE HERRAMIENTAS
if(True):
	barraherr = tk.Frame(window, relief=SOLID, bd=2, backgroun="#242b33")
	barraherr.pack(side=TOP, fill=X, pady = 2)

	botBuscar = tk.Button(barraherr, text="AGREGAR NUEVO LOTE", compound="top", backgroun="#b3f2bc", font=("Helvetica", 10, "bold"))
	botImprimir = tk.Button(barraherr, text="EDITAR LOTE", compound="top", backgroun="#f2f0b3", font=("Helvetica", 10, "bold"))
	botAyuda = tk.Button(barraherr, text="EXPORTAR EXCEL", compound="top", backgroun="#f2f0b3", font=("Helvetica", 10, "bold"), command = exportarExcel)
	botCerrar = tk.Button(barraherr, text="bot 5nasd", compound="top", backgroun="#FF6E6E", font=("Helvetica", 10, "bold"))

	padX=3
	padY=2

	botBuscar.pack(side=LEFT, padx=padX, pady=padY)
	botImprimir.pack(side=LEFT, padx=padX, pady=padY)
	botAyuda.pack(side=LEFT, padx=padX, pady=padY)
	botCerrar.pack(side=LEFT, padx=padX, pady=padY)

#BARRA DE TITULO
if(True):
	barraTitulo = tk.Frame(window, relief=SOLID, bd=2, backgroun="#242b33")
	barraTitulo.pack(side=TOP, fill=X)

	textTitulo = StringVar()
	textTitulo.set("REMATE:")
	textID = StringVar()
	textID.set("")

	lbl_titulo = tk.Label(barraTitulo, font=("Helvetica Neue",12,"bold"), anchor="n", backgroun="#242b33", foreground = "#ffffff")
	lbl_titulo.pack()
	lbl_titulo.config(textvariable=textTitulo)

	diccionario_objetos["textTitulo"] = textTitulo
	diccionario_objetos["textID"] = textID

#BODY
if(True):

	lblBody = tk.Label(window, backgroun="#242b33")
	lblBody.pack(side=TOP, fill=BOTH, padx=2, pady=2)
	lblBody.config(width="1", height="100")

	padX=3
	padY=2

	lbl_tabla = Label(lblBody)
	lbl_tabla.place(x=2, y=0, width=1012, height=250)

	lbl_datos = Label(lblBody)
	lbl_datos.place(x=2, y=254, width=1012, height=230)

	#TABLA
	if(True):
		sbr = Scrollbar(lbl_tabla)
		sbr.pack(side=RIGHT, fill="y")


		tabla = ttk.Treeview(lbl_tabla, columns=["CORRAL", "VENDEDOR", "CANTIDAD", "CATEGORIA", "PINTURA", "KGS", "PROMEDIO", "PRECIO", "COMPRADOR", "TOTAL"], selectmode=tk.BROWSE, show='headings') 
		tabla.pack(side=LEFT, fill="both", expand=True)
		sbr.config(command=tabla.yview)
		tabla.config(yscrollcommand=sbr.set)


		tabla.heading("CORRAL", text="CORRAL", command=lambda: treeview_sort_column(tabla, "CORRAL", False))
		tabla.heading("VENDEDOR", text="VENDEDOR", command=lambda: treeview_sort_column(tabla, "VENDEDOR", False))
		tabla.heading("CANTIDAD", text="CANTIDAD", command=lambda: treeview_sort_column(tabla, "CANTIDAD", False))
		tabla.heading("CATEGORIA", text="CATEGORIA", command=lambda: treeview_sort_column(tabla, "CATEGORIA", False))
		tabla.heading("PINTURA", text="PINTURA", command=lambda: treeview_sort_column(tabla, "PINTURA", False))
		tabla.heading("KGS", text="KGS", command=lambda: treeview_sort_column(tabla, "KGS", False))
		tabla.heading("PROMEDIO", text="PROMEDIO", command=lambda: treeview_sort_column(tabla, "PROMEDIO", False))
		tabla.heading("PRECIO", text="PRECIO", command=lambda: treeview_sort_column(tabla, "PRECIO", False))
		tabla.heading("COMPRADOR", text="COMPRADOR", command=lambda: treeview_sort_column(tabla, "COMPRADOR", False))
		tabla.heading("TOTAL", text="TOTAL", command=lambda: treeview_sort_column(tabla, "TOTAL", False))

		tabla.column("CORRAL", width=30)
		tabla.column("VENDEDOR", width=150)
		tabla.column("CANTIDAD", width=30)
		tabla.column("CATEGORIA", width=30)
		tabla.column("PINTURA", width=30)
		tabla.column("KGS", width=30)
		tabla.column("PROMEDIO", width=30)
		tabla.column("PRECIO", width=30)
		tabla.column("COMPRADOR", width=150)
		tabla.column("TOTAL", width=30)

		tabla.bind("<Double-1>", (lambda event: elegirItem(tabla.item(tabla.selection()))))
		tabla.bind("<Return>", (lambda event: elegirItem(tabla.item(tabla.selection()))))

		diccionario_objetos["tabla"] = tabla

	#DATOS
	if(True):
		lblBuscador = tk.Label(lbl_datos, backgroun="#f0f0f0", text="PRODUCTOR", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblBuscador.place(x=2, y=2, width=300, height=226)

		lblLote = tk.Label(lbl_datos, backgroun="#f0f0f0", text="PRODUCTOR", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblLote.place(x=304, y=2, width=300, height=226)

		lblComprador = tk.Label(lbl_datos, backgroun="#f0f0f0", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblComprador.place(x=606, y=25, width=400, height=87)
		lblPrecio = tk.Label(lbl_datos, backgroun="#f0f0f0", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblPrecio.place(x=606, y=137, width=200, height=91)

		tk.Label(lbl_datos, backgroun="#f2f0b3", text="COMPRADOR", font=("Helvetica", 10, "bold"), foreground="#000000", relief=SOLID, bd=2).place(x=606, y=2, width=400, height=25)
		tk.Label(lbl_datos, backgroun="#f2f0b3", text="PRECIO", font=("Helvetica", 10, "bold"), foreground="#000000", relief=SOLID, bd=2).place(x=606, y=114, width=200, height=25)

		#LOTE
		if(True):

			texto_catHacienda = StringVar()
			texto_catHacienda.set("")
			texto_catVenta = StringVar()
			texto_catVenta.set("")

			lbl_catVenta = tk.Label(lblLote, font=("Helvetica Neue",12, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_catVenta.place(x=0, y=0, width=290)
			lbl_catVenta.config(textvariable=texto_catVenta)

			lbl_catHacienda = tk.Label(lblLote, font=("Helvetica Neue",10,"bold"), anchor="w", backgroun="#f0f0f0")
			lbl_catHacienda.place(x=0, y=20, width=290)
			lbl_catHacienda.config(textvariable=texto_catHacienda)

			tk.Label(lblLote, text="Corral", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=0, y=50, width=75, height=13)
			tk.Label(lblLote, text="Cantidad", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=75, y=50, width=75, height=13)
			tk.Label(lblLote, text="Peso Neto", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=150, y=50, width=75, height=13)
			tk.Label(lblLote, text="Peso Prom", font=("Helvetica Neue",8), anchor="c", backgroun="#9bd1c1").place(x=225, y=50, width=71, height=13)


			texto_corral = StringVar()
			texto_corral.set("")
			texto_cantidad = StringVar()
			texto_cantidad.set("")
			texto_neto = StringVar()
			texto_neto.set("")
			texto_promedio = StringVar()
			texto_promedio.set("")


			lbl_corral = tk.Label(lblLote, font=("Helvetica Neue",15,"bold"), anchor="c", backgroun="#f0f0f0")
			lbl_corral.place(x=0, y=67, width=75)
			lbl_corral.config(textvariable=texto_corral)

			lbl_cantidad = tk.Label(lblLote, font=("Helvetica Neue",15,"bold"), anchor="c", backgroun="#f0f0f0")
			lbl_cantidad.place(x=75, y=67, width=75)
			lbl_cantidad.config(textvariable=texto_cantidad)

			lbl_neto = tk.Label(lblLote, font=("Helvetica Neue",15,"bold"), anchor="c", backgroun="#f0f0f0")
			lbl_neto.place(x=150, y=67, width=75)
			lbl_neto.config(textvariable=texto_neto)

			lbl_promedio = tk.Label(lblLote, font=("Helvetica Neue",15,"bold"), anchor="c", backgroun="#f0f0f0")
			lbl_promedio.place(x=225, y=67, width=71)
			lbl_promedio.config(textvariable=texto_promedio)

			txt_observaciones = scrolledtext.ScrolledText(lblLote, backgroun="#edfffa")
			txt_observaciones.place(x = 0, y = 120, width = 225+71, height = 100)
			txt_observaciones.insert("1.0", "Para comezar a cargar: \n1) Seleccione un remate\n2) Seleccione un catalogo\n3) Doble click sobre el lote\n4) Buscar comprador\n5) Colocar precio por kilo\n6) Guardar")
			txt_observaciones.config(state="disabled")

			def editarLote():
				id_lote = diccionario_objetos["id_lote"]
				ventanaIngreso2.ventana1(id_lote, "NULL", "NULL", window)

			btn_editarLote = tk.Button(lblLote, text="Editar", compound="top", backgroun="#dbdbdb", font=("Helvetica", 10, "bold"), command=editarLote, state="disabled")
			btn_editarLote.place(x=230, y=5, width=60, height=18)

			diccionario_objetos["datosLote_texto_catHacienda"] = texto_catHacienda
			diccionario_objetos["datosLote_texto_catVenta"] = texto_catVenta
			diccionario_objetos["datosLote_texto_corral"] = texto_corral
			diccionario_objetos["datosLote_texto_cantidad"] = texto_cantidad
			diccionario_objetos["datosLote_texto_neto"] = texto_neto
			diccionario_objetos["datosLote_texto_promedio"] = texto_promedio
			diccionario_objetos["datosLote_txt_observaciones"] = txt_observaciones
			diccionario_objetos["btn_editarLote"] = btn_editarLote

		#COMPRADOR
		if(True):
			texto_alias = StringVar()
			texto_alias.set("")
			texto_razon = StringVar()
			texto_razon.set("")
			texto_cuit = StringVar()
			texto_cuit.set("")

			lbl_alias = tk.Label(lblComprador, font=("Helvetica Neue", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_alias.place(x=2, y=2, width=250)
			lbl_alias.config(textvariable=texto_alias)

			lbl_razon = tk.Label(lblComprador, font=("Helvetica Neue", 10), anchor="w", backgroun="#f0f0f0")
			lbl_razon.place(x=2, y=25, width=250)
			lbl_razon.config(textvariable=texto_razon)

			lbl_cuit = tk.Label(lblComprador, font=("verdana", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_cuit.place(x=43, y=55, width=150)
			lbl_cuit.config(textvariable=texto_cuit)

			Label(lblComprador, font=("verdana",10), text="CUIT:", backgroun="#f0f0f0").place(x=0, y=55)

			Label(lblComprador, font=("verdana",8), text="KGs:", backgroun="#f0f0f0").place(x=273, y=0)
			Label(lblComprador, font=("verdana",8), text="$ total:", backgroun="#f0f0f0").place(x=260, y=20)
			Label(lblComprador, font=("verdana",8), text="Cabezas:", backgroun="#f0f0f0").place(x=247, y=40)

			texto_kgs = StringVar()
			texto_kgs.set("")
			texto_total = StringVar()
			texto_total.set("")
			texto_cabezas = StringVar()
			texto_cabezas.set("")

			lbl_kgs = tk.Label(lblComprador, font=("Helvetica Neue", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_kgs.place(x=305, y=-2, width=90)
			lbl_kgs.config(textvariable=texto_kgs)

			lbl_total = tk.Label(lblComprador, font=("Helvetica Neue", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_total.place(x=305, y=18, width=90)
			lbl_total.config(textvariable=texto_total)

			lbl_cabezas = tk.Label(lblComprador, font=("Helvetica Neue", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_cabezas.place(x=305, y=38, width=90)
			lbl_cabezas.config(textvariable=texto_cabezas)

			btn_productorAuxiliar = tk.Button(lblComprador, text="Nuevo productor auxiliar", compound="top", backgroun="#dbdbdb", font=("Helvetica", 10, "bold"), command=nuevoProductorAuxiliar, state="disabled")
			btn_productorAuxiliar.place(x=213, y=62, width=180, height=18)

			diccionario_objetos["texto_alias"] = texto_alias
			diccionario_objetos["texto_razon"] = texto_razon
			diccionario_objetos["texto_cuit"] = texto_cuit
			diccionario_objetos["texto_kgs"] = texto_kgs
			diccionario_objetos["texto_total"] = texto_total
			diccionario_objetos["texto_cabezas"] = texto_cabezas
			diccionario_objetos["btn_productorAuxiliar"] = btn_productorAuxiliar

		#BOTONES
		if(True):
			btn_guardar = tk.Button(lbl_datos, text="GUARDAR", compound="top", backgroun="#b3f2bc", font=("Helvetica", 20, "bold"), state = "disabled", command=guardarCompraventa)
			btn_guardar.place(x=810, y=114, width=196, height=60)

			btn_eliminar = tk.Button(lbl_datos, text="ELIMINAR", compound="top", backgroun="#FF6E6E", font=("Helvetica", 15, "bold"), state = "disabled", command=eliminarCompraventa)
			btn_eliminar.place(x=810, y=180, width=196, height=48)

			diccionario_objetos["btn_guardar"] = btn_guardar
			diccionario_objetos["btn_eliminar"] = btn_eliminar

		#PRECIO
		if(True):
			Label(lblPrecio, font=("verdana",18, "bold"), text="$/kg", backgroun="#f0f0f0").grid(column=0, row=0, padx = 5, pady = 20)
			entry_precio = tk.Entry(lblPrecio, font=("verdana",18, "bold"), backgroun="#f0f0f0", width=6)
			entry_precio.grid(column=1, row=0, padx = 5, pady = 20)

			diccionario_objetos["entry_precio"] = entry_precio

	#BUSCADOR PRODUCTORES
	if(True):
		lbl_comprador_aux = Label(lblBuscador, backgroun="#f0f0f0")
		lbl_comprador_aux.place(x = 3, y = 0, width = 290, height = 222)

		lbl_ventana_productor_buscador_entry = tk.LabelFrame(lbl_comprador_aux, text="Filtrar", backgroun="#f0f0f0")
		lbl_ventana_productor_buscador_tabla = tk.LabelFrame(lbl_comprador_aux, text="Productores", backgroun="#f0f0f0")

		lbl_ventana_productor_buscador_entry.grid(column = 0, row = 0)
		lbl_ventana_productor_buscador_tabla.grid(column = 0, row = 1)

		#--
		entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="31")
		entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = 5)

		btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar", command= lambda: compradorFiltrar())
		btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 0)

		sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
		sbr_productor.pack(side=RIGHT, fill="y")

		tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("alias", "cuit"), selectmode=tk.BROWSE, height=6, show='headings') 
		tabla_productor.pack(side=LEFT, fill="both", expand=True)
		sbr_productor.config(command=tabla_productor.yview)
		tabla_productor.config(yscrollcommand=sbr_productor.set)

		tabla_productor.heading("alias", text="ALIAS")
		tabla_productor.heading("cuit", text="CUIT/DNI")

		tabla_productor.column("alias", width=150)
		tabla_productor.column("cuit", width=100)

		diccionario_objetos["entry_comprador"] = entry_filtrar_productor
		diccionario_objetos["tabla_compradores"] = tabla_productor

		entry_filtrar_productor.bind("<Return>", (lambda event: compradorFiltrar()))
		tabla_productor.bind('<Double-1>', (lambda event: seleccionarTablaComprador()))
		tabla_productor.bind('<Return>', (lambda event: seleccionarTablaComprador()))
		btn_produc_filtrar.bind("<Button-3>", (lambda event: compradorFiltrarUsados()))

diccionario_objetos["textID"].set(1)



window.bind("<Control-s>", (lambda event: window.destroy()))
window.mainloop()

