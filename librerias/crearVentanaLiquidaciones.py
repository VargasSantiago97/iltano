#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

#import ventanaIngreso
#import PDF_catalogo
import ventanaPlanDePagos
import pdf_preliquidacion

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

direccionBaseDeDatos = 'database/iltanohacienda.db'

#CREAR DICCIONARIOS
if(True):
	diccionario_textos = {}
	diccionario_objetos = {}
	diccionario_pinturas = {}
	dicCat = {}
	dicCatUbic = {}
	dicProductores = {}
	diccionario_objetos["ID_LOTE_A_EDITAR"] = "NULL"
	
	dicReceptorLiquidacionCompra = {}
	dicRemateLiquidacionCompra = {}
	dicFirmaLiquidacionCompra = {}
	
	dicReceptorLiquidacionCompra["cuit"] = ""
	dicReceptorLiquidacionCompra["nombre"] = ""
	dicReceptorLiquidacionCompra["iva"] = ""
	dicReceptorLiquidacionCompra["iibb"] = ""
	dicReceptorLiquidacionCompra["caracter"] = ""
	dicReceptorLiquidacionCompra["domicilio"] = ""
	dicReceptorLiquidacionCompra["localidad"] = ""
	dicReceptorLiquidacionCompra["provincia"] = ""
	dicReceptorLiquidacionCompra["postal"] = ""
	dicReceptorLiquidacionCompra["renspa"] = ""
	dicReceptorLiquidacionCompra["ruca"] = ""
	dicReceptorLiquidacionCompra["telefono"] = ""
	
	dicRemateLiquidacionCompra["fecha"] = ""
	dicRemateLiquidacionCompra["tipoDocumento"] = ""
	dicRemateLiquidacionCompra["numeroDocumento"] = ""
	dicRemateLiquidacionCompra["titulo"] = ""
	dicRemateLiquidacionCompra["condicion"] = ""
	dicRemateLiquidacionCompra["destino"] = ""
	
	dicFirmaLiquidacionCompra["nombre"] = ""
	dicFirmaLiquidacionCompra["cuit"] = ""

	diccionario_valores = {}
	diccionario_valores["alicuotaComision"] = "5.0"
	diccionario_valores["alicuotaDescuento"] = "0.0"
	diccionario_valores["alicuotaInteres"] = "0.0"
	diccionario_valores["alicuotaInteresDias"] = "0.0"
	diccionario_valores["alicuotaComisionVentas"] = "5.0"
	diccionario_valores["alicuotaDescuentoVentas"] = "0.0"
	diccionario_valores["alicuotaInteresVentas"] = "0.0"
	diccionario_valores["alicuotaInteresDiasVentas"] = "0.0"

	diccionario_observacionesCompras = {}
	diccionario_observacionesVentas = {}

	diccionario_gastos = {}
	diccionario_gastosVentas = {}

	dicLotes = {}
	dicLotesUbic = {}

	dicCompras = {}
	dicVentas = {}

fechaActual = str(time.strftime("%d-%m-%y"))
fechaHOY = str(time.strftime("%d/%m/%y"))

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
def actualizar_db2(con, tabla, condiciones, seleecionar):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT " + str(seleecionar) + " FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows

def actualizarProductores():
	con = sql_connection()
	condiciones = ""
	rows = actualizar_db(con, "productores", condiciones)
	for row in rows:
		dicProductores[str(row[3])] = str(row[1])

#DATOS REMATE
def actualizarDatosRemate():
	con = sql_connection()
	condiciones = " WHERE nombre = '" + str(rematename) + "'"
	rows = actualizar_db(con, "remate", condiciones)

	row = rows[0]

	dicRemateLiquidacionCompra["fecha"] = str(row[2])
	dicRemateLiquidacionCompra["tipoDocumento"] = str("PRE-LIQUIDACION DE COMPRA")
	dicRemateLiquidacionCompra["numeroDocumento"] = str("")
	dicRemateLiquidacionCompra["titulo"] = str(row[1])
	dicRemateLiquidacionCompra["condicion"] = str("")
	dicRemateLiquidacionCompra["destino"] = str("")

#Tabla PRODUCTOR
def productorFiltrar():
	pal_clave = str(diccionario_objetos["entry_productor"].get())

	con = sql_connection()
	condiciones =  ' WHERE (nombre LIKE "%' + pal_clave + '%" OR razon LIKE "%' + pal_clave + '%" OR ndoc LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%" OR con_iva LIKE "%' + pal_clave + '%" OR localidad LIKE "%' + pal_clave + '%" OR provincia LIKE "%' + pal_clave + '%" OR ruca LIKE "%' + pal_clave + '%" OR establecimiento LIKE "%' + pal_clave + '%") AND estado = "activo"'
	rows = actualizar_db(con, "productores", condiciones)

	if(len(rows)==1):
		cargarDatosProductor(rows[0][3])
		cargarTablaProductores([])
	else:
		cargarTablaProductores(rows)
def cargarTablaProductores(rows):
	tabla = diccionario_objetos["tabla_productores"]

	for j in tabla.get_children():
		tabla.delete(j)

	try:
		for row in rows:
			texto_alias = str(row[1])
			texto_cuit = str(row[3])

			tabla.insert("", tk.END, tags=(str(row[0]), str(row[3]),"oddrow",), values = (texto_alias,
				texto_cuit,))
		tabla.tag_configure('oddrow', background='orange')
	except:
		messagebox.showerror("ERROR", "Error al cargar")
def seleccionarTablaProductor():

	tabla = diccionario_objetos["tabla_productores"]

	seleccion = tabla.item(tabla.selection())

	productor = seleccion["tags"][1]

	cargarDatosProductor(productor)
def cargarDatosProductor(productor):
	con = sql_connection()
	condiciones = " WHERE ndoc = '" + str(productor) + "'"
	rows = actualizar_db(con, "productores", condiciones)

	row = rows[0]

	dicVentas.clear()
	dicCompras.clear()
	diccionario_gastosVentas.clear()
	diccionario_gastos.clear()
	diccionario_observacionesCompras.clear()
	diccionario_observacionesVentas.clear()

	texto_alias = str(row[1])
	texto_razon = str(row[2])
	texto_cuit = str(row[3])
	texto_ruca = str(row[19])
	texto_observaciones = str(row[13])

	diccionario_objetos["texto_alias"].set(texto_alias)
	diccionario_objetos["texto_razon"].set(texto_razon)
	diccionario_objetos["texto_cuit"].set(texto_cuit)
	diccionario_objetos["texto_ruca"].set(texto_ruca)

	diccionario_objetos["txt_observaciones"].configure(state="normal")
	diccionario_objetos["txt_observaciones"].delete("1.0", tk.END)
	diccionario_objetos["txt_observaciones"].insert("1.0", texto_observaciones)
	diccionario_objetos["txt_observaciones"].configure(state="disabled")

	dicReceptorLiquidacionCompra["cuit"] = texto_cuit
	dicReceptorLiquidacionCompra["nombre"] = texto_razon
	dicReceptorLiquidacionCompra["iva"] = str(row[6])
	dicReceptorLiquidacionCompra["iibb"] = ""
	dicReceptorLiquidacionCompra["caracter"] = ""
	dicReceptorLiquidacionCompra["domicilio"] = str(row[7])
	dicReceptorLiquidacionCompra["localidad"] = str(row[8])
	dicReceptorLiquidacionCompra["provincia"] = str(row[9])
	dicReceptorLiquidacionCompra["postal"] = str(row[10])
	dicReceptorLiquidacionCompra["renspa"] = ""
	dicReceptorLiquidacionCompra["ruca"] = str(row[19])
	dicReceptorLiquidacionCompra["telefono"] = str(row[17])

	#buscarCompras()
	diccionario_gastos.clear()
	buscarGuardado()

#BUSCAR COMPRAS GUARDADAS
def buscarGuardado():
	cuit = diccionario_objetos["texto_cuit"].get()

	con = sql_connection()
	condiciones = " WHERE productor = '" + str(cuit) + "' AND remate ='" + str(rematename) + "'"
	rows = actualizar_db(con, "liquidacionesGuardadas", condiciones)

	if(rows == []):
		buscarCompras()
		buscarVentas()
	else:
		MsgBox = messagebox.askquestion('ATENCION', 'Existe una liquidacion guardada.\n¿Desea cargarlo?', icon = 'warning')
		if(MsgBox == 'yes'):
			buscarDatosGuardados(rows[len(rows)-1][2])
		else:
			buscarCompras()
			buscarVentas()

#CARGAR COMPROBANTES COMPRAS
def buscarCompras():
	con = sql_connection()
	condiciones = " WHERE comprador = '" + str(diccionario_objetos["texto_cuit"].get()) + "'"
	rows = actualizar_db(con, "compraventa", condiciones)

	i = 0
	dicCompras.clear()
	for row in rows:
		lote = row[1]

		con = sql_connection()
		condiciones = " WHERE id = '" + lote + "'"
		rows_lote = actualizar_db(con, "lotes", condiciones)

		row_lote = rows_lote[0]

		dicCompras[str(i)] = {
		"id" : str(row_lote[0]),
		"precio" : str(row[3]),
		"remate" : str(row_lote[1]),
		"productor" : str(row_lote[2]),
		"cantidad" : str(row_lote[3]),
		"corral" : str(row_lote[4]),
		"catVenta" : str(row_lote[5]),
		"catHacienda" : str(row_lote[6]),
		"pintura" : str(row_lote[7]),
		"kgBruto" : str(row_lote[12]),
		"kgProm" : str(row_lote[13]),
		"dte" : str(row_lote[16]),
		"flete" : str(row_lote[17])
		}
		i+=1

	cargarCompras()
def cargarCompras():
	tabla = diccionario_objetos["tabla_compras"]


	for j in tabla.get_children():
		tabla.delete(j)

	try:
		cant_compras = len(dicCompras)
		for i in range(0, cant_compras):
			precio = float(dicCompras[str(i)]["precio"])
			peso = float(dicCompras[str(i)]["kgBruto"])
			cantidad = float(dicCompras[str(i)]["cantidad"])

			precioxunidad = str(round((precio*peso)/cantidad, 2))
			bruto = str(round(precio*peso, 2))
			iva = str(round(precio*peso*0.105, 2))

			x_vendedor = str(dicProductores[dicCompras[str(i)]["productor"]])
			x_corral = str(dicCompras[str(i)]["corral"])
			x_categoria = str(dicCompras[str(i)]["catHacienda"])
			x_um = "Cabezas"
			x_cantidad = str(dicCompras[str(i)]["cantidad"])
			x_precioPorUnidad = precioxunidad
			x_bruto = bruto
			x_porcentajeIva = "10.5"
			x_precioIva = iva

			tabla.insert("", tk.END, values = (x_vendedor,
				x_corral,
				x_categoria,
				x_um,
				x_cantidad,
				x_precioPorUnidad,
				x_bruto,
				x_porcentajeIva,
				x_precioIva,))

		crearComision()
	except:
		messagebox.showerror("ERROR", "Error al cargar")
def crearComision():
	try:
		baseImponible = calcularBaseImponible()
		descuento = baseImponible*float(diccionario_valores["alicuotaDescuento"])/100
		baseImponible = baseImponible - descuento
		x_gasto = str("COMISIÓN")
		x_base = str(baseImponible)
		x_alicuota = float(diccionario_valores["alicuotaComision"])
		x_importe = str(round(baseImponible*x_alicuota/100, 2))
		x_porcentajeIva = str("10.5")
		x_precioIva = str(round(baseImponible*x_alicuota*0.105/100, 2))

		diccionario_gastos["0"] = {
		"id" : "comision",
		"gasto" : x_gasto,
		"base" : x_base,
		"alicuota" : str(round(x_alicuota, 2)),
		"importe" : x_importe,
		"porcentajeIva" : x_porcentajeIva,
		"precioIva" : x_precioIva,
		}
		cargarGastos()
	except:
		messagebox.showerror("ERROR", "Error al cargar")
def cargarGastos():
	tabla = diccionario_objetos["tabla_comprasGastos"]

	for j in tabla.get_children():
		tabla.delete(j)

	total_gastos = 0.0
	total_gastosIva = 0.0

	for i in range(0, len(diccionario_gastos)):

		x_gasto = diccionario_gastos[str(i)]["gasto"]
		x_base = diccionario_gastos[str(i)]["base"]
		x_alicuota = diccionario_gastos[str(i)]["alicuota"]
		x_importe = diccionario_gastos[str(i)]["importe"]
		x_porcentajeIva = diccionario_gastos[str(i)]["porcentajeIva"]
		x_precioIva = diccionario_gastos[str(i)]["precioIva"]

		tabla.insert("", tk.END, diccionario_gastos[str(i)]["id"], values = (x_gasto,
			x_base,
			x_alicuota,
			x_importe,
			x_porcentajeIva,
			x_precioIva,))
		total_gastos = total_gastos + float(x_importe)
		total_gastosIva = total_gastosIva + float(x_precioIva)

	diccionario_valores["total_gastos"] = str(round(total_gastos, 2))
	diccionario_valores["total_gastosIva"] = str(round(total_gastosIva, 2))
	calcularTotales()
	cargarTablaObservacionesCompras()

def calcularTotales():

	baseImponible = calcularBaseImponible()

	total_gastos = float(diccionario_valores["total_gastos"])
	total_gastosIva = float(diccionario_valores["total_gastosIva"])

	porcentaje_descuento = float(diccionario_valores["alicuotaDescuento"])
	porcentaje_interes = float(diccionario_valores["alicuotaInteres"])
	dias_interes = float(diccionario_valores["alicuotaInteresDias"])
	alicuota_comision = float(diccionario_valores["alicuotaComision"])


	martillo = baseImponible
	descuento = baseImponible*porcentaje_descuento/100
	subtotal = baseImponible-descuento
	interes = baseImponible*dias_interes*porcentaje_interes/100
	comisionIva = (subtotal*alicuota_comision/100)+(subtotal*alicuota_comision/100*0.105)
	retencion = 0.0
	ivaHacienda = (baseImponible-descuento)*0.105
	ivaInteres = interes*0.21
	total = subtotal + interes + ivaHacienda + ivaInteres + total_gastos + total_gastosIva

	texto_martillo = str(round(martillo, 2))
	texto_descuento = str(round(descuento, 2))
	texto_subtotal = str(round(subtotal, 2))
	texto_interes = str(round(interes, 2))
	texto_comisionIva = str(round(comisionIva, 2))
	texto_retencion = str(round(retencion, 2))
	texto_ivaHacienda = str(round(ivaHacienda, 2))
	texto_ivaInteres = str(round(ivaInteres, 2))
	texto_total = str(round(total, 2))
	texto_gastos = str(round(total_gastos, 2))
	texto_gastosIva = str(round(total_gastosIva, 2))


	diccionario_objetos["compras_texto_martillo"].set(texto_martillo)
	diccionario_objetos["compras_texto_descuento"].set(texto_descuento)
	diccionario_objetos["compras_texto_subtotal"].set(texto_subtotal)
	diccionario_objetos["compras_texto_interes"].set(texto_interes)
	diccionario_objetos["compras_texto_comisionIva"].set(texto_comisionIva)
	diccionario_objetos["compras_texto_retencion"].set(texto_retencion)
	diccionario_objetos["compras_texto_total"].set(texto_total)
	diccionario_objetos["compras_texto_ivaHacienda"].set(texto_ivaHacienda)
	diccionario_objetos["compras_texto_ivaInteres"].set(texto_ivaInteres)
	diccionario_objetos["compras_texto_gastos"].set(texto_gastos)
	diccionario_objetos["compras_texto_gastosIva"].set(texto_gastosIva)

def agregarGasto():
	windowGasto = Tk()
	windowGasto.geometry("500x500")

	tk.Label(windowGasto, text="Gasto:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=20, width=200)
	tk.Label(windowGasto, text="Base imponible $:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=70, width=200)
	tk.Label(windowGasto, text="Alicuota:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=120, width=200)
	tk.Label(windowGasto, text="Importe:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=170, width=200)
	tk.Label(windowGasto, text="IVA %:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=220, width=200)
	tk.Label(windowGasto, text="IVA $:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=270, width=200)

	entry_gasto = Entry(windowGasto, font=("Helvetica Neue", 14))
	entry_baseImponible = Entry(windowGasto, font=("Helvetica Neue", 14))
	entry_alicuota = Entry(windowGasto, font=("Helvetica Neue", 14))
	entry_importe = Entry(windowGasto, font=("Helvetica Neue", 14))
	entry_ivaPorcentaje = Entry(windowGasto, font=("Helvetica Neue", 14))
	entry_ivaImporte = Entry(windowGasto, font=("Helvetica Neue", 14))

	entry_gasto.place(x=220, y=20, width=200)
	entry_baseImponible.place(x=220, y=70, width=200)
	entry_alicuota.place(x=220, y=120, width=200)
	entry_importe.place(x=220, y=170, width=200)
	entry_ivaPorcentaje.place(x=220, y=220, width=200)
	entry_ivaImporte.place(x=220, y=270, width=200)

	entry_ivaPorcentaje.insert(0, 21.0)

	def guardarAgregarGasto():
		gasto = str(entry_gasto.get())
		baseImponible = str(entry_baseImponible.get())
		alicuota = str(entry_alicuota.get())
		importe = str(entry_importe.get())
		porcentajeIva = str(entry_ivaPorcentaje.get())
		precioIva = str(entry_ivaImporte.get())

		diccionario_gastos[str(len(diccionario_gastos))] = {
		"id" : str(len(diccionario_gastos)),
		"gasto" : gasto,
		"base" : baseImponible,
		"alicuota" : alicuota,
		"importe" : importe,
		"porcentajeIva" : porcentajeIva,
		"precioIva" : precioIva,
		}
		cargarGastos()

		windowGasto.destroy()

	btn_guardar = tk.Button(windowGasto, text="GUARDAR", font=("Helvetica Neue", 15), command = guardarAgregarGasto, backgroun="#a4ff9e")
	btn_guardar.place(x=165, y=350, width=150, height=70)

	def enter_entry_gasto():
		entry_baseImponible.focus()

	def enter_entry_baseImponible():
		entry_alicuota.focus()

	def enter_entry_alicuota():
		entry_importe.focus()
		entry_importe.delete(0, tk.END)
		entry_ivaImporte.delete(0, tk.END)

		importe = float(entry_alicuota.get())/100*float(entry_baseImponible.get())
		iva = float(entry_ivaPorcentaje.get())/100*importe

		entry_importe.insert(0, importe)
		entry_ivaImporte.insert(0, iva)

	def enter_entry_importe():
		entry_ivaImporte.delete(0, tk.END)

		iva = float(entry_ivaPorcentaje.get())/100*float(entry_importe.get())

		entry_ivaImporte.insert(0, iva)
		entry_ivaPorcentaje.focus()

	def enter_entry_ivaPorcentaje():
		entry_ivaImporte.focus()
		entry_ivaImporte.delete(0, tk.END)

		iva = float(entry_ivaPorcentaje.get())/100*float(entry_importe.get())

		entry_ivaImporte.insert(0, iva)
	def enter_entry_ivaImporte():
		guardarAgregarGasto()
	
	entry_gasto.bind('<Return>', (lambda event: enter_entry_gasto()))
	entry_baseImponible.bind('<Return>', (lambda event: enter_entry_baseImponible()))
	entry_alicuota.bind('<Return>', (lambda event: enter_entry_alicuota()))
	entry_importe.bind('<Return>', (lambda event: enter_entry_importe()))
	entry_ivaPorcentaje.bind('<Return>', (lambda event: enter_entry_ivaPorcentaje()))
	entry_ivaImporte.bind('<Return>', (lambda event: enter_entry_ivaImporte()))

	windowGasto.mainloop()

def calcularBaseImponible():
	baseImponible = 0
	cant_compras = len(dicCompras)
	for i in range(0, cant_compras):
		precio = float(dicCompras[str(i)]["precio"])
		peso = float(dicCompras[str(i)]["kgBruto"])
		bruto = str(round(precio*peso, 2))
		baseImponible = baseImponible + float(bruto)

	return baseImponible

def cargarTablaObservacionesCompras():
	tabla = diccionario_objetos["tabla_comprasObservaciones"]

	for i in tabla.get_children():
		tabla.delete(i)

	try:
		for i in range(0, len(diccionario_observacionesCompras)):
			texto_cuota = diccionario_observacionesCompras[str(i)]["cuota"]
			texto_fecha = diccionario_observacionesCompras[str(i)]["fecha"]
			texto_monto = diccionario_observacionesCompras[str(i)]["monto"]

			tabla.insert("", tk.END, values = (texto_cuota,
				texto_fecha, texto_monto))
	except:
		messagebox.showerror("ERROR", "Error al cargar plan de pagos")


#CARGAR COMPROBANTES VENTAS
def buscarVentas():
	con = sql_connection()
	condiciones = " WHERE vendedor = '" + str(diccionario_objetos["texto_cuit"].get()) + "'"
	rows = actualizar_db(con, "compraventa", condiciones)

	i = 0
	dicVentas.clear()
	for row in rows:
		lote = row[1]

		con = sql_connection()
		condiciones = " WHERE id = '" + lote + "'"
		rows_lote = actualizar_db(con, "lotes", condiciones)

		row_lote = rows_lote[0]

		dicVentas[str(i)] = {
		"id" : str(row_lote[0]),
		"precio" : str(row[3]),
		"remate" : str(row_lote[1]),
		"productor" : str(row[2]),
		"cantidad" : str(row_lote[3]),
		"corral" : str(row_lote[4]),
		"catVenta" : str(row_lote[5]),
		"catHacienda" : str(row_lote[6]),
		"pintura" : str(row_lote[7]),
		"kgBruto" : str(row_lote[12]),
		"kgProm" : str(row_lote[13]),
		"dte" : str(row_lote[16]),
		"flete" : str(row_lote[17])
		}
		i+=1

	cargarVentas()
def cargarVentas():
	tabla = diccionario_objetos["tabla_ventas"]


	for j in tabla.get_children():
		tabla.delete(j)

	try:
		cant_ventas = len(dicVentas)
		for i in range(0, cant_ventas):
			precio = float(dicVentas[str(i)]["precio"])
			peso = float(dicVentas[str(i)]["kgBruto"])
			cantidad = float(dicVentas[str(i)]["cantidad"])

			precioxunidad = str(round((precio*peso)/cantidad, 2))
			bruto = str(round(precio*peso, 2))
			iva = str(round(precio*peso*0.105, 2))

			x_vendedor = str(dicProductores[dicVentas[str(i)]["productor"]])
			x_corral = str(dicVentas[str(i)]["corral"])
			x_categoria = str(dicVentas[str(i)]["catHacienda"])
			x_um = "Cabezas"
			x_cantidad = str(dicVentas[str(i)]["cantidad"])
			x_precioPorUnidad = precioxunidad
			x_bruto = bruto
			x_porcentajeIva = "10.5"
			x_precioIva = iva

			tabla.insert("", tk.END, values = (x_vendedor,
				x_corral,
				x_categoria,
				x_um,
				x_cantidad,
				x_precioPorUnidad,
				x_bruto,
				x_porcentajeIva,
				x_precioIva,))

		crearComisionVentas()
	except:
		messagebox.showerror("ERROR", "Error al cargar")
def crearComisionVentas():
	try:
		baseImponible = calcularBaseImponibleVentas()
		descuento = baseImponible*float(diccionario_valores["alicuotaDescuentoVentas"])/100
		baseImponible = baseImponible - descuento
		x_gasto = str("COMISIÓN")
		x_base = str(baseImponible)
		x_alicuota = float(diccionario_valores["alicuotaComisionVentas"])
		x_importe = str(round(baseImponible*x_alicuota/100, 2))
		x_porcentajeIva = str("10.5")
		x_precioIva = str(round(baseImponible*x_alicuota*0.105/100, 2))

		diccionario_objetos["TEXTOCOMISION"].set(baseImponible-float(x_importe))

		diccionario_gastosVentas["0"] = {
		"id" : "comision",
		"gasto" : x_gasto,
		"base" : x_base,
		"alicuota" : str(round(x_alicuota, 2)),
		"importe" : x_importe,
		"porcentajeIva" : x_porcentajeIva,
		"precioIva" : x_precioIva,
		}
		cargarGastosVentas()
	except:
		messagebox.showerror("ERROR", "Error al cargar")
def cargarGastosVentas():
	tabla = diccionario_objetos["tabla_ventasGastos"]

	for j in tabla.get_children():
		tabla.delete(j)

	total_gastos = 0.0
	total_gastosIva = 0.0

	for i in range(0, len(diccionario_gastosVentas)):

		x_gasto = diccionario_gastosVentas[str(i)]["gasto"]
		x_base = diccionario_gastosVentas[str(i)]["base"]
		x_alicuota = diccionario_gastosVentas[str(i)]["alicuota"]
		x_importe = diccionario_gastosVentas[str(i)]["importe"]
		x_porcentajeIva = diccionario_gastosVentas[str(i)]["porcentajeIva"]
		x_precioIva = diccionario_gastosVentas[str(i)]["precioIva"]

		tabla.insert("", tk.END, diccionario_gastosVentas[str(i)]["id"], values = (x_gasto,
			x_base,
			x_alicuota,
			x_importe,
			x_porcentajeIva,
			x_precioIva,))
		total_gastos = total_gastos + float(x_importe)
		total_gastosIva = total_gastosIva + float(x_precioIva)

	diccionario_valores["total_gastosVentas"] = str(round(total_gastos, 2))
	diccionario_valores["total_gastosIvaVentas"] = str(round(total_gastosIva, 2))
	calcularTotalesVentas()
	cargarTablaObservacionesVentas()

def calcularTotalesVentas():

	baseImponible = calcularBaseImponibleVentas()

	total_gastos = float(diccionario_valores["total_gastosVentas"])
	total_gastosIva = float(diccionario_valores["total_gastosIvaVentas"])

	porcentaje_descuento = float(diccionario_valores["alicuotaDescuentoVentas"])
	porcentaje_interes = float(diccionario_valores["alicuotaInteresVentas"])
	dias_interes = float(diccionario_valores["alicuotaInteresDiasVentas"])
	alicuota_comision = float(diccionario_valores["alicuotaComisionVentas"])

	martillo = baseImponible
	descuento = baseImponible*porcentaje_descuento/100
	subtotal = baseImponible-descuento
	interes = baseImponible*dias_interes*porcentaje_interes/100
	comisionIva = (subtotal*alicuota_comision/100)+(subtotal*alicuota_comision/100*0.105)
	retencion = 0.0
	ivaHacienda = (baseImponible-descuento)*0.105
	ivaInteres = interes*0.21
	total = subtotal + interes + ivaHacienda + ivaInteres - total_gastos - total_gastosIva

	texto_martillo = str(round(martillo, 2))
	texto_descuento = str(round(descuento, 2))
	texto_subtotal = str(round(subtotal, 2))
	texto_interes = str(round(interes, 2))
	texto_comisionIva = str(round(comisionIva, 2))
	texto_retencion = str(round(retencion, 2))
	texto_ivaHacienda = str(round(ivaHacienda, 2))
	texto_ivaInteres = str(round(ivaInteres, 2))
	texto_total = str(round(total, 2))
	texto_gastos = str(round(total_gastos, 2))
	texto_gastosIva = str(round(total_gastosIva, 2))


	diccionario_objetos["ventas_texto_martillo"].set(texto_martillo)
	diccionario_objetos["ventas_texto_descuento"].set(texto_descuento)
	diccionario_objetos["ventas_texto_subtotal"].set(texto_subtotal)
	diccionario_objetos["ventas_texto_interes"].set(texto_interes)
	diccionario_objetos["ventas_texto_comisionIva"].set(texto_comisionIva)
	diccionario_objetos["ventas_texto_retencion"].set(texto_retencion)
	diccionario_objetos["ventas_texto_total"].set(texto_total)
	diccionario_objetos["ventas_texto_ivaHacienda"].set(texto_ivaHacienda)
	diccionario_objetos["ventas_texto_ivaInteres"].set(texto_ivaInteres)
	diccionario_objetos["ventas_texto_gastos"].set(texto_gastos)
	diccionario_objetos["ventas_texto_gastosIva"].set(texto_gastosIva)

def agregarGastoVentas():
	windowGastoVentas = Tk()
	windowGastoVentas.geometry("500x500")

	tk.Label(windowGastoVentas, text="Gasto:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=20, width=200)
	tk.Label(windowGastoVentas, text="Base imponible $:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=70, width=200)
	tk.Label(windowGastoVentas, text="Alicuota:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=120, width=200)
	tk.Label(windowGastoVentas, text="Importe:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=170, width=200)
	tk.Label(windowGastoVentas, text="IVA %:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=220, width=200)
	tk.Label(windowGastoVentas, text="IVA $:", font=("Helvetica Neue", 14), anchor="e").place(x=10, y=270, width=200)

	entry_gasto = Entry(windowGastoVentas, font=("Helvetica Neue", 14))
	entry_baseImponible = Entry(windowGastoVentas, font=("Helvetica Neue", 14))
	entry_alicuota = Entry(windowGastoVentas, font=("Helvetica Neue", 14))
	entry_importe = Entry(windowGastoVentas, font=("Helvetica Neue", 14))
	entry_ivaPorcentaje = Entry(windowGastoVentas, font=("Helvetica Neue", 14))
	entry_ivaImporte = Entry(windowGastoVentas, font=("Helvetica Neue", 14))

	entry_gasto.place(x=220, y=20, width=200)
	entry_baseImponible.place(x=220, y=70, width=200)
	entry_alicuota.place(x=220, y=120, width=200)
	entry_importe.place(x=220, y=170, width=200)
	entry_ivaPorcentaje.place(x=220, y=220, width=200)
	entry_ivaImporte.place(x=220, y=270, width=200)

	entry_ivaPorcentaje.insert(0, 21.0)

	def guardarAgregarGastoVentas():
		gasto = str(entry_gasto.get())
		baseImponible = str(entry_baseImponible.get())
		alicuota = str(entry_alicuota.get())
		importe = str(entry_importe.get())
		porcentajeIva = str(entry_ivaPorcentaje.get())
		precioIva = str(entry_ivaImporte.get())

		diccionario_gastosVentas[str(len(diccionario_gastosVentas))] = {
		"id" : str(len(diccionario_gastosVentas)),
		"gasto" : gasto,
		"base" : baseImponible,
		"alicuota" : alicuota,
		"importe" : importe,
		"porcentajeIva" : porcentajeIva,
		"precioIva" : precioIva,
		}
		cargarGastosVentas()

		windowGastoVentas.destroy()

	btn_guardar = tk.Button(windowGastoVentas, text="GUARDAR", font=("Helvetica Neue", 15), command = guardarAgregarGastoVentas, backgroun="#a4ff9e")
	btn_guardar.place(x=165, y=350, width=150, height=70)

	def enter_entry_gasto():
		entry_baseImponible.focus()

	def enter_entry_baseImponible():
		entry_alicuota.focus()

	def enter_entry_alicuota():
		entry_importe.focus()
		entry_importe.delete(0, tk.END)
		entry_ivaImporte.delete(0, tk.END)

		importe = float(entry_alicuota.get())/100*float(entry_baseImponible.get())
		iva = float(entry_ivaPorcentaje.get())/100*importe

		entry_importe.insert(0, importe)
		entry_ivaImporte.insert(0, iva)

	def enter_entry_importe():
		entry_ivaImporte.delete(0, tk.END)

		iva = float(entry_ivaPorcentaje.get())/100*float(entry_importe.get())

		entry_ivaImporte.insert(0, iva)
		entry_ivaPorcentaje.focus()

	def enter_entry_ivaPorcentaje():
		entry_ivaImporte.focus()
		entry_ivaImporte.delete(0, tk.END)

		iva = float(entry_ivaPorcentaje.get())/100*float(entry_importe.get())

		entry_ivaImporte.insert(0, iva)
	def enter_entry_ivaImporte():
		guardarAgregarGasto()
	
	entry_gasto.bind('<Return>', (lambda event: enter_entry_gasto()))
	entry_baseImponible.bind('<Return>', (lambda event: enter_entry_baseImponible()))
	entry_alicuota.bind('<Return>', (lambda event: enter_entry_alicuota()))
	entry_importe.bind('<Return>', (lambda event: enter_entry_importe()))
	entry_ivaPorcentaje.bind('<Return>', (lambda event: enter_entry_ivaPorcentaje()))
	entry_ivaImporte.bind('<Return>', (lambda event: enter_entry_ivaImporte()))

	windowGastoVentas.mainloop()

def calcularBaseImponibleVentas():
	baseImponible = 0
	cant_ventas = len(dicVentas)
	for i in range(0, cant_ventas):
		precio = float(dicVentas[str(i)]["precio"])
		peso = float(dicVentas[str(i)]["kgBruto"])
		bruto = str(round(precio*peso, 2))
		baseImponible = baseImponible + float(bruto)

	return baseImponible

def cargarTablaObservacionesVentas():
	tabla = diccionario_objetos["tabla_ventasObservaciones"]

	for i in tabla.get_children():
		tabla.delete(i)

	try:
		for i in range(0, len(diccionario_observacionesVentas)):
			texto_cuota = diccionario_observacionesVentas[str(i)]["cuota"]
			texto_fecha = diccionario_observacionesVentas[str(i)]["fecha"]
			texto_monto = diccionario_observacionesVentas[str(i)]["monto"]

			tabla.insert("", tk.END, values = (texto_cuota,
				texto_fecha, texto_monto))
	except:
		messagebox.showerror("ERROR", "Error al cargar plan de pagos")
#----------    CONSTRUCTORES     -----------
def labelProductorInfo(lbl_productor):
	lbl_info = tk.LabelFrame(lbl_productor, text="Productor", backgroun="#E0F8F1")
	lbl_info.place(x = 5, y = 0, width = 290, height = 198)

	texto_alias = StringVar()
	texto_alias.set("") # Caso 1
	texto_razon = StringVar()
	texto_razon.set("")
	texto_cuit = StringVar()
	texto_cuit.set("")
	texto_ruca = StringVar()
	texto_ruca.set("")


	lbl_alias = tk.Label(lbl_info, font=("Helvetica Neue",10,"bold"), anchor="w", backgroun="#E0F8F1")
	lbl_alias.place(x=0, y=0, width=285)
	lbl_alias.config(textvariable=texto_alias)

	lbl_razon = tk.Label(lbl_info, font=("Helvetica Neue",8), anchor="w", backgroun="#E0F8F1")
	lbl_razon.place(x=0, y=25, width=285)
	lbl_razon.config(textvariable=texto_razon)

	lbl_cuit = tk.Label(lbl_info, font=("verdana",10), anchor="w", backgroun="#E0F8F1")
	lbl_cuit.place(x=40, y=63, width=140)
	lbl_cuit.config(textvariable=texto_cuit)

	lbl_ruca = tk.Label(lbl_info, font=("verdana",10), anchor="w", backgroun="#E0F8F1")
	lbl_ruca.place(x=215, y=63, width=70)
	lbl_ruca.config(textvariable=texto_ruca)


	Label(lbl_info, font=("verdana",10), text="CUIT:", backgroun="#E0F8F1").place(x=0, y=65)
	Label(lbl_info, font=("verdana",10), text="RUCA:", backgroun="#E0F8F1").place(x=170, y=65)

	txt_observaciones = scrolledtext.ScrolledText(lbl_info, backgroun="#edfffa")
	txt_observaciones.place(x = 0, y = 95, width = 285, height = 80)
	txt_observaciones.config(state="disabled")

	diccionario_objetos["texto_alias"] = texto_alias
	diccionario_objetos["texto_razon"] = texto_razon
	diccionario_objetos["texto_cuit"] = texto_cuit
	diccionario_objetos["texto_ruca"] = texto_ruca
	diccionario_objetos["txt_observaciones"] = txt_observaciones
def labelProductorBuscador(lbl_productor):
	#--Buscador
	lbl_comprador_aux = Label(lbl_productor, backgroun="#E0F8F1")
	lbl_comprador_aux.place(x = 5, y = 220, width = 290, height = 475)

	lbl_ventana_productor_buscador_entry = tk.LabelFrame(lbl_comprador_aux, text="Filtrar", backgroun="#E0F8F1")
	lbl_ventana_productor_buscador_tabla = tk.LabelFrame(lbl_comprador_aux, text="Productores", backgroun="#E0F8F1")

	lbl_ventana_productor_buscador_entry.grid(column = 0, row = 0)
	lbl_ventana_productor_buscador_tabla.grid(column = 0, row = 1)

	#--
	entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="31")
	entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = 5)

	btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar", command= lambda: productorFiltrar())
	btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 0)

	sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
	sbr_productor.pack(side=RIGHT, fill="y")


	tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("cliente", "doc"), selectmode=tk.BROWSE, height=19, show='headings') 
	tabla_productor.pack(side=LEFT, fill="both", expand=True)
	sbr_productor.config(command=tabla_productor.yview)
	tabla_productor.config(yscrollcommand=sbr_productor.set)

	tabla_productor.heading("cliente", text="Productor", command=lambda: treeview_sort_column(tabla_productor, "cliente", False))
	tabla_productor.heading("doc", text="CUIT/DNI", command=lambda: treeview_sort_column(tabla_productor, "doc", False))

	tabla_productor.column("cliente", width=165)
	tabla_productor.column("doc", width=100)

	diccionario_objetos["entry_productor"] = entry_filtrar_productor
	diccionario_objetos["tabla_productores"] = tabla_productor

	entry_filtrar_productor.bind("<Return>", (lambda event: productorFiltrar()))
	tabla_productor.bind('<Double-1>', (lambda event: seleccionarTablaProductor()))
	tabla_productor.bind('<Return>', (lambda event: seleccionarTablaProductor()))

def labelCompras(label_compras):
	lbl_tablaCompras = tk.LabelFrame(label_compras, text="COMPRAS", backgroun="#E0F8F1")
	lbl_tablaCompras.place(x = 5, y = 5, width = 955, height = 200)

	lbl_tablaGastos = tk.LabelFrame(label_compras, text="GASTOS", backgroun="#E0F8F1")
	lbl_tablaGastos.place(x = 5, y = 210, width = 955, height = 200)

	lbl_tablaObservaciones = tk.LabelFrame(label_compras, text="Financiacion", backgroun="#E0F8F1")
	lbl_tablaObservaciones.place(x = 5, y = 415, width = 300, height = 160)

	lbl_totales = tk.LabelFrame(label_compras, text="TOTALES", backgroun="#E0F8F1")
	lbl_totales.place(x = 310, y = 415, width = 650, height = 160)

	lbl_acciones = tk.LabelFrame(label_compras, text="Acciones", backgroun="#E0F8F1")
	lbl_acciones.place(x = 5, y = 575, width = 955, height = 100)

	#TABLA COMPRAS
	if(True):
		sbr_compras = Scrollbar(lbl_tablaCompras)
		sbr_compras.pack(side=RIGHT, fill="y")

		tabla_compras = ttk.Treeview(lbl_tablaCompras, columns=("vendedor", "corral", "categoria", "um", "cantidad", "precio_um", "bruto", "porcentaje_iva", "precio_iva"), selectmode=tk.BROWSE, show='headings') 
		tabla_compras.pack(side=LEFT, fill="both", expand=True)
		sbr_compras.config(command=tabla_compras.yview)
		tabla_compras.config(yscrollcommand=sbr_compras.set)

		tabla_compras.heading("vendedor", text="Vendedor", command=lambda: treeview_sort_column(tabla_compras, "vendedor", False))
		tabla_compras.heading("corral", text="Corral", command=lambda: treeview_sort_column(tabla_compras, "corral", False))
		tabla_compras.heading("categoria", text="Categoria", command=lambda: treeview_sort_column(tabla_compras, "categoria", False))
		tabla_compras.heading("um", text="UM", command=lambda: treeview_sort_column(tabla_compras, "um", False))
		tabla_compras.heading("cantidad", text="Cantidad", command=lambda: treeview_sort_column(tabla_compras, "cantidad", False))
		tabla_compras.heading("precio_um", text="$ UM", command=lambda: treeview_sort_column(tabla_compras, "precio_um", False))
		tabla_compras.heading("bruto", text="Bruto", command=lambda: treeview_sort_column(tabla_compras, "bruto", False))
		tabla_compras.heading("porcentaje_iva", text="% IVA", command=lambda: treeview_sort_column(tabla_compras, "porcentaje_iva", False))
		tabla_compras.heading("precio_iva", text="$ IVA", command=lambda: treeview_sort_column(tabla_compras, "precio_iva", False))

		tabla_compras.column("vendedor", width=100)
		tabla_compras.column("corral", width=10)
		tabla_compras.column("categoria", width=100)
		tabla_compras.column("um", width=10)
		tabla_compras.column("cantidad", width=10)
		tabla_compras.column("precio_um", width=10)
		tabla_compras.column("bruto", width=10)
		tabla_compras.column("porcentaje_iva", width=10)
		tabla_compras.column("precio_iva", width=10)

		diccionario_objetos["tabla_compras"] = tabla_compras

	#TABLA GASTOS
	if(True):
		sbr_comprasGastos = Scrollbar(lbl_tablaGastos)
		sbr_comprasGastos.pack(side=RIGHT, fill="y")

		tabla_comprasGastos = ttk.Treeview(lbl_tablaGastos, columns=("gasto", "base_imponible", "alicuota", "importe", "porcentaje_iva", "precio_iva"), selectmode=tk.BROWSE, show='headings') 
		tabla_comprasGastos.pack(side=LEFT, fill="both", expand=True)
		sbr_comprasGastos.config(command=tabla_comprasGastos.yview)
		tabla_comprasGastos.config(yscrollcommand=sbr_comprasGastos.set)

		tabla_comprasGastos.heading("gasto", text="Gastos", command=lambda: treeview_sort_column(tabla_comprasGastos, "gasto", False))
		tabla_comprasGastos.heading("base_imponible", text="Base Imponible $", command=lambda: treeview_sort_column(tabla_comprasGastos, "base_imponible", False))
		tabla_comprasGastos.heading("alicuota", text="Alicuota %", command=lambda: treeview_sort_column(tabla_comprasGastos, "alicuota", False))
		tabla_comprasGastos.heading("importe", text="Importe $", command=lambda: treeview_sort_column(tabla_comprasGastos, "importe", False))
		tabla_comprasGastos.heading("porcentaje_iva", text="IVA %", command=lambda: treeview_sort_column(tabla_comprasGastos, "porcentaje_iva", False))
		tabla_comprasGastos.heading("precio_iva", text="IVA $", command=lambda: treeview_sort_column(tabla_comprasGastos, "precio_iva", False))

		tabla_comprasGastos.column("gasto", width=200)
		tabla_comprasGastos.column("base_imponible", width=100)
		tabla_comprasGastos.column("alicuota", width=165)
		tabla_comprasGastos.column("importe", width=100)
		tabla_comprasGastos.column("porcentaje_iva", width=100)
		tabla_comprasGastos.column("precio_iva", width=100)

		diccionario_objetos["tabla_comprasGastos"] = tabla_comprasGastos

	#TABLA Financiacion
	if(True):
		sbr_comprasObservaciones = Scrollbar(lbl_tablaObservaciones)
		sbr_comprasObservaciones.pack(side=RIGHT, fill="y")

		tabla_comprasObservaciones = ttk.Treeview(lbl_tablaObservaciones, columns=("cuota", "fecha", "importe"), selectmode=tk.BROWSE, show='headings') 
		tabla_comprasObservaciones.pack(side=LEFT, fill="both", expand=True)
		sbr_comprasObservaciones.config(command=tabla_comprasObservaciones.yview)
		tabla_comprasObservaciones.config(yscrollcommand=sbr_comprasObservaciones.set)

		tabla_comprasObservaciones.heading("cuota", text="Cuota", command=lambda: treeview_sort_column(tabla_comprasObservaciones, "cuota", False))
		tabla_comprasObservaciones.heading("fecha", text="Fecha", command=lambda: treeview_sort_column(tabla_comprasObservaciones, "fecha", False))
		tabla_comprasObservaciones.heading("importe", text="Importe $", command=lambda: treeview_sort_column(tabla_comprasObservaciones, "importe", False))


		tabla_comprasObservaciones.column("cuota", width=10)
		tabla_comprasObservaciones.column("fecha", width=10)
		tabla_comprasObservaciones.column("importe", width=10)

		diccionario_objetos["tabla_comprasObservaciones"] = tabla_comprasObservaciones

	#TOTALES
	if(True):
		var_subir = +3
		var_x = 70
		tk.Label(lbl_totales, text="Subtotal Martillo $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 0+var_subir, width = 180)
		tk.Label(lbl_totales, text="$", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 175+var_x, y = 23+var_subir, width = 10)
		tk.Label(lbl_totales, text="Descuento pago contado %", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = var_x-50, y = 23+var_subir, width = 180)
		tk.Label(lbl_totales, text="Subtotal $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 46+var_subir, width = 180)
		tk.Label(lbl_totales, text="$", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 175+var_x, y = 69+var_subir, width = 10)
		tk.Label(lbl_totales, text="Int. dias de pago dif. %", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = var_x-70, y = 69+var_subir, width = 140)
		tk.Label(lbl_totales, text="Comision+IVA $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 92+var_subir, width = 180)
		tk.Label(lbl_totales, text="Comision %", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = var_x-70, y = 98+var_subir, width = 100)
		tk.Label(lbl_totales, text="Retencion IIBB $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 115+var_subir, width = 180)

		texto_martillo = StringVar()
		texto_descuento = StringVar()
		texto_subtotal = StringVar()
		texto_interes = StringVar()
		texto_comisionIva = StringVar()
		texto_retencion = StringVar()
		texto_total = StringVar()
		texto_ivaHacienda = StringVar()
		texto_ivaInteres = StringVar()
		texto_alicuotaDescuento = StringVar()
		texto_alicuotaInteres = StringVar()
		texto_alicuotaInteresDias = StringVar()
		texto_alicuotaComision = StringVar()
		texto_gastos = StringVar()
		texto_gastosIva = StringVar()


		texto_martillo.set("")
		texto_descuento.set("")
		texto_subtotal.set("")
		texto_interes.set("")
		texto_comisionIva.set("")
		texto_retencion.set("")
		texto_total.set("")
		texto_ivaHacienda.set("")
		texto_ivaInteres.set("")
		texto_alicuotaDescuento.set(diccionario_valores["alicuotaDescuento"])
		texto_alicuotaInteres.set(diccionario_valores["alicuotaInteres"])
		texto_alicuotaInteresDias.set(diccionario_valores["alicuotaInteresDias"])
		texto_alicuotaComision.set(diccionario_valores["alicuotaComision"])
		texto_gastos.set("")
		texto_gastosIva.set("")


		lbl_martillo = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_martillo.place(x=185+var_x, y=0, width=100)
		lbl_martillo.config(textvariable=texto_martillo)

		lbl_descuento = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_descuento.place(x=185+var_x, y=23, width=100)
		lbl_descuento.config(textvariable=texto_descuento)

		lbl_subtotal = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_subtotal.place(x=185+var_x, y=46, width=100)
		lbl_subtotal.config(textvariable=texto_subtotal)

		lbl_interes = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_interes.place(x=185+var_x, y=69, width=100)
		lbl_interes.config(textvariable=texto_interes)

		lbl_comisionIva = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_comisionIva.place(x=185+var_x, y=92, width=100)
		lbl_comisionIva.config(textvariable=texto_comisionIva)

		lbl_retencion = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_retencion.place(x=185+var_x, y=115, width=100)
		lbl_retencion.config(textvariable=texto_retencion)

		varx_total = 30
		tk.Label(lbl_totales, text="TOTAL LIQUIDADO $", font=("Helvetica Neue",12, "bold"), backgroun="#E0F8F1", anchor="c").place(x = 300+varx_total, y = 110+var_subir, width = 160)

		lbl_total = tk.Label(lbl_totales, font=("Helvetica Neue",18,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_total.place(x=460+varx_total, y=106, width=155)
		lbl_total.config(textvariable=texto_total)

		tk.Label(lbl_totales, text="IVA Hacienda (10.5%) $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 0+var_subir, width = 130)
		tk.Label(lbl_totales, text="IVA Interes (21.0%) $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 23+var_subir, width = 130)
		tk.Label(lbl_totales, text="Total gastos $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 46+var_subir, width = 130)
		tk.Label(lbl_totales, text="IVA gastos $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 69+var_subir, width = 130)

		lbl_ivaHacienda = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_ivaHacienda.place(x=545, y=0, width=97)
		lbl_ivaHacienda.config(textvariable=texto_ivaHacienda)

		lbl_ivaInteres = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_ivaInteres.place(x=545, y=23, width=97)
		lbl_ivaInteres.config(textvariable=texto_ivaInteres)

		lbl_gastos = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_gastos.place(x=545, y=46, width=97)
		lbl_gastos.config(textvariable=texto_gastos)

		lbl_gastosIva = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_gastosIva.place(x=545, y=69, width=97)
		lbl_gastosIva.config(textvariable=texto_gastosIva)



		lbl_alicuotaDescuento = tk.Label(lbl_totales, font=("Helvetica Neue",8), anchor="w", backgroun="#E0F8F1")
		lbl_alicuotaDescuento.place(x=var_x+130, y=26, width=40)
		lbl_alicuotaDescuento.config(textvariable=texto_alicuotaDescuento)

		lbl_alicuotaInteres = tk.Label(lbl_totales, font=("Helvetica Neue",8), anchor="w", backgroun="#E0F8F1")
		lbl_alicuotaInteres.place(x=145, y=72, width=50)
		lbl_alicuotaInteres.config(textvariable=texto_alicuotaInteres)

		lbl_alicuotaInteresDias = tk.Label(lbl_totales, font=("Helvetica Neue",8), anchor="w", backgroun="#E0F8F1")
		lbl_alicuotaInteresDias.place(x=200, y=72, width=40)
		lbl_alicuotaInteresDias.config(textvariable=texto_alicuotaInteresDias)

		lbl_alicuotaComision = tk.Label(lbl_totales, font=("Helvetica Neue",15, "bold"), anchor="w", backgroun="#E0F8F1", foreground = "#FF0000")
		lbl_alicuotaComision.place(x=100, y=95, width=60)
		lbl_alicuotaComision.config(textvariable=texto_alicuotaComision)



		diccionario_objetos["compras_texto_martillo"] = texto_martillo
		diccionario_objetos["compras_texto_descuento"] = texto_descuento
		diccionario_objetos["compras_texto_subtotal"] = texto_subtotal
		diccionario_objetos["compras_texto_interes"] = texto_interes
		diccionario_objetos["compras_texto_comisionIva"] = texto_comisionIva
		diccionario_objetos["compras_texto_retencion"] = texto_retencion
		diccionario_objetos["compras_texto_total"] = texto_total
		diccionario_objetos["compras_texto_ivaHacienda"] = texto_ivaHacienda
		diccionario_objetos["compras_texto_ivaInteres"] = texto_ivaInteres
		diccionario_objetos["compras_texto_gastos"] = texto_gastos
		diccionario_objetos["compras_texto_gastosIva"] = texto_gastosIva

		diccionario_objetos["texto_alicuotaDescuento"] = texto_alicuotaDescuento
		diccionario_objetos["texto_alicuotaInteres"] = texto_alicuotaInteres
		diccionario_objetos["texto_alicuotaInteresDias"] = texto_alicuotaInteresDias
		diccionario_objetos["texto_alicuotaComision"] = texto_alicuotaComision

	#ACCIONES
	if(True):
		btn_financiacion = tk.Button(lbl_acciones, text="Plan de\npagos", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: ventanaPlanDePagos.planDePagos(diccionario_observacionesCompras, cargarTablaObservacionesCompras, fechaActual))
		btn_financiacion.place(x = 5, y = 5, width = 110, height = 70)


		btn_receptorLiquidacionCompra = tk.Button(lbl_acciones, text="Receptor", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: receptorLiquidacionCompra())
		btn_receptorLiquidacionCompra.place(x = 120, y = 5, width = 110, height = 20)

		btn_remateLiquidacionCompra = tk.Button(lbl_acciones, text="Remate", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: remateLiquidacionCompra())
		btn_remateLiquidacionCompra.place(x = 120, y = 30, width = 110, height = 20)

		btn_firmaLiquidacionCompra = tk.Button(lbl_acciones, text="Firma", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: firmaLiquidacionCompra())
		btn_firmaLiquidacionCompra.place(x = 120, y = 55, width = 110, height = 20)


		btn_imprimirLiquidacionCompra = tk.Button(lbl_acciones, text="Imprimir\nPre-Liquidacion\nde COMPRAS", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: preLiquidacionDeCompra())
		btn_imprimirLiquidacionCompra.place(x = 235, y = 5, width = 110, height = 70)

		btn_agregarGasto = tk.Button(lbl_acciones, text="Agregar\nGasto\nde Compras", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: agregarGasto())
		btn_agregarGasto.place(x = 350, y = 5, width = 110, height = 70)

		btn_guardar = tk.Button(lbl_acciones, text="GUARDAR", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: guardarLiquidaciones())
		btn_guardar.place(x = 465, y = 5, width = 110, height = 70)

		btn_alicuotas = tk.Button(lbl_acciones, text="Alicuotas\nde Compras", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: alicuotas())
		btn_alicuotas.place(x = 580, y = 5, width = 110, height = 70)
def labelVentas(label_ventas):
	lbl_tablaVentas = tk.LabelFrame(label_ventas, text="VENTAS", backgroun="#E0F8F1")
	lbl_tablaVentas.place(x = 5, y = 5, width = 955, height = 200)

	lbl_tablaGastos = tk.LabelFrame(label_ventas, text="GASTOS", backgroun="#E0F8F1")
	lbl_tablaGastos.place(x = 5, y = 210, width = 955, height = 200)

	lbl_tablaObservaciones = tk.LabelFrame(label_ventas, text="Financiacion", backgroun="#E0F8F1")
	lbl_tablaObservaciones.place(x = 5, y = 415, width = 300, height = 160)

	lbl_totales = tk.LabelFrame(label_ventas, text="TOTALES", backgroun="#E0F8F1")
	lbl_totales.place(x = 310, y = 415, width = 650, height = 160)

	lbl_acciones = tk.LabelFrame(label_ventas, text="Acciones", backgroun="#E0F8F1")
	lbl_acciones.place(x = 5, y = 575, width = 955, height = 100)

	#TABLA VENTAS
	if(True):
		sbr_ventas = Scrollbar(lbl_tablaVentas)
		sbr_ventas.pack(side=RIGHT, fill="y")

		tabla_ventas = ttk.Treeview(lbl_tablaVentas, columns=("comprador", "corral", "categoria", "um", "cantidad", "precio_um", "bruto", "porcentaje_iva", "precio_iva"), selectmode=tk.BROWSE, show='headings') 
		tabla_ventas.pack(side=LEFT, fill="both", expand=True)
		sbr_ventas.config(command=tabla_ventas.yview)
		tabla_ventas.config(yscrollcommand=sbr_ventas.set)

		tabla_ventas.heading("comprador", text="Comprador", command=lambda: treeview_sort_column(tabla_ventas, "comprador", False))
		tabla_ventas.heading("corral", text="Corral", command=lambda: treeview_sort_column(tabla_ventas, "corral", False))
		tabla_ventas.heading("categoria", text="Categoria", command=lambda: treeview_sort_column(tabla_ventas, "categoria", False))
		tabla_ventas.heading("um", text="UM", command=lambda: treeview_sort_column(tabla_ventas, "um", False))
		tabla_ventas.heading("cantidad", text="Cantidad", command=lambda: treeview_sort_column(tabla_ventas, "cantidad", False))
		tabla_ventas.heading("precio_um", text="$ UM", command=lambda: treeview_sort_column(tabla_ventas, "precio_um", False))
		tabla_ventas.heading("bruto", text="Bruto", command=lambda: treeview_sort_column(tabla_ventas, "bruto", False))
		tabla_ventas.heading("porcentaje_iva", text="% IVA", command=lambda: treeview_sort_column(tabla_ventas, "porcentaje_iva", False))
		tabla_ventas.heading("precio_iva", text="$ IVA", command=lambda: treeview_sort_column(tabla_ventas, "precio_iva", False))

		tabla_ventas.column("comprador", width=100)
		tabla_ventas.column("corral", width=10)
		tabla_ventas.column("categoria", width=100)
		tabla_ventas.column("um", width=10)
		tabla_ventas.column("cantidad", width=10)
		tabla_ventas.column("precio_um", width=10)
		tabla_ventas.column("bruto", width=10)
		tabla_ventas.column("porcentaje_iva", width=10)
		tabla_ventas.column("precio_iva", width=10)

		diccionario_objetos["tabla_ventas"] = tabla_ventas

	#TABLA GASTOS
	if(True):
		sbr_ventasGastos = Scrollbar(lbl_tablaGastos)
		sbr_ventasGastos.pack(side=RIGHT, fill="y")

		tabla_ventasGastos = ttk.Treeview(lbl_tablaGastos, columns=("gasto", "base_imponible", "alicuota", "importe", "porcentaje_iva", "precio_iva"), selectmode=tk.BROWSE, show='headings') 
		tabla_ventasGastos.pack(side=LEFT, fill="both", expand=True)
		sbr_ventasGastos.config(command=tabla_ventasGastos.yview)
		tabla_ventasGastos.config(yscrollcommand=sbr_ventasGastos.set)

		tabla_ventasGastos.heading("gasto", text="Gastos", command=lambda: treeview_sort_column(tabla_ventasGastos, "gasto", False))
		tabla_ventasGastos.heading("base_imponible", text="Base Imponible $", command=lambda: treeview_sort_column(tabla_ventasGastos, "base_imponible", False))
		tabla_ventasGastos.heading("alicuota", text="Alicuota %", command=lambda: treeview_sort_column(tabla_ventasGastos, "alicuota", False))
		tabla_ventasGastos.heading("importe", text="Importe $", command=lambda: treeview_sort_column(tabla_ventasGastos, "importe", False))
		tabla_ventasGastos.heading("porcentaje_iva", text="IVA %", command=lambda: treeview_sort_column(tabla_ventasGastos, "porcentaje_iva", False))
		tabla_ventasGastos.heading("precio_iva", text="IVA $", command=lambda: treeview_sort_column(tabla_ventasGastos, "precio_iva", False))

		tabla_ventasGastos.column("gasto", width=200)
		tabla_ventasGastos.column("base_imponible", width=100)
		tabla_ventasGastos.column("alicuota", width=165)
		tabla_ventasGastos.column("importe", width=100)
		tabla_ventasGastos.column("porcentaje_iva", width=100)
		tabla_ventasGastos.column("precio_iva", width=100)

		diccionario_objetos["tabla_ventasGastos"] = tabla_ventasGastos

	#TABLA Financiacion
	if(True):
		sbr_ventasObservaciones = Scrollbar(lbl_tablaObservaciones)
		sbr_ventasObservaciones.pack(side=RIGHT, fill="y")

		tabla_ventasObservaciones = ttk.Treeview(lbl_tablaObservaciones, columns=("cuota", "fecha", "importe"), selectmode=tk.BROWSE, show='headings') 
		tabla_ventasObservaciones.pack(side=LEFT, fill="both", expand=True)
		sbr_ventasObservaciones.config(command=tabla_ventasObservaciones.yview)
		tabla_ventasObservaciones.config(yscrollcommand=sbr_ventasObservaciones.set)

		tabla_ventasObservaciones.heading("cuota", text="Cuota", command=lambda: treeview_sort_column(tabla_ventasObservaciones, "cuota", False))
		tabla_ventasObservaciones.heading("fecha", text="Fecha", command=lambda: treeview_sort_column(tabla_ventasObservaciones, "fecha", False))
		tabla_ventasObservaciones.heading("importe", text="Importe $", command=lambda: treeview_sort_column(tabla_ventasObservaciones, "importe", False))


		tabla_ventasObservaciones.column("cuota", width=10)
		tabla_ventasObservaciones.column("fecha", width=10)
		tabla_ventasObservaciones.column("importe", width=10)

		diccionario_objetos["tabla_ventasObservaciones"] = tabla_ventasObservaciones

	#TOTALES
	if(True):
		var_subir = +3
		var_x = 70
		tk.Label(lbl_totales, text="Subtotal Martillo $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 0+var_subir, width = 180)
		tk.Label(lbl_totales, text="$", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 175+var_x, y = 23+var_subir, width = 10)
		tk.Label(lbl_totales, text="Descuento pago contado %", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = var_x-50, y = 23+var_subir, width = 180)
		tk.Label(lbl_totales, text="Subtotal $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 46+var_subir, width = 180)
		tk.Label(lbl_totales, text="$", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 175+var_x, y = 69+var_subir, width = 10)
		tk.Label(lbl_totales, text="Int. dias de pago dif. %", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = var_x-70, y = 69+var_subir, width = 140)
		tk.Label(lbl_totales, text="Comision+IVA $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 92+var_subir, width = 180)
		tk.Label(lbl_totales, text="Comision %", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = var_x-70, y = 98+var_subir, width = 100)
		tk.Label(lbl_totales, text="Retencion IIBB $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5+var_x, y = 115+var_subir, width = 180)

		texto_martillo = StringVar()
		texto_descuento = StringVar()
		texto_subtotal = StringVar()
		texto_interes = StringVar()
		texto_comisionIva = StringVar()
		texto_retencion = StringVar()
		texto_total = StringVar()
		texto_ivaHacienda = StringVar()
		texto_ivaInteres = StringVar()
		texto_alicuotaDescuento = StringVar()
		texto_alicuotaInteres = StringVar()
		texto_alicuotaInteresDias = StringVar()
		texto_alicuotaComision = StringVar()
		texto_gastos = StringVar()
		texto_gastosIva = StringVar()
		TEXTOCOMISION = StringVar()


		texto_martillo.set("")
		texto_descuento.set("")
		texto_subtotal.set("")
		texto_interes.set("")
		texto_comisionIva.set("")
		texto_retencion.set("")
		texto_total.set("")
		texto_ivaHacienda.set("")
		texto_ivaInteres.set("")
		texto_alicuotaDescuento.set(diccionario_valores["alicuotaDescuento"])
		texto_alicuotaInteres.set(diccionario_valores["alicuotaInteres"])
		texto_alicuotaInteresDias.set(diccionario_valores["alicuotaInteresDias"])
		texto_alicuotaComision.set(diccionario_valores["alicuotaComision"])
		texto_gastos.set("")
		texto_gastosIva.set("")


		lbl_martillo = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_martillo.place(x=185+var_x, y=0, width=100)
		lbl_martillo.config(textvariable=texto_martillo)

		lbl_descuento = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_descuento.place(x=185+var_x, y=23, width=100)
		lbl_descuento.config(textvariable=texto_descuento)

		lbl_subtotal = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_subtotal.place(x=185+var_x, y=46, width=100)
		lbl_subtotal.config(textvariable=texto_subtotal)

		lbl_interes = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_interes.place(x=185+var_x, y=69, width=100)
		lbl_interes.config(textvariable=texto_interes)

		lbl_comisionIva = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_comisionIva.place(x=185+var_x, y=92, width=100)
		lbl_comisionIva.config(textvariable=texto_comisionIva)

		lbl_retencion = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_retencion.place(x=185+var_x, y=115, width=100)
		lbl_retencion.config(textvariable=texto_retencion)

		varx_total = 30
		tk.Label(lbl_totales, text="TOTAL LIQUIDADO $", font=("Helvetica Neue",12, "bold"), backgroun="#E0F8F1", anchor="c").place(x = 300+varx_total, y = 110+var_subir, width = 160)

		lbl_total = tk.Label(lbl_totales, font=("Helvetica Neue",18,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_total.place(x=460+varx_total, y=106, width=155)
		lbl_total.config(textvariable=texto_total)

		tk.Label(lbl_totales, text="IVA Hacienda (10.5%) $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 0+var_subir, width = 130)
		tk.Label(lbl_totales, text="IVA Interes (21.0%) $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 23+var_subir, width = 130)
		tk.Label(lbl_totales, text="Total gastos $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 46+var_subir, width = 130)
		tk.Label(lbl_totales, text="IVA gastos $", font=("Helvetica Neue",8, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 415, y = 69+var_subir, width = 130)

		lbl_ivaHacienda = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_ivaHacienda.place(x=545, y=0, width=97)
		lbl_ivaHacienda.config(textvariable=texto_ivaHacienda)

		lbl_ivaInteres = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_ivaInteres.place(x=545, y=23, width=97)
		lbl_ivaInteres.config(textvariable=texto_ivaInteres)

		lbl_gastos = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_gastos.place(x=545, y=46, width=97)
		lbl_gastos.config(textvariable=texto_gastos)

		lbl_gastosIva = tk.Label(lbl_totales, font=("Helvetica Neue",12,"bold"), anchor="w", backgroun="#E0F8F1")
		lbl_gastosIva.place(x=545, y=69, width=97)
		lbl_gastosIva.config(textvariable=texto_gastosIva)



		lbl_alicuotaDescuento = tk.Label(lbl_totales, font=("Helvetica Neue",8), anchor="w", backgroun="#E0F8F1")
		lbl_alicuotaDescuento.place(x=var_x+130, y=26, width=40)
		lbl_alicuotaDescuento.config(textvariable=texto_alicuotaDescuento)

		lbl_alicuotaInteres = tk.Label(lbl_totales, font=("Helvetica Neue",8), anchor="w", backgroun="#E0F8F1")
		lbl_alicuotaInteres.place(x=145, y=72, width=50)
		lbl_alicuotaInteres.config(textvariable=texto_alicuotaInteres)

		lbl_alicuotaInteresDias = tk.Label(lbl_totales, font=("Helvetica Neue",8), anchor="w", backgroun="#E0F8F1")
		lbl_alicuotaInteresDias.place(x=200, y=72, width=40)
		lbl_alicuotaInteresDias.config(textvariable=texto_alicuotaInteresDias)

		lbl_alicuotaComision = tk.Label(lbl_totales, font=("Helvetica Neue",15, "bold"), anchor="w", backgroun="#E0F8F1", foreground = "#FF0000")
		lbl_alicuotaComision.place(x=100, y=95, width=60)
		lbl_alicuotaComision.config(textvariable=texto_alicuotaComision)



		diccionario_objetos["ventas_texto_martillo"] = texto_martillo
		diccionario_objetos["ventas_texto_descuento"] = texto_descuento
		diccionario_objetos["ventas_texto_subtotal"] = texto_subtotal
		diccionario_objetos["ventas_texto_interes"] = texto_interes
		diccionario_objetos["ventas_texto_comisionIva"] = texto_comisionIva
		diccionario_objetos["ventas_texto_retencion"] = texto_retencion
		diccionario_objetos["ventas_texto_total"] = texto_total
		diccionario_objetos["ventas_texto_ivaHacienda"] = texto_ivaHacienda
		diccionario_objetos["ventas_texto_ivaInteres"] = texto_ivaInteres
		diccionario_objetos["ventas_texto_gastos"] = texto_gastos
		diccionario_objetos["ventas_texto_gastosIva"] = texto_gastosIva

		diccionario_objetos["ventas_texto_alicuotaDescuento"] = texto_alicuotaDescuento
		diccionario_objetos["ventas_texto_alicuotaInteres"] = texto_alicuotaInteres
		diccionario_objetos["ventas_texto_alicuotaInteresDias"] = texto_alicuotaInteresDias
		diccionario_objetos["ventas_texto_alicuotaComision"] = texto_alicuotaComision
		diccionario_objetos["TEXTOCOMISION"] = TEXTOCOMISION
		

	#ACCIONES
	if(True):
		btn_financiacion = tk.Button(lbl_acciones, text="Plan de\npagos", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: ventanaPlanDePagos.planDePagos(diccionario_observacionesVentas, cargarTablaObservacionesVentas, fechaActual))
		btn_financiacion.place(x = 5, y = 5, width = 110, height = 70)


		btn_receptorLiquidacionCompra = tk.Button(lbl_acciones, text="Receptor", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: receptorLiquidacionCompra())
		btn_receptorLiquidacionCompra.place(x = 120, y = 5, width = 110, height = 20)

		btn_remateLiquidacionCompra = tk.Button(lbl_acciones, text="Remate", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: remateLiquidacionCompra())
		btn_remateLiquidacionCompra.place(x = 120, y = 30, width = 110, height = 20)

		btn_firmaLiquidacionCompra = tk.Button(lbl_acciones, text="Firma", font=("Helvetica Neue",10, "bold"), backgroun="#fffd9e", command= lambda: firmaLiquidacionCompra())
		btn_firmaLiquidacionCompra.place(x = 120, y = 55, width = 110, height = 20)


		btn_imprimirLiquidacionCompra = tk.Button(lbl_acciones, text="Imprimir\nPre-Liquidacion\nde VENTAS", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: preLiquidacionDeVenta())
		btn_imprimirLiquidacionCompra.place(x = 235, y = 5, width = 110, height = 70)

		btn_agregarGasto = tk.Button(lbl_acciones, text="Agregar\nGasto\nde Ventas", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: agregarGastoVentas())
		btn_agregarGasto.place(x = 350, y = 5, width = 110, height = 70)

		btn_guardar = tk.Button(lbl_acciones, text="GUARDAR", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: guardarLiquidaciones())
		btn_guardar.place(x = 465, y = 5, width = 110, height = 70)

		btn_alicuotas = tk.Button(lbl_acciones, text="Alicuotas\nde Ventas", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: alicuotasVentas())
		btn_alicuotas.place(x = 580, y = 5, width = 110, height = 70)

		btn_retencion = tk.Button(lbl_acciones, text="Agregar\nretención\nIIBB", font=("Helvetica Neue",10, "bold"), backgroun="#a4ff9e", command= lambda: retencionVentas(float(TEXTOCOMISION.get())))
		btn_retencion.place(x = 695, y = 5, width = 110, height = 70)


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

		entities = [x_lote,
		x_comprador,
		x_precio,
		x_remate,
		x_estado]

		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO compraventa VALUES(NULL, ?, ?, ?, ?, ?)", entities)
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

#PRELIQUIDACIONES
def receptorLiquidacionCompra():
	windowReceptor = Tk()
	windowReceptor.title("Datos del Receptor")
	windowReceptor.geometry("500x500")
	windowReceptor.config(backgroun="#E0F8F1")

	tk.Label(windowReceptor, text="CUIT", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 5, width = 180)
	tk.Label(windowReceptor, text="Nombre y apellido", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 35, width = 180)
	tk.Label(windowReceptor, text="Situacion IVA", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 65, width = 180)
	tk.Label(windowReceptor, text="N° IIBB", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 95, width = 180)
	tk.Label(windowReceptor, text="Caracter", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 125, width = 180)
	tk.Label(windowReceptor, text="Domicilio", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 155, width = 180)
	tk.Label(windowReceptor, text="Localidad", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 185, width = 180)
	tk.Label(windowReceptor, text="Provincia", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 215, width = 180)
	tk.Label(windowReceptor, text="Codigo postal", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 245, width = 180)
	tk.Label(windowReceptor, text="N° Renspa", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 275, width = 180)
	tk.Label(windowReceptor, text="N° RUCA", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 305, width = 180)
	tk.Label(windowReceptor, text="Telefono", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 335, width = 180)

	entry_cuit = Entry(windowReceptor)
	entry_cuit.place(x = 200, y = 5, width = 280)

	entry_nombre = Entry(windowReceptor)
	entry_nombre.place(x = 200, y = 36, width = 280)

	entry_iva = Entry(windowReceptor)
	entry_iva.place(x = 200, y = 65, width = 280)

	entry_iibb = Entry(windowReceptor)
	entry_iibb.place(x = 200, y = 95, width = 280)

	entry_caracter = Entry(windowReceptor)
	entry_caracter.place(x = 200, y = 125, width = 280)

	entry_domicilio = Entry(windowReceptor)
	entry_domicilio.place(x = 200, y = 155, width = 280)

	entry_localidad = Entry(windowReceptor)
	entry_localidad.place(x = 200, y = 185, width = 280)

	entry_provincia = Entry(windowReceptor)
	entry_provincia.place(x = 200, y = 215, width = 280)

	entry_postal = Entry(windowReceptor)
	entry_postal.place(x = 200, y = 245, width = 280)

	entry_renspa = Entry(windowReceptor)
	entry_renspa.place(x = 200, y = 275, width = 280)

	entry_ruca = Entry(windowReceptor)
	entry_ruca.place(x = 200, y = 305, width = 280)

	entry_telefono = Entry(windowReceptor)
	entry_telefono.place(x=200, y=335, width = 280)

	entry_cuit.delete(0, tk.END)
	entry_nombre.delete(0, tk.END)
	entry_iva.delete(0, tk.END)
	entry_iibb.delete(0, tk.END)
	entry_caracter.delete(0, tk.END)
	entry_domicilio.delete(0, tk.END)
	entry_localidad.delete(0, tk.END)
	entry_provincia.delete(0, tk.END)
	entry_postal.delete(0, tk.END)
	entry_renspa.delete(0, tk.END)
	entry_ruca.delete(0, tk.END)
	entry_telefono.delete(0, tk.END)

	entry_cuit.insert(0, dicReceptorLiquidacionCompra["cuit"])
	entry_nombre.insert(0, dicReceptorLiquidacionCompra["nombre"])
	entry_iva.insert(0, dicReceptorLiquidacionCompra["iva"])
	entry_iibb.insert(0, dicReceptorLiquidacionCompra["iibb"])
	entry_caracter.insert(0, dicReceptorLiquidacionCompra["caracter"])
	entry_domicilio.insert(0, dicReceptorLiquidacionCompra["domicilio"])
	entry_localidad.insert(0, dicReceptorLiquidacionCompra["localidad"])
	entry_provincia.insert(0, dicReceptorLiquidacionCompra["provincia"])
	entry_postal.insert(0, dicReceptorLiquidacionCompra["postal"])
	entry_renspa.insert(0, dicReceptorLiquidacionCompra["renspa"])
	entry_ruca.insert(0, dicReceptorLiquidacionCompra["ruca"])
	entry_telefono.insert(0, dicReceptorLiquidacionCompra["telefono"])


	def guardarDatosComprador():
		dicReceptorLiquidacionCompra["cuit"] = entry_cuit.get()
		dicReceptorLiquidacionCompra["nombre"] = entry_nombre.get()
		dicReceptorLiquidacionCompra["iva"] = entry_iva.get()
		dicReceptorLiquidacionCompra["iibb"] = entry_iibb.get()
		dicReceptorLiquidacionCompra["caracter"] = entry_caracter.get()
		dicReceptorLiquidacionCompra["domicilio"] = entry_domicilio.get()
		dicReceptorLiquidacionCompra["localidad"] = entry_localidad.get()
		dicReceptorLiquidacionCompra["provincia"] = entry_provincia.get()
		dicReceptorLiquidacionCompra["postal"] = entry_postal.get()
		dicReceptorLiquidacionCompra["renspa"] = entry_renspa.get()
		dicReceptorLiquidacionCompra["ruca"] = entry_ruca.get()
		dicReceptorLiquidacionCompra["telefono"] = entry_telefono.get()

		windowReceptor.destroy()

	btn_guardar = tk.Button(windowReceptor, text="GUARDAR", font=("verdana",15, "bold"), backgroun="#76f5b7", command=guardarDatosComprador)
	btn_guardar.place(x = 170, y = 400, width=150, height=70)

	windowReceptor.mainloop()
def remateLiquidacionCompra():
	windowRemate = Tk()
	windowRemate.title("Datos del Remate")
	windowRemate.geometry("500x330")
	windowRemate.config(backgroun="#E0F8F1")

	tk.Label(windowRemate, text="FECHA", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 5, width = 180)
	tk.Label(windowRemate, text="TIPO DOCUMENTO", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 35, width = 180)
	tk.Label(windowRemate, text="NUMERO DOCUMENTO", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 65, width = 180)
	tk.Label(windowRemate, text="TITULO REMATE", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 95, width = 180)
	tk.Label(windowRemate, text="CONDICION DE PAGO", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 125, width = 180)
	tk.Label(windowRemate, text="DESTINO TROPA", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 155, width = 180)

	entry_fecha = Entry(windowRemate)
	entry_fecha.place(x = 200, y = 5, width = 280)

	entry_tipoDocumento = Entry(windowRemate)
	entry_tipoDocumento.place(x = 200, y = 36, width = 280)

	entry_numeroDocumento = Entry(windowRemate)
	entry_numeroDocumento.place(x = 200, y = 65, width = 280)

	entry_titulo = Entry(windowRemate)
	entry_titulo.place(x = 200, y = 95, width = 280)

	entry_condicion = Entry(windowRemate)
	entry_condicion.place(x = 200, y = 125, width = 280)

	entry_destino = Entry(windowRemate)
	entry_destino.place(x = 200, y = 155, width = 280)

	entry_fecha.delete(0, tk.END)
	entry_tipoDocumento.delete(0, tk.END)
	entry_numeroDocumento.delete(0, tk.END)
	entry_titulo.delete(0, tk.END)
	entry_condicion.delete(0, tk.END)
	entry_destino.delete(0, tk.END)


	entry_fecha.insert(0, dicRemateLiquidacionCompra["fecha"])
	entry_tipoDocumento.insert(0, dicRemateLiquidacionCompra["tipoDocumento"])
	entry_numeroDocumento.insert(0, dicRemateLiquidacionCompra["numeroDocumento"])
	entry_titulo.insert(0, dicRemateLiquidacionCompra["titulo"])
	entry_condicion.insert(0, dicRemateLiquidacionCompra["condicion"])
	entry_destino.insert(0, dicRemateLiquidacionCompra["destino"])

	def guardarDatosRemate():
		dicRemateLiquidacionCompra["fecha"] = entry_fecha.get()
		dicRemateLiquidacionCompra["tipoDocumento"] = entry_tipoDocumento.get()
		dicRemateLiquidacionCompra["numeroDocumento"] = entry_numeroDocumento.get()
		dicRemateLiquidacionCompra["titulo"] = entry_titulo.get()
		dicRemateLiquidacionCompra["condicion"] = entry_condicion.get()
		dicRemateLiquidacionCompra["destino"] = entry_destino.get()

		windowRemate.destroy()

	btn_guardar = tk.Button(windowRemate, text="GUARDAR", font=("verdana",15, "bold"), backgroun="#76f5b7", command=guardarDatosRemate)
	btn_guardar.place(x = 170, y = 230, width=150, height=70)

	windowRemate.mainloop()
def firmaLiquidacionCompra():
	windowFirma = Tk()
	windowFirma.title("Datos del Representante")
	windowFirma.geometry("500x200")
	windowFirma.config(backgroun="#E0F8F1")

	tk.Label(windowFirma, text="Nombre", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 5, width = 180)
	tk.Label(windowFirma, text="CUIT", font=("Helvetica Neue",10, "bold"), backgroun="#E0F8F1", anchor="e").place(x = 5, y = 35, width = 180)

	entry_nombre = Entry(windowFirma)
	entry_nombre.place(x = 200, y = 5, width = 280)

	entry_cuit = Entry(windowFirma)
	entry_cuit.place(x = 200, y = 36, width = 280)


	entry_nombre.delete(0, tk.END)
	entry_cuit.delete(0, tk.END)


	entry_nombre.insert(0, dicFirmaLiquidacionCompra["nombre"])
	entry_cuit.insert(0, dicFirmaLiquidacionCompra["cuit"])


	def guardarDatosFirma():
		dicFirmaLiquidacionCompra["nombre"] = entry_nombre.get()
		dicFirmaLiquidacionCompra["cuit"] = entry_cuit.get()

		windowFirma.destroy()

	btn_guardar = tk.Button(windowFirma, text="GUARDAR", font=("verdana",15, "bold"), backgroun="#76f5b7", command=guardarDatosFirma)
	btn_guardar.place(x = 170, y = 100, width=150, height=70)

	windowFirma.mainloop()

def preLiquidacionDeCompra():
	diccionarioEnviar = {}

	try:
		dire = filedialog.askdirectory()
		dire = dire + "/PreLiquidacion de Compra " + fechaActual + " " + str(dicReceptorLiquidacionCompra["nombre"]) +".pdf"

		diccionarioDatos = {
		"ruta" : dire,	
		"fecha" : dicRemateLiquidacionCompra["fecha"],
		"tipoDocumento" : dicRemateLiquidacionCompra["tipoDocumento"],
		"numeroDocumento" : dicRemateLiquidacionCompra["numeroDocumento"],
		"remate" : dicRemateLiquidacionCompra["titulo"],
		"condicion" : dicRemateLiquidacionCompra["condicion"],
		"destino" : dicRemateLiquidacionCompra["destino"],
		"titulo" : "Pre-Liquidacion de compra de " + str(dicReceptorLiquidacionCompra["nombre"]),
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del remate")
		return 0

	try:
		diccionarioReceptor = {
		"CUIT" : dicReceptorLiquidacionCompra["cuit"],
		"situacionIVA" : dicReceptorLiquidacionCompra["iva"],
		"domicilio" : dicReceptorLiquidacionCompra["domicilio"],
		"codpostal" : dicReceptorLiquidacionCompra["postal"],
		"nombreyapellido" : dicReceptorLiquidacionCompra["nombre"],
		"IIBB" : dicReceptorLiquidacionCompra["iibb"],
		"localidad" : dicReceptorLiquidacionCompra["localidad"],
		"renspa" : dicReceptorLiquidacionCompra["renspa"],
		"caracter" : dicReceptorLiquidacionCompra["caracter"],
		"provincia" : dicReceptorLiquidacionCompra["provincia"],
		"ruca" : dicReceptorLiquidacionCompra["ruca"],
		"DTE" : "",
		"contacto" : dicReceptorLiquidacionCompra["telefono"],
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del receptor")
		return 0
	try:
		diccionarioEmisor = {
		"CUIT" : dicFirmaLiquidacionCompra["cuit"],
		"nombreyapellido" : dicFirmaLiquidacionCompra["nombre"],
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del emisor (firmas)")
		return 0

	try:
		diccionarioConceptos = {}
		tabla = diccionario_objetos["tabla_compras"]
		j=0
		for i in tabla.get_children():
			diccionarioConceptos[str(j)] = {
			"cliente" : tabla.item(i)["values"][0],
			"categoria" : str(tabla.item(i)["values"][2]),
			"um" : str(tabla.item(i)["values"][3]),
			"cantidad" : str(tabla.item(i)["values"][4]),
			"$um" : str(tabla.item(i)["values"][5]),
			"$bruto" : str(tabla.item(i)["values"][6]),
			"iva" : str(tabla.item(i)["values"][7]),
			"$iva" : str(tabla.item(i)["values"][8]),
			}
			j += 1
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de los conceptos")
		return 0

	try:
		diccionarioGastos = {}
		tabla = diccionario_objetos["tabla_comprasGastos"]

		llaves = list(diccionario_gastos.keys())

		for i in range(0, len(diccionario_gastos)):
			diccionarioGastos[str(i)] = {
			"gastos" : str(diccionario_gastos[llaves[i]]["gasto"]),
			"base" : str(diccionario_gastos[llaves[i]]["base"]),
			"alicuota" : str(diccionario_gastos[llaves[i]]["alicuota"]),
			"importe" : str(diccionario_gastos[llaves[i]]["importe"]),
			"iva" : str(diccionario_gastos[llaves[i]]["porcentajeIva"]),
			"$iva" : str(diccionario_gastos[llaves[i]]["precioIva"]),
			}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de los gastos")
		return 0


	try:
		interesPorcentaje = str(diccionario_objetos["texto_alicuotaInteres"].get())
		interesDias = str(diccionario_objetos["texto_alicuotaInteresDias"].get())
		ivaHaciendaPorcentaje = str("10.5")
		ivaInteresPorcentaje = str("21.0")
		subtotalMartillo = str(diccionario_objetos["compras_texto_martillo"].get())
		descuento = str(diccionario_objetos["compras_texto_descuento"].get())
		subtotal = str(diccionario_objetos["compras_texto_subtotal"].get())
		interes = str(diccionario_objetos["compras_texto_interes"].get())
		ivaHacienda = str(diccionario_objetos["compras_texto_ivaHacienda"].get())
		ivaInteres = str(diccionario_objetos["compras_texto_ivaInteres"].get())
		comisionIva = str(diccionario_objetos["compras_texto_comisionIva"].get())
		retencion = str(diccionario_objetos["compras_texto_retencion"].get())
		total = str(diccionario_objetos["compras_texto_total"].get())

		diccionarioTotales = {
		"interesPorcentaje" : interesPorcentaje,
		"interesDias" : interesDias,
		"ivaHaciendaPorcentaje" : ivaHaciendaPorcentaje,
		"ivaInteresPorcentaje" : ivaInteresPorcentaje,
		"subtotalMartillo" : subtotalMartillo,
		"descuento" : descuento,
		"subtotal" : subtotal,
		"interes" : interes,
		"ivaHacienda" : ivaHacienda,
		"ivaInteres" : ivaInteres,
		"comisionIva" : comisionIva,
		"retencion" : retencion,
		"total" : total,
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de Totales")
		return 0

	try:
		diccionarioObservaciones = {}
		tabla = diccionario_objetos["tabla_comprasObservaciones"]
		j=0
		for i in tabla.get_children():
			diccionarioObservaciones[str(j)] = {
			"cuota" : str(tabla.item(i)["values"][0]),
			"fecha" : str(tabla.item(i)["values"][1]),
			"monto" : str(tabla.item(i)["values"][2]),
			}
			j += 1
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de las observaciones")
		return 0


	diccionarioEnviar["datos"] = diccionarioDatos
	diccionarioEnviar["receptor"] = diccionarioReceptor
	diccionarioEnviar["emisor"] = diccionarioEmisor
	diccionarioEnviar["conceptos"] = diccionarioConceptos
	diccionarioEnviar["gastos"] = diccionarioGastos
	diccionarioEnviar["totales"] = diccionarioTotales
	diccionarioEnviar["observaciones"] = diccionarioObservaciones

	pdf_preliquidacion.preliquidacionPDF(diccionarioEnviar)
def preLiquidacionDeVenta():
	diccionarioEnviar = {}

	try:
		dire = filedialog.askdirectory()
		dire = dire + "/PreLiquidacion de Venta " + fechaActual + " " + str(dicReceptorLiquidacionCompra["nombre"]) +".pdf"
		diccionarioDatos = {
		"ruta" : dire,	
		"fecha" : dicRemateLiquidacionCompra["fecha"],
		"tipoDocumento" : "PRE-LIQUIDACION DE VENTA",
		"numeroDocumento" : dicRemateLiquidacionCompra["numeroDocumento"],
		"remate" : dicRemateLiquidacionCompra["titulo"],
		"condicion" : dicRemateLiquidacionCompra["condicion"],
		"destino" : dicRemateLiquidacionCompra["destino"],
		"titulo" : "Pre-Liquidacion de venta de " + str(dicReceptorLiquidacionCompra["nombre"]),
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del remate")
		return 0

	try:
		diccionarioReceptor = {
		"CUIT" : dicReceptorLiquidacionCompra["cuit"],
		"situacionIVA" : dicReceptorLiquidacionCompra["iva"],
		"domicilio" : dicReceptorLiquidacionCompra["domicilio"],
		"codpostal" : dicReceptorLiquidacionCompra["postal"],
		"nombreyapellido" : dicReceptorLiquidacionCompra["nombre"],
		"IIBB" : dicReceptorLiquidacionCompra["iibb"],
		"localidad" : dicReceptorLiquidacionCompra["localidad"],
		"renspa" : dicReceptorLiquidacionCompra["renspa"],
		"caracter" : dicReceptorLiquidacionCompra["caracter"],
		"provincia" : dicReceptorLiquidacionCompra["provincia"],
		"ruca" : dicReceptorLiquidacionCompra["ruca"],
		"DTE" : "",
		"contacto" : dicReceptorLiquidacionCompra["telefono"],
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del receptor")
		return 0
	try:
		diccionarioEmisor = {
		"CUIT" : dicFirmaLiquidacionCompra["cuit"],
		"nombreyapellido" : dicFirmaLiquidacionCompra["nombre"],
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del emisor (firmas)")
		return 0

	try:
		diccionarioConceptos = {}
		tabla = diccionario_objetos["tabla_ventas"]
		j=0
		for i in tabla.get_children():
			diccionarioConceptos[str(j)] = {
			"cliente" : tabla.item(i)["values"][0],
			"categoria" : str(tabla.item(i)["values"][2]),
			"um" : str(tabla.item(i)["values"][3]),
			"cantidad" : str(tabla.item(i)["values"][4]),
			"$um" : str(tabla.item(i)["values"][5]),
			"$bruto" : str(tabla.item(i)["values"][6]),
			"iva" : str(tabla.item(i)["values"][7]),
			"$iva" : str(tabla.item(i)["values"][8]),
			}
			j += 1
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de los conceptos")
		return 0

	try:
		diccionarioGastos = {}
		tabla = diccionario_objetos["tabla_ventasGastos"]

		llaves = list(diccionario_gastosVentas.keys())

		for i in range(0, len(diccionario_gastosVentas)):
			diccionarioGastos[str(i)] = {
			"gastos" : str(diccionario_gastosVentas[llaves[i]]["gasto"]),
			"base" : str(diccionario_gastosVentas[llaves[i]]["base"]),
			"alicuota" : str(diccionario_gastosVentas[llaves[i]]["alicuota"]),
			"importe" : str(diccionario_gastosVentas[llaves[i]]["importe"]),
			"iva" : str(diccionario_gastosVentas[llaves[i]]["porcentajeIva"]),
			"$iva" : str(diccionario_gastosVentas[llaves[i]]["precioIva"]),
			}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de los gastos")
		return 0

	try:
		interesPorcentaje = str(diccionario_objetos["ventas_texto_alicuotaInteres"].get())
		interesDias = str(diccionario_objetos["ventas_texto_alicuotaInteresDias"].get())
		ivaHaciendaPorcentaje = str("10.5")
		ivaInteresPorcentaje = str("21.0")
		subtotalMartillo = str(diccionario_objetos["ventas_texto_martillo"].get())
		descuento = str(diccionario_objetos["ventas_texto_descuento"].get())
		subtotal = str(diccionario_objetos["ventas_texto_subtotal"].get())
		interes = str(diccionario_objetos["ventas_texto_interes"].get())
		ivaHacienda = str(diccionario_objetos["ventas_texto_ivaHacienda"].get())
		ivaInteres = str(diccionario_objetos["ventas_texto_ivaInteres"].get())
		comisionIva = str(diccionario_objetos["ventas_texto_comisionIva"].get())
		retencion = str(diccionario_objetos["ventas_texto_retencion"].get())
		total = str(diccionario_objetos["ventas_texto_total"].get())


		diccionarioTotales = {
		"interesPorcentaje" : interesPorcentaje,
		"interesDias" : interesDias,
		"ivaHaciendaPorcentaje" : ivaHaciendaPorcentaje,
		"ivaInteresPorcentaje" : ivaInteresPorcentaje,
		"subtotalMartillo" : subtotalMartillo,
		"descuento" : descuento,
		"subtotal" : subtotal,
		"interes" : interes,
		"ivaHacienda" : ivaHacienda,
		"ivaInteres" : ivaInteres,
		"comisionIva" : comisionIva,
		"retencion" : retencion,
		"total" : total,
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de Totales")
		return 0

	try:
		diccionarioObservaciones = {}
		tabla = diccionario_objetos["tabla_ventasObservaciones"]
		j=0
		for i in tabla.get_children():
			diccionarioObservaciones[str(j)] = {
			"cuota" : str(tabla.item(i)["values"][0]),
			"fecha" : str(tabla.item(i)["values"][1]),
			"monto" : str(tabla.item(i)["values"][2]),
			}
			j += 1
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de las observaciones")
		return 0


	diccionarioEnviar["datos"] = diccionarioDatos
	diccionarioEnviar["receptor"] = diccionarioReceptor
	diccionarioEnviar["emisor"] = diccionarioEmisor
	diccionarioEnviar["conceptos"] = diccionarioConceptos
	diccionarioEnviar["gastos"] = diccionarioGastos
	diccionarioEnviar["totales"] = diccionarioTotales
	diccionarioEnviar["observaciones"] = diccionarioObservaciones

	pdf_preliquidacion.preliquidacionPDF(diccionarioEnviar)
	diccionarioEnviar.clear()


def exportacion(window):
	lbl_productor = Label(window, backgroun="#E0F8F1")
	lbl_productor.place(x = 2, y = 2, width = 300, height = 700)

	lbl_pestañas = Label(window, backgroun="#E0F8F1")
	lbl_pestañas.place(x = 304, y = 2, width = 978, height = 700)

	#EN LABEL PRODUCTOR
	if(True):
		labelProductorInfo(lbl_productor)
		labelProductorBuscador(lbl_productor)


	#EN LABEL PESTAÑAS
	if(True):
		pestañas = ttk.Notebook(lbl_pestañas)

		label_compras = Label(window, backgroun="#E0F8F1")
		label_ventas = Label(window, backgroun="#E0F8F1")

		pestañas.add(label_compras, text="LIQUIDACION DE COMPRA", padding = 0)
		pestañas.add(label_ventas, text="LIQUIDACION DE VENTA", padding = 0)

		pestañas.place(x = 0, y = 0, relwidth = 1, relheight = 1)

		#EN PESTAÑA LIQUIDACION DE COMPRA
		if(True):
			labelCompras(label_compras)
			labelVentas(label_ventas)




	productorFiltrar()
	actualizarProductores()
	actualizarDatosRemate()

	#MENU
	if(True):
		barraMenu = Menu(window)

		mnuArchivo = Menu(barraMenu)
		mnuArchivo.add_command(label="Abrir")
		mnuArchivo.add_command(label="Nuevo")
		mnuArchivo.add_command(label="Guardar")
		mnuArchivo.add_command(label="Cerrar")
		mnuArchivo.add_command(label="Salir")

		barraMenu.add_cascade(label="Archivo", menu = mnuArchivo)

		window.config(menu = barraMenu)

def guardarLiquidaciones():
	con = sql_connection()
	condiciones = " WHERE productor = '" + str(diccionario_objetos["texto_cuit"].get()) + "' AND remate = '" + str(rematename) + "'"
	rows = actualizar_db(con, "liquidacionesGuardadas", condiciones)

	if(len(rows) == 0):
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea guardar estas liquidaciones?', icon = 'warning')
		if(MsgBox == 'yes'):
			guardarLiquidacionesNuevo()
	else:
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea editar estas liquidaciones?', icon = 'warning')
		if(MsgBox == 'yes'):
			guardarLiquidacionesNuevo()
def guardarLiquidacionesNuevo():
	HoraMinutosSegundos = str(time.strftime("%H-%M-%S"))
	codigoUnico = str(diccionario_objetos["texto_cuit"].get()) + "_" + str(rematename) + "_" + HoraMinutosSegundos

	productor = str(diccionario_objetos["texto_cuit"].get())
	#GUARDAR LIQUIDACION CODIGO
	try:
		entities = [productor, codigoUnico, rematename]

		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO liquidacionesGuardadas VALUES(NULL, ?, ?, ?)", entities)
		con.commit()
	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Guardadas")

	#GUARDAR COMPRAS
	try:
		for i in range(0, len(dicCompras)):
			remate = rematename
			productor = str(diccionario_objetos["texto_cuit"].get())
			fecha = fechaHOY
			vendedor = dicCompras[str(i)]["productor"]
			corral = dicCompras[str(i)]["corral"]
			categoria = dicCompras[str(i)]["catHacienda"]
			um = "Cabezas"
			cantidad = dicCompras[str(i)]["cantidad"]
			precioUm = str(round((float(dicCompras[str(i)]["precio"])*float(dicCompras[str(i)]["kgBruto"]))/float(dicCompras[str(i)]["cantidad"]), 2))
			bruto = str(round(float(dicCompras[str(i)]["precio"])*float(dicCompras[str(i)]["kgBruto"]), 2))
			porcentajeIva = "10.5"
			precioIva = str(round(float(bruto)*0.105, 2))

			entities = [
			remate,
			productor,
			fecha,
			vendedor,
			corral,
			categoria,
			um,
			cantidad,
			precioUm,
			bruto,
			porcentajeIva,
			precioIva,
			codigoUnico
			]

			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO liquidacionCompras VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
			con.commit()
	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Compras")

	#GUARDAR GASTOS-COMPRAS
	try:
		for i in range(0, len(diccionario_gastos)):
			remate = rematename
			productor = str(diccionario_objetos["texto_cuit"].get())
			fecha = fechaHOY
			gasto = diccionario_gastos[str(i)]["gasto"]
			baseImponible = diccionario_gastos[str(i)]["base"]
			alicuota = diccionario_gastos[str(i)]["alicuota"]
			importe = diccionario_gastos[str(i)]["importe"]
			porcentajeIva = diccionario_gastos[str(i)]["porcentajeIva"]
			precioIva = diccionario_gastos[str(i)]["precioIva"]

			entities = [
			remate,
			productor,
			fecha,
			gasto,
			baseImponible,
			alicuota,
			importe,
			porcentajeIva,
			precioIva,
			codigoUnico
			]

			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO liquidacionGastosCompras VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
			con.commit()
	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Gastos-Compras")


	#GUARDAR Financiacion-Compras
	try:
		entities = [
		rematename,
		str(diccionario_objetos["texto_cuit"].get()),
		fechaHOY]

		for i in range(0, 12):
			try:
				cuota = diccionario_observacionesCompras[str(i)]["cuota"]
			except:
				cuota = ""
			try:
				fecha = diccionario_observacionesCompras[str(i)]["fecha"]
			except:
				fecha = ""
			try:
				monto = diccionario_observacionesCompras[str(i)]["monto"]
			except:
				monto = ""

			entities.append(cuota)
			entities.append(fecha)
			entities.append(monto)

		entities.append(codigoUnico)

		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO liquidacionFinanciacionCompras VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
		con.commit()

	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Financiacion-Compras")

	#GUARDAR TOTALES-Compras
	try:
		martillo = diccionario_objetos["compras_texto_martillo"].get()
		porcentajeDescuento = diccionario_objetos["texto_alicuotaDescuento"].get()
		precioDescuento = diccionario_objetos["compras_texto_descuento"].get()
		subtotal = diccionario_objetos["compras_texto_subtotal"].get()
		porcentajeInteres = diccionario_objetos["texto_alicuotaInteres"].get()
		diasInteres = diccionario_objetos["texto_alicuotaInteresDias"].get()
		precioInteres = diccionario_objetos["compras_texto_interes"].get()
		comisionIva = diccionario_objetos["compras_texto_comisionIva"].get()
		retencionIIBB = diccionario_objetos["compras_texto_retencion"].get()
		ivaHacienda = diccionario_objetos["compras_texto_ivaHacienda"].get()
		ivaInteres = diccionario_objetos["compras_texto_ivaInteres"].get()
		ivaGastos = diccionario_objetos["compras_texto_gastosIva"].get()
		totalGastos = diccionario_objetos["compras_texto_gastos"].get()
		porcentajeComision = diccionario_objetos["texto_alicuotaComision"].get()

		entities = [
		martillo,
		porcentajeDescuento,
		precioDescuento,
		subtotal,
		porcentajeInteres,
		diasInteres,
		precioInteres,
		comisionIva,
		retencionIIBB,
		ivaHacienda,
		ivaInteres,
		ivaGastos,
		totalGastos,
		porcentajeComision,
		codigoUnico
		]

		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO liquidacionTotalesCompras VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
		con.commit()

	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Totales-Compras")


	#VENTAS ------------------------------------------


	#GUARDAR VENTAS
	try:
		for i in range(0, len(dicVentas)): 
			remate = rematename
			productor = str(diccionario_objetos["texto_cuit"].get())
			fecha = fechaHOY
			comprador = dicVentas[str(i)]["productor"]
			corral = dicVentas[str(i)]["corral"]
			categoria = dicVentas[str(i)]["catHacienda"]
			um = "Cabezas"
			cantidad = dicVentas[str(i)]["cantidad"]
			precioUm = str(round((float(dicVentas[str(i)]["precio"])*float(dicVentas[str(i)]["kgBruto"]))/float(dicVentas[str(i)]["cantidad"]), 2))
			bruto = str(round(float(dicVentas[str(i)]["precio"])*float(dicVentas[str(i)]["kgBruto"]), 2))
			porcentajeIva = "10.5"
			precioIva = str(round(float(bruto)*0.105, 2))

			entities = [
			remate,
			productor,
			fecha,
			comprador,
			corral,
			categoria,
			um,
			cantidad,
			precioUm,
			bruto,
			porcentajeIva,
			precioIva,
			codigoUnico
			]

			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO liquidacionVentas VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
			con.commit()

	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Compras")

	#GUARDAR GASTOS-VENTAS
	try:
		for i in range(0, len(diccionario_gastosVentas)):
			remate = rematename
			productor = str(diccionario_objetos["texto_cuit"].get())
			fecha = fechaHOY
			gasto = diccionario_gastosVentas[str(i)]["gasto"]
			baseImponible = diccionario_gastosVentas[str(i)]["base"]
			alicuota = diccionario_gastosVentas[str(i)]["alicuota"]
			importe = diccionario_gastosVentas[str(i)]["importe"]
			porcentajeIva = diccionario_gastosVentas[str(i)]["porcentajeIva"]
			precioIva = diccionario_gastosVentas[str(i)]["precioIva"]

			entities = [
			remate,
			productor,
			fecha,
			gasto,
			baseImponible,
			alicuota,
			importe,
			porcentajeIva,
			precioIva,
			codigoUnico
			]

			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO liquidacionGastosVentas VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
			con.commit()

	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Gastos-Compras")


	#GUARDAR Financiacion-Ventas
	try:
		entities = [
		rematename,
		str(diccionario_objetos["texto_cuit"].get()),
		fechaHOY]

		for i in range(0, 12):
			try:
				cuota = diccionario_observacionesVentas[str(i)]["cuota"]
			except:
				cuota = ""
			try:
				fecha = diccionario_observacionesVentas[str(i)]["fecha"]
			except:
				fecha = ""
			try:
				monto = diccionario_observacionesVentas[str(i)]["monto"]
			except:
				monto = ""

			entities.append(cuota)
			entities.append(fecha)
			entities.append(monto)

		entities.append(codigoUnico)

		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO liquidacionFinanciacionVentas VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
		con.commit()

	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Financiacion-Compras")

	#GUARDAR TOTALES-Ventas
	try:
		martillo = diccionario_objetos["ventas_texto_martillo"].get()
		porcentajeDescuento = diccionario_objetos["ventas_texto_alicuotaDescuento"].get()
		precioDescuento = diccionario_objetos["ventas_texto_descuento"].get()
		subtotal = diccionario_objetos["ventas_texto_subtotal"].get()
		porcentajeInteres = diccionario_objetos["ventas_texto_alicuotaInteres"].get()
		diasInteres = diccionario_objetos["ventas_texto_alicuotaInteresDias"].get()
		precioInteres = diccionario_objetos["ventas_texto_interes"].get()
		comisionIva = diccionario_objetos["ventas_texto_comisionIva"].get()
		retencionIIBB = diccionario_objetos["ventas_texto_retencion"].get()
		ivaHacienda = diccionario_objetos["ventas_texto_ivaHacienda"].get()
		ivaInteres = diccionario_objetos["ventas_texto_ivaInteres"].get()
		ivaGastos = diccionario_objetos["ventas_texto_gastosIva"].get()
		totalGastos = diccionario_objetos["ventas_texto_gastos"].get()
		porcentajeComision = diccionario_objetos["ventas_texto_alicuotaComision"].get()

		entities = [
		martillo,
		porcentajeDescuento,
		precioDescuento,
		subtotal,
		porcentajeInteres,
		diasInteres,
		precioInteres,
		comisionIva,
		retencionIIBB,
		ivaHacienda,
		ivaInteres,
		ivaGastos,
		totalGastos,
		porcentajeComision,
		codigoUnico
		]


		con = sql_connection()
		cursorObj = con.cursor()
		cursorObj.execute("INSERT INTO liquidacionTotalesVentas VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
		con.commit()

	except:
		messagebox.showerror("ERROR", "No se pudo cargar liquidaciones Totales-Ventas")





def alicuotas():
	windowAlicuotas = Tk()
	windowAlicuotas.geometry("500x400")
	windowAlicuotas.title("Alicuotas para el calculo de COMPRAS")

	tk.Label(windowAlicuotas, text="Comision %", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 20, width = 290)
	tk.Label(windowAlicuotas, text="Descuento pago contado %", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 70, width = 290)
	tk.Label(windowAlicuotas, text="Intereses dias diferidos %", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 120, width = 290)
	tk.Label(windowAlicuotas, text="a dias", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 170, width = 290)


	entry_porcentaje_comision = Entry(windowAlicuotas, font = ("Helvetica Neue", 15))
	entry_porcentaje_comision.place(x = 300, y =20, width = 60)

	entry_porcentaje_descuento = Entry(windowAlicuotas, font = ("Helvetica Neue", 15))
	entry_porcentaje_descuento.place(x = 300, y = 70, width = 60)

	entry_porcentaje_interes = Entry(windowAlicuotas, font = ("Helvetica Neue", 15))
	entry_porcentaje_interes.place(x = 300, y = 120, width = 60)

	entry_dias_interes = Entry(windowAlicuotas, font = ("Helvetica Neue", 15))
	entry_dias_interes.place(x = 300, y = 170, width = 60)

	entry_porcentaje_descuento.insert(0, diccionario_valores["alicuotaDescuento"])
	entry_porcentaje_interes.insert(0, diccionario_valores["alicuotaInteres"])
	entry_dias_interes.insert(0, diccionario_valores["alicuotaInteresDias"])
	entry_porcentaje_comision.insert(0, diccionario_valores["alicuotaComision"])

	def guardarAlicuotas():
		try:
			comision = float(entry_porcentaje_comision.get())
			descuento = float(entry_porcentaje_descuento.get())
			interes = float(entry_porcentaje_interes.get())
			dias = float(entry_dias_interes.get())
		except:
			messagebox.showerror("ERROR", "Formato inválido")
			return 0
		diccionario_valores["alicuotaComision"] = str(round(comision, 2))
		diccionario_valores["alicuotaDescuento"] = str(round(descuento, 2))
		diccionario_valores["alicuotaInteres"] = str(round(interes, 2))
		diccionario_valores["alicuotaInteresDias"] = str(round(dias, 2))

		diccionario_objetos["texto_alicuotaDescuento"].set(str(round(descuento, 2)))
		diccionario_objetos["texto_alicuotaInteres"].set(str(round(interes, 2)))
		diccionario_objetos["texto_alicuotaInteresDias"].set(str(round(dias, 2)))
		diccionario_objetos["texto_alicuotaComision"].set(str(round(comision, 2)))


		crearComision()

		windowAlicuotas.destroy()

	btn_guardar = tk.Button(windowAlicuotas, text="GUARDAR", font=("Helvetica Neue",15, "bold"), backgroun="#a4ff9e", command= lambda: guardarAlicuotas())
	btn_guardar.place(x = 200, y = 250, width = 110, height = 70)



	windowAlicuotas.mainloop()
def alicuotasVentas():
	windowAlicuotasVentas = Tk()
	windowAlicuotasVentas.geometry("500x400")
	windowAlicuotasVentas.title("Alicuotas para el calculo de VENTAS")

	tk.Label(windowAlicuotasVentas, text="Comision %", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 20, width = 290)
	tk.Label(windowAlicuotasVentas, text="Descuento pago contado %", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 70, width = 290)
	tk.Label(windowAlicuotasVentas, text="Intereses dias diferidos %", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 120, width = 290)
	tk.Label(windowAlicuotasVentas, text="a dias", font=("Helvetica Neue",14, "bold"), anchor="e").place(x = 0, y = 170, width = 290)


	entry_porcentaje_comision = Entry(windowAlicuotasVentas, font = ("Helvetica Neue", 15))
	entry_porcentaje_comision.place(x = 300, y =20, width = 60)

	entry_porcentaje_descuento = Entry(windowAlicuotasVentas, font = ("Helvetica Neue", 15))
	entry_porcentaje_descuento.place(x = 300, y = 70, width = 60)

	entry_porcentaje_interes = Entry(windowAlicuotasVentas, font = ("Helvetica Neue", 15))
	entry_porcentaje_interes.place(x = 300, y = 120, width = 60)

	entry_dias_interes = Entry(windowAlicuotasVentas, font = ("Helvetica Neue", 15))
	entry_dias_interes.place(x = 300, y = 170, width = 60)

	entry_porcentaje_descuento.insert(0, diccionario_valores["alicuotaDescuentoVentas"])
	entry_porcentaje_interes.insert(0, diccionario_valores["alicuotaInteresVentas"])
	entry_dias_interes.insert(0, diccionario_valores["alicuotaInteresDiasVentas"])
	entry_porcentaje_comision.insert(0, diccionario_valores["alicuotaComisionVentas"])

	def guardarAlicuotasVentas():
		try:
			comision = float(entry_porcentaje_comision.get())
			descuento = float(entry_porcentaje_descuento.get())
			interes = float(entry_porcentaje_interes.get())
			dias = float(entry_dias_interes.get())
		except:
			messagebox.showerror("ERROR", "Formato inválido")
			return 0
		diccionario_valores["alicuotaComisionVentas"] = str(round(comision, 2))
		diccionario_valores["alicuotaDescuentoVentas"] = str(round(descuento, 2))
		diccionario_valores["alicuotaInteresVentas"] = str(round(interes, 2))
		diccionario_valores["alicuotaInteresDiasVentas"] = str(round(dias, 2))

		diccionario_objetos["ventas_texto_alicuotaDescuento"].set(str(round(descuento, 2)))
		diccionario_objetos["ventas_texto_alicuotaInteres"].set(str(round(interes, 2)))
		diccionario_objetos["ventas_texto_alicuotaInteresDias"].set(str(round(dias, 2)))
		diccionario_objetos["ventas_texto_alicuotaComision"].set(str(round(comision, 2)))


		crearComisionVentas()

		windowAlicuotasVentas.destroy()

	btn_guardar = tk.Button(windowAlicuotasVentas, text="GUARDAR", font=("Helvetica Neue",15, "bold"), backgroun="#a4ff9e", command= lambda: guardarAlicuotasVentas())
	btn_guardar.place(x = 200, y = 250, width = 110, height = 70)



	windowAlicuotasVentas.mainloop()
def retencionVentas(baseImponible):
	windowsRetencionVentas = Tk()
	windowsRetencionVentas.geometry("800x300")
	windowsRetencionVentas.title("RETENCION IIBB")

	varx=20

	tk.Label(windowsRetencionVentas, text="RET IIBB CHACO", font=("Helvetica Neue",10, "bold"), anchor="c", backgroun="#d5e5f7").place(x = 20+varx, y = 70, width = 150)
	tk.Label(windowsRetencionVentas, text="ADICIONAL 10%", font=("Helvetica Neue",10, "bold"), anchor="c", backgroun="#d5e5f7").place(x = 20+varx, y = 120, width = 150)

	tk.Label(windowsRetencionVentas, text="Base Imponible $", font=("Helvetica Neue",8, "bold"), anchor="c", backgroun="#d5e5f7").place(x = 180+varx, y = 45, width = 100)
	tk.Label(windowsRetencionVentas, text="Alicuota %", font=("Helvetica Neue",8, "bold"), anchor="c", backgroun="#d5e5f7").place(x = 290+varx, y = 45, width = 100)
	tk.Label(windowsRetencionVentas, text="Importe $", font=("Helvetica Neue",8, "bold"), anchor="c", backgroun="#d5e5f7").place(x = 400+varx, y = 45, width = 100)
	tk.Label(windowsRetencionVentas, text="IVA %", font=("Helvetica Neue",8, "bold"), anchor="c", backgroun="#d5e5f7").place(x = 510+varx, y = 45, width = 100)
	tk.Label(windowsRetencionVentas, text="IVA $", font=("Helvetica Neue",8, "bold"), anchor="c", backgroun="#d5e5f7").place(x = 620+varx, y = 45, width = 100)


	entry_baseRetencion = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_baseRetencion.place(x = 180+varx, y =70, width = 100)

	entry_baseAdicional = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_baseAdicional.place(x = 180+varx, y = 120, width = 100)


	entry_alicuotaRetencion = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_alicuotaRetencion.place(x = 290+varx, y =70, width = 100)

	entry_alicuotaAdicional = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_alicuotaAdicional.place(x = 290+varx, y = 120, width = 100)


	entry_importeRetencion = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_importeRetencion.place(x = 400+varx, y =70, width = 100)

	entry_importeAdicional = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_importeAdicional.place(x = 400+varx, y = 120, width = 100)


	entry_ivaRetencion = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_ivaRetencion.place(x = 510+varx, y =70, width = 100)

	entry_ivaAdicional = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_ivaAdicional.place(x = 510+varx, y = 120, width = 100)


	entry_precioIvaRetencion = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_precioIvaRetencion.place(x = 620+varx, y =70, width = 100)

	entry_precioIvaAdicional = Entry(windowsRetencionVentas, font = ("Helvetica Neue", 12))
	entry_precioIvaAdicional.place(x = 620+varx, y = 120, width = 100)


	entry_baseRetencion.delete(0, tk.END)
	entry_baseAdicional.delete(0, tk.END)
	entry_alicuotaRetencion.delete(0, tk.END)
	entry_alicuotaAdicional.delete(0, tk.END)
	entry_importeRetencion.delete(0, tk.END)
	entry_importeAdicional.delete(0, tk.END)
	entry_ivaRetencion.delete(0, tk.END)
	entry_ivaAdicional.delete(0, tk.END)
	entry_precioIvaRetencion.delete(0, tk.END)
	entry_precioIvaAdicional.delete(0, tk.END)


	entry_baseRetencion.insert(0, baseImponible)
	entry_baseAdicional.insert(0, baseImponible)
	entry_alicuotaRetencion.insert(0, 0.750)
	entry_alicuotaAdicional.insert(0, 0.075)
	entry_importeRetencion.insert(0, round(baseImponible*float(entry_alicuotaRetencion.get())/100, 2))
	entry_importeAdicional.insert(0, round(baseImponible*float(entry_alicuotaAdicional.get())/100, 2))
	entry_ivaRetencion.insert(0, 0.0)
	entry_ivaAdicional.insert(0, 0.0)
	entry_precioIvaRetencion.insert(0, 0.0)
	entry_precioIvaAdicional.insert(0, 0.0)

	def guardarIIBB():
		gasto = "RET IIBB CHACO"
		baseImponible = str(entry_baseRetencion.get())
		alicuota = str(entry_alicuotaRetencion.get())
		importe = str(entry_importeRetencion.get())
		porcentajeIva = str(entry_ivaRetencion.get())
		precioIva = str(entry_precioIvaRetencion.get())

		diccionario_gastosVentas[str(len(diccionario_gastosVentas))] = {
		"id" : str(len(diccionario_gastosVentas)),
		"gasto" : gasto,
		"base" : baseImponible,
		"alicuota" : alicuota,
		"importe" : importe,
		"porcentajeIva" : porcentajeIva,
		"precioIva" : precioIva,
		}
		#------------------------------------------------
		gasto = "ADICIONAL CHACO 10% LEY 666 K"
		baseImponible = str(entry_baseAdicional.get())
		alicuota = str(entry_alicuotaAdicional.get())
		importe = str(entry_importeAdicional.get())
		porcentajeIva = str(entry_ivaAdicional.get())
		precioIva = str(entry_precioIvaAdicional.get())

		diccionario_gastosVentas[str(len(diccionario_gastosVentas))] = {
		"id" : str(len(diccionario_gastosVentas)),
		"gasto" : gasto,
		"base" : baseImponible,
		"alicuota" : alicuota,
		"importe" : importe,
		"porcentajeIva" : porcentajeIva,
		"precioIva" : precioIva,
		}

		cargarGastosVentas()
		windowsRetencionVentas.destroy()



	btn_guardar = tk.Button(windowsRetencionVentas, text="GUARDAR", font=("Helvetica Neue",15, "bold"), backgroun="#a4ff9e", command= lambda: guardarIIBB())
	btn_guardar.place(x = 350, y = 200, width = 110, height = 70)



	windowsRetencionVentas.mainloop()




def buscarDatosGuardados(codigo):
	#Obtener datos guardados
	"""
	if(True):
		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_compras = actualizar_db(con, "liquidacionCompras", condiciones)
		except:
			rows_compras = []
			messagebox.showerror("ERROR", "Error al buscar compras en la DB")

		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_comprasFinanciacion = actualizar_db(con, "liquidacionFinanciacionCompras", condiciones)
		except:
			rows_comprasFinanciacion = []
			messagebox.showerror("ERROR", "Error al buscar Financiacion Compras en la DB")

		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_comprasGastos = actualizar_db(con, "liquidacionGastosCompras", condiciones)
		except:
			rows_comprasGastos = []
			messagebox.showerror("ERROR", "Error al buscar Gastos compras en la DB")

		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_comprasTotales = actualizar_db(con, "liquidacionTotalesCompras", condiciones)
		except:
			rows_comprasTotales = []
			messagebox.showerror("ERROR", "Error al buscar Totales compras en la DB")

		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_ventas = actualizar_db(con, "liquidacionVentas", condiciones)
		except:
			rows_ventas = []
			messagebox.showerror("ERROR", "Error al buscar ventas en la DB")

		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_ventasFinanciacion = actualizar_db(con, "liquidacionFinanciacionVentas", condiciones)
		except:
			rows_ventasFinanciacion = []
			messagebox.showerror("ERROR", "Error al buscar financiacion ventas en la DB")

		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_ventasGastos = actualizar_db(con, "liquidacionGastosVentas", condiciones)
		except:
			rows_ventasGastos = []
			messagebox.showerror("ERROR", "Error al buscar gastos ventas en la DB")

		try:
			con = sql_connection()
			condiciones = " WHERE CODIGO = '" + str(codigo) + "'"
			rows_ventasTotales = actualizar_db(con, "liquidacionTotalesVentas", condiciones)
		except:
			rows_ventasTotales = []
			messagebox.showerror("ERROR", "Error al buscar totales ventas en la DB")

	rows_compras
	rows_comprasFinanciacion
	rows_comprasGastos
	rows_comprasTotales

	rows_ventas
	rows_ventasFinanciacion
	rows_ventasGastos
	rows_ventasTotales
	"""
	messagebox.showinfo("ATENCION", "Funcion no disponible, se puede ver lo guardado en la pestaña 'Exportacion', o volver a guardar")




window1 = Tk()
window1.title("PRE-LIQUIDACIONES")
window1.geometry("1285x728")
window1.configure(backgroun="#2C4D4F") #E8F6FA
exportacion(window1)
window1.mainloop()
