#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

import tablaElegir
import pdf_preliquidacion2

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

dicc_objetos={"varFullScreen" : 0, "varFullScreenDetalles" : False}
diccionario_objetos = {}

diccionarioLotes = {}

direccionBaseDeDatos = "database/iltanohacienda.db"

diccionario_objetos["direccion"] = "C:/Users/Santiago/Desktop/exportaciones"

ubicLiquidaciones = "C:/Users/Santiago/Desktop/exportaciones/liquidaciones"

diccionarioEnviar = {}


window = Tk()
window.title("IL TANO HACIENDA SAS")
window.geometry("1024x600")
window.resizable(0,0)
window.configure(backgroun="#000000") #E8F6FA
window.attributes('-fullscreen', dicc_objetos["varFullScreen"])

diccionario_objetos["id_remate_alias"] = "remate1"
diccionario_objetos["id_catalogo_alias"] = "nuevoCat"
diccionario_objetos["numero_remate"] = "200702"

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
def printDiccionario(diccionario):
	print(json.dumps(diccionario, indent=4))

#PRODUCTORES
def vendedorFiltrar():
	pal_clave = str(diccionario_objetos["entry_productor"].get())
	remate = diccionario_objetos["id_remate_alias"]
	catalogo = diccionario_objetos["id_catalogo_alias"]

	#obtener lotes vendidos de compraventa
	con = sql_connection()
	condiciones = " WHERE estado = 'activo' AND remate = '" + remate + "'"
	rows = actualizar_db_selec(con, "lote", "compraventa", condiciones)

	rows_vendedores = []
	#obtener vendedor de esos lotes
	for row in rows:
		con = sql_connection()
		condiciones = " WHERE id = " + str(row[0])
		rows_prodLotes = actualizar_db_selec(con, "productor", "lotes", condiciones)

		if len(rows_prodLotes) != 0:
			if rows_prodLotes[0] not in rows_vendedores:
				rows_vendedores.append(rows_prodLotes[0])
		else:
			messagebox.showerror("ERROR", "ERROR")


	#tupla = ("x", productor, "", cuit)
	enviar = []

	for row in rows_vendedores:
		con = sql_connection()
		condiciones = " WHERE nombre = '" + str(row[0]) + "' AND estado = 'activo'"
		prod = actualizar_db(con, "productores", condiciones)

		if prod != []:
			tupla = ("", prod[0][1], "", prod[0][3])
			if tupla not in enviar:
				enviar.append(tupla)
		else:
			messagebox.showerror("ERROR", "ERROR")

	cargarTablaVendedores(enviar)

def cargarTablaVendedores(rows):

	tabla = diccionario_objetos["tabla_vendedores"]

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
def seleccionarTablaVendedor():
	remate = diccionario_objetos["id_remate_alias"]
	catalogo = diccionario_objetos["id_catalogo_alias"]

	diccionarioLotes.clear()

	diccionario_objetos["totalCabezas"] = 0
	diccionario_objetos["totalKg"] = 0

	diccionario_objetos["entry_num"].delete(0, tk.END)
	diccionario_objetos["entry_dte"].delete(0, tk.END)
	diccionario_objetos["txt_observaciones"].delete("1.0", tk.END)

	tabla = diccionario_objetos["tabla_vendedores"]
	seleccion = tabla.item(tabla.selection())
	productor = seleccion["tags"][1]


	diccionario_objetos["entry_num"].insert(0, numeroLiquidacion(productor))

	actualizarDicLotes(productor)

	#printDiccionario(diccionarioLotes)
	cargarDatosVendedor(productor)
	cargarTablaLotes()
	calcularSubtotal()
	calcularIntereses()
	calcularIvaHacienda()
	calcularIvaInteres()
	cargarTablaGastos()
	calcularRetencion()
	calcularTOTAL()

	diccionario_objetos["btn_guardar"].config(state = "normal")
	#diccionario_objetos["btn_eliminar"].config(state = "normal")
	diccionario_objetos["btn_exportar"].config(state = "normal")

def cargarDatosVendedor(productor):
	con = sql_connection()
	condiciones = " WHERE nombre = '" + str(productor) + "'"
	rows = actualizar_db(con, "productores", condiciones)

	if len(rows)==0:
		messagebox.showerror("ERROR", "Error encontrando al productor en la base de datos")
		return 0

	#CARGAR
	row = rows[0]

	diccionario_objetos["entry_nombre"].delete(0, tk.END)
	diccionario_objetos["entry_cuit"].delete(0, tk.END)
	diccionario_objetos["entry_iva"].delete(0, tk.END)
	diccionario_objetos["entry_iibb"].delete(0, tk.END)
	diccionario_objetos["entry_caracter"].delete(0, tk.END)
	diccionario_objetos["entry_domicilio"].delete(0, tk.END)
	diccionario_objetos["entry_localidad"].delete(0, tk.END)
	diccionario_objetos["entry_provincia"].delete(0, tk.END)
	diccionario_objetos["entry_codPostal"].delete(0, tk.END)
	diccionario_objetos["entry_renspa"].delete(0, tk.END)
	diccionario_objetos["entry_ruca"].delete(0, tk.END)

	diccionario_objetos["entry_nombre"].insert(0, str(row[2]))
	diccionario_objetos["entry_cuit"].insert(0, str(row[3]))
	diccionario_objetos["entry_iva"].insert(0, str(row[6]))
	diccionario_objetos["entry_iibb"].insert(0, str(""))
	diccionario_objetos["entry_caracter"].insert(0, str(""))
	diccionario_objetos["entry_domicilio"].insert(0, str(row[7]))
	diccionario_objetos["entry_localidad"].insert(0, str(row[8]))
	diccionario_objetos["entry_provincia"].insert(0, str(row[9]))
	diccionario_objetos["entry_codPostal"].insert(0, str(row[10]))
	diccionario_objetos["entry_renspa"].insert(0, str(""))
	diccionario_objetos["entry_ruca"].insert(0, str(row[19]))

	diccionario_objetos["id_productor_alias"] = str(row[1])

	if (str(row[6]) == "Monotributista"):
		checkiva.set(0)
	else:
		checkiva.set(1)

def numeroLiquidacion(productor):
	remate = diccionario_objetos["id_remate_alias"]
	remateNumero = diccionario_objetos["numero_remate"]

	con = sql_connection()
	condiciones = " WHERE remate = '" + remate + "' AND productor = '" + productor + "'"
	rows = actualizar_db(con, "numeroLiquidacionesVenta", condiciones)

	numero = "0"

	if len(rows) == 1:
		numero = rows[0][3]
	if len(rows) == 0:
		con = sql_connection()
		condiciones = " WHERE remate = '" + remate + "'"
		rows = actualizar_db(con, "numeroLiquidacionesVenta", condiciones)

		try:
			numObtenido = int(rows[len(rows)-1][3]) + 1
		except:
			numObtenido = 1

		try:
			entities = [str(remate), str(productor), str(numObtenido)]

			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO numeroLiquidacionesVenta VALUES(NULL, ?, ?, ?)", entities)
			con.commit()
		except:
			messagebox.showerror("ERROR", "Error guardando el numero de liquidacion en la base de datos")


		numero = str(numObtenido)

	return remateNumero + "-" + numero.zfill(3)
	
#CARGAR LOTES
def actualizarDicLotes(productor):
	remate = diccionario_objetos["id_remate_alias"]

	con = sql_connection()
	condiciones = " WHERE estado = 'activo' AND remate = '" + remate + "'"
	rows = actualizar_db(con, "compraventa", condiciones)

	totalCabezas = 0
	totalKg = 0
	i = 0

	if len(rows) != 0:
		for row in rows:
			lote = row[1]

			con = sql_connection()
			condiciones = " WHERE id = " + str(lote)
			rows_lote = actualizar_db(con, "lotes", condiciones)

			if len(rows_lote) != 0:
				row_lote = rows_lote[0]
				if row_lote[2] == productor:
					#ESTE lote pertenece al productor:
					try:
						cabezas = int(row_lote[3])
					except:
						cabezas = 0

					try:
						kg = int(row_lote[12])
					except:
						kg = 0

					totalCabezas = totalCabezas + cabezas
					totalKg = totalKg + kg


					#VERIFICAR PRODUCTOR, EN CASO DE SER PROD AUXILIAR Y PINTURA
					con = sql_connection()
					condiciones = " WHERE nombre = '" + str(row[2]) + "'"
					rows_productor = actualizar_db(con, "productores", condiciones)

					if len(rows_productor) == 0:
						con = sql_connection()
						condiciones = " WHERE alias = '" + str(row[2]) + "' AND remate = '" + remate + "'"
						rows_productorDeAuxiliar = actualizar_db(con, "productoresAuxiliares", condiciones)

						if len(rows_productorDeAuxiliar) == 0:
							cliente = "-"
						else:
							cliente = str(rows_productorDeAuxiliar[0][4])
					else:
						cliente = str(rows_productor[0][1])

					con = sql_connection()
					condiciones = " WHERE remate = '" + remate + "' AND productor = '" + cliente + "'"
					row_pintura = actualizar_db_selec(con, "pintura", "pintura", condiciones)

					if len(row_pintura) == 0:
						pintura = "-"
					else:
						pintura = str(row_pintura[0][0])

					x_id = str(row_lote[0])
					x_corral = str(row_lote[4])
					x_cliente = cliente
					x_categoria = str(row_lote[6])
					x_pintura = pintura
					x_cantidad = str(row_lote[3])
					x_kgs = str(row_lote[12])
					x_precio = str(row[3])

					try:
						bruto = round(float(row_lote[12]) * float(row[3]), 2)
					except:
						bruto = 0

					x_bruto = str(bruto)

					diccionarioLotes[str(i)] = {
					"id" : x_id,
					"corral" : x_corral,
					"cliente" : x_cliente,
					"categoria" : x_categoria,
					"pintura" : x_pintura,
					"cantidad" : x_cantidad,
					"kgs" : x_kgs,
					"precio" : x_precio,
					"bruto" : x_bruto,
					}
					i += 1

	else:
		messagebox.showerror("ERROR", "No existen compraventas")

	diccionario_objetos["totalCabezas"] = totalCabezas
	diccionario_objetos["totalKg"] = totalKg

	diccionario_objetos["entry_totalCabezas"].delete(0, tk.END)
	diccionario_objetos["entry_totalCabezas"].insert(0, totalCabezas)

	diccionario_objetos["entry_totalKg"].delete(0, tk.END)
	diccionario_objetos["entry_totalKg"].insert(0, round(totalKg, 2))

def cargarTablaLotes():
	tabla = diccionario_objetos["tabla"]

	subtotalMarillo = 0

	for i in tabla.get_children():
		tabla.delete(i)

	cant_lotes = len(diccionarioLotes)

	for i in range(0, cant_lotes):
		tabla.insert("", str(i), tags=str(i), text = diccionarioLotes[str(i)]["id"], iid= diccionarioLotes[str(i)]["id"], values = (diccionarioLotes[str(i)]["corral"],
			diccionarioLotes[str(i)]["cliente"],
			diccionarioLotes[str(i)]["categoria"],
			diccionarioLotes[str(i)]["pintura"],
			diccionarioLotes[str(i)]["cantidad"],
			diccionarioLotes[str(i)]["kgs"],
			diccionarioLotes[str(i)]["precio"],
			diccionarioLotes[str(i)]["bruto"]))
		subtotalMarillo = subtotalMarillo + float(diccionarioLotes[str(i)]["bruto"])

	diccionario_objetos["subtotalMarillo"] = subtotalMarillo

#Calculos
def calcularSubtotal():
	subtotalMarillo = diccionario_objetos["subtotalMarillo"]
	try:
		porcDescuento = float(diccionario_objetos["entry_porcDescuento"].get())
	except:
		messagebox.showinfo("Atencion", "Porcentaje de descuento no aceptado")
		diccionario_objetos["entry_porcDescuento"].delete(0, tk.END)
		diccionario_objetos["entry_porcDescuento"].insert(0, 0)
		porcDescuento = 0

	descuento = round(porcDescuento / 100 * subtotalMarillo, 2)
	try:
		subtotal = round(subtotalMarillo - descuento, 2)
	except:
		subtotal = 0

	diccionario_objetos["entry_subtotalMartillo"].delete(0, tk.END)
	diccionario_objetos["entry_descuento"].delete(0, tk.END)
	diccionario_objetos["entry_subtotal"].delete(0, tk.END)

	diccionario_objetos["entry_subtotalMartillo"].insert(0, subtotalMarillo)
	diccionario_objetos["entry_descuento"].insert(0, descuento)
	diccionario_objetos["entry_subtotal"].insert(0, subtotal)
def calcularIntereses():
	subtotal = float(diccionario_objetos["entry_subtotal"].get())

	try:
		entry_interesDias = float(diccionario_objetos["entry_interesDias"].get())
	except:
		messagebox.showinfo("Atencion", "Dias de intereses no aceptado")
		diccionario_objetos["entry_interesDias"].delete(0, tk.END)
		diccionario_objetos["entry_interesDias"].insert(0, 0)
		entry_interesDias = 0

	try:
		entry_interesPorcentaje = float(diccionario_objetos["entry_interesPorcentaje"].get())
	except:
		messagebox.showinfo("Atencion", "Porcentaje de intereses no aceptado")
		diccionario_objetos["entry_interesPorcentaje"].delete(0, tk.END)
		diccionario_objetos["entry_interesPorcentaje"].insert(0, 0.0)
		entry_interesPorcentaje = 0

	intereses = round(subtotal *entry_interesDias * entry_interesPorcentaje / 100, 2)

	diccionario_objetos["entry_intereses"].delete(0, tk.END)
	diccionario_objetos["entry_intereses"].insert(0, intereses)
def calcularIvaHacienda():
	realizarCalculo = diccionario_objetos["checkiva"].get()
	if(realizarCalculo):
		try:
			subtotal = float(diccionario_objetos["entry_subtotal"].get())
		except:
			messagebox.showinfo("Atencion", "Subtotal no aceptado")
			subtotal = 0

		ivaHacienda = round(subtotal*0.105 ,2)
	else:
		ivaHacienda = 0.0

	diccionario_objetos["entry_ivaHacienda"].delete(0, tk.END)
	diccionario_objetos["entry_ivaHacienda"].insert(0, ivaHacienda)
def calcularIvaInteres():
	try:
		subtotal = float(diccionario_objetos["entry_intereses"].get())
	except:
		messagebox.showinfo("Atencion", "Intereses no aceptado")
		subtotal = 0

	ivaInteres = round(subtotal*0.21 ,2)

	diccionario_objetos["entry_ivaInteres"].delete(0, tk.END)
	diccionario_objetos["entry_ivaInteres"].insert(0, ivaInteres)
def cargarTablaGastos():
	tabla = diccionario_objetos["tablaGastos"]

	try:
		subtotal = float(diccionario_objetos["entry_subtotal"].get())
	except:
		subtotal = 0

	try:
		comisionPorcentaje = float(diccionario_objetos["entry_comisionPorcentaje"].get())
	except:
		comisionPorcentaje = 0

	comision = round(subtotal * comisionPorcentaje / 100, 2)
	ivaComision = round(comision*0.105 ,2)

	diccionario_objetos["comision"] = comision

	diccionario_objetos["entry_comisionIva"].delete(0, tk.END)
	diccionario_objetos["entry_comisionIva"].insert(0, round(comision + ivaComision, 2))

	for i in tabla.get_children():
		tabla.delete(i)

	tabla.insert("", tk.END, values = ("Comision", str(subtotal), str(comisionPorcentaje), str(comision), str("10.5"), str(ivaComision)))
def calcularRetencion():
	realizarCalculo = diccionario_objetos["checkretencion"].get()
	if(realizarCalculo):
		try:
			subtotal = float(diccionario_objetos["entry_subtotalMartillo"].get()) - float(diccionario_objetos["comision"])
		except:
			messagebox.showinfo("Atencion", "subtotalMarillo o gastos no aceptado")
			subtotal = 0
		retencion = round(subtotal*0.0075 + subtotal*0.00075 ,2)
	else:
		retencion = 0.0

	diccionario_objetos["entry_retencion"].delete(0, tk.END)
	diccionario_objetos["entry_retencion"].insert(0, retencion)

def calcularTOTAL():
	try:
		subtotal = float(diccionario_objetos["entry_subtotal"].get())
		intereses = float(diccionario_objetos["entry_intereses"].get())
		ivaHacienda = float(diccionario_objetos["entry_ivaHacienda"].get())
		ivaIntereses = float(diccionario_objetos["entry_ivaInteres"].get())
		comisionIva = float(diccionario_objetos["entry_comisionIva"].get())
		retencion = float(diccionario_objetos["entry_retencion"].get())
	except:
		messagebox.showinfo("Atencion", "Error obteniendo datos para el calculo del total")
		return 0

	TOTAL = round(subtotal + intereses + ivaHacienda + ivaIntereses - comisionIva - retencion, 2)

	diccionario_objetos["entry_total"].delete(0, tk.END)
	diccionario_objetos["entry_total"].insert(0, TOTAL)

def REALIZARCalculos():
	calcularSubtotal()
	calcularIntereses()
	calcularIvaHacienda()
	calcularIvaInteres()
	cargarTablaGastos()
	calcularRetencion()
	calcularTOTAL()

#CREAR LIQUIDACION DE COMPRA
def guardar():
	diccionarioEnviar.clear()

	try:
		dire = diccionario_objetos["direccion"]
		dire = dire + "/PreLiquidacion de Venta " + str(diccionario_objetos["entry_num"].get()) + " ~ " + diccionario_objetos["id_productor_alias"] + " ~ " + str(time.strftime("%d-%m-%y")) + " ~ " + str(time.strftime("%H-%M-%S")) + "hs.pdf"

		diccionarioDatos = {
		"ruta" : dire,	
		"fecha" : str(diccionario_objetos["entry_fecha"].get()),
		"tipoDocumento" : "PRE-LIQUIDACION DE VENTA",
		"numeroDocumento" : str(diccionario_objetos["entry_num"].get()),
		"remate" : diccionario_objetos["id_remate_alias"],
		"condicion" : str(diccionario_objetos["entry_condPago"].get()),
		"destino" : str(diccionario_objetos["entry_destino"].get()),
		"titulo" : "Pre-Liquidacion de venta de " + str(diccionario_objetos["entry_nombre"].get()),
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del remate")
		return 0

	try:
		diccionarioReceptor = {
		"CUIT" : str(diccionario_objetos["entry_cuit"].get()),
		"situacionIVA" : str(diccionario_objetos["entry_iva"].get()),
		"domicilio" :str(diccionario_objetos["entry_domicilio"].get()),
		"codpostal" : str(diccionario_objetos["entry_codPostal"].get()),
		"nombreyapellido" : str(diccionario_objetos["entry_nombre"].get()),
		"IIBB" : str(diccionario_objetos["entry_iibb"].get()),
		"localidad" : str(diccionario_objetos["entry_localidad"].get()),
		"renspa" : str(diccionario_objetos["entry_renspa"].get()),
		"caracter" : str(diccionario_objetos["entry_caracter"].get()),
		"provincia" : str(diccionario_objetos["entry_provincia"].get()),
		"ruca" : str(diccionario_objetos["entry_ruca"].get()),
		"DTE" : str(diccionario_objetos["entry_dte"].get()),
		"contacto" : str(diccionario_objetos["entry_contacto"].get()),
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del receptor")
		return 0
	try:
		diccionarioEmisor = {
		"CUIT" : "30-71648051-4",
		"nombreyapellido" : "P/P IL TANO HACIENDA S.A.S.",
		}
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos del emisor (firmas)")
		return 0

	try:
		diccionarioConceptos = {}
		tabla = diccionario_objetos["tabla"]
		j=0
		for i in tabla.get_children():
			diccionarioConceptos[str(j)] = {
			"cliente" : str(tabla.item(i)["values"][1]),
			"categoria" : str(tabla.item(i)["values"][2]), #
			"corral" : str(tabla.item(i)["values"][0]), #corral
			"pintura" : str(tabla.item(i)["values"][3]), #pintura
			"cantidad" : str(tabla.item(i)["values"][4]), #cantidad
			"kg" : str(tabla.item(i)["values"][5]), #kg
			"$kg" : str(tabla.item(i)["values"][6]), #$kg
			"total" : str(tabla.item(i)["values"][7]), #importe
			}
			j += 1
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de los conceptos")
		return 0

	try:
		diccionarioGastos = {}
		tabla = diccionario_objetos["tablaGastos"]
		j=0
		for i in tabla.get_children():
			diccionarioGastos[str(j)] = {
			"gastos" : str(tabla.item(i)["values"][0]),
			"base" : str(tabla.item(i)["values"][1]),
			"alicuota" : str(tabla.item(i)["values"][2]),
			"importe" : str(tabla.item(i)["values"][3]),
			"iva" : str(tabla.item(i)["values"][4]),
			"$iva" : str(tabla.item(i)["values"][5]),
			}
			j += 1
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de los gastos")
		return 0

	try:
		interesPorcentaje = str(diccionario_objetos["entry_interesPorcentaje"].get())
		interesDias = str(diccionario_objetos["entry_interesDias"].get())
		ivaHaciendaPorcentaje = str("10.5")
		ivaInteresPorcentaje = str("21.0")
		subtotalMartillo = str(diccionario_objetos["entry_subtotalMartillo"].get())
		descuento = str(diccionario_objetos["entry_descuento"].get())
		subtotal = str(diccionario_objetos["entry_subtotal"].get())
		interes = str(diccionario_objetos["entry_intereses"].get())
		ivaHacienda = str(diccionario_objetos["entry_ivaHacienda"].get())
		ivaInteres = str(diccionario_objetos["entry_ivaInteres"].get())
		comisionIva = str(diccionario_objetos["entry_comisionIva"].get())
		retencion = str(diccionario_objetos["entry_retencion"].get())
		total = str(diccionario_objetos["entry_total"].get())
		totalCabezas = str(diccionario_objetos["totalCabezas"])
		totalKg = str(diccionario_objetos["totalKg"])
		observaciones = str(diccionario_objetos["txt_observaciones"].get("1.0", tk.END)).replace("\n", ' ')

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
		"totalCabezas" : totalCabezas,
		"totalKg" : totalKg,
		"observaciones" : observaciones,
		}

	except:
		messagebox.showerror("ERROR", "Error al obtener los datos de Totales")
		return 0

	try:
		diccionarioObservaciones = {}
		diccionarioObservaciones["0"] = {
		"cuota" : str("nanana"),
		"fecha" : str("nanana"),
		"monto" : str("10"),
		}

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

	try:
		ubic = ubicLiquidaciones + "/"
		archivoName = "liq_vent_" + str(diccionario_objetos["entry_num"].get()) + "_" + diccionario_objetos["id_productor_alias"] + ".json"
		archivo = open(ubic + archivoName, "w")
		archivo.write(json.dumps(diccionarioEnviar, indent=4))
		archivo.close()
	except:
		messagebox.showerror("ERROR", "Error al guardar liquidacion")
	try:
		con = sql_connection()
		condiciones = " WHERE remate = '" + diccionario_objetos["id_remate_alias"] + "' AND productor = '" + diccionario_objetos["id_productor_alias"] + "'"
		rows = actualizar_db(con, "liquidacionesVentaGuardadas", condiciones)
		if len(rows) == 0:
			try:
				entities = [diccionario_objetos["id_remate_alias"], diccionario_objetos["id_productor_alias"], str(diccionario_objetos["entry_num"].get()), archivoName]
				con = sql_connection()
				cursorObj = con.cursor()
				cursorObj.execute("INSERT INTO liquidacionesVentaGuardadas VALUES(NULL, ?, ?, ?, ?)", entities)
				con.commit()
			except:
				messagebox.showerror("ERROR", "Error al cargar en base de datos")
		else:
			try:
				entities = [str(diccionario_objetos["entry_num"].get()), archivoName, str(rows[0][0])]

				con = sql_connection()
				cursorObj = con.cursor()
				cursorObj.execute("UPDATE liquidacionesVentaGuardadas SET liquidacion = ?, nombre = ? WHERE id = ?", entities)
				con.commit()
			except:
				messagebox.showerror("ERROR", "Error al editar en base de datos")
	except:
		messagebox.showerror("ERROR", "Error al guardar en base de datos")
def guardarExportar():
	guardar()
	try:
		pdf_preliquidacion2.preliquidacionPDF(diccionarioEnviar)
	except:
		messagebox.showerror("ERROR", "Error al guardar PDF liquidacion")


#BARRA DE TITULO
if(True):
	barraTitulo = tk.Frame(window, relief=SOLID, bd=2, backgroun="#242b33")
	barraTitulo.pack(side=TOP, fill=X)

	tk.Label(barraTitulo, text="LIQUIDACIONES DE VENTA", font=("Helvetica Neue",12,"bold"), anchor="n", backgroun="#242b33", foreground = "#ffffff").pack()

#BODY
if(True):

	lblBody = tk.Label(window, backgroun="#242b33")
	lblBody.pack(side=TOP, fill=BOTH, padx=2, pady=2)
	lblBody.config(width="1", height="100")

	padX=3
	padY=2

	lbl_tabla = Label(lblBody)
	lbl_tabla.place(x=2, y=0, width=1012, height=150)

	lbl_tablaGastos = Label(lblBody)
	lbl_tablaGastos.place(x=2, y=155, width=1012, height=95)

	lbl_datos = Label(lblBody)
	lbl_datos.place(x=2, y=254, width=1012, height=310)

	#TABLA LOTES
	if(True):
		sbr = Scrollbar(lbl_tabla)
		sbr.pack(side=RIGHT, fill="y")


		tabla = ttk.Treeview(lbl_tabla, columns=["CORRAL", "CLIENTE", "CATEGORIA", "PINTURA", "CANTIDAD", "KGS", "PRECIO", "BRUTO"], selectmode=tk.BROWSE, show='headings') 
		tabla.pack(side=LEFT, fill="both", expand=True)
		sbr.config(command=tabla.yview)
		tabla.config(yscrollcommand=sbr.set)


		tabla.heading("CORRAL", text="CORRAL", command=lambda: treeview_sort_column(tabla, "CORRAL", False))
		tabla.heading("CLIENTE", text="CLIENTE", command=lambda: treeview_sort_column(tabla, "CLIENTE", False))
		tabla.heading("CATEGORIA", text="CATEGORIA", command=lambda: treeview_sort_column(tabla, "CATEGORIA", False))
		tabla.heading("PINTURA", text="PINTURA", command=lambda: treeview_sort_column(tabla, "PINTURA", False))
		tabla.heading("CANTIDAD", text="CANTIDAD", command=lambda: treeview_sort_column(tabla, "CANTIDAD", False))
		tabla.heading("KGS", text="KGS", command=lambda: treeview_sort_column(tabla, "KGS", False))
		tabla.heading("PRECIO", text="PRECIO", command=lambda: treeview_sort_column(tabla, "PRECIO", False))
		tabla.heading("BRUTO", text="BRUTO", command=lambda: treeview_sort_column(tabla, "BRUTO", False))


		tabla.column("CORRAL", width=30)
		tabla.column("CLIENTE", width=150)
		tabla.column("CATEGORIA", width=150)
		tabla.column("PINTURA", width=30)
		tabla.column("CANTIDAD", width=30)
		tabla.column("KGS", width=30)
		tabla.column("PRECIO", width=30)
		tabla.column("BRUTO", width=30)


		#tabla.bind("<Double-1>", (lambda event: elegirItem(tabla.item(tabla.selection()))))
		#tabla.bind("<Return>", (lambda event: elegirItem(tabla.item(tabla.selection()))))

		diccionario_objetos["tabla"] = tabla


	#TABLA GASTOS
	if(True):
		sbrGastos = Scrollbar(lbl_tablaGastos)
		sbrGastos.pack(side=RIGHT, fill="y")


		tablaGastos = ttk.Treeview(lbl_tablaGastos, columns=["GASTOS", "BASE IMPONIBLE", "ALICUOTA", "IMPORTE", "%IVA", "$IVA"], selectmode=tk.BROWSE, show='headings') 
		tablaGastos.pack(side=LEFT, fill="both", expand=True)
		sbrGastos.config(command=tablaGastos.yview)
		tablaGastos.config(yscrollcommand=sbrGastos.set)


		tablaGastos.heading("GASTOS", text="GASTOS", command=lambda: treeview_sort_column(tablaGastos, "GASTOS", False))
		tablaGastos.heading("BASE IMPONIBLE", text="BASE IMPONIBLE", command=lambda: treeview_sort_column(tablaGastos, "BASE IMPONIBLE", False))
		tablaGastos.heading("ALICUOTA", text="ALICUOTA", command=lambda: treeview_sort_column(tablaGastos, "ALICUOTA", False))
		tablaGastos.heading("IMPORTE", text="IMPORTE", command=lambda: treeview_sort_column(tablaGastos, "IMPORTE", False))
		tablaGastos.heading("%IVA", text="%IVA", command=lambda: treeview_sort_column(tablaGastos, "%IVA", False))
		tablaGastos.heading("$IVA", text="$IVA", command=lambda: treeview_sort_column(tablaGastos, "$IVA", False))


		tablaGastos.column("GASTOS", width=250)
		tablaGastos.column("BASE IMPONIBLE", width=30)
		tablaGastos.column("ALICUOTA", width=30)
		tablaGastos.column("IMPORTE", width=30)
		tablaGastos.column("%IVA", width=30)
		tablaGastos.column("$IVA", width=30)



		tablaGastos.bind("<Double-1>", (lambda event: elegirItem(tablaGastos.item(tablaGastos.selection()))))
		tablaGastos.bind("<Return>", (lambda event: elegirItem(tablaGastos.item(tablaGastos.selection()))))

		diccionario_objetos["tablaGastos"] = tablaGastos


	#DATOS
	if(True):
		lblBuscador = tk.Label(lbl_datos, backgroun="#f0f0f0", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblBuscador.place(x=2, y=2, width=300, height=306)

		lblDatosVendedor1 = tk.Label(lbl_datos, backgroun="#f0f0f0", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblDatosVendedor1.place(x=304, y=2, width=300, height=306)

		lblTotalesPadre = tk.Label(lbl_datos, backgroun="#f0f0f0", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblTotalesPadre.place(x=606, y=2, width=400, height=306)

		lblTotales = tk.Label(lblTotalesPadre, backgroun="#f0f0f0")
		lblTotales.grid(column=0, row=0)

		lblBotonesAxiones = tk.Label(lblTotalesPadre, backgroun="#f0f0f0")
		lblBotonesAxiones.grid(column=0, row=1)

		pestañas = ttk.Notebook(lblDatosVendedor1)

		lblDatosVendedor = Label(lblDatosVendedor1)
		lblDatosVarios = Label(lblDatosVendedor1)

		pestañas.add(lblDatosVarios, text="DATOS LIQUIDACION", padding = 5)
		pestañas.add(lblDatosVendedor, text="DATOS VENDEDOR", padding = 3)

		#pestañas.place(x = 0, y = 0, relwidth = 1, relheight = 1)
		pestañas.pack()


	#DATOS VARIOS
	if(True):
		tk.Label(lblDatosVarios, text="N°:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 0, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="Fecha:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 1, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="DTE:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 2, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="Cond. Pago:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 3, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="Destino:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 4, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="Contacto:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 5, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="Total KG:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 6, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="Tot. Cabezas:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 7, pady=1, padx=5)
		tk.Label(lblDatosVarios, text="Observaciones:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 8, pady=1, padx=5)

		entry_num = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		entry_fecha = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		entry_dte = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		entry_condPago = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		entry_destino = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		entry_contacto = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		entry_totalKg = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		entry_totalCabezas = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')
		#entry_observaciones = Entry(lblDatosVarios, font=("Helvetica", 10), width=24, justify='center')

		txt_observaciones = scrolledtext.ScrolledText(lblDatosVarios, width=19, height=3)
		txt_observaciones.grid(column=1, row=8)

		entry_num.grid(sticky="W", column=1, row=0)
		entry_fecha.grid(sticky="W", column=1, row=1)
		entry_dte.grid(sticky="W", column=1, row=2)
		entry_condPago.grid(sticky="W", column=1, row=3)
		entry_destino.grid(sticky="W", column=1, row=4)
		entry_contacto.grid(sticky="W", column=1, row=5)
		entry_totalKg.grid(sticky="W", column=1, row=6)
		entry_totalCabezas.grid(sticky="W", column=1, row=7)
		#entry_observaciones.grid(sticky="W", column=1, row=8)

		diccionario_objetos["entry_num"] = entry_num
		diccionario_objetos["entry_fecha"] = entry_fecha
		diccionario_objetos["entry_dte"] = entry_dte
		diccionario_objetos["entry_condPago"] = entry_condPago
		diccionario_objetos["entry_destino"] = entry_destino
		diccionario_objetos["entry_contacto"] = entry_contacto
		diccionario_objetos["entry_totalKg"] = entry_totalKg
		diccionario_objetos["entry_totalCabezas"] = entry_totalCabezas
		diccionario_objetos["txt_observaciones"] = txt_observaciones


	#DATOS COMPRADOR
	if(True):
		tk.Label(lblDatosVendedor, text="Nombre:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 0, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="CUIT:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 1, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="IVA:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 2, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="IIBB:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 3, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="Carácter:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 4, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="Domicilio:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 5, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="Localidad:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 6, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="Provincia:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 7, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="Cod Postal:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 8, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="Renspa:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 9, pady=1, padx=5)
		tk.Label(lblDatosVendedor, text="Ruca:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 10, pady=1, padx=5)

		entry_nombre = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_cuit = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_iva = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_iibb = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_caracter = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_domicilio = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_localidad = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_provincia = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_codPostal = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_renspa = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')
		entry_ruca = Entry(lblDatosVendedor, font=("Helvetica", 10), width=28, justify='center')

		entry_nombre.grid(column=1, row=0)
		entry_cuit.grid(column=1, row=1)
		entry_iva.grid(column=1, row=2)
		entry_iibb.grid(column=1, row=3)
		entry_caracter.grid(column=1, row=4)
		entry_domicilio.grid(column=1, row=5)
		entry_localidad.grid(column=1, row=6)
		entry_provincia.grid(column=1, row=7)
		entry_codPostal.grid(column=1, row=8)
		entry_renspa.grid(column=1, row=9)
		entry_ruca.grid(column=1, row=10)

		diccionario_objetos["entry_nombre"] = entry_nombre
		diccionario_objetos["entry_cuit"] = entry_cuit
		diccionario_objetos["entry_iva"] = entry_iva
		diccionario_objetos["entry_iibb"] = entry_iibb
		diccionario_objetos["entry_caracter"] = entry_caracter
		diccionario_objetos["entry_domicilio"] = entry_domicilio
		diccionario_objetos["entry_localidad"] = entry_localidad
		diccionario_objetos["entry_provincia"] = entry_provincia
		diccionario_objetos["entry_codPostal"] = entry_codPostal
		diccionario_objetos["entry_renspa"] = entry_renspa
		diccionario_objetos["entry_ruca"] = entry_ruca


	#TOTALES
	if(True):
		tk.Label(lblTotales, text="Subtotal Martillo:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 0, pady=1, padx=5)
		tk.Label(lblTotales, text="Descuento pago contado:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 1, pady=1, padx=5)
		tk.Label(lblTotales, text="SUBTOTAL:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 0, row = 2, pady=1, padx=5)
		tk.Label(lblTotales, text="Interes dias de pago diferido:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 3, pady=1, padx=5)
		tk.Label(lblTotales, text="IVA hacienda:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 4, pady=1, padx=5)
		tk.Label(lblTotales, text="IVA interes:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 5, pady=1, padx=5)
		tk.Label(lblTotales, text="Comision + IVA:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 6, pady=1, padx=5)
		tk.Label(lblTotales, text="RETENCION IIBB:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10)).grid(sticky="E", column = 0, row = 7, pady=1, padx=5)
		tk.Label(lblTotales, text="TOTAL LIQUIDADO:", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 12, "bold")).grid(sticky="E", column = 0, row = 8, pady=1, padx=5)

		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 0, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 1, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 2, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 3, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 4, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 5, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 6, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 1, row = 7, pady=1)
		tk.Label(lblTotales, text="$", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 12, "bold")).grid(sticky="E", column = 1, row = 8, pady=1)

		entry_subtotalMartillo = Entry(lblTotales, font=("Helvetica", 10), width=13, justify='right')
		entry_descuento = Entry(lblTotales, font=("Helvetica", 10), width=13, justify='right')
		entry_subtotal = Entry(lblTotales, font=("Helvetica", 10, "bold"), width=13, justify='right')
		entry_intereses = Entry(lblTotales, font=("Helvetica", 10), width=13, justify='right')
		entry_ivaHacienda = Entry(lblTotales, font=("Helvetica", 10), width=13, justify='right')
		entry_ivaInteres = Entry(lblTotales, font=("Helvetica", 10), width=13, justify='right')
		entry_comisionIva = Entry(lblTotales, font=("Helvetica", 10), width=13, justify='right')
		entry_retencion = Entry(lblTotales, font=("Helvetica", 10), width=13, justify='right')
		entry_total = Entry(lblTotales, font=("Helvetica", 12, "bold"), width=10, justify='right')



		entry_subtotalMartillo.grid(column=2, row=0)
		entry_descuento.grid(column=2, row=1)
		entry_subtotal.grid(column=2, row=2)
		entry_intereses.grid(column=2, row=3)
		entry_ivaHacienda.grid(column=2, row=4)
		entry_ivaInteres.grid(column=2, row=5)
		entry_comisionIva.grid(column=2, row=6)
		entry_retencion.grid(column=2, row=7)
		entry_total.grid(column=2, row=8)


		diccionario_objetos["entry_subtotalMartillo"] = entry_subtotalMartillo
		diccionario_objetos["entry_descuento"] = entry_descuento
		diccionario_objetos["entry_subtotal"] = entry_subtotal
		diccionario_objetos["entry_intereses"] = entry_intereses
		diccionario_objetos["entry_ivaHacienda"] = entry_ivaHacienda
		diccionario_objetos["entry_ivaInteres"] = entry_ivaInteres
		diccionario_objetos["entry_comisionIva"] = entry_comisionIva
		diccionario_objetos["entry_retencion"] = entry_retencion
		diccionario_objetos["entry_total"] = entry_total

		#porcentajes
		tk.Label(lblTotales, text="%", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 3, row = 1, pady=1)
		entry_porcDescuento = Entry(lblTotales, font=("Helvetica", 10), width=4)
		entry_porcDescuento.grid(column=4, row=1, padx = 2)
		entry_porcDescuento.insert(0, 0.0)

		tk.Label(lblTotales, text="dias", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 8)).grid(sticky="S", column = 3, row = 2, pady=1)
		tk.Label(lblTotales, text="%", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 8)).grid(sticky="S", column = 4, row = 2, pady=1)

		entry_interesPorcentaje = Entry(lblTotales, font=("Helvetica", 10), width=5)
		entry_interesDias = Entry(lblTotales, font=("Helvetica", 10), width=5)

		entry_interesPorcentaje.grid(sticky="N", column = 3, row = 3, pady=1, padx = 2)
		entry_interesDias.grid(sticky="N", column = 4, row = 3, pady=1, padx = 2)

		entry_interesPorcentaje.insert(0, 0.0)
		entry_interesDias.insert(0, 0)

		tk.Label(lblTotales, text="%", backgroun="#f0f0f0", foreground="#000000", font=("Helvetica", 10, "bold")).grid(sticky="E", column = 3, row = 6, pady=1)

		entry_comisionPorcentaje = Entry(lblTotales, font=("Helvetica", 10), width=5)
		entry_comisionPorcentaje.grid(column=4, row=6)
		entry_comisionPorcentaje.insert(0, 0.0)

		diccionario_objetos["entry_porcDescuento"] = entry_porcDescuento
		diccionario_objetos["entry_interesPorcentaje"] = entry_interesPorcentaje
		diccionario_objetos["entry_interesDias"] = entry_interesDias
		diccionario_objetos["entry_comisionPorcentaje"] = entry_comisionPorcentaje

		#Checkbutton
		checkiva = IntVar()
		checkretencion = IntVar()

		checkiva.set(1)
		checkretencion.set(1)

		Checkbutton(lblTotales, text="Calc", variable=checkiva, onvalue=1, offvalue=0, command=REALIZARCalculos).grid(column=3, row=4)
		Checkbutton(lblTotales, text="Calc", variable=checkretencion, onvalue=1, offvalue=0, command=REALIZARCalculos).grid(column=3, row=7)

		diccionario_objetos["checkiva"] = checkiva
		diccionario_objetos["checkretencion"] = checkretencion

		entry_porcDescuento.bind("<Return>", (lambda event: REALIZARCalculos()))
		entry_interesPorcentaje.bind("<Return>", (lambda event: REALIZARCalculos()))
		entry_interesDias.bind("<Return>", (lambda event: REALIZARCalculos()))
		entry_comisionPorcentaje.bind("<Return>", (lambda event: REALIZARCalculos()))

	#BOTONES
	if(True):
		btn_guardar = tk.Button(lblBotonesAxiones, text="GUARDAR", compound="top", backgroun="#b3f2bc", font=("Helvetica", 15, "bold"), state = "disabled", command = guardar)
		btn_guardar.grid(column=0, row=0, pady = 15, padx = 10)

		#btn_eliminar = tk.Button(lblBotonesAxiones, text="ELIMINAR", compound="top", backgroun="#FF6E6E", font=("Helvetica", 15, "bold"), state = "disabled")
		#btn_eliminar.grid(column=1, row=0, pady = 20, padx = 10)

		btn_exportar = tk.Button(lblBotonesAxiones, text="GUARDAR Y\nEXPORTAR PDF", compound="top", backgroun="#b3f2bc", font=("Helvetica", 9, "bold"), state = "disabled", command=guardarExportar)
		btn_exportar.grid(column=2, row=0, pady = 15, padx = 10)

		diccionario_objetos["btn_guardar"] = btn_guardar
		#diccionario_objetos["btn_eliminar"] = btn_eliminar
		diccionario_objetos["btn_exportar"] = btn_exportar


	#BUSCADOR PRODUCTORES
	if(True):
		lbl_comprador_aux = Label(lblBuscador, backgroun="#f0f0f0")
		lbl_comprador_aux.place(x = 3, y = 0, width = 290, height = 302)

		lbl_ventana_productor_buscador_entry = tk.LabelFrame(lbl_comprador_aux, text="Filtrar", backgroun="#f0f0f0")
		lbl_ventana_productor_buscador_tabla = tk.LabelFrame(lbl_comprador_aux, text="Productores", backgroun="#f0f0f0")

		lbl_ventana_productor_buscador_entry.grid(column = 0, row = 0)
		lbl_ventana_productor_buscador_tabla.grid(column = 0, row = 1)

		#--
		entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="31")
		entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = 5)

		btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar", command= lambda: vendedorFiltrar())
		btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 0)

		sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
		sbr_productor.pack(side=RIGHT, fill="y")

		tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("alias", "cuit"), selectmode=tk.BROWSE, height=10, show='headings') 
		tabla_productor.pack(side=LEFT, fill="both", expand=True)
		sbr_productor.config(command=tabla_productor.yview)
		tabla_productor.config(yscrollcommand=sbr_productor.set)

		tabla_productor.heading("alias", text="ALIAS")
		tabla_productor.heading("cuit", text="CUIT/DNI")

		tabla_productor.column("alias", width=150)
		tabla_productor.column("cuit", width=100)

		diccionario_objetos["entry_productor"] = entry_filtrar_productor
		diccionario_objetos["tabla_vendedores"] = tabla_productor

		entry_filtrar_productor.bind("<Return>", (lambda event: vendedorFiltrar()))
		tabla_productor.bind('<Double-1>', (lambda event: seleccionarTablaVendedor()))
		tabla_productor.bind('<Return>', (lambda event: seleccionarTablaVendedor()))


vendedorFiltrar()

window.bind("<Control-s>", (lambda event: window.destroy()))
window.mainloop()
