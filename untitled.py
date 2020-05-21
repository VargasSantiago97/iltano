#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from librerias import comprobantes
#from librerias import crearVentanaProductor
#from librerias import crearVentanaIngreso

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


TITLE_WINDOW_PRINCIPAL = "Gestor de Remates IL TANO HACIENDA SAS"
#TAMAÑO_WINDOW_PRINCIPAL = "1222x768"
TAMAÑO_WINDOW_PRINCIPAL = "1325x768"



def sql_connection():
	try:
		con = sqlite3.connect('database/mydatabase.db')
		return con
	except Error:
		print(Error)

def actualizar_db(con, tabla):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + str(tabla))
	rows = cursorObj.fetchall()

	return rows


def actualizar_tabla_filtrada(rows, tabla_productores_movimiento):
	for i in tabla_productores_movimiento.get_children():
		tabla_productores_movimiento.delete(i)
	i=0
	for row in rows:
		tabla_productores_movimiento.insert("", tk.END, text = str(row[0]), iid=i, values = (str(row[4]), str(row[2])))
		i = i + 1 


#INICIO DEL PROGRAMA:
window = Tk()
window.title(TITLE_WINDOW_PRINCIPAL)
window.geometry(TAMAÑO_WINDOW_PRINCIPAL)

pestañas = ttk.Notebook(window)

label_movimientos = Label(window, backgroun="#E8F6FA")
label_configuracion = Label(window)
label_productores = Label(window)
label_preferencias = Label(window)
label_ingreso = Label(window, backgroun="#E8F6FA") #bg='#2C4D4F'

pestañas.add(label_movimientos, text="Movimientos", padding = 20)
pestañas.add(label_productores, text="Productores", padding = 0)
pestañas.add(label_ingreso, text="Ingreso", padding = 20)
pestañas.add(label_preferencias, text="Preferencias", padding = 20)
pestañas.add(label_configuracion, text="Configuracion", padding = 0)

pestañas.place(x = 0, y = 0, relwidth = 1, relheight = 1)

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#            PESTAÑA 1 "MOVIMIENTOS"
#----------------------------------------------------------------------
#----------------------------------------------------------------------

#--------------------------------------------------------
#PESTAÑA 1: PRODUCTOR
#--------------------------------------------------------
lbl_ventana_productor_buscador = LabelFrame(label_movimientos, text="Buscar productor")
lbl_ventana_productor_informacion = LabelFrame(label_movimientos, text="Informacion")
lbl_ventana_productor_acciones = LabelFrame(label_movimientos, text="Acciones")

lbl_ventana_productor_buscador.place(x = 2, y = 2, width = 390, height = 210)
lbl_ventana_productor_informacion.place(x = 400, y = 2, width = 450, height = 210)
lbl_ventana_productor_acciones.place(x = 858, y = 2, width = 421, height = 210)

#--Buscador
lbl_ventana_productor_buscador_entry = LabelFrame(lbl_ventana_productor_buscador, text="Filtrar")
lbl_ventana_productor_buscador_tabla = LabelFrame(lbl_ventana_productor_buscador, text="Productores")

lbl_ventana_productor_buscador_entry.grid(column = 0, row = 0, padx = 2, pady = 2)
lbl_ventana_productor_buscador_tabla.grid(column = 0, row = 1, padx = 10, pady = 5)

#--
entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="43")
entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = padY)

btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar")
btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 5)

sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
sbr_productor.pack(side=RIGHT, fill="y")

tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("cliente", "doc"), selectmode=tk.BROWSE, height=4)
tabla_productor.pack(side=LEFT, fill="both", expand=True)
sbr_productor.config(command=tabla_productor.yview)
tabla_productor.config(yscrollcommand=sbr_productor.set)

tabla_productor.heading("#0", text="Cód.")
tabla_productor.heading("cliente", text="Productor")
tabla_productor.heading("doc", text="CUIT/DNI")

tabla_productor.column("#0", width=40)
tabla_productor.column("cliente", width=180)
tabla_productor.column("doc", width=120)

entry_filtrar_productor.bind("<Return>", (lambda event: productFiltrar()))

#Informacion
lbl_ventana_productor_informacion_nombre = Label(lbl_ventana_productor_informacion)
lbl_ventana_productor_informacion_datos = Label(lbl_ventana_productor_informacion)

lbl_ventana_productor_informacion_nombre.place(x = 10, y = 10, width = 432, height = 40)
lbl_ventana_productor_informacion_datos.place(x = 10, y = 65, width = 432, height = 115)


texto_nombre = StringVar()
texto_nombre.set("Bienvenidosada1234564789101112") # Caso 1
texto_cuit = StringVar()
texto_cuit.set("00-00000000-0")
texto_conIva = StringVar()
texto_conIva.set("Consumidor final")
texto_conIva.set("Responsable inscripto")
texto_estado = StringVar()
texto_estado.set("$ 00.000.000,00")
texto_compras = StringVar()
texto_compras.set("$ 00.000.000,00")
texto_ventas = StringVar()
texto_ventas.set("$ 00.000.000,00")
texto_cobros = StringVar()
texto_cobros.set("$ 00.000.000,00")
texto_pagos = StringVar()
texto_pagos.set("$ 00.000.000,00")


lbl_nombre = Label(lbl_ventana_productor_informacion_nombre, font=("verdana",24), text="")
lbl_nombre.place(x=0, y=0)
lbl_nombre.config(textvariable=texto_nombre)


lbl_cuit = Label(lbl_ventana_productor_informacion_datos, font=("verdana",15), text="")
lbl_cuit.place(x=5, y=0)
lbl_cuit.config(textvariable=texto_cuit)

lbl_conIva = Label(lbl_ventana_productor_informacion_datos, font=("verdana",11), text="")
lbl_conIva.place(x=250, y=5)
lbl_conIva.config(textvariable=texto_conIva)

lbl_estado = Label(lbl_ventana_productor_informacion_datos, font=("verdana",18), text="")
lbl_estado.place(x=110, y=80)
lbl_estado.config(textvariable=texto_estado)

Label(lbl_ventana_productor_informacion_datos, font=("verdana",8), text="Compras:").place(x=0, y=37)
Label(lbl_ventana_productor_informacion_datos, font=("verdana",8), text="Ventas").place(x=0, y=57)
Label(lbl_ventana_productor_informacion_datos, font=("verdana",8), text="Cobros:").place(x=250, y=37)
Label(lbl_ventana_productor_informacion_datos, font=("verdana",8), text="Pagos").place(x=250, y=57)


lbl_compras = Label(lbl_ventana_productor_informacion_datos, font=("verdana",10), text="")
lbl_compras.place(x=60, y=35)
lbl_compras.config(textvariable=texto_compras)

lbl_ventas = Label(lbl_ventana_productor_informacion_datos, font=("verdana",10), text="")
lbl_ventas.place(x=60, y=55)
lbl_ventas.config(textvariable=texto_ventas)

lbl_cobros = Label(lbl_ventana_productor_informacion_datos, font=("verdana",10), text="")
lbl_cobros.place(x=300, y=35)
lbl_cobros.config(textvariable=texto_cobros)

lbl_pagos = Label(lbl_ventana_productor_informacion_datos, font=("verdana",10), text="")
lbl_pagos.place(x=300, y=55)
lbl_pagos.config(textvariable=texto_pagos)

#Acciones:
btn_nueva_compra = tk.Button(lbl_ventana_productor_acciones, text="Agregar\n\nMOVIMIENTO", backgroun="#CBF9E1", command= lambda: comprobantes.abrir_ventana("compra", "2", "asd"))
btn_nueva_compra.place(x=10, y = 20, width = 98, height = 60)

btn_nueva_venta = tk.Button(lbl_ventana_productor_acciones, text="Agregar\n\nRETENCION", backgroun="#CBF9E1", command= lambda: comprobantes.abrir_ventana("venta", texto_cuit.get(), ""))
btn_nueva_venta.place(x=110, y = 20, width = 98, height = 60)

btn_nuevo_cobro = tk.Button(lbl_ventana_productor_acciones, text="Agregar\n\nCOBRO", backgroun="#CBF9E1")
btn_nuevo_cobro.place(x=210, y = 20, width = 98, height = 60)

btn_nuevo_pago = tk.Button(lbl_ventana_productor_acciones, text="Agregar\n\nPAGO", backgroun="#CBF9E1")
btn_nuevo_pago.place(x=310, y = 20, width = 98, height = 60)

btn_exportar_tabla = tk.Button(lbl_ventana_productor_acciones, text="Exportar\n\nTABLA", backgroun="#D6F4F8")
btn_exportar_tabla.place(x=10, y = 100, width = 98, height = 60)

btn_exportar_listado = tk.Button(lbl_ventana_productor_acciones, text="Exportar\nListado\nProductor", backgroun="#D6F4F8")
btn_exportar_listado.place(x=110, y = 100, width = 98, height = 60)

btn_exportar_estado = tk.Button(lbl_ventana_productor_acciones, text="Exportar\nEstado\nProductor", backgroun="#D6F4F8")
btn_exportar_estado.place(x=210, y = 100, width = 98, height = 60)

btn_exportar_todo = tk.Button(lbl_ventana_productor_acciones, text="Exportar\nEstado\nProductores", backgroun="#D6F4F8")
btn_exportar_todo.place(x=310, y = 100, width = 98, height = 60)

"""
19 caracteres maximo, verdana 24
32 caracteres maximo, verdana 14
56 caracteres maximo, verdana 8
"""

#--------------------------------------------------------
#PESTAÑA 1: TABLA MOVIMIENTOS
#--------------------------------------------------------
lbl_ventana_movimientos_filtrar = LabelFrame(label_movimientos, text="Filtros")
lbl_ventana_movimientos_tabla = LabelFrame(label_movimientos, text="Movimientos")

lbl_ventana_movimientos_filtrar.place(x = 2, y = 214, width = 130, height = 274)
lbl_ventana_movimientos_tabla.place(x = 134, y = 214, width = 1145, height = 274)

lbl_base_tabla = Label(lbl_ventana_movimientos_tabla)
lbl_base_tabla.grid(column = 0, row = 0)

sbr = Scrollbar(lbl_base_tabla)
sbr.pack(side=RIGHT, fill="y")

tabla = ttk.Treeview(lbl_base_tabla, columns=("fecha", "evento", "cliente", "descripcion", "movimiento", "comprobante", "bruto", "iva_bruto", "gastos", "iva_gastos", "excento", "neto"), selectmode=tk.BROWSE, height=11)
tabla.pack(side=LEFT, fill="both", expand=True)
sbr.config(command=tabla.yview)
tabla.config(yscrollcommand=sbr.set)

tabla.heading("#0", text="Cod.")
tabla.heading("cliente", text="Productor")
tabla.heading("fecha", text="Fecha")
tabla.heading("evento", text="Evento")
tabla.heading("descripcion", text="Descripcion")
tabla.heading("movimiento", text="Movimiento")
tabla.heading("comprobante", text="Comprobante")
tabla.heading("bruto", text="Bruto")
tabla.heading("iva_bruto", text="IVA Bruto")
tabla.heading("gastos", text="Gastos")
tabla.heading("iva_gastos", text="IVA Gastos")
tabla.heading("excento", text="Excento")
tabla.heading("neto", text="Neto")


tabla.column("#0", width=50)
tabla.column("cliente", width=140)
tabla.column("fecha", width=55)
tabla.column("evento", width=65)
tabla.column("descripcion", width=120)
tabla.column("movimiento", width=75)
tabla.column("comprobante", width=115)
tabla.column("bruto", width=80)
tabla.column("iva_bruto", width=80)
tabla.column("gastos", width=80)
tabla.column("iva_gastos", width=80)
tabla.column("excento", width=80)
tabla.column("neto", width=100)

for i in range(0, 50):
	tabla.insert("", tk.END, text = str(i), iid=i, values = ("00/00/00", 
			"jiaaa", 
			"jiaaa", 
			"jiaaa", 
			"jiaaa", 
			"180 00001-00000000", 
			"jiaaa", 
			"jiaaa", 
			"jiaaa", 
			"$10000000.00", 
			"jiaaa", 
			"jiaaa"))

#Filtros Movimientos

combo_movimientos_dia = Combobox(lbl_ventana_movimientos_filtrar)
combo_movimientos_dia.place(x=10, y=10, width=100)
combo_movimientos_dia["values"] = ["Día", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
combo_movimientos_dia.current(0)

combo_movimientos_mes = Combobox(lbl_ventana_movimientos_filtrar)
combo_movimientos_mes.place(x=10, y=30, width=100)
combo_movimientos_mes["values"] = ["Mes", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
combo_movimientos_mes.current(0)

combo_movimientos_año = Combobox(lbl_ventana_movimientos_filtrar)
combo_movimientos_año.place(x=10, y=50, width=100)
combo_movimientos_año["values"] = ["Año", 2019, 2020, 2021]
combo_movimientos_año.current(0)

combo_movimientos_evento = Combobox(lbl_ventana_movimientos_filtrar)
combo_movimientos_evento.place(x=10, y=80, width=100)
combo_movimientos_evento["values"] = ["Evento"]
combo_movimientos_evento.current(0)

combo_movimientos_movimiento = Combobox(lbl_ventana_movimientos_filtrar)
combo_movimientos_movimiento.place(x=10, y=110, width=100)
combo_movimientos_movimiento["values"] = ["Movimiento"]
combo_movimientos_movimiento.current(0)


#--------------------------------------------------------
#PESTAÑA 1: TABLA PAGOS
#--------------------------------------------------------
lbl_ventana_pagos_filtrar = LabelFrame(label_movimientos, text="Filtros")
lbl_ventana_pagos_tabla = LabelFrame(label_movimientos, text="Pagos")

lbl_ventana_pagos_filtrar.place(x = 2, y = 490, width = 130, height = 210)
lbl_ventana_pagos_tabla.place(x = 134, y = 490, width = 1145, height = 210)

lbl_base_tabla_pagos = Label(lbl_ventana_pagos_tabla)
lbl_base_tabla_pagos.grid(column = 0, row = 0)

sbr_pagos = Scrollbar(lbl_base_tabla_pagos)
sbr_pagos.pack(side=RIGHT, fill="y")

tabla_pagos = ttk.Treeview(lbl_base_tabla_pagos, columns=("fecha", "evento", "cliente", "descripcion", "movimiento", "comprobante", "bruto", "iva_bruto", "gastos", "iva_gastos", "excento", "neto"), selectmode=tk.BROWSE, height=8)
tabla_pagos.pack(side=LEFT, fill="both", expand=True)
sbr_pagos.config(command=tabla_pagos.yview)
tabla_pagos.config(yscrollcommand=sbr_pagos.set)

tabla_pagos.heading("#0", text="Cod.")
tabla_pagos.heading("cliente", text="Productor")
tabla_pagos.heading("fecha", text="Fecha")
tabla_pagos.heading("evento", text="Evento")
tabla_pagos.heading("descripcion", text="Descripcion")
tabla_pagos.heading("movimiento", text="Movimiento")
tabla_pagos.heading("comprobante", text="Comprobante")
tabla_pagos.heading("bruto", text="Bruto")
tabla_pagos.heading("iva_bruto", text="IVA Bruto")
tabla_pagos.heading("gastos", text="Gastos")
tabla_pagos.heading("iva_gastos", text="IVA Gastos")
tabla_pagos.heading("excento", text="Excento")
tabla_pagos.heading("neto", text="Neto")


tabla_pagos.column("#0", width=50)
tabla_pagos.column("cliente", width=140)
tabla_pagos.column("fecha", width=55)
tabla_pagos.column("evento", width=65)
tabla_pagos.column("descripcion", width=120)
tabla_pagos.column("movimiento", width=75)
tabla_pagos.column("comprobante", width=115)
tabla_pagos.column("bruto", width=80)
tabla_pagos.column("iva_bruto", width=80)
tabla_pagos.column("gastos", width=80)
tabla_pagos.column("iva_gastos", width=80)
tabla_pagos.column("excento", width=80)
tabla_pagos.column("neto", width=100)

for i in range(0, 50):
	tabla_pagos.insert("", tk.END, text = str(i), iid=i, values = ("00/00/00", 
			"jiaaa", 
			"jiaaa", 
			"jiaaa", 
			"jiaaa", 
			"180 00001-00000000", 
			"jiaaa", 
			"jiaaa", 
			"jiaaa", 
			"$10000000.00", 
			"jiaaa", 
			"jiaaa"))


#Filtros pagos

combo_pagos_dia = Combobox(lbl_ventana_pagos_filtrar)
combo_pagos_dia.place(x=10, y=10, width=100)
combo_pagos_dia["values"] = ["Día", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
combo_pagos_dia.current(0)

combo_pagos_mes = Combobox(lbl_ventana_pagos_filtrar)
combo_pagos_mes.place(x=10, y=30, width=100)
combo_pagos_mes["values"] = ["Mes", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
combo_pagos_mes.current(0)

combo_pagos_año = Combobox(lbl_ventana_pagos_filtrar)
combo_pagos_año.place(x=10, y=50, width=100)
combo_pagos_año["values"] = ["Año", 2019, 2020, 2021]
combo_pagos_año.current(0)

combo_pagos_evento = Combobox(lbl_ventana_pagos_filtrar)
combo_pagos_evento.place(x=10, y=80, width=100)
combo_pagos_evento["values"] = ["Evento"]
combo_pagos_evento.current(0)

combo_pagos_movimiento = Combobox(lbl_ventana_pagos_filtrar)
combo_pagos_movimiento.place(x=10, y=110, width=100)
combo_pagos_movimiento["values"] = ["Movimiento"]
combo_pagos_movimiento.current(0)




#con = sql_connection()
#rows = actualizar_db(con, "productores")
#actualizar_tabla_filtrada(rows, tabla_productor)


def selec():
	codigo_obtenido = tabla_productor.item((tabla_productor.selection()[0]))
	texto_nombre.set(codigo_obtenido['values'][0])
	texto_cuit.set(codigo_obtenido['values'][1])
	texto_conIva.set("")


tabla_productor.bind("<Double-1>", (lambda event: selec()))



#----------------------------------------------------------------------
#----------------------------------------------------------------------
#            PESTAÑA 2 "PRODUCTORES"
#----------------------------------------------------------------------
#----------------------------------------------------------------------

#--------------------------------------------------------
#PESTAÑA 2: TABLA
#--------------------------------------------------------

#crearVentanaProductor.ventanaProductor(label_productores)
#crearVentanaIngreso.ventanaIngreso(label_ingreso)

window.mainloop()
