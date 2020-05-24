#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

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
diccionario_datos = {}
diccionario_entry_pesaje = {}
diccionario_entry_hacienda = {}
diccionario_entry_observaciones = {}
diccionario_entry_dte = {}
diccionario_entry_flete = {}
diccionario_entry_flete["flete"] = "flete n°"


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

def guardar():
	entities = []
	try:
		entities = [str(diccionario_datos["remate"]), 
		str(diccionario_datos["cuit"]), 
		str(diccionario_entry_hacienda["entry_cantidad"].get()), 
		str(diccionario_entry_hacienda["entry_corral"].get()), 
		str(diccionario_entry_hacienda["combo_catVenta"].get()),
		str(diccionario_entry_hacienda["combo_catHacienda"].get()), 
		str(diccionario_entry_hacienda["entry_pintura"].get()), 
		str(diccionario_entry_pesaje["entry_brutoTropa"].get()), 
		str(diccionario_entry_pesaje["entry_brutoPromedio"].get()), 
		str(diccionario_entry_pesaje["entry_desbastePorcentaje"].get()),
		str(diccionario_entry_pesaje["entry_desbasteKg"].get()),
		str(diccionario_entry_pesaje["entry_netoTropa"].get()),
		str(diccionario_entry_pesaje["entry_netoPromedio"].get()), 
		str(diccionario_entry_observaciones["entry_observaciones"].get()),
		str(diccionario_entry_observaciones["txt_observaciones"].get("1.0", tk.END)),
		str(diccionario_entry_dte["entry_dte"].get()),
		str(diccionario_entry_flete["flete"]),
		"activo"]
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos")

	if(diccionario_datos["lote"]=="nuevo"):
		if(entities!=[]):
			try:
				con = sql_connection()
				cursorObj = con.cursor()
				cursorObj.execute("INSERT INTO lotes VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
				con.commit()
				messagebox.showinfo("Éxito", "Lote ingresado con éxito!")
			except:
				messagebox.showerror("ERROR", "Error al cargar los datos a la DB")
	else:
		if(entities!=[]):
			respuesta = messagebox.askquestion("ATENCION", "¿Desea EDITAR esta lote?")
			if respuesta == 'yes':
				try:
					entities.append(diccionario_datos["lote"])
					con = sql_connection()
					cursorObj = con.cursor()
					cursorObj.execute('UPDATE lotes SET remate = ?, productor = ?, cantidad = ?, corral = ?, catVenta = ?, catHacienda = ?, pintura = ?, kgBruto = ?, kgProm = ?, desbastePorcentaje = ?, desbasteKg = ?, neto = ?, netoPromedio = ?, observaciones = ?, observacionesDescripcion = ?, dte = ?, flete = ?, estado = ? where id = ?', entities)
					con.commit()
					messagebox.showinfo("Éxito", "Lote ingresado con éxito!")
				except:
					messagebox.showerror("ERROR", "Error al cargar los datos a la DB")

	diccionario_datos["funcion"](diccionario_datos["cuit"])
	diccionario_datos["funcion2"]()
	diccionario_datos["funcion3"]()




def foco(entry):
	entry.focus()

def obtenerCatVenta():
	lista = []
	con = sql_connection()
	rows = actualizar_db(con, "catVenta", "")

	for row in rows:
		lista.append(row[2])

	return lista

def obtenerCatHacienda():
	lista = []
	con = sql_connection()
	rows = actualizar_db(con, "catHacienda", "")

	for row in rows:
		lista.append(row[2])

	return lista

def obtenerPintura():
	try:
		con = sql_connection()
		condiciones = " WHERE remate = '" + diccionario_datos["remate"] + "' AND productor = '" + diccionario_datos["cuit"] + "'"
		rows = actualizar_db(con, "pintura", condiciones)
		return rows[0][2]
	except:
		return ""





		diccionario_entry_pesaje["entry_brutoTropa"] = entry_brutoTropa
		diccionario_entry_pesaje["entry_brutoPromedio"] = entry_brutoPromedio
		diccionario_entry_pesaje["entry_desbastePorcentaje"] = entry_desbastePorcentaje
		diccionario_entry_pesaje["entry_desbasteKg"] = entry_desbasteKg
		diccionario_entry_pesaje["entry_netoTropa"] = entry_netoTropa
		diccionario_entry_pesaje["entry_netoPromedio"] = entry_netoPromedio


def calc_brutoTropa():
	entrada = ""
	try:
		entrada = float(diccionario_entry_pesaje["entry_brutoTropa"].get())
	except:
		messagebox.showerror("ERROR", "Ingrese un numero válido")

	try:
		cantidad = float(diccionario_entry_hacienda["entry_cantidad"].get())
	except:
		messagebox.showerror("ERROR", "No se pudo obtener cantidad")

	try:
		KgBrutoPromedio = round(entrada/cantidad, 2)
		diccionario_entry_pesaje["entry_brutoPromedio"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_brutoPromedio"].insert(0, str(KgBrutoPromedio))
		diccionario_entry_pesaje["entry_brutoPromedio"].focus()

		diccionario_entry_pesaje["entry_desbasteKg"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_desbastePorcentaje"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_desbasteKg"].insert(0, 0.0)
		diccionario_entry_pesaje["entry_desbastePorcentaje"].insert(0, 0.0)

		diccionario_entry_pesaje["entry_netoTropa"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_netoPromedio"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_netoTropa"].insert(0, entrada)
		diccionario_entry_pesaje["entry_netoPromedio"].insert(0, KgBrutoPromedio)

	except:
		messagebox.showerror("ERROR", "Error de cálculo, verifique los datos")

def calc_brutoPromedio():
	entrada = ""
	try:
		entrada = float(diccionario_entry_pesaje["entry_brutoPromedio"].get())
	except:
		messagebox.showerror("ERROR", "Ingrese un numero válido")

	try:
		diccionario_entry_pesaje["entry_netoPromedio"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_netoPromedio"].insert(0, entrada)
		diccionario_entry_pesaje["entry_desbastePorcentaje"].focus()

	except:
		messagebox.showerror("ERROR", "Error de cálculo, verifique los datos")

def calc_desbastePorcentaje():
	try:
		entrada_neto = float(diccionario_entry_pesaje["entry_brutoTropa"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener neto")

	try:
		entrada_promedio = float(diccionario_entry_pesaje["entry_brutoPromedio"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener promedio")

	try:
		entrada = float(diccionario_entry_pesaje["entry_desbastePorcentaje"].get())
	except:
		messagebox.showerror("ERROR", "Ingrese un numero válido")

	try:
		desbasteKilos = round(entrada_neto*(entrada/100), 2)
		netoTropa = round(entrada_neto - desbasteKilos, 2)
		netoPromedio = round(entrada_promedio - (entrada_promedio*(entrada/100)), 2)


		diccionario_entry_pesaje["entry_desbasteKg"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_desbasteKg"].insert(0, desbasteKilos)

		diccionario_entry_pesaje["entry_netoTropa"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_netoPromedio"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_netoTropa"].insert(0, netoTropa)
		diccionario_entry_pesaje["entry_netoPromedio"].insert(0, netoPromedio)

		diccionario_entry_pesaje["entry_desbasteKg"].focus()

	except:
		messagebox.showerror("ERROR", "Error de cálculo, verifique los datos")

def calc_desbasteKg():
	try:
		entrada_neto = float(diccionario_entry_pesaje["entry_brutoTropa"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener neto")

	try:
		entrada_promedio = float(diccionario_entry_pesaje["entry_brutoPromedio"].get())
	except:
		messagebox.showerror("ERROR", "Error al obtener promedio")

	try:
		entrada = float(diccionario_entry_pesaje["entry_desbasteKg"].get())
	except:
		messagebox.showerror("ERROR", "Ingrese un numero válido")

	try:
		desbastePorcentaje = round((entrada/entrada_neto)*100, 2)
		netoTropa = round(entrada_neto - entrada, 2)
		netoPromedio = round(entrada_promedio - (entrada_promedio*(desbastePorcentaje/100)), 2)


		diccionario_entry_pesaje["entry_desbastePorcentaje"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_desbastePorcentaje"].insert(0, desbastePorcentaje)

		diccionario_entry_pesaje["entry_netoTropa"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_netoPromedio"].delete(0, tk.END)
		diccionario_entry_pesaje["entry_netoTropa"].insert(0, netoTropa)
		diccionario_entry_pesaje["entry_netoPromedio"].insert(0, netoPromedio)

		diccionario_entry_pesaje["entry_netoTropa"].focus()

	except:
		messagebox.showerror("ERROR", "Error de cálculo, verifique los datos")

def cargarLote():
	con = sql_connection()
	condiciones = " WHERE id = " + str(diccionario_datos["lote"])
	rows = actualizar_db(con, "lotes", condiciones)
	
	row = rows[0]

	borrarTodo()

	diccionario_entry_hacienda["entry_cantidad"].insert(0, str(row[3]))
	diccionario_entry_hacienda["combo_catVenta"].current(0)#5
	diccionario_entry_hacienda["combo_catHacienda"].current(0)#6
	diccionario_entry_hacienda["entry_corral"].insert(0, str(row[4]))
	diccionario_entry_hacienda["entry_pintura"].insert(0, str(row[7]))

	diccionario_entry_pesaje["entry_brutoTropa"].insert(0, str(row[8]))
	diccionario_entry_pesaje["entry_brutoPromedio"].insert(0, str(row[9]))
	diccionario_entry_pesaje["entry_desbastePorcentaje"].insert(0, str(row[10]))
	diccionario_entry_pesaje["entry_desbasteKg"].insert(0, str(row[11]))
	diccionario_entry_pesaje["entry_netoTropa"].insert(0, str(row[12]))
	diccionario_entry_pesaje["entry_netoPromedio"].insert(0, str(row[13]))

	diccionario_entry_observaciones["entry_observaciones"].insert(0, str(row[14]))
	diccionario_entry_observaciones["txt_observaciones"].insert("1.0", str(row[15]))#15

	diccionario_entry_dte["entry_dte"].insert(0, str(row[16]))

	diccionario_entry_flete["flete"] = str(row[17])


def borrarTodo():
	diccionario_entry_hacienda["entry_cantidad"].delete(0, tk.END)
	diccionario_entry_hacienda["combo_catVenta"].current(0)
	diccionario_entry_hacienda["combo_catHacienda"].current(0)
	diccionario_entry_hacienda["entry_corral"].delete(0, tk.END)
	diccionario_entry_hacienda["entry_pintura"].delete(0, tk.END)

	diccionario_entry_pesaje["entry_brutoTropa"].delete(0, tk.END)
	diccionario_entry_pesaje["entry_brutoPromedio"].delete(0, tk.END)
	diccionario_entry_pesaje["entry_desbastePorcentaje"].delete(0, tk.END)
	diccionario_entry_pesaje["entry_desbasteKg"].delete(0, tk.END)
	diccionario_entry_pesaje["entry_netoTropa"].delete(0, tk.END)
	diccionario_entry_pesaje["entry_netoPromedio"].delete(0, tk.END)

	diccionario_entry_observaciones["entry_observaciones"].delete(0, tk.END)
	diccionario_entry_observaciones["txt_observaciones"].delete("1.0", tk.END)

	diccionario_entry_dte["entry_dte"].delete(0, tk.END)

	diccionario_entry_flete["flete"] = "flete n°"



def ingreso(cuit, lote, remate, cargarTablaLotes, limpiarLote, cargarTabla):

	diccionario_datos["cuit"] = cuit
	diccionario_datos["lote"] = lote
	diccionario_datos["remate"] = remate
	diccionario_datos["funcion"] = cargarTablaLotes
	diccionario_datos["funcion2"] = limpiarLote
	diccionario_datos["funcion3"] = cargarTabla

	window = Tk()

	if(lote == "nuevo"):
		window.title("Cargar nuevo lote")
		text_boton = "GUARDAR"
	else:
		window.title("Editar lote")
		text_boton = "EDITAR"

	window.geometry("700x500")
	window.configure(bg='#E8F6FA')

	#PESTAÑAS
	if(True):
		pestañas = ttk.Notebook(window)

		label_hacienda = Label(window, backgroun="#E8F6FA")
		label_pesaje = Label(window, backgroun="#E8F6FA")
		label_observaciones = Label(window, backgroun="#E8F6FA")
		label_dte = Label(window, backgroun="#E8F6FA")
		label_flete = Label(window, backgroun="#E8F6FA")

		pestañas.add(label_hacienda, text="Hacienda", padding = 20)
		pestañas.add(label_pesaje, text="Pesaje", padding = 20)
		pestañas.add(label_observaciones, text="Observaciones", padding = 20)
		pestañas.add(label_dte, text="DTE", padding = 20)
		pestañas.add(label_flete, text="Flete", padding = 20)

		pestañas.place(x = 0, y = 0, width = 700, height = 400)

	modificar_altura = 0

	#PESTAÑA HACIENDA
	if(True):
		tk.Label(label_hacienda, font=("verdana",16), text="CANTIDAD:", anchor="e", bg='#E8F6FA').place(x=20, y=10, width = 300, height = 30)	
		tk.Label(label_hacienda, font=("verdana",16), text="CATEGORIA DE VENTA:", anchor="e", bg='#E8F6FA').place(x=20, y=60, width = 300, height = 30)	
		tk.Label(label_hacienda, font=("verdana",16), text="CATEGORIA DE HACIENDA:", anchor="e", bg='#E8F6FA').place(x=20, y=110, width = 300, height = 30)	
		tk.Label(label_hacienda, font=("verdana",16), text="CORRAL:", anchor="e", bg='#E8F6FA').place(x=20, y=160, width = 300, height = 30)	
		tk.Label(label_hacienda, font=("verdana",16), text="PINTURA:", anchor="e", bg='#E8F6FA').place(x=20, y=210, width = 300, height = 30)

		entry_cantidad = Entry(label_hacienda, font=("verdana",14))
		combo_catVenta = Combobox(label_hacienda, state="readonly", font=("verdana",14))
		combo_catHacienda = Combobox(label_hacienda, state="readonly", font=("verdana",14))
		entry_corral = Entry(label_hacienda, font=("verdana",14))
		entry_pintura = Entry(label_hacienda, font=("verdana",14))

		diccionario_entry_hacienda["entry_cantidad"] = entry_cantidad
		diccionario_entry_hacienda["combo_catVenta"] = combo_catVenta
		diccionario_entry_hacienda["combo_catHacienda"] = combo_catHacienda
		diccionario_entry_hacienda["entry_corral"] = entry_corral
		diccionario_entry_hacienda["entry_pintura"] = entry_pintura

		entry_cantidad.place(x=350, y=10+modificar_altura, width = 150)
		combo_catVenta.place(x=350, y=60+modificar_altura, width = 150)
		combo_catHacienda.place(x=350, y=110+modificar_altura, width = 150)
		entry_corral.place(x=350, y=160+modificar_altura, width = 150)
		entry_pintura.place(x=350, y=210+modificar_altura, width = 150)

		combo_catVenta["values"] = obtenerCatVenta()
		combo_catHacienda["values"] = obtenerCatHacienda()

		entry_pintura.delete(0, tk.END)
		entry_pintura.insert(0, obtenerPintura())

		entry_cantidad.bind("<Return>", (lambda event: foco(combo_catVenta)))
		combo_catVenta.bind("<Return>", (lambda event: foco(combo_catHacienda)))
		combo_catHacienda.bind("<Return>", (lambda event: foco(entry_corral)))
		entry_corral.bind("<Return>", (lambda event: foco(entry_pintura)))
		entry_pintura.bind("<Return>", (lambda event: foco(entry_brutoTropa)))

	#PESTAÑA PESAJE
	if(True):
		tk.Label(label_pesaje, font=("verdana",16), text="KG BRUTO TROPA:", anchor="e", bg='#E8F6FA').place(x=20, y=10, width = 300, height = 30)	
		tk.Label(label_pesaje, font=("verdana",16), text="KG BRUTO PROMEDIO:", anchor="e", bg='#E8F6FA').place(x=20, y=60, width = 300, height = 30)	
		tk.Label(label_pesaje, font=("verdana",16), text="DESBASTE %:", anchor="e", bg='#E8F6FA').place(x=20, y=110, width = 300, height = 30)	
		tk.Label(label_pesaje, font=("verdana",16), text="DESBASTE KG:", anchor="e", bg='#E8F6FA').place(x=20, y=160, width = 300, height = 30)	
		tk.Label(label_pesaje, font=("verdana",16), text="KG NETO TROPA:", anchor="e", bg='#E8F6FA').place(x=20, y=210, width = 300, height = 30)
		tk.Label(label_pesaje, font=("verdana",16), text="KG NETO PROMEDIO:", anchor="e", bg='#E8F6FA').place(x=20, y=260, width = 300, height = 30)

		entry_brutoTropa = Entry(label_pesaje, font=("verdana",14))
		entry_brutoPromedio = Entry(label_pesaje, font=("verdana",14))
		entry_desbastePorcentaje = Entry(label_pesaje, font=("verdana",14))
		entry_desbasteKg = Entry(label_pesaje, font=("verdana",14))
		entry_netoTropa = Entry(label_pesaje, font=("verdana",14))
		entry_netoPromedio = Entry(label_pesaje, font=("verdana",14))


		entry_brutoTropa.place(x=350, y=10+modificar_altura, width = 150)
		entry_brutoPromedio.place(x=350, y=60+modificar_altura, width = 150)
		entry_desbastePorcentaje.place(x=350, y=110+modificar_altura, width = 150)
		entry_desbasteKg.place(x=350, y=160+modificar_altura, width = 150)
		entry_netoTropa.place(x=350, y=210+modificar_altura, width = 150)
		entry_netoPromedio.place(x=350, y=260+modificar_altura, width = 150)

		diccionario_entry_pesaje["entry_brutoTropa"] = entry_brutoTropa
		diccionario_entry_pesaje["entry_brutoPromedio"] = entry_brutoPromedio
		diccionario_entry_pesaje["entry_desbastePorcentaje"] = entry_desbastePorcentaje
		diccionario_entry_pesaje["entry_desbasteKg"] = entry_desbasteKg
		diccionario_entry_pesaje["entry_netoTropa"] = entry_netoTropa
		diccionario_entry_pesaje["entry_netoPromedio"] = entry_netoPromedio


		entry_brutoTropa.bind("<Return>", (lambda event: calc_brutoTropa()))
		entry_brutoPromedio.bind("<Return>", (lambda event: calc_brutoPromedio()))
		entry_desbastePorcentaje.bind("<Return>", (lambda event: calc_desbastePorcentaje()))
		entry_desbasteKg.bind("<Return>", (lambda event: calc_desbasteKg()))
		entry_netoTropa.bind("<Return>", (lambda event: foco(entry_netoPromedio)))

	#PESTAÑA OBSERVACIONES
	if(True):
		tk.Label(label_observaciones, font=("verdana",14), text="Observaciones:", anchor="n", bg='#E8F6FA').place(x=20, y=18, width = 150)

		entry_observaciones = Entry(label_observaciones, font=("verdana",14))
		entry_observaciones.place(x=200, y=20+modificar_altura, width = 300)

		txt_observaciones = scrolledtext.ScrolledText(label_observaciones)
		txt_observaciones.place(x = 200, y = 70, width = 300, height = 150)

		diccionario_entry_observaciones["entry_observaciones"] = entry_observaciones
		diccionario_entry_observaciones["txt_observaciones"] = txt_observaciones

	#PESTAÑA DTE
	if(True):
		tk.Label(label_dte, font=("verdana",12), text="DTE:", anchor="e", bg='#E8F6FA').place(x=10, y=10, width = 150)

		entry_dte = Entry(label_dte, font=("verdana",12))
		entry_dte.place(x=200, y=10+modificar_altura, width = 300)

		diccionario_entry_dte["entry_dte"] = entry_dte

		lbl_origen = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
		lbl_destino = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="sunken")

		lbl_origen.place(x=20, y=50, width = 300, height =150)
		lbl_destino.place(x=340, y=50, width = 300, height =150)


		tk.Label(lbl_origen, font=("verdana",8), text="Datos de origen:", anchor="n", bg='#E8F6FA').place(x=0, y=0, width = 296)
		tk.Label(lbl_destino, font=("verdana",8), text="Datos de destino:", anchor="n", bg='#E8F6FA').place(x=0, y=0, width = 296)

		tk.Label(lbl_origen, font=("verdana",8), text="Localidad:", anchor="e", bg='#FFFFFF').place(x=20, y=30, width = 80)
		tk.Label(lbl_origen, font=("verdana",8), text="Provincia:", anchor="e", bg='#FFFFFF').place(x=20, y=50, width = 80)
		tk.Label(lbl_origen, font=("verdana",8), text="Renspa:", anchor="e", bg='#FFFFFF').place(x=20, y=80, width = 80)
		tk.Label(lbl_origen, font=("verdana",8), text="Titular:", anchor="e", bg='#FFFFFF').place(x=20, y=100, width = 80)
		tk.Label(lbl_origen, font=("verdana",8), text="CUIT:", anchor="e", bg='#FFFFFF').place(x=20, y=120, width = 80)

		entry_localidadOrigen = Entry(lbl_origen, font=("verdana",8))
		entry_provinciaOrigen = Entry(lbl_origen, font=("verdana",8))
		entry_renspaOrigen = Entry(lbl_origen, font=("verdana",8))
		entry_titularOrigen = Entry(lbl_origen, font=("verdana",8))
		entry_cuitOrigen = Entry(lbl_origen, font=("verdana",8))

		entry_localidadOrigen.place(x=120, y=30, width = 150)
		entry_provinciaOrigen.place(x=120, y=50, width = 150)
		entry_renspaOrigen.place(x=120, y=80, width = 150)
		entry_titularOrigen.place(x=120, y=100, width = 150)
		entry_cuitOrigen.place(x=120, y=120, width = 150)


		tk.Label(lbl_destino, font=("verdana",8), text="Localidad:", anchor="e", bg='#FFFFFF').place(x=20, y=30, width = 80)
		tk.Label(lbl_destino, font=("verdana",8), text="Provincia:", anchor="e", bg='#FFFFFF').place(x=20, y=50, width = 80)
		tk.Label(lbl_destino, font=("verdana",8), text="Renspa:", anchor="e", bg='#FFFFFF').place(x=20, y=80, width = 80)
		tk.Label(lbl_destino, font=("verdana",8), text="Titular:", anchor="e", bg='#FFFFFF').place(x=20, y=100, width = 80)
		tk.Label(lbl_destino, font=("verdana",8), text="CUIT:", anchor="e", bg='#FFFFFF').place(x=20, y=120, width = 80)

		entry_localidadDestino = Entry(lbl_destino, font=("verdana",8))
		entry_provinciaDestino = Entry(lbl_destino, font=("verdana",8))
		entry_renspaDestino = Entry(lbl_destino, font=("verdana",8))
		entry_titularDestino = Entry(lbl_destino, font=("verdana",8))
		entry_cuitDestino = Entry(lbl_destino, font=("verdana",8))

		entry_localidadDestino.place(x=120, y=30, width = 150)
		entry_provinciaDestino.place(x=120, y=50, width = 150)
		entry_renspaDestino.place(x=120, y=80, width = 150)
		entry_titularDestino.place(x=120, y=100, width = 150)
		entry_cuitDestino.place(x=120, y=120, width = 150)

		#DTE ANIMALES
		lbl_animalesAgregar = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="groove")
		lbl_animalesTabla = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="groove")

		lbl_animalesAgregar.place(x=20, y=210, width = 150, height =120)
		lbl_animalesTabla.place(x=190, y=210, width = 450, height =120)

		combo_dte_motivo = Combobox(lbl_animalesAgregar, state="readonly")
		combo_dte_especie = Combobox(lbl_animalesAgregar, state="readonly")
		combo_dte_categoria = Combobox(lbl_animalesAgregar, state="readonly")
		entry_dte_cantidad = Entry(lbl_animalesAgregar)
		tk.Label(lbl_animalesAgregar, font=("verdana",8), text="Cantidad:", bg='#FFFFFF').place(x=20, y=85)


		combo_dte_motivo.place(x=20, y=10, width = 110)
		combo_dte_especie.place(x=20, y=35, width = 110)
		combo_dte_categoria.place(x=20, y=60, width = 110)
		entry_dte_cantidad.place(x=90, y=85, width = 40)



		#Tabla
		sbr = Scrollbar(lbl_animalesTabla)
		sbr.pack(side=RIGHT, fill="y")

		tabla = ttk.Treeview(lbl_animalesTabla, columns=("especie", "categoria", "cantidad"), selectmode=tk.BROWSE, height=2)
		tabla.pack(side=LEFT, fill="both", expand=True)
		sbr.config(command=tabla.yview)
		tabla.config(yscrollcommand=sbr.set)

		tabla.heading("#0", text="Motivo")
		tabla.heading("especie", text="Especie")
		tabla.heading("categoria", text="Categoria")
		tabla.heading("cantidad", text="Cantidad")

		tabla.column("#0", width=115)
		tabla.column("especie", width=115)
		tabla.column("categoria", width=115)
		tabla.column("cantidad", width=50)

		def animalAgregar():
			motivo = str(combo_dte_motivo.get())
			especie = str(combo_dte_especie.get())
			categoria = str(combo_dte_categoria.get())
			cantidad = str(entry_dte_cantidad.get())

			tabla.insert("", tk.END, text = motivo, values = (especie, categoria,cantidad))
			#tabla.insert("", tk.END, text = "", values = ("", "TOTAL","25"))

		entry_dte_cantidad.bind("<Return>", (lambda event: animalAgregar()))

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





	btn_guardar = tk.Button(window, text=text_boton, backgroun="#CBF9E1", font=("Helvetica Neue",15,"bold"), command = guardar)
	btn_guardar.place(x=250, y = 420, width = 200, height = 60)

	btn_1 = tk.Button(window, text="BORRAR", backgroun="#CBF9E1", font=("Helvetica Neue",15,"bold"), command = borrarTodo)
	btn_1.place(x=500, y = 420, width = 200, height = 60)

	if(diccionario_datos["lote"]!="nuevo"):
		cargarLote()

		


	window.bind("<F5>", (lambda event: guardar(text_guardar, obtenerdatos(), borrarCampos, entry_alias, cargarCampos)))
	window.mainloop()


cuit = "20-40500364-4"
lote = "nuevo"
remate = "remate1"

def func():
	print("Func 1")
def func2():
	print("Func 2")
def func3():
	print("Func 3")

#ingreso(cuit, lote, remate, func, func2, func3)