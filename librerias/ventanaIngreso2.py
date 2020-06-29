#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

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

from PIL import Image,ImageTk

diccionarioObjetos = {}
direccionBaseDeDatos = 'database/iltanohacienda.db'
#direccionBaseDeDatos = r"\\192.168.50.120\proyecto\iltano db\iltanohacienda.db"

diccionarioObjetos["REMATE_CORRECTO"] = False
diccionarioObjetos["PRODUCTOR_CORRECTO"] = False
diccionarioObjetos["BUSCAR"] = "remate"

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

def ayuda():
	messagebox.showinfo("Atencion", "Ayuda no disponible")
	pass
def buscar():
	if(diccionarioObjetos["BUSCAR"]=="remate"):
		buscarRemate()
	else:
		buscarProductor()
def buscarRemate():
	diccionarioObjetos["REMATE_CORRECTO"] = False
	diccionarioObjetos["texto_fecha"].set("")
	def funcsalirr(ssss):
		con = sql_connection()
		condiciones = " WHERE id = " + str(ssss)
		rows = actualizar_db(con, "remate", condiciones)
		diccionarioObjetos["entry_remate"].delete(0, tk.END)
		diccionarioObjetos["entry_remate"].insert(0, rows[0][1])
		verificarRemate()

	dicc_buscar = {"seleccionar" : "remate",
	"columnas" : {"0":{"id" : "nombre", "cabeza" : "Remate", "ancho" : 180, "row" : 1}, "1":{"id" : "fecha", "cabeza" : "Fecha", "ancho" : 60, "row" : 2}, "2":{"id" : "tipo", "cabeza" : "Tipo", "ancho" : 70, "row" : 3}},
	"db" : direccionBaseDeDatos,
	"tabla" : "remate",
	"condiciones" : ' WHERE (nombre LIKE  "%' + str(diccionarioObjetos["entry_remate"].get()) + '%" OR fecha LIKE "%' + str(diccionarioObjetos["entry_remate"].get()) + '%" OR tipo LIKE "%' + str(diccionarioObjetos["entry_remate"].get()) + '%") AND estado = "activo"',
	"dimensionesVentana" : "336x400"}
	tablaElegir.tabla_elegir(dicc_buscar, funcsalirr)
def buscarProductor():
	diccionarioObjetos["PRODUCTOR_CORRECTO"] = False
	diccionarioObjetos["texto_cuit"].set("")
	def funcsalirr(ssss):

		con = sql_connection()
		condiciones = " WHERE id = " + str(ssss)
		rows = actualizar_db(con, "productores", condiciones)

		diccionarioObjetos["entry_vendedor"].delete(0, tk.END)
		diccionarioObjetos["entry_vendedor"].insert(0, rows[0][1])

		verificarVendedor()

	dicc_buscar = {"seleccionar" : "productor",
	"columnas" : {"0":{"id" : "alias", "cabeza" : "Alias", "ancho" : 180, "row" : 1}, "1":{"id" : "razon", "cabeza" : "Razon Social", "ancho" : 180, "row" : 2}, "2":{"id" : "cuit", "cabeza" : "CUIT", "ancho" : 110, "row" : 3}},
	"db" : direccionBaseDeDatos,
	"tabla" : "productores",
	"condiciones" : ' WHERE (nombre LIKE  "%' + str(diccionarioObjetos["entry_vendedor"].get()) + '%" OR razon LIKE "%' + str(diccionarioObjetos["entry_vendedor"].get()) + '%" OR ndoc LIKE "%' + str(diccionarioObjetos["entry_vendedor"].get()) + '%") AND estado = "activo"',
	"dimensionesVentana" : "500x400"}
	tablaElegir.tabla_elegir(dicc_buscar, funcsalirr)
def buscarDte():
	diccionarioObjetos["PRODUCTOR_CORRECTO"] = False
	diccionarioObjetos["texto_cuit"].set("")
	def funcsalirrdte(ssss):

		con = sql_connection()
		condiciones = " WHERE id = " + str(ssss)
		rows = actualizar_db(con, "dte", condiciones)

		diccionarioObjetos["entry_dte"].delete(0, tk.END)
		diccionarioObjetos["entry_dte"].insert(0, rows[0][3])


	dicc_buscar = {"seleccionar" : "DTE usados",
	"columnas" : {"0":{"id" : "Productor", "cabeza" : "PRODUCTOR", "ancho" : 180, "row" : 1}, "1":{"id" : "remate", "cabeza" : "REMATE", "ancho" : 180, "row" : 2}, "2":{"id" : "dte", "cabeza" : "DTE", "ancho" : 110, "row" : 3}},
	"db" : direccionBaseDeDatos,
	"tabla" : "dte",
	"condiciones" : ' WHERE productor = "' + str(diccionarioObjetos["entry_vendedor"].get()) + '" AND remate = "' + str(diccionarioObjetos["entry_remate"].get()) + '"',
	"dimensionesVentana" : "500x400"}
	tablaElegir.tabla_elegir(dicc_buscar, funcsalirrdte)


def verificarLote():
	idLote = diccionarioObjetos["idLote"]

	con = sql_connection()
	condiciones = " WHERE id = '" + str(idLote) + "'"
	rows = actualizar_db(con, "lotes", condiciones)

	if len(rows) > 0:
		borrarCampos()
		activarCampos()
		cargarDatosLote(rows[0])
		botonesEditar()
	else:
		messagebox.showerror("ERROR", "Error al buscar LOTE")
def verificarRemate():
	idRemate = diccionarioObjetos["entry_remate"].get()

	con = sql_connection()
	condiciones = " WHERE nombre = '" + str(idRemate) + "'"
	rows = actualizar_db(con, "remate", condiciones)

	if len(rows) > 0:
		diccionarioObjetos["REMATE_CORRECTO"] = True
		diccionarioObjetos["texto_fecha"].set("Fecha: " + str(rows[0][2]))
		diccionarioObjetos["entry_vendedor"].focus()
		diccionarioObjetos["BUSCAR"] = "productor"
	else:
		diccionarioObjetos["REMATE_CORRECTO"] = False
		diccionarioObjetos["texto_fecha"].set("ERROR: Error al buscar REMATE")
		messagebox.showerror("ERROR", "Error al buscar REMATE")

	verificarActivar()
def verificarVendedor():
	idVendedor = diccionarioObjetos["entry_vendedor"].get()

	con = sql_connection()
	condiciones = " WHERE nombre = '" + str(idVendedor) + "' AND estado='activo'"
	rows_productor = actualizar_db(con, "productores", condiciones)

	con = sql_connection()
	condiciones = " WHERE productor = '" + idVendedor + "' AND remate = '" + str(diccionarioObjetos["entry_remate"].get()) + "'"
	rows_pintura = actualizar_db(con, "pintura", condiciones)
	if len(rows_pintura) == 1:
		pintura = rows_pintura[0][2]
	else:
		pintura = "S/P"
	diccionarioObjetos["PINTURA"] = pintura

	if len(rows_productor) > 0:
		diccionarioObjetos["PRODUCTOR_CORRECTO"] = True
		diccionarioObjetos["texto_cuit"].set("PINTURA: " + pintura + "  |  obs: " + str(rows_productor[0][13]))

	else:
		diccionarioObjetos["PRODUCTOR_CORRECTO"] = False
		diccionarioObjetos["texto_cuit"].set("ERROR: Error al buscar PRODUCTOR")
		messagebox.showerror("ERROR", "Error al buscar PRODUCTOR")

	verificarActivar()

def verificarActivar():
	if ((diccionarioObjetos["REMATE_CORRECTO"] == True) and (diccionarioObjetos["PRODUCTOR_CORRECTO"] == True)):
		if(diccionarioObjetos["idLote"]==""):
			activarCampos()
			botonesNuevo()
		else:
			activarCampos()
			botonesEditar()
	else:
		desactivarCampos()
		botonesInicio()
def activarCampos():
	diccionarioObjetos["entry_remate"].config(state="normal")
	diccionarioObjetos["entry_vendedor"].config(state="normal")
	diccionarioObjetos["entry_corral"].config(state="normal")
	diccionarioObjetos["entry_cantidad"].config(state="normal")
	diccionarioObjetos["combo_catVenta"].config(state="normal")
	diccionarioObjetos["combo_catHacienda"].config(state="normal")
	diccionarioObjetos["entry_brutoTropa"].config(state="normal")
	diccionarioObjetos["entry_desbastePorcentaje"].config(state="normal")
	diccionarioObjetos["entry_netoTropa"].config(state="normal")
	diccionarioObjetos["entry_netoPromedio"].config(state="normal")
	diccionarioObjetos["entry_observaciones"].config(state="normal")
	diccionarioObjetos["txt_observaciones"].config(state="normal")
	diccionarioObjetos["entry_dte"].config(state="normal")
def desactivarCampos():

	diccionarioObjetos["entry_corral"].config(state="disabled")
	diccionarioObjetos["entry_cantidad"].config(state="disabled")
	diccionarioObjetos["combo_catVenta"].config(state="disabled")
	diccionarioObjetos["combo_catHacienda"].config(state="disabled")
	diccionarioObjetos["entry_brutoTropa"].config(state="disabled")
	diccionarioObjetos["entry_desbastePorcentaje"].config(state="disabled")
	diccionarioObjetos["entry_netoTropa"].config(state="disabled")
	diccionarioObjetos["entry_netoPromedio"].config(state="disabled")
	diccionarioObjetos["entry_observaciones"].config(state="disabled")
	diccionarioObjetos["txt_observaciones"].config(state="disabled")
	diccionarioObjetos["entry_dte"].config(state="disabled")

def borrarCampos():

	diccionarioObjetos["entry_corral"].delete(0, tk.END)
	diccionarioObjetos["entry_cantidad"].delete(0, tk.END)
	diccionarioObjetos["entry_brutoTropa"].delete(0, tk.END)
	diccionarioObjetos["entry_desbastePorcentaje"].delete(0, tk.END)
	diccionarioObjetos["entry_netoTropa"].delete(0, tk.END)
	diccionarioObjetos["entry_netoPromedio"].delete(0, tk.END)
	diccionarioObjetos["entry_observaciones"].delete(0, tk.END)
	diccionarioObjetos["txt_observaciones"].delete("1.0", tk.END)

	diccionarioObjetos["entry_desbastePorcentaje"].insert(0, 0.0)

def cargarDatosLote(row):

	idd = str(row[0])
	remate = str(row[1])
	productor = str(row[2])
	cantidad = str(row[3])
	corral = str(row[4])
	catVenta = str(row[5])
	catHacienda = str(row[6])
	pintura = str(row[7])
	kgBruto = str(row[8])
	kgProm = str(row[9])
	desbastePorcentaje = str(row[10])
	desbasteKg = str(row[11])
	neto = str(row[12])
	netoPromedio = str(row[13])
	observaciones = str(row[14])
	observacionesDescripcion = str(row[15])
	dte = str(row[16])
	flete = str(row[17])
	estado = str(row[18])

	diccionarioObjetos["textTitulo"].set("LOTE " + idd)

	diccionarioObjetos["combo_catVenta"].set(catVenta)
	diccionarioObjetos["combo_catHacienda"].set(catHacienda)

	diccionarioObjetos["entry_remate"].insert(0, remate)
	diccionarioObjetos["entry_vendedor"].insert(0, productor)
	diccionarioObjetos["entry_corral"].insert(0, corral)
	diccionarioObjetos["entry_cantidad"].insert(0, cantidad)
	diccionarioObjetos["entry_brutoTropa"].insert(0, kgBruto)
	diccionarioObjetos["entry_desbastePorcentaje"].insert(0, desbastePorcentaje)
	diccionarioObjetos["entry_netoTropa"].insert(0, neto)
	diccionarioObjetos["entry_netoPromedio"].insert(0, netoPromedio)
	diccionarioObjetos["entry_observaciones"].insert(0, observaciones)
	diccionarioObjetos["txt_observaciones"].insert("1.0", observacionesDescripcion)
	diccionarioObjetos["entry_dte"].insert(0, dte)

	#consultas
	con = sql_connection()
	condiciones = " WHERE productor = '" + productor + "' AND remate = '" + remate + "'"
	rows_pintura = actualizar_db(con, "pintura", condiciones)

	con = sql_connection()
	condiciones = " WHERE nombre = '" + productor + "' AND estado = 'activo'"
	rows_productor = actualizar_db(con, "productores", condiciones)

	con = sql_connection()
	condiciones = " WHERE nombre = '" + remate + "' AND estado = 'activo'"
	rows_remate = actualizar_db(con, "remate", condiciones)


	#setear
	if len(rows_pintura) == 1:
		pintura = rows_pintura[0][2]
	else:
		pintura = "S/P"
	diccionarioObjetos["PINTURA"] = pintura


	if len(rows_productor) == 1:
		diccionarioObjetos["texto_cuit"].set("PINTURA: " + pintura + "  |  obs: " + str(rows_productor[0][13]))
		diccionarioObjetos["PRODUCTOR_CORRECTO"] = True
	else:
		diccionarioObjetos["PRODUCTOR_CORRECTO"] = False
		diccionarioObjetos["texto_cuit"].set("ERROR, PRODUCTOR NO EXISTE")


	if len(rows_remate) == 1:
		diccionarioObjetos["texto_fecha"].set("Fecha: " + str(rows_remate[0][2]))
		diccionarioObjetos["REMATE_CORRECTO"] = True
	else:
		diccionarioObjetos["REMATE_CORRECTO"] = False
		diccionarioObjetos["texto_fecha"].set("ERROR, REMATE NO EXISTE")


def guardar():
	try:
		x_remate = diccionarioObjetos["entry_remate"].get()
		x_productor = diccionarioObjetos["entry_vendedor"].get()
		x_cantidad = diccionarioObjetos["entry_cantidad"].get()
		x_corral = diccionarioObjetos["entry_corral"].get()
		x_catVenta = diccionarioObjetos["combo_catVenta"].get()
		x_catHacienda = diccionarioObjetos["combo_catHacienda"].get()
		x_pintura = diccionarioObjetos["PINTURA"]
		x_kgBruto = diccionarioObjetos["entry_brutoTropa"].get()
		x_kgProm = ""
		x_desbastePorcentaje = diccionarioObjetos["entry_desbastePorcentaje"].get()
		x_desbasteKg = ""
		x_neto = diccionarioObjetos["entry_netoTropa"].get()
		x_netoPromedio = diccionarioObjetos["entry_netoPromedio"].get()
		x_observaciones = diccionarioObjetos["entry_observaciones"].get()
		x_observacionesDescripcion = diccionarioObjetos["txt_observaciones"].get("1.0", tk.END)
		x_dte = diccionarioObjetos["entry_dte"].get()
		x_flete = ""
		x_estado = "activo"

		entities = [str(x_remate),
		str(x_productor),
		str(x_cantidad),
		str(x_corral),
		str(x_catVenta),
		str(x_catHacienda),
		str(x_pintura),
		str(x_kgBruto),
		str(x_kgProm),
		str(x_desbastePorcentaje),
		str(x_desbasteKg),
		str(x_neto),
		str(x_netoPromedio),
		str(x_observaciones),
		str(x_observacionesDescripcion),
		str(x_dte),
		str(x_flete),
		str(x_estado)]

	except:
		messagebox.showerror("ERROR", "No se pudo obtener los datos")
		return 0

	try:
		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO lotes VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
		con.commit()
		escape()
	except:
		messagebox.showerror("ERROR", "No se pudo Guardar")
		return 0

	#GUARDAR DTE USADO
	try:
		#verificar si existe
		con = sql_connection()
		condiciones = " WHERE productor = '" + str(x_productor) + "' AND remate = '" + str(x_remate) + "' AND dte = '" + str(x_dte) + "'"
		rows = actualizar_db(con, "dte", condiciones)

		if len(rows) == 0:
			entities = [str(x_productor), str(x_remate), str(x_dte)]
			try:
				con = sql_connection()
				cursorObj = con.cursor()
				cursorObj.execute("INSERT INTO dte VALUES(NULL, ?, ?, ?)", entities)
				con.commit()
			except:
				messagebox.showerror("ERROR", "No se pudo Guardar el DTE")
				return 0
	except:
		pass


def editar():
	try:
		x_id = diccionarioObjetos["idLote"]
		x_remate = diccionarioObjetos["entry_remate"].get()
		x_productor = diccionarioObjetos["entry_vendedor"].get()
		x_cantidad = diccionarioObjetos["entry_cantidad"].get()
		x_corral = diccionarioObjetos["entry_corral"].get()
		x_catVenta = diccionarioObjetos["combo_catVenta"].get()
		x_catHacienda = diccionarioObjetos["combo_catHacienda"].get()
		x_pintura = diccionarioObjetos["PINTURA"]
		x_kgBruto = diccionarioObjetos["entry_brutoTropa"].get()
		x_kgProm = ""
		x_desbastePorcentaje = diccionarioObjetos["entry_desbastePorcentaje"].get()
		x_desbasteKg = ""
		x_neto = diccionarioObjetos["entry_netoTropa"].get()
		x_netoPromedio = diccionarioObjetos["entry_netoPromedio"].get()
		x_observaciones = diccionarioObjetos["entry_observaciones"].get()
		x_observacionesDescripcion = diccionarioObjetos["txt_observaciones"].get("1.0", tk.END)
		x_dte = diccionarioObjetos["entry_dte"].get()
		x_flete = ""
		x_estado = "activo"

		entities = [str(x_remate),
		str(x_productor),
		str(x_cantidad),
		str(x_corral),
		str(x_catVenta),
		str(x_catHacienda),
		str(x_pintura),
		str(x_kgBruto),
		str(x_kgProm),
		str(x_desbastePorcentaje),
		str(x_desbasteKg),
		str(x_neto),
		str(x_netoPromedio),
		str(x_observaciones),
		str(x_observacionesDescripcion),
		str(x_dte),
		str(x_flete),
		str(x_estado),
		str(x_id)]

	except:
		messagebox.showerror("ERROR", "No se pudo obtener los datos")
		return 0

	try:
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea editar?\nID DB: ' + str(x_id), icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE lotes SET remate = ?, productor = ?, cantidad = ?, corral = ?, catVenta = ?, catHacienda = ?, pintura = ?, kgBruto = ?, kgProm = ?, desbastePorcentaje = ?, desbasteKg = ?, neto = ?, netoPromedio = ?, observaciones = ?, observacionesDescripcion = ?, dte = ?, flete = ?, estado = ? where id = ?', entities)
			con.commit()
			messagebox.showinfo("Editado", "EDITADO con Éxito")
			escape()
	except:
		messagebox.showerror("ERROR", "No se pudo editar")
def borrar():
	try:
		x_id = diccionarioObjetos["idLote"]

		if(x_id==""):
			messagebox.showerror("ERROR", "Lote no seleccionado")
			return 0

		MsgBox = messagebox.askquestion('ATENCION', '¿Desea BORRAR?\nID DB: ' + str(x_id), icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE lotes SET estado = "borrado" where id = ' + str(x_id))
			con.commit()
			messagebox.showinfo("Borrado", "Borrado con Éxito")
			escape()
	except:
		messagebox.showerror("ERROR", "No se pudo borrar")

def botonesEditar():
	diccionarioObjetos["botGuardar"]["state"] = "disabled"
	diccionarioObjetos["botBorrar"]["state"] = "normal"
	diccionarioObjetos["botEditar"]["state"] = "normal"
	diccionarioObjetos["botBuscar"]["state"] = "normal"
def botonesNuevo():
	diccionarioObjetos["botGuardar"]["state"] = "normal"
	diccionarioObjetos["botBorrar"]["state"] = "disabled"
	diccionarioObjetos["botEditar"]["state"] = "disabled"
	diccionarioObjetos["botBuscar"]["state"] = "normal"
def botonesInicio():
	diccionarioObjetos["botGuardar"]["state"] = "disabled"
	diccionarioObjetos["botBorrar"]["state"] = "disabled"
	diccionarioObjetos["botEditar"]["state"] = "disabled"
	diccionarioObjetos["botBuscar"]["state"] = "normal"

def escape():
	diccionarioObjetos["idLote"]=""
	borrarCampos()
	#desactivarCampos()
	botonesInicio()

def obtenerCatVenta():
	lista = []
	con = sql_connection()
	condiciones = " WHERE estado = 'activo'"
	rows = actualizar_db(con, "catVenta", condiciones)

	for row in rows:
		lista.append(row[2])

	return lista
def obtenerCatHacienda():
	lista = []
	con = sql_connection()
	condiciones = " WHERE estado = 'activo'"
	rows = actualizar_db(con, "catHacienda", condiciones)

	for row in rows:
		lista.append(row[2])

	return lista

def foco(entry):
	entry.focus()

#CALCULOS
def calc_brutoTropa():
	try:
		entrada = float(diccionarioObjetos["entry_brutoTropa"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener bruto")
		return 0

	try:
		desbastePorcentaje = float(diccionarioObjetos["entry_desbastePorcentaje"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener desbaste")
		return 0

	try:
		kgNeto = round(entrada - entrada * (desbastePorcentaje/100))
		diccionarioObjetos["entry_netoTropa"].delete(0, tk.END)
		diccionarioObjetos["entry_desbastePorcentaje"].focus()
		diccionarioObjetos["entry_netoTropa"].insert(0, kgNeto)

		calc_promedio()

	except:
		messagebox.showerror("ERROR", "Error de cálculo, verifique los datos")
def calc_desbastePorcentaje():
	try:
		entrada_neto = float(diccionarioObjetos["entry_brutoTropa"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener neto")
		return 0

	try:
		desbastePorcentaje = float(diccionarioObjetos["entry_desbastePorcentaje"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener desbaste")
		return 0

	try:
		kgNeto = round(entrada_neto - entrada_neto * (desbastePorcentaje/100))
		diccionarioObjetos["entry_netoTropa"].delete(0, tk.END)
		diccionarioObjetos["entry_netoTropa"].focus()
		diccionarioObjetos["entry_netoTropa"].insert(0, kgNeto)

		calc_promedio()

	except:
		messagebox.showerror("ERROR", "Error de cálculo, verifique los datos")
def calc_promedio():
	try:
		entrada_neto = float(diccionarioObjetos["entry_netoTropa"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener neto")
		return 0

	try:
		cantidad = float(diccionarioObjetos["entry_cantidad"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener cantidad de animales")
		return 0

	try:
		kgPromedio = round(entrada_neto/cantidad)
		diccionarioObjetos["entry_netoPromedio"].delete(0, tk.END)
		diccionarioObjetos["entry_netoPromedio"].insert(0, kgPromedio)

	except:
		messagebox.showerror("ERROR", "Error de cálculo, verifique los datos")

def bodyLote(window):
	"""
	id
	remate
	productor
	cantidad
	corral
	catVenta
	catHacienda
	pintura
	kgBruto
	kgProm
	desbastePorcentaje
	desbasteKg
	neto
	netoPromedio
	observaciones
	observacionesDescripcion
	dte
	flete
	estado
	"""
	lbl_datosPrincipales = tk.Label(window, backgroun="#BAE7FF")
	lbl_datosPrincipales.place(x=0, y=0, width=692, height=110)

	lbl_datosLotes = tk.Label(window, backgroun="#BAE7FF")
	lbl_datosLotes.place(x=0, y=115, width=692, height=295)

	#LABEL DATOS PRINCIPALES
	if(True):
		lbl_remate = tk.Label(lbl_datosPrincipales, backgroun="#E6F5FF")
		lbl_vendedor = tk.Label(lbl_datosPrincipales, backgroun="#E6F5FF")

		lbl_remate.place(x = 10, y = 10, width = 672, height = 40)
		lbl_vendedor.place(x = 10, y = 55, width = 672, height = 40)

		#REMATE
		if(True):
			tk.Label(lbl_remate, text = "Remate", font=("Helvetica Neue",10), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 0, padx=5, pady=5)
			entry_remate = Entry(lbl_remate, width="32")
			entry_remate.grid(sticky = "e", column = 1, row = 0, padx=5, pady=5)
			entry_remate.focus()

			texto_fecha = StringVar()
			texto_fecha.set("")

			lbl_fecha = tk.Label(lbl_remate, font=("Helvetica Neue",10,"bold"), backgroun="#E6F5FF", width=45, anchor="w")
			lbl_fecha.grid(sticky = "e", column = 2, row = 0, padx=20, pady=5)
			lbl_fecha.config(textvariable=texto_fecha)

			diccionarioObjetos["entry_remate"] = entry_remate
			diccionarioObjetos["texto_fecha"] = texto_fecha

		#VENDEDOR
		if(True):
			def asdd():
				print("sep")
			tk.Label(lbl_vendedor, text = "Vendedor", font=("Helvetica Neue",10), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 0, padx=5, pady=5)
			entry_vendedor = Entry(lbl_vendedor, width="30")
			entry_vendedor.grid(sticky = "e", column = 1, row = 0, padx=5, pady=5)

			texto_cuit = StringVar()
			texto_cuit.set("")

			lbl_cuit = tk.Label(lbl_vendedor, font=("Helvetica Neue",10,"bold"), backgroun="#E6F5FF", width=45, anchor="w")
			lbl_cuit.grid(sticky = "e", column = 2, row = 0, padx=20, pady=5)
			lbl_cuit.config(textvariable=texto_cuit)

			diccionarioObjetos["entry_vendedor"] = entry_vendedor
			diccionarioObjetos["texto_cuit"] = texto_cuit
		
		entry_remate.bind("<Return>", (lambda event: buscarRemate()))
		entry_vendedor.bind("<Return>", (lambda event: buscarProductor()))

		entry_remate.bind("<F5>", (lambda event: buscarRemate()))
		entry_vendedor.bind("<F5>", (lambda event: buscarProductor()))

		def setearRemate():
			diccionarioObjetos["BUSCAR"] = "remate"
			diccionarioObjetos["botBuscar"]["state"] = "normal"
		def setearProductor():
			diccionarioObjetos["BUSCAR"] = "productor"
			diccionarioObjetos["botBuscar"]["state"] = "normal"

		entry_remate.bind("<Button-1>", (lambda event: setearRemate()))
		entry_vendedor.bind("<Button-1>", (lambda event: setearProductor()))

	#LABEL DATOS LOTES
	if(True):
		pestañas = ttk.Notebook(lbl_datosLotes)

		label_hacienda = Label(lbl_datosLotes, backgroun="#E8F6FA")
		label_observaciones = Label(lbl_datosLotes, backgroun="#E8F6FA")
		label_dte = Label(lbl_datosLotes, backgroun="#E8F6FA")
		label_flete = Label(lbl_datosLotes, backgroun="#E8F6FA")

		pestañas.add(label_hacienda, text="Hacienda", padding = 10)
		pestañas.add(label_observaciones, text="Observaciones", padding = 10)
		pestañas.add(label_dte, text="DTE", padding = 10)
		pestañas.add(label_flete, text="Flete", padding = 10)

		#pestañas.place(x = 0, y = 0, width = 700, height = 400)
		pestañas.place(relwidth = 1, relheight=1)

		#PESTAÑA HACIENDA
		if(True):
			tk.Label(label_hacienda, font=("verdana",14), text="CORRAL:", anchor="e", bg='#E8F6FA').place(x=20, y=10, width = 300, height = 20)	
			tk.Label(label_hacienda, font=("verdana",14), text="CANTIDAD:", anchor="e", bg='#E8F6FA').place(x=20, y=40, width = 300, height = 20)	
			tk.Label(label_hacienda, font=("verdana",14), text="CATEGORIA DE VENTA:", anchor="e", bg='#E8F6FA').place(x=20, y=70, width = 300, height = 20)	
			tk.Label(label_hacienda, font=("verdana",14), text="CATEGORIA DE HACIENDA:", anchor="e", bg='#E8F6FA').place(x=20, y=100, width = 300, height = 20)	

			modificar_altura = 0

			diccionarioObjetos["entry_corral"] = Entry(label_hacienda, font=("verdana",12, "bold"))
			diccionarioObjetos["entry_cantidad"] = Entry(label_hacienda, font=("verdana",12, "bold"))
			diccionarioObjetos["combo_catVenta"] = Combobox(label_hacienda, state="readonly", font=("verdana",12))
			diccionarioObjetos["combo_catHacienda"] = Combobox(label_hacienda, state="readonly", font=("verdana",12))

			diccionarioObjetos["entry_corral"].place(x=330, y=10+modificar_altura, width = 150)
			diccionarioObjetos["entry_cantidad"].place(x=330, y=40+modificar_altura, width = 150)
			diccionarioObjetos["combo_catVenta"].place(x=330, y=70+modificar_altura, width = 150)
			diccionarioObjetos["combo_catHacienda"].place(x=330, y=100+modificar_altura, width = 150)

			diccionarioObjetos["combo_catVenta"]["values"] = obtenerCatVenta()
			diccionarioObjetos["combo_catHacienda"]["values"] = obtenerCatHacienda()

			diccionarioObjetos["entry_corral"].bind("<Return>", (lambda event: foco(diccionarioObjetos["entry_cantidad"])))
			diccionarioObjetos["entry_cantidad"].bind("<Return>", (lambda event: foco(diccionarioObjetos["combo_catVenta"])))
			diccionarioObjetos["combo_catVenta"].bind("<Return>", (lambda event: foco(diccionarioObjetos["combo_catHacienda"])))

	
			modificar_altura = 4

			tk.Label(label_hacienda, font=("verdana",14), text="KG BRUTO TROPA:", anchor="e", bg='#E8F6FA').place(x=10, y=140, width = 200, height = 30)	
			tk.Label(label_hacienda, font=("verdana",14), text="DESBASTE %:", anchor="e", bg='#E8F6FA').place(x=380, y=140, width = 150, height = 30)	
			tk.Label(label_hacienda, font=("verdana",14), text="KG NETO TROPA:", anchor="e", bg='#E8F6FA').place(x=20, y=170, width = 300, height = 30)
			tk.Label(label_hacienda, font=("verdana",14), text="KG NETO PROMEDIO:", anchor="e", bg='#E8F6FA').place(x=20, y=200, width = 300, height = 30)

			diccionarioObjetos["entry_brutoTropa"] = Entry(label_hacienda, font=("verdana",12))
			diccionarioObjetos["entry_desbastePorcentaje"] = Entry(label_hacienda, font=("verdana",12))
			diccionarioObjetos["entry_netoTropa"] = Entry(label_hacienda, font=("verdana",12, "bold"))
			diccionarioObjetos["entry_netoPromedio"] = Entry(label_hacienda, font=("verdana",12, "bold"))

			diccionarioObjetos["entry_brutoTropa"].place(x=220, y=140+modificar_altura, width = 100)
			diccionarioObjetos["entry_desbastePorcentaje"].place(x=530, y=140+modificar_altura, width = 100)
			diccionarioObjetos["entry_netoTropa"].place(x=330, y=170+modificar_altura, width = 150)
			diccionarioObjetos["entry_netoPromedio"].place(x=330, y=200+modificar_altura, width = 150)

			diccionarioObjetos["entry_desbastePorcentaje"].insert(0, 0.0)

			diccionarioObjetos["entry_brutoTropa"].bind("<Return>", (lambda event: calc_brutoTropa()))
			diccionarioObjetos["entry_desbastePorcentaje"].bind("<Return>", (lambda event: calc_desbastePorcentaje()))
			diccionarioObjetos["entry_netoTropa"].bind("<Return>", (lambda event: calc_promedio()))

			diccionarioObjetos["combo_catHacienda"].bind("<Return>", (lambda event: foco(diccionarioObjetos["entry_brutoTropa"])))

		#PESTAÑA OBSERVACIONES
		if(True):
			tk.Label(label_observaciones, font=("verdana",14), text="Observaciones:", anchor="n", bg='#E8F6FA').place(x=20, y=18, width = 150)

			diccionarioObjetos["entry_observaciones"] = Entry(label_observaciones, font=("verdana",14))
			diccionarioObjetos["entry_observaciones"].place(x=200, y=20+modificar_altura, width = 300)

			diccionarioObjetos["txt_observaciones"] = scrolledtext.ScrolledText(label_observaciones)
			diccionarioObjetos["txt_observaciones"].place(x = 200, y = 70, width = 300, height = 150)

		#PESTAÑA DTE
		if(True):
			tk.Label(label_dte, font=("verdana",12), text="DTE:", anchor="e", bg='#E8F6FA').place(x=40, y=10, width = 150)

			diccionarioObjetos["entry_dte"] = Entry(label_dte, font=("verdana",12))
			diccionarioObjetos["entry_dte"].place(x=200, y=6+modificar_altura, width = 300)

			diccionarioObjetos["entry_dte"].bind("<Return>", (lambda event: buscarDte()))
			diccionarioObjetos["entry_dte"].bind("<F5>", (lambda event: buscarDte()))

		#PESTAÑA FLETE
		if(True):
			tk.Label(label_flete, font=("verdana",12, "bold"), text="Flete:", anchor="e", bg='#E8F6FA').place(x=10, y=10, width = 170)

			#select.get()
			select = IntVar()
			rad1 = tk.Radiobutton(label_flete,text='Propio', value=1,variable = select, font=("verdana",12), anchor="w", bg='#E8F6FA')
			rad2 = tk.Radiobutton(label_flete,text='Tercero', value=2,variable = select, font=("verdana",12), anchor="w", bg='#E8F6FA')
			rad3 = tk.Radiobutton(label_flete,text='Otros', value=3,variable = select, font=("verdana",12), anchor="w", bg='#E8F6FA')

			rad1.place(x=200, y=10, width = 100)
			rad2.place(x=200, y=30, width = 100)
			rad3.place(x=200, y=50, width = 100)

			select.set(2)

	#tk.Label(window, text = "Comentarios", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 8, padx=10, pady=10)

	#entryNombre = Entry(window, font=("Helvetica Neue",14))
	#entryNombre.grid(sticky = "w", column = 1, row = 1, padx=0, pady=10)
	#diccionarioObjetos["entryNombre"] = entryNombre

	"""
	diccionarioObjetos["botBuscar"]["state"] = "normal"

	entryNombre.focus()
	entryNombre.bind('<Return>', (lambda event: verificar()))
	entryNombre.bind('<Button-1>', (lambda event: activarBuscar()))
	entryFecha.bind('<Button-1>', (lambda event: desactivarBuscar()))

	entryFecha.bind('<Return>', (lambda event: entryTipo.focus()))
	entryNombre.bind('<F5>', (lambda event: buscar()))
	"""

def ventana1(idLote, idRemate, idVendedor):

	def cerrarVentana():
		window.destroy()

	dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}

	window = Tk()
	window.title("LOTE")
	window.geometry("700x500+200+50")
	window.configure(backgroun="#E6F5FF") #E8F6FA
	window.resizable(0,1)

	iconGuardar = Image.open('iconos/guardar.png')
	iconBorrar = Image.open('iconos/borrar.png')
	iconEditar = Image.open('iconos/editar.png')
	iconBuscar = Image.open('iconos/buscar.png')
	iconAyuda = Image.open('iconos/ayuda.png')
	iconCerrar = Image.open('iconos/cerrar.png')

	iconGuardar = ImageTk.PhotoImage(iconGuardar)
	iconBorrar = ImageTk.PhotoImage(iconBorrar)
	iconEditar = ImageTk.PhotoImage(iconEditar)
	iconBuscar = ImageTk.PhotoImage(iconBuscar)
	iconAyuda = ImageTk.PhotoImage(iconAyuda)
	iconCerrar = ImageTk.PhotoImage(iconCerrar)

	barraherr = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraherr.pack(side=TOP, fill=X, pady = 2)

	barraTitulo = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraTitulo.pack(side=TOP, fill=X)

	lblBody = tk.Label(window, backgroun="#E6F5FF")
	lblBody.pack(side=TOP, fill=X, padx=2)
	lblBody.config(width="1", height="100")

	botGuardar = tk.Button(barraherr, image=iconGuardar, compound="top", backgroun="#b3f2bc", command=guardar)
	botBorrar = tk.Button(barraherr, image=iconBorrar, compound="top", backgroun="#FFaba8", command = borrar)
	botEditar = tk.Button(barraherr, image=iconEditar, compound="top", backgroun="#f2f0b3", command = editar)
	botBuscar = tk.Button(barraherr, image=iconBuscar, compound="top", command=buscar,backgroun="#b1fae3")
	botAyuda = tk.Button(barraherr, image=iconAyuda, compound="top", command=ayuda, backgroun="#f2f0b3")
	botCerrar = tk.Button(barraherr, image=iconCerrar, compound="top", command=cerrarVentana, backgroun="#FF6E6E")

	

	padX=3
	padY=2

	botGuardar.pack(side=LEFT, padx=padX, pady=padY)
	botBorrar.pack(side=LEFT, padx=padX, pady=padY)
	botEditar.pack(side=LEFT, padx=padX, pady=padY)
	botBuscar.pack(side=LEFT, padx=padX+20, pady=padY)
	botAyuda.pack(side=LEFT, padx=padX, pady=padY)
	botCerrar.pack(side=LEFT, padx=padX, pady=padY)

	botGuardar["state"] = "disabled"
	botBorrar["state"] = "disabled"
	botEditar["state"] = "disabled"
	botBuscar["state"] = "disabled"

	textTitulo = StringVar()
	textTitulo.set("LOTE")
	textID = StringVar()
	textID.set("")

	lbl_titulo = tk.Label(barraTitulo, font=("Helvetica Neue",10,"bold"), anchor="n", backgroun="#BAE7FF")
	lbl_titulo.pack()
	lbl_titulo.config(textvariable=textTitulo)

	diccionarioObjetos["botGuardar"] = botGuardar
	diccionarioObjetos["botBorrar"] = botBorrar
	diccionarioObjetos["botEditar"] = botEditar
	diccionarioObjetos["botBuscar"] = botBuscar

	diccionarioObjetos["textTitulo"] = textTitulo
	diccionarioObjetos["textID"] = textID
	

	window.bind("<Escape>", (lambda event: escape()))

	bodyLote(lblBody)
	escape()
	if(idLote != "NULL"):
		diccionarioObjetos["idLote"] = idLote
		verificarLote()
	else:
		diccionarioObjetos["idLote"] = ""
		if(idRemate != "NULL"):
			diccionarioObjetos["entry_remate"].delete(0, tk.END)
			diccionarioObjetos["entry_remate"].insert(0, idRemate)
			verificarRemate()
			verificarActivar()
		if(idVendedor != "NULL"):
			diccionarioObjetos["entry_vendedor"].delete(0, tk.END)
			diccionarioObjetos["entry_vendedor"].insert(0, idVendedor)
			verificarVendedor()
			verificarActivar()

	window.mainloop()

ventana1("NULL", "NULL", "NULL")