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

window = Tk()
window.title("IL TANO HACIENDA SAS")
window.geometry("1024x600")
window.resizable(0,0)
window.configure(backgroun="#000000") #E8F6FA

dicRemates = {
	"seleccionar" : "REMATES",
	
	"columnas" : {
		"0":{
			"id" : "num1", 
			"cabeza" : "CORRAL", 
			"ancho" : 30, 
			"row" : 1}, 
		"1":{
			"id" : "num2", 
			"cabeza" : "VENDEDOR", 
			"ancho" : 100, 
			"row" : 2},
		"2":{
			"id" : "num3", 
			"cabeza" : "CANTIDAD", 
			"ancho" : 30, 
			"row" : 4},
		"3":{
			"id" : "num4", 
			"cabeza" : "CATEGORIA", 
			"ancho" : 100, 
			"row" : 6},
		"4":{
			"id" : "num5", 
			"cabeza" : "PINTURA", 
			"ancho" : 30, 
			"row" : 7},
		"5":{
			"id" : "num6", 
			"cabeza" : "KGS", 
			"ancho" : 30, 
			"row" : 7},
		"6":{
			"id" : "num7", 
			"cabeza" : "PROMEDIO", 
			"ancho" : 30, 
			"row" : 7},
		"7":{
			"id" : "num8", 
			"cabeza" : "PRECIO", 
			"ancho" : 30, 
			"row" : 7},
		"8":{
			"id" : "num9", 
			"cabeza" : "COMPRADOR", 
			"ancho" : 100, 
			"row" : 7},
		},
	
	"consulta": {
		"db" : 'database/iltanohacienda.db',
		"tabla" : "remate",
		"condiciones" : ' WHERE estado = "activo"'},
	"filtros" : {
		"0" : {
			"id": "nombre",
			"cabeza":"Alias",
		},
		"1" : {
			"id": "fecha",
			"cabeza":"Fecha",
		},
		"2" : {
			"id": "tipo",
			"cabeza":"Tipo",
		},
		"3" : {
			"id": "predio",
			"cabeza":"Predio",
		},
		"4" : {
			"id": "localidad",
			"cabeza":"Localidad",
		},
		"5" : {
			"id": "martillo",
			"cabeza":"Martillo",
		},
	},
	}

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
	mnuRemate.add_command(label="Cambiar")

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

	botBuscar = tk.Button(barraherr, text="bot 1\nasd", compound="top", backgroun="#b3f2bc")
	botImprimir = tk.Button(barraherr, text="bot 2", compound="top", backgroun="#f2f0b3")
	botExcel = tk.Button(barraherr, text="bot 3", compound="top", backgroun="#f2f0b3")
	botAyuda = tk.Button(barraherr, text="bot 4", compound="top", backgroun="#f2f0b3")
	botCerrar = tk.Button(barraherr, text="bot 5", compound="top", backgroun="#FF6E6E")

	padX=3
	padY=2

	botBuscar.pack(side=LEFT, padx=padX+20, pady=padY)
	botImprimir.pack(side=LEFT, padx=padX, pady=padY)
	botExcel.pack(side=LEFT, padx=padX, pady=padY)
	botAyuda.pack(side=LEFT, padx=padX+20, pady=padY)
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

		columnas = []
		for i in range(0, len(dicRemates["columnas"])):
			columnas.append(dicRemates["columnas"][str(i)]["id"])
		columnas = tuple(columnas)

		tabla = ttk.Treeview(lbl_tabla, columns=columnas, selectmode=tk.BROWSE, show='headings') 
		tabla.pack(side=LEFT, fill="both", expand=True)
		sbr.config(command=tabla.yview)
		tabla.config(yscrollcommand=sbr.set)


		for i in range(0, len(dicRemates["columnas"])):
			tabla.heading(dicRemates["columnas"][str(i)]["id"], text=dicRemates["columnas"][str(i)]["cabeza"], command=lambda: treeview_sort_column(tabla, dicRemates["columnas"][str(i)]["id"], False))
			tabla.column(dicRemates["columnas"][str(i)]["id"], width=dicRemates["columnas"][str(i)]["ancho"])


		tabla.bind("<Double-1>", (lambda event: elegir(tabla.item(tabla.selection()))))
		tabla.bind("<Return>", (lambda event: elegir(tabla.item(tabla.selection()))))




window.mainloop()

