#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

#import ventanaIngreso
#import PDF_catalogo


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

diccionario_objetos = {}

def cargarTablaObservaciones(nuevoDic, tabla_comprasObservaciones):
	tabla = tabla_comprasObservaciones

	for j in tabla.get_children():
		tabla.delete(j)

	try:
		for i in range(0, len(nuevoDic)):
			texto_cuota = nuevoDic[str(i)]["cuota"]
			texto_fecha = nuevoDic[str(i)]["fecha"]
			texto_monto = nuevoDic[str(i)]["monto"]

			tabla.insert("", tk.END, values = (texto_cuota,
				texto_fecha, texto_monto))
	except:
		messagebox.showerror("ERROR", "Error al cargar")

def guardar(tabla_comprasObservaciones):
	nuevoDic = {}
	j=0
	for i in range(0, 12):
		if (diccionario_objetos["entry" + str(i+1) + "_monto"].get() != ""):
			nuevoDic[str(j)] = {
			"cuota" : str(diccionario_objetos["entry" + str(i+1) + "_cuota"].get()),
			"fecha" : str(diccionario_objetos["entry" + str(i+1) + "_fecha"].get()),
			"monto" : str(diccionario_objetos["entry" + str(i+1) + "_monto"].get()),
			}
			j+=1
	cargarTablaObservaciones(nuevoDic, tabla_comprasObservaciones)

def planDePagos(tabla_comprasObservaciones, fecha_actual):

	window = Tk()
	window.title("Plan de pagos")
	window.geometry("280x450")

	entry1_cuota = Entry(window)
	entry1_fecha = Entry(window)
	entry1_monto = Entry(window)

	entry2_cuota = Entry(window)
	entry2_fecha = Entry(window)
	entry2_monto = Entry(window)

	entry3_cuota = Entry(window)
	entry3_fecha = Entry(window)
	entry3_monto = Entry(window)

	entry4_cuota = Entry(window)
	entry4_fecha = Entry(window)
	entry4_monto = Entry(window)

	entry5_cuota = Entry(window)
	entry5_fecha = Entry(window)
	entry5_monto = Entry(window)

	entry6_cuota = Entry(window)
	entry6_fecha = Entry(window)
	entry6_monto = Entry(window)

	entry7_cuota = Entry(window)
	entry7_fecha = Entry(window)
	entry7_monto = Entry(window)

	entry8_cuota = Entry(window)
	entry8_fecha = Entry(window)
	entry8_monto = Entry(window)

	entry9_cuota = Entry(window)
	entry9_fecha = Entry(window)
	entry9_monto = Entry(window)

	entry10_cuota = Entry(window)
	entry10_fecha = Entry(window)
	entry10_monto = Entry(window)

	entry11_cuota = Entry(window)
	entry11_fecha = Entry(window)
	entry11_monto = Entry(window)

	entry12_cuota = Entry(window)
	entry12_fecha = Entry(window)
	entry12_monto = Entry(window)



	entry1_cuota.place(x = 10, y = 10, width=80)
	entry1_fecha.place(x = 100, y = 10, width=80)
	entry1_monto.place(x = 190, y = 10, width=80)
	entry2_cuota.place(x = 10, y = 40, width=80)
	entry2_fecha.place(x = 100, y = 40, width=80)
	entry2_monto.place(x = 190, y = 40, width=80)
	entry3_cuota.place(x = 10, y = 70, width=80)
	entry3_fecha.place(x = 100, y = 70, width=80)
	entry3_monto.place(x = 190, y = 70, width=80)
	entry4_cuota.place(x = 10, y = 100, width=80)
	entry4_fecha.place(x = 100, y = 100, width=80)
	entry4_monto.place(x = 190, y = 100, width=80)
	entry5_cuota.place(x = 10, y = 130, width=80)
	entry5_fecha.place(x = 100, y = 130, width=80)
	entry5_monto.place(x = 190, y = 130, width=80)
	entry6_cuota.place(x = 10, y = 160, width=80)
	entry6_fecha.place(x = 100, y = 160, width=80)
	entry6_monto.place(x = 190, y = 160, width=80)
	entry7_cuota.place(x = 10, y = 190, width=80)
	entry7_fecha.place(x = 100, y = 190, width=80)
	entry7_monto.place(x = 190, y = 190, width=80)
	entry8_cuota.place(x = 10, y = 220, width=80)
	entry8_fecha.place(x = 100, y = 220, width=80)
	entry8_monto.place(x = 190, y = 220, width=80)
	entry9_cuota.place(x = 10, y = 250, width=80)
	entry9_fecha.place(x = 100, y = 250, width=80)
	entry9_monto.place(x = 190, y = 250, width=80)
	entry10_cuota.place(x = 10, y = 280, width=80)
	entry10_fecha.place(x = 100, y = 280, width=80)
	entry10_monto.place(x = 190, y = 280, width=80)
	entry11_cuota.place(x = 10, y = 310, width=80)
	entry11_fecha.place(x = 100, y = 310, width=80)
	entry11_monto.place(x = 190, y = 310, width=80)
	entry12_cuota.place(x = 10, y = 340, width=80)
	entry12_fecha.place(x = 100, y = 340, width=80)
	entry12_monto.place(x = 190, y = 340, width=80)

	entry1_cuota.insert(0, "Cuota N°: 1")
	entry2_cuota.insert(0, "Cuota N°: 2")
	entry3_cuota.insert(0, "Cuota N°: 3")
	entry4_cuota.insert(0, "Cuota N°: 4")
	entry5_cuota.insert(0, "Cuota N°: 5")
	entry6_cuota.insert(0, "Cuota N°: 6")
	entry7_cuota.insert(0, "Cuota N°: 7")
	entry8_cuota.insert(0, "Cuota N°: 8")
	entry9_cuota.insert(0, "Cuota N°: 9")
	entry10_cuota.insert(0, "Cuota N°: 10")
	entry11_cuota.insert(0, "Cuota N°: 11")
	entry12_cuota.insert(0, "Cuota N°: 12")

	entry1_fecha.insert(0, fecha_actual)

	diccionario_objetos["entry1_monto"] = entry1_monto
	diccionario_objetos["entry2_monto"] = entry2_monto
	diccionario_objetos["entry3_monto"] = entry3_monto
	diccionario_objetos["entry4_monto"] = entry4_monto
	diccionario_objetos["entry5_monto"] = entry5_monto
	diccionario_objetos["entry6_monto"] = entry6_monto
	diccionario_objetos["entry7_monto"] = entry7_monto
	diccionario_objetos["entry8_monto"] = entry8_monto
	diccionario_objetos["entry9_monto"] = entry9_monto
	diccionario_objetos["entry10_monto"] = entry10_monto
	diccionario_objetos["entry11_monto"] = entry11_monto
	diccionario_objetos["entry12_monto"] = entry12_monto

	diccionario_objetos["entry1_fecha"] = entry1_fecha
	diccionario_objetos["entry2_fecha"] = entry2_fecha
	diccionario_objetos["entry3_fecha"] = entry3_fecha
	diccionario_objetos["entry4_fecha"] = entry4_fecha
	diccionario_objetos["entry5_fecha"] = entry5_fecha
	diccionario_objetos["entry6_fecha"] = entry6_fecha
	diccionario_objetos["entry7_fecha"] = entry7_fecha
	diccionario_objetos["entry8_fecha"] = entry8_fecha
	diccionario_objetos["entry9_fecha"] = entry9_fecha
	diccionario_objetos["entry10_fecha"] = entry10_fecha
	diccionario_objetos["entry11_fecha"] = entry11_fecha
	diccionario_objetos["entry12_fecha"] = entry12_fecha

	diccionario_objetos["entry1_cuota"] = entry1_cuota
	diccionario_objetos["entry2_cuota"] = entry2_cuota
	diccionario_objetos["entry3_cuota"] = entry3_cuota
	diccionario_objetos["entry4_cuota"] = entry4_cuota
	diccionario_objetos["entry5_cuota"] = entry5_cuota
	diccionario_objetos["entry6_cuota"] = entry6_cuota
	diccionario_objetos["entry7_cuota"] = entry7_cuota
	diccionario_objetos["entry8_cuota"] = entry8_cuota
	diccionario_objetos["entry9_cuota"] = entry9_cuota
	diccionario_objetos["entry10_cuota"] = entry10_cuota
	diccionario_objetos["entry11_cuota"] = entry11_cuota
	diccionario_objetos["entry12_cuota"] = entry12_cuota


	btn_guardar = tk.Button(window, text="GUARDAR", backgroun="#a4ff9e", font=("Helvetica Neue",12,"bold"), command= lambda: guardar(tabla_comprasObservaciones))
	btn_guardar.place(x = 70, y = 380, width = 130, height = 50)


	window.mainloop()


#planDePagos("asd", "31/05/20")