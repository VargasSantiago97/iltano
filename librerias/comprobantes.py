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

padX = 5
padY = 5


TITLE_WINDOW_PRINCIPAL = "Comprobante"
#TAMAÑO_WINDOW_PRINCIPAL = "1222x768"
TAMAÑO_WINDOW_PRINCIPAL = "700x450"

def sql_connection():
	try:
		con = sqlite3.connect('../database/mydatabase.db')
		return con
	except Error:
		print(Error)

def sql_connection_2():
	try:
		con = sqlite3.connect('../database2/mydatabase.db')
		return con
	except Error:
		print(Error)


def actualizar_db(con, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows

def conseguir_condicion(entrada):
	if entrada == "0":
		return "Responsable Inscripto"
	if entrada == "1":
		return "Monotributista"	
	if entrada == "2":
		return "Consumidor Final"	
	if entrada == "3":
		return "Exento"	
	if entrada == "4":
		return "No especificado"


def abrir_ventana(mov, productor, cod):

	TITLE_WINDOW_PRINCIPAL = "Comprobante de " + mov

	window_comprobante = Tk()
	window_comprobante.title(TITLE_WINDOW_PRINCIPAL)
	window_comprobante.geometry(TAMAÑO_WINDOW_PRINCIPAL)
	window_comprobante.configure(bg='#E8F6FA')
	window_comprobante.resizable(0,0)

	Label(window_comprobante, text="PRODUCTOR", font=("verdana",10), background='#E8F6FA').place(x=38, y=20)
	Label(window_comprobante, text="COMPROBANTE", font=("verdana",10), background='#E8F6FA').place(x=20, y=50)
	Label(window_comprobante, text="FECHA", font=("verdana",10), background='#E8F6FA').place(x=75, y=80)
	Label(window_comprobante, text="PERIODO", font=("verdana",10), background='#E8F6FA').place(x=300, y=80)

	entry_buscar = Entry(window_comprobante)
	entry_buscar.place(x=130, y=20, width="160")
	entry_buscar.focus()

	entry_tipo = Entry(window_comprobante)
	entry_tipo.place(x=130, y=50, width="30")

	entry_letra = Entry(window_comprobante)
	entry_letra.place(x=163, y=50, width="20")

	entry_punto = Entry(window_comprobante)
	entry_punto.place(x=186, y=50, width="40")

	entry_factura = Entry(window_comprobante)
	entry_factura.place(x=230, y=50, width="60")


	entry_productor_nombre = Entry(window_comprobante, font=("verdana",10), foreground="#0F32E7", background = "white")
	entry_productor_nombre.place(x=300, y=19, width=380, height=25)
	entry_productor_nombre.insert(0, "<== Ingrese palabras clave, luego presione enter")
	entry_productor_nombre.config(state="disabled")


	entry_productor_cuit = Entry(window_comprobante, font=("verdana",10), foreground="#0F32E7", background = "white")
	entry_productor_cuit.place(x=300, y=49, width=130, height=25)
	entry_productor_cuit.insert(0, "CUIT")
	entry_productor_cuit.config(state="disabled")

	entry_productor_iva = Entry(window_comprobante, font=("verdana",10), foreground="#0F32E7", background = "white")
	entry_productor_iva.place(x=440, y=49, width=240, height=25)
	entry_productor_iva.insert(0, "Condicion IVA")
	entry_productor_iva.config(state="disabled")

	entry_fecha = Entry(window_comprobante)
	entry_fecha.place(x=130, y=80, width="60")

	combo_periodo = Combobox(window_comprobante).place(x=370, y=80)

	#PESTAÑAS:
	pestañas = ttk.Notebook(window_comprobante)

	label_importes = Label(window_comprobante, background='#E8F6FA')
	label_items = Label(window_comprobante)
	label_observaciones = Label(window_comprobante)
	label_comp_asociados = Label(window_comprobante)

	pestañas.add(label_importes, text="IMPORTES", padding = 20)
	pestañas.add(label_items, text="ITEMS", padding = 5)
	pestañas.add(label_observaciones, text="OBSERVACIONES", padding = 20)
	pestañas.add(label_comp_asociados, text="COMPROBANTES ASOCIADOS", padding = 20)

	pestañas.place(x = 20, y = 130, width = 660, height = 250)

	#PESTAÑA IMPORTES:
	Label(label_importes, font=("verdana",10), text="Neto 21%", anchor="e", background='#E8F6FA').place(x=20, y=20, width=100, height=25)
	Label(label_importes, font=("verdana",10), text="Neto 10.5%", anchor="e", background='#E8F6FA').place(x=20, y=50, width=100, height=25)
	Label(label_importes, font=("verdana",10), text="No gravado", anchor="e", background='#E8F6FA').place(x=20, y=80, width=100, height=25)

	entry_neto21 = Entry(label_importes)
	entry_neto21.place(x=130, y=20, width="80")

	entry_neto10 = Entry(label_importes)
	entry_neto10.place(x=130, y=50, width="80")

	entry_nogravado = Entry(label_importes)
	entry_nogravado.place(x=130, y=80, width="80")

	#--

	Label(label_importes, font=("verdana",10), text="I.V.A. 21%", anchor="e", background='#E8F6FA').place(x=250, y=20, width=100, height=25)
	Label(label_importes, font=("verdana",10), text="I.V.A. 10.5%", anchor="e", background='#E8F6FA').place(x=250, y=50, width=100, height=25)
	Label(label_importes, font=("verdana",10), text="TOTAL", anchor="e", background='#E8F6FA').place(x=250, y=80, width=100, height=25)

	entry_21 = Entry(label_importes)
	entry_21.place(x=360, y=20, width="80")

	entry_10 = Entry(label_importes)
	entry_10.place(x=360, y=50, width="80")

	entry_total = Entry(label_importes)
	entry_total.place(x=360, y=80, width="80")

	entry_neto21.insert(0, 00.00)
	entry_neto10.insert(0, 00.00)
	entry_nogravado.insert(0, 00.00)
	entry_21.insert(0, 00.00)
	entry_10.insert(0, 00.00)
	entry_total.insert(0, 00.00)


	#PESTAÑA ITEMS:

	lbl_agregar_item = LabelFrame(label_items, text="Cargar nuevo")
	lbl_tabla_items = LabelFrame(label_items, text="Items")

	lbl_agregar_item.place(x = 3, y = 0, width = 640, height = 80)
	lbl_tabla_items.place(x = 3, y = 80, width = 640, height = 274)

	lbl_base_tabla = Label(lbl_tabla_items)
	lbl_base_tabla.grid(column = 0, row = 0)

	sbr = Scrollbar(lbl_base_tabla)
	sbr.pack(side=RIGHT, fill="y")

	tabla = ttk.Treeview(lbl_base_tabla, columns=("item", "cantidad", "precio", "neto", "iva", "total"), selectmode=tk.BROWSE, height=4)
	tabla.pack(side=LEFT, fill="both", expand=True)
	sbr.config(command=tabla.yview)
	tabla.config(yscrollcommand=sbr.set)

	tabla.heading("#0", text="Cod.")
	tabla.heading("item", text="Item")
	tabla.heading("cantidad", text="Cantidad")
	tabla.heading("precio", text="Unidades")
	tabla.heading("neto", text="$/Unidad")
	tabla.heading("iva", text="$ Bruto")
	tabla.heading("total", text="$ IVA")



	tabla.column("#0", width=50)
	tabla.column("item", width=155)
	tabla.column("cantidad", width=70)
	tabla.column("precio", width=90)
	tabla.column("neto", width=90)
	tabla.column("iva", width=70)
	tabla.column("total", width=90)

	Label(lbl_agregar_item, font=("verdana",10), text="Item", anchor="e").place(x=5, y=5, width=70, height=25)
	Label(lbl_agregar_item, font=("verdana",10), text="Cantidad", anchor="e").place(x=5, y=30, width=70, height=25)
	Label(lbl_agregar_item, font=("verdana",10), text="$/Unidad", anchor="e").place(x=250, y=30, width=65, height=25)
	Label(lbl_agregar_item, font=("verdana",10), text="$Bruto", anchor="e").place(x=380, y=30, width=50, height=25)
	Label(lbl_agregar_item, font=("verdana",10), text="% IVA", anchor="e").place(x=500, y=30, width=45, height=25)

	entry_item = Entry(lbl_agregar_item)
	entry_item.place(x=90, y=6, width="80")

	entry_cantidad = Entry(lbl_agregar_item)
	entry_cantidad.config(state="disabled")
	entry_cantidad.place(x=90, y=31, width="80")

	entry_unidades = Entry(lbl_agregar_item)
	entry_unidades.insert(0, "Cabeza")
	entry_unidades.config(state="disabled")
	entry_unidades.place(x=180, y=31, width="50")

	entry_item_desc = Entry(lbl_agregar_item)
	entry_item_desc.config(state="disabled")
	entry_item_desc.place(x=180, y=6, width="450")

	entry_item_precio_unidad = Entry(lbl_agregar_item)
	entry_item_precio_unidad.config(state="disabled")
	entry_item_precio_unidad.place(x=320, y=31, width="50")

	entry_item_precio_bruto = Entry(lbl_agregar_item)
	entry_item_precio_bruto.config(state="disabled")
	entry_item_precio_bruto.place(x=435, y=31, width="50")

	combo_iva = Combobox(lbl_agregar_item)
	combo_iva.place(x=550, y=31, width=80)
	combo_iva["values"] = ["0.0", "10.5", "21.0"]
	combo_iva.current(0)


	#PESTAÑA OBSERVACIONES:

	txt_observaciones = scrolledtext.ScrolledText(label_observaciones)
	txt_observaciones.place(x = 0, y = 0, relwidth = 1, relheight = 1)

	#PESTAÑA COMPROBANTES ASOCIADOS:
	lbl_base_tabla_asociados = Label(label_comp_asociados)
	lbl_base_tabla_asociados.place(x = 2, y = 8)

	sbr_asociados = Scrollbar(lbl_base_tabla_asociados)
	sbr_asociados.pack(side=RIGHT, fill="y")

	tabla_asociados = ttk.Treeview(lbl_base_tabla_asociados, columns=("tipo", "comprobante", "productor", "cuit", "neto"), selectmode=tk.BROWSE, height=7)
	tabla_asociados.pack(side=LEFT, fill="both", expand=True)
	sbr_asociados.config(command=tabla_asociados.yview)
	tabla_asociados.config(yscrollcommand=sbr_asociados.set)

	tabla_asociados.heading("#0", text="Cod.")
	tabla_asociados.heading("tipo", text="Tipo")
	tabla_asociados.heading("comprobante", text="Comprobante")
	tabla_asociados.heading("productor", text="Productor")
	tabla_asociados.heading("cuit", text="CUIT")
	tabla_asociados.heading("neto", text="Neto")


	tabla_asociados.column("#0", width=50)
	tabla_asociados.column("tipo", width=70)
	tabla_asociados.column("comprobante", width=120)
	tabla_asociados.column("productor", width=170)
	tabla_asociados.column("cuit", width=90)
	tabla_asociados.column("neto", width=93)


	tabla_asociados.insert("", tk.END, text = str(0), iid=0, values = ("Descripcion Producto " + str(0), 
			"5", 
			"Cabeza", 
			"20-40500364-4", 
			"$500.000,00",
			"$00,00"))

	diccionario_respuesta = {"respuesta" : "NULL", "respuesta_item" : "NULL"}

	diccionario_orden = {
	"cabezal1" : "Cod",
	"cabezal2" : "Nombre",
	"cabezal3" : "Documento"
	}

	def tabla_elegir(rows, orden, funcion_salida):
		diccionario_respuesta["respuesta"] = "NULL"
		diccionario_respuesta["respuesta_codigo"] = "NULL"

		window_new = Tk()
		window_new.geometry("336x400")
		window_new.title("Seleccionar")
		window_new.resizable(0,0)

		lbl_tabla_elegir = Label(window_new)
		lbl_tabla_elegir.grid(column = 0, row = 0, padx=5, pady=5)

		sbr_elegir = Scrollbar(lbl_tabla_elegir)
		sbr_elegir.pack(side=RIGHT, fill="y")

		tabla_elegir = ttk.Treeview(lbl_tabla_elegir, columns=(orden["cabezal2"], orden["cabezal3"]), selectmode=tk.BROWSE, height=15)
		tabla_elegir.pack(side=LEFT, fill="both", expand=True)
		sbr_elegir.config(command=tabla_elegir.yview)
		tabla_elegir.config(yscrollcommand=sbr_elegir.set)

		tabla_elegir.heading("#0", text=orden["cabezal1"])
		tabla_elegir.heading(orden["cabezal2"], text=orden["cabezal2"])
		tabla_elegir.heading(orden["cabezal3"], text=orden["cabezal3"])

		tabla_elegir.column("#0", width=60)
		tabla_elegir.column(orden["cabezal2"], width=150)
		tabla_elegir.column(orden["cabezal3"], width=100)

		for i in tabla_elegir.get_children():
			tabla_elegir.delete()

		i = 0
		for row in rows:
			tabla_elegir.insert("", tk.END,  text = str(row[0]), iid=i, values = (row[1], row[2]))
			i = i+1


		def cerrar_window_elegir():
			window_new.destroy()


		def elegir():
			diccionario_respuesta["respuesta"] = (tabla_elegir.item(tabla_elegir.selection()[0]))['values']
			diccionario_respuesta["respuesta_codigo"] = (tabla_elegir.item(tabla_elegir.selection()[0], option = "text"))
			funcion_salida()

			#str((tabla_elegir.item(tabla_elegir.selection()[0]))['values'])

		tabla_elegir.bind("<Double-1>", (lambda event: elegir()))
		Button(window_new, text="Cerrar", command=lambda: cerrar_window_elegir()).grid(column = 0, row = 1, padx=5, pady=10)

		window_new.bind("<Escape>", (lambda event: cerrar_window_elegir()))
		window_new.mainloop()


	def cargar_productor(entrada):
		entry_productor_nombre.config(state="normal")
		entry_productor_nombre.delete(0, tk.END)
		entry_productor_nombre.insert(0, entrada["nombre"])
		entry_productor_nombre.config(state="disabled")

		entry_productor_cuit.config(state="normal")
		entry_productor_cuit.delete(0, tk.END)
		entry_productor_cuit.insert(0, entrada["documento"])
		entry_productor_cuit.config(state="disabled")

		entry_productor_iva.config(state="normal")
		entry_productor_iva.delete(0, tk.END)
		entry_productor_iva.insert(0, entrada["condicion"])
		entry_productor_iva.config(state="disabled")

		entry_tipo.focus()

	def cargar_item(entrada):
		entry_item.config(state="normal")
		entry_item.delete(0, tk.END)
		entry_item.insert(0, entrada["codigo"])

		entry_cantidad.config(state="normal")
		entry_cantidad.delete(0, tk.END)
		entry_cantidad.insert(0, 1)
		entry_cantidad.focus()

		entry_unidades.config(state="normal")
		entry_unidades.delete(0, tk.END)
		entry_unidades.insert(0, entrada["unidades"])


		entry_item_desc.config(state="normal")
		entry_item_desc.delete(0, tk.END)
		entry_item_desc.insert(0, entrada["nombre"])

		entry_item_precio_unidad.config(state="normal")
		entry_item_precio_unidad.delete(0, tk.END)
		entry_item_precio_unidad.insert(0, entrada["precio_unidad"])


		combo_iva.current(int(entrada["porcentaje_iva"]))

	def cargar_tipo(entrada):
		entry_tipo.delete(0, tk.END)
		entry_tipo.insert(0, entrada["codigo"])

		entry_letra.delete(0, tk.END)
		entry_letra.insert(0, entrada["letra"])

		entry_punto.focus()



	def buscar_productor2():
		pal_clave = diccionario_respuesta["respuesta"][1]
		con = sql_connection()
		condiciones = ' WHERE documento = "' + pal_clave + '"'
		rows = actualizar_db(con, "productores", condiciones)
		condicion = conseguir_condicion(rows[0][5])
		datos_productor = {
		"codigo" : rows[0][0],
		"nombre" : rows[0][3],
		"documento" : rows[0][2],
		"condicion" :  condicion,
		}
		cargar_productor(datos_productor)

	def buscar_item2():
		pal_clave = str(diccionario_respuesta["respuesta"][0])
		con = sql_connection_2()
		condiciones = ' WHERE descripcion = "' + pal_clave + '"'
		rows = actualizar_db(con, "item", condiciones)
		datos_item = {
		"codigo" : rows[0][1],
		"nombre" : rows[0][2],
		"unidades" : rows[0][3],
		"precio_unidad" : rows[0][4],
		"porcentaje_iva" : rows[0][5],
		}
		cargar_item(datos_item)

	def buscar_tipo2():
		pal_clave = str(diccionario_respuesta["respuesta_codigo"])
		con = sql_connection_2()
		condiciones = ' WHERE codigo_comprobante = "' + pal_clave + '"'
		rows = actualizar_db(con, "tipo_comprobante", condiciones)
		datos_item = {
		"codigo" : rows[0][1],
		"descripcion" : rows[0][2],
		"letra" : rows[0][4],
		}
		cargar_tipo(datos_item)


	def buscar_productor():
		pal_clave = str(entry_buscar.get())
		con = sql_connection()
		condiciones = ' WHERE alias LIKE "%' + pal_clave + '%" OR documento LIKE "%' + pal_clave + '%" OR nombre LIKE "%' + pal_clave + '%"'
		rows = actualizar_db(con, "productores", condiciones)
		if (len(rows) == 0):
			messagebox.showerror("ERROR", "No se encontraron coincidencias en la base de datos")
		else:
			if(len(rows) == 1):
				condicion = conseguir_condicion(rows[0][5])
				datos_productor = {
				"codigo" : rows[0][0],
				"nombre" : rows[0][3],
				"documento" : rows[0][2],
				"condicion" :  condicion,
				}
				cargar_productor(datos_productor)
			else:
				diccionario_orden = {
				"cabezal1" : "Cod",
				"cabezal2" : "Nombre",
				"cabezal3" : "Documento"
				}
				rows_enviar = []

				for row in rows:
					rows_enviar.append((row[0], row[3], row[2]))

				tabla_elegir(rows_enviar, diccionario_orden, buscar_productor2)


	def buscar_item():
		pal_clave = str(entry_item.get())
		con = sql_connection_2()
		condiciones = ' WHERE codigo LIKE "%' + pal_clave + '%" OR descripcion LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%"'
		rows = actualizar_db(con, "item", condiciones)
		if (len(rows) == 0):
			messagebox.showerror("ERROR", "No se encontraron coincidencias en la base de datos")
		else:
			if(len(rows) == 1):
				datos_item = {
				"codigo" : rows[0][1],
				"nombre" : rows[0][2],
				"unidades" : rows[0][3],
				"precio_unidad" : rows[0][4],
				"porcentaje_iva" : rows[0][5],
				}
				cargar_item(datos_item)
			else:
				diccionario_orden = {
				"cabezal1" : "Cod",
				"cabezal2" : "Descripcion",
				"cabezal3" : "Unidad"
				}
				rows_enviar = []

				for row in rows:
					rows_enviar.append((row[1], row[2], row[3]))

				tabla_elegir(rows_enviar, diccionario_orden, buscar_item2)

	def buscar_tipo():
		pal_clave = str(entry_tipo.get())
		con = sql_connection_2()
		condiciones = ' WHERE codigo_comprobante LIKE "%' + pal_clave + '%" OR descripcion LIKE "%' + pal_clave + '%"'
		rows = actualizar_db(con, "tipo_comprobante", condiciones)
		if (len(rows) == 0):
			messagebox.showerror("ERROR", "No se encontraron coincidencias en la base de datos")
		else:
			if(len(rows) == 1):
				datos_item = {
				"codigo" : rows[0][1],
				"descripcion" : rows[0][2],
				"letra" : rows[0][4],
				}
				cargar_tipo(datos_item)
			else:
				diccionario_orden = {
				"cabezal1" : "Cod",
				"cabezal2" : "Descripcion",
				"cabezal3" : "Letra"
				}
				rows_enviar = []

				for row in rows:
					rows_enviar.append((row[1], row[2], row[4]))

				tabla_elegir(rows_enviar, diccionario_orden, buscar_tipo2)

	entry_tipo.bind("<Return>", (lambda event: buscar_tipo()))
	entry_item.bind("<Return>", (lambda event: buscar_item()))
	entry_buscar.bind("<Return>", (lambda event: buscar_productor()))

	def calculo1():
		try:
			iva = float(21.00)
			bruto = float(entry_neto21.get())

			final_iva_bruto = bruto*(iva/100)

			entry_21.delete(0, tk.END)
			entry_21.insert(0, round(final_iva_bruto, 2))

			final_neto = float(entry_neto21.get()) + float(entry_neto10.get()) + float(entry_nogravado.get()) + float(entry_21.get()) + float(entry_10.get())
			entry_total.delete(0, tk.END)
			entry_total.insert(0, round(final_neto, 2))
		except:
			messagebox.showerror("ERROR", "No se pudo realizar el calculo.\n - Revise que los campos contengan números.\n - El separador decimal es un punto.")



	def calculo2():
		try:
			iva = float(10.50)
			bruto = float(entry_neto10.get())

			final_iva_bruto = bruto*(iva/100)

			entry_10.delete(0, tk.END)
			entry_10.insert(0, round(final_iva_bruto, 2))

			final_neto = float(entry_neto21.get()) + float(entry_neto10.get()) + float(entry_nogravado.get()) + float(entry_21.get()) + float(entry_10.get())
			entry_total.delete(0, tk.END)
			entry_total.insert(0, round(final_neto, 2))
		except:
			messagebox.showerror("ERROR", "No se pudo realizar el calculo.\n - Revise que los campos contengan números.\n - El separador decimal es un punto.\n - Los campos vacios deberán tener un cero '0'")

		
	def calculo3():
		try:
			final_neto = float(entry_neto21.get()) + float(entry_neto10.get()) + float(entry_nogravado.get()) + float(entry_21.get()) + float(entry_10.get())
			entry_total.delete(0, tk.END)
			entry_total.insert(0, round(final_neto, 2))
		except:
			messagebox.showerror("ERROR", "No se pudo realizar el calculo.\n - Revise que los campos contengan números.\n - El separador decimal es un punto.\n - Los campos vacios deberán tener un cero '0'")


	def calculo4():
		try:
			final_neto = float(entry_neto21.get()) + float(entry_neto10.get()) + float(entry_nogravado.get()) + float(entry_21.get()) + float(entry_10.get())
			entry_total.delete(0, tk.END)
			entry_total.insert(0, round(final_neto, 2))
		except:
			messagebox.showerror("ERROR", "No se pudo realizar el calculo.\n - Revise que los campos contengan números.\n - El separador decimal es un punto.\n - Los campos vacios deberán tener un cero '0'")


	def calculo5():
		try:
			final_neto = float(entry_neto21.get()) + float(entry_neto10.get()) + float(entry_nogravado.get()) + float(entry_21.get()) + float(entry_10.get())
			entry_total.delete(0, tk.END)
			entry_total.insert(0, round(final_neto, 2))
		except:
			messagebox.showerror("ERROR", "No se pudo realizar el calculo.\n - Revise que los campos contengan números.\n - El separador decimal es un punto.\n - Los campos vacios deberán tener un cero '0'")

	def focus(entry):
		entry.focus()

	def calculo6():
		try:
			cant = float(entry_cantidad.get())
		except:
			messagebox.showerror("ERROR", "- En 'Cantidad' ingrese un numero entero, o real.\n - El separador decimal es el punto.")

		try:
			precio = float(entry_item_precio_unidad.get())
		except:
			messagebox.showerror("ERROR", "- En 'Precio por Unidad' ingrese un numero entero, o real.\n - El separador decimal es el punto.")

		try:
			iva = float(combo_iva.get())
		except:
			messagebox.showerror("ERROR", "- En 'IVA' ingrese un numero entero, o real.\n - El separador decimal es el punto.")
		
		try:
			bruto = cant * precio

			entry_item_precio_bruto.config(state = "normal")
			entry_item_precio_bruto.delete(0, tk.END)
			entry_item_precio_bruto.insert(0, round(bruto, 2))
			entry_item_precio_bruto.focus()
		except:
			messagebox.showerror("ERROR", "Error calculando el precio Bruto")

	def agregar_item():
		try:
			descripcion = str(entry_item_desc.get())
		except:
			messagebox.showerror("ERROR", "Error en Descripcion")

		try:
			codigo = str(entry_item.get())
		except:
			messagebox.showerror("ERROR", "Error en codigo")

		try:
			cantidad = str(entry_cantidad.get())
		except:
			messagebox.showerror("ERROR", "Error en cantidad")

		try:
			unidades = str(entry_unidades.get())
		except:
			messagebox.showerror("ERROR", "Error en unidades")

		try:
			precio_unidad = str(entry_item_precio_unidad.get())
		except:
			messagebox.showerror("ERROR", "Error en Precio por Unidad")

		try:
			bruto = str(entry_item_precio_bruto.get())
		except:
			messagebox.showerror("ERROR", "Error en precio Bruto")

		try:
			porcentaje_iva = str(combo_iva.get())
			iva_calc = float(combo_iva.get())
			bruto_calc = float(entry_item_precio_bruto.get())

			total_iva_calc = bruto_calc*(iva_calc/100)
			total_iva = str(round(total_iva_calc, 2))
		except:
			messagebox.showerror("ERROR", "Error obteniendo alicuota de IVA")

		try:
			diccionario_item = {
			"codigo" : codigo,
			"descripcion" : descripcion,
			"cantidad" : cantidad,
			"unidades" : unidades,
			"$unidad" : precio_unidad,
			"$bruto" : bruto,
			"$iva" : total_iva,
			}

			tabla.insert("", tk.END, text = diccionario_item["codigo"], values = (diccionario_item["descripcion"], 
				diccionario_item["cantidad"], 
				diccionario_item["unidades"], 
				diccionario_item["$unidad"], 
				diccionario_item["$bruto"],
				diccionario_item["$iva"]))
			desactivar_item()
		except:
			messagebox.showerror("ERROR", "Error cargando item a la tabla")


	diccionario_item = {
	"codigo" : "NULL",
	"descripcion" : "NULL",
	"cantidad" : "NULL",
	"unidades" : "NULL",
	"$unidad" : "NULL",
	"$bruto" : "NULL",
	"$iva" : "NULL",
	}
	#montos
	entry_neto21.bind("<Return>", (lambda event: calculo1()))
	entry_neto10.bind("<Return>", (lambda event: calculo2()))
	entry_nogravado.bind("<Return>", (lambda event: calculo3()))
	entry_21.bind("<Return>", (lambda event: calculo4()))
	entry_10.bind("<Return>", (lambda event: calculo5()))

	#items
	entry_cantidad.bind("<Return>", (lambda event: focus(entry_item_precio_unidad)))
	entry_item_precio_unidad.bind("<Return>", (lambda event: calculo6()))
	entry_item_precio_bruto.bind("<Return>", (lambda event: agregar_item()))
	entry_item_desc.bind("<Return>", (lambda event: focus(entry_cantidad)))
	entry_unidades.bind("<Return>", (lambda event: focus(entry_item_precio_unidad)))
	combo_iva.bind("<Return>", (lambda event: focus(entry_item_precio_bruto)))


	#VERIFICAR FACTURA

	def verificar_factura():
		cuit = str(entry_productor_cuit.get())
		punto_venta = str(entry_punto.get())
		numero = str(entry_factura.get())
		tipo = str(entry_tipo.get())

		punto_venta_ok = punto_venta.zfill(5)
		numero_ok = numero.zfill(8)

		con = sql_connection_2()
		condiciones = ' WHERE cuit = "' + cuit + '" AND punto_venta = "' + punto_venta_ok + '" AND numero = "' + numero_ok + '" AND tipo_comprobante = "' + tipo + '"'
		rows = actualizar_db(con, "movimientos", condiciones)
		if (len(rows) == 0):
			borrar_contenido()
		else:
			if (len(rows) == 1):
				borrar_contenido()
				diccionario_movimiento = row_a_productor(rows[0])
				cargar_movimiento(diccionario_movimiento)
			else:
				messagebox.showerror("ERROR", "Este productor tiene mas de un movimiento con ese codigo. \n - Verifique la base de datos.")

	def borrar_contenido():
		entry_buscar.delete(0, tk.END)

		entry_productor_nombre.config(state = "normal")
		entry_productor_iva.config(state = "normal")
		entry_productor_cuit.config(state = "normal")

		entry_productor_nombre.delete(0, tk.END)
		entry_productor_iva.delete(0, tk.END)
		entry_productor_cuit.delete(0, tk.END)

		entry_productor_nombre.config(state = "disabled")
		entry_productor_iva.config(state = "disabled")
		entry_productor_cuit.config(state = "disabled")

		entry_tipo.delete(0, tk.END)
		entry_letra.delete(0, tk.END)
		entry_punto.delete(0, tk.END)
		entry_factura.delete(0, tk.END)

		entry_neto21.delete(0, tk.END)
		entry_neto10.delete(0, tk.END)
		entry_21.delete(0, tk.END)
		entry_10.delete(0, tk.END)
		entry_nogravado.delete(0, tk.END)
		entry_total.delete(0, tk.END)

		txt_observaciones.delete("1.0", tk.END)

		for i in tabla.get_children():
			tabla.delete(i)

		for i in tabla_asociados.get_children():
			tabla_asociados.delete(i)

		desactivar_item()
		entry_buscar.focus()

	def cargar_movimiento(entrada):
		entry_neto21.insert(0 , entrada["neto21"])
		entry_neto10.insert(0 , entrada["neto10"])
		entry_21.insert(0 , entrada["iva21"])
		entry_10.insert(0 , entrada["iva10"])
		entry_nogravado.insert(0 , entrada["no_gravado"])
		entry_total.insert(0 , entrada["total"])

		codigo_comprobant = codigo_comprobante(entrada)
		cargar_items(codigo_comprobant)
		txt_observaciones.insert("1.0", entrada["observaciones"])


	entry_punto.bind("<Return>", (lambda event: focus(entry_factura)))
	entry_factura.bind("<Return>", (lambda event: verificar_factura()))


	def codigo_comprobante(entrada):
		try:
			salida = entrada["cuit"] + "_" + entrada["tipo_comprobante"] + "_" + entrada["punto_venta"] + "_" + entrada["numero"]
			return salida
		except:
			messagebox.showerror("ERROR", "Error generando el codigo de comprobante")

	def cargar_items(codigo):
		con = sql_connection_2()
		condiciones = ' WHERE codigo_movimiento = "' + codigo + '"'
		rows = actualizar_db(con, "items", condiciones)

		for row in rows:
			item_dicc = row_a_item(row)
			tabla.insert("", tk.END, text = item_dicc["id"], values = ("descripcion", 
				item_dicc["cantidad"], 
				item_dicc["unidades"], 
				item_dicc["precio_unidad"], 
				item_dicc["bruto"],
				item_dicc["total_iva"]))


	def row_a_item(row):
		item_dicc = {
		"id" : row[0],
		"codigo_movimiento" : row[1],
		"unidades" : row[2],
		"cantidad" : row[3],
		"precio_unidad" : row[4],
		"bruto" : row[5],
		"porcentaje_iva" : row[6],
		"total_iva" : row[7],
		"grupo" : row[8],
		"rubro" : row[9],
		"concepto" : row[10],
		}
		return item_dicc

	def row_a_productor(row):
		product_dicc = {
		"id" : row[0],
		"cod" : row[1],
		"cuit" : row[2],
		"tipo_comprobante" : row[3],
		"punto_venta" : row[4],
		"numero" : row[5],
		"fecha" : row[6],
		"periodo" : row[7],
		"neto21" : row[8],
		"neto10" : row[9],
		"no_gravado" : row[10],
		"iva21" : row[11],
		"iva10" : row[12],
		"total" : row[13],
		"observaciones" : row[14],
		"creado_el" : row[15],
		"creado_por" : row[16],
		}

		return product_dicc

	def desactivar_item():
		entry_item.focus()
		entry_item.delete(0, tk.END)

		entry_item_desc.delete(0, tk.END)
		entry_item_precio_bruto.delete(0, tk.END)
		entry_item_precio_unidad.delete(0, tk.END)
		entry_cantidad.delete(0, tk.END)
		entry_unidades.delete(0, tk.END)

		entry_item_desc.config(state = "disabled")
		entry_item_precio_bruto.config(state = "disabled")
		entry_item_precio_unidad.config(state = "disabled")
		entry_cantidad.config(state = "disabled")
		entry_unidades.config(state = "disabled")

		combo_iva.current(0)

	def cerrar_ventana_principal():
		window_comprobante.destroy()

	btn_guardar = tk.Button(window_comprobante, text="GUARDAR\n(F1)", background="#BAF0B8", command = lambda: abrir_ventana("mov", "productor", "cod"))
	btn_eliminar = tk.Button(window_comprobante, text="ELIMINAR", background="#EF9090")
	btn_borrar = tk.Button(window_comprobante, text="Borrar campos", background="#D6F4F8", command = borrar_contenido)

	btn_guardar.place(x = 175, y = 400, width = 100, height = 40)
	btn_eliminar.place(x = 300, y = 400, width = 100, height = 40)
	btn_borrar.place(x = 425, y = 400, width = 100, height = 40)


	window_comprobante.bind("<Escape>", (lambda event: cerrar_ventana_principal()))
	window_comprobante.mainloop()

#abrir_ventana("compra", "2", "asd")
#txt_descripcion.get("1.0", tk.END)
#Falta la parte de comprobantes asociados