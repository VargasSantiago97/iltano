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

dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}
diccionario_objetos = {}

direccionBaseDeDatos = "librerias/database/iltanohacienda.db"

window = Tk()
window.title("IL TANO HACIENDA SAS")
window.geometry("1024x600")
window.resizable(0,0)
window.configure(backgroun="#000000") #E8F6FA

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
def treeview_sort_column(tv, col, reverse):
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, command=lambda: \
	treeview_sort_column(tv, col, not reverse))

def compradorFiltrar():
	pal_clave = str(diccionario_objetos["entry_comprador"].get())

	con = sql_connection()
	condiciones =  ' WHERE (nombre LIKE "%' + pal_clave + '%" OR razon LIKE "%' + pal_clave + '%" OR ndoc LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%" OR con_iva LIKE "%' + pal_clave + '%" OR localidad LIKE "%' + pal_clave + '%" OR provincia LIKE "%' + pal_clave + '%" OR ruca LIKE "%' + pal_clave + '%" OR establecimiento LIKE "%' + pal_clave + '%") AND estado = "activo"'
	rows = actualizar_db(con, "productores", condiciones)
	if(len(rows)==1):
		#cargarDatosComprador(rows[0][3])
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

	diccionario_objetos["texto_aliasComprador"].set(texto_alias)
	diccionario_objetos["texto_razonComprador"].set(texto_razon)
	diccionario_objetos["texto_cuitComprador"].set(texto_cuit)


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

#BARRA DE MENU
if(True):
	def pantCompleta():
		window.attributes('-fullscreen', dicc_objetos["varFullScreen"])
		dicc_objetos["varFullScreen"] = not dicc_objetos["varFullScreen"]
	
	def salirWindow():
		window.destroy()

	barraMenu = Menu(window)
	barraMenu.option_add('*tearOff', False)


	mnuArchivo = Menu(barraMenu)
	mnuArchivo.add_command(label="Abrir")
	mnuArchivo.add_command(label="Nuevo")
	mnuArchivo.add_command(label="Guardar")
	mnuArchivo.add_command(label="Cerrar")
	mnuArchivo.add_command(label="Salir", command = salirWindow)

	mnuRemate = Menu(barraMenu)
	mnuRemate.add_command(label="Remate", command = lambda: ventanaRemates.ventana1("NULL"))
	mnuRemate.add_command(label="Listado de remates")
	mnuRemate.add_separator()
	mnuRemate.add_command(label="Seleccionar remate")

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
	mnuProductores.add_command(label="Productores AUX")
	mnuProductores.add_separator()
	mnuProductores.add_command(label="Productores usados")


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


	mnuCatalogo = Menu(barraMenu)
	mnuCatalogo.add_command(label="Catalogo")

	mnuConfiguracion = Menu(barraMenu)
	mnuConfiguracion.add_command(label="Administrar Empresa")
	mnuConfiguracion.add_separator()
	mnuConfiguracion.add_command(label="Sincronizacion en la NUBE")
	mnuConfiguracion.add_separator()
	mnuConfiguracion.add_command(label="Copia de seguridad")
	mnuConfiguracion.add_command(label="RESTAURAR copia de seguridad")
	mnuConfiguracion.add_separator()
	mnuConfiguracion.add_command(label="Pantalla detalles", command = pantallaDetalles)
	mnuConfiguracion.add_separator()
	mnuConfiguracion.add_command(label="Pantalla completa", command = pantCompleta)
	mnuConfiguracion.add_command(label="Salir", command = salirWindow)

	barraMenu.add_cascade(label="Archivo", menu = mnuArchivo)
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

	botBuscar = tk.Button(barraherr, text="AGREGAR\nNUEVO LOTE", compound="top", backgroun="#b3f2bc", font=("Helvetica", 10, "bold"))
	botImprimir = tk.Button(barraherr, text="EDITAR\nLOTE", compound="top", backgroun="#f2f0b3", font=("Helvetica", 10, "bold"))
	botExcel = tk.Button(barraherr, text="BORRAR\nLOTE", compound="top", backgroun="#FF6E6E", font=("Helvetica", 10, "bold"))
	botAyuda = tk.Button(barraherr, text="bot 4\nasd", compound="top", backgroun="#f2f0b3", font=("Helvetica", 10, "bold"))
	botCerrar = tk.Button(barraherr, text="bot 5\nasd", compound="top", backgroun="#FF6E6E", font=("Helvetica", 10, "bold"))

	padX=3
	padY=2

	botBuscar.pack(side=LEFT, padx=padX, pady=padY)
	botImprimir.pack(side=LEFT, padx=padX, pady=padY)
	botExcel.pack(side=LEFT, padx=padX, pady=padY)
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


		tabla = ttk.Treeview(lbl_tabla, columns=["CORRAL", "VENDEDOR", "CANTIDAD", "CATEGORIA", "PINTURA", "KGS", "PROMEDIO", "PRECIO", "COMPRADOR"], selectmode=tk.BROWSE, show='headings') 
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


		tabla.column("CORRAL", width=30)
		tabla.column("VENDEDOR", width=200)
		tabla.column("CANTIDAD", width=30)
		tabla.column("CATEGORIA", width=30)
		tabla.column("PINTURA", width=30)
		tabla.column("KGS", width=30)
		tabla.column("PROMEDIO", width=30)
		tabla.column("PRECIO", width=30)
		tabla.column("COMPRADOR", width=200)


		tabla.bind("<Double-1>", (lambda event: elegir(tabla.item(tabla.selection()))))
		tabla.bind("<Return>", (lambda event: elegir(tabla.item(tabla.selection()))))

	#DATOS
	if(True):
		lblBuscador = tk.Label(lbl_datos, backgroun="#f0f0f0", text="PRODUCTOR", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblBuscador.place(x=2, y=2, width=300, height=226)

		lblLote = tk.Label(lbl_datos, backgroun="#f0f0f0", text="PRODUCTOR", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblLote.place(x=304, y=2, width=300, height=226)

		lblComprador = tk.Label(lbl_datos, backgroun="#f0f0f0", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblComprador.place(x=606, y=25, width=400, height=87)
		lblPrecio = tk.Label(lbl_datos, backgroun="#f0f0f0", foreground="#FFFFFF", relief=SOLID, bd=2)
		lblPrecio.place(x=606, y=114, width=200, height=114)

		tk.Label(lbl_datos, backgroun="#f2f0b3", text="COMPRADOR", font=("Helvetica", 10, "bold"), foreground="#000000", relief=SOLID, bd=2).place(x=606, y=2, width=400, height=25)
		tk.Label(lbl_datos, backgroun="#f2f0b3", text="PRECIO", font=("Helvetica", 10, "bold"), foreground="#000000", relief=SOLID, bd=2).place(x=606, y=114, width=200, height=25)

		#LOTE
		if(True):

			texto_catHacienda = StringVar()
			texto_catHacienda.set("Ternero")
			texto_catVenta = StringVar()
			texto_catVenta.set("Abasto Conserva")

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
			texto_corral.set("02BIS")
			texto_cantidad = StringVar()
			texto_cantidad.set("16")
			texto_neto = StringVar()
			texto_neto.set("9999")
			texto_promedio = StringVar()
			texto_promedio.set("999")


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
			txt_observaciones.insert("1.0", "ASDASDASD")
			txt_observaciones.config(state="disabled")

			diccionario_objetos["datosLote_texto_catHacienda"] = texto_catHacienda
			diccionario_objetos["datosLote_texto_catVenta"] = texto_catVenta
			diccionario_objetos["datosLote_texto_corral"] = texto_corral
			diccionario_objetos["datosLote_texto_cantidad"] = texto_cantidad
			diccionario_objetos["datosLote_texto_neto"] = texto_neto
			diccionario_objetos["datosLote_texto_promedio"] = texto_promedio
			diccionario_objetos["datosLote_txt_observaciones"] = txt_observaciones

		#COMPRADOR
		if(True):
			texto_alias = StringVar()
			texto_alias.set("Fernandez Lucas Ramon Matias")
			texto_razon = StringVar()
			texto_razon.set("asdasd")
			texto_cuit = StringVar()
			texto_cuit.set("20-40500364-4")

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
			texto_kgs.set("99999")
			texto_total = StringVar()
			texto_total.set("9999999.99")
			texto_cabezas = StringVar()
			texto_cabezas.set("999")

			lbl_kgs = tk.Label(lblComprador, font=("Helvetica Neue", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_kgs.place(x=305, y=-2, width=90)
			lbl_kgs.config(textvariable=texto_kgs)

			lbl_total = tk.Label(lblComprador, font=("Helvetica Neue", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_total.place(x=305, y=18, width=90)
			lbl_total.config(textvariable=texto_total)

			lbl_cabezas = tk.Label(lblComprador, font=("Helvetica Neue", 10, "bold"), anchor="w", backgroun="#f0f0f0")
			lbl_cabezas.place(x=305, y=38, width=90)
			lbl_cabezas.config(textvariable=texto_cabezas)

			btn_productorAuxiliar = tk.Button(lblComprador, text="Nuevo productor auxiliar", compound="top", backgroun="#dbdbdb", font=("Helvetica", 10, "bold"))
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
			btn_guardar = tk.Button(lbl_datos, text="GUARDAR", compound="top", backgroun="#b3f2bc", font=("Helvetica", 20, "bold"))
			btn_guardar.place(x=810, y=114, width=196, height=60)

			btn_eliminar = tk.Button(lbl_datos, text="ELIMINAR", compound="top", backgroun="#FF6E6E", font=("Helvetica", 15, "bold"))
			btn_eliminar.place(x=810, y=180, width=196, height=48)


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


window.mainloop()

