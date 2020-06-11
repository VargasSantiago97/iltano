#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

from librerias import ventanaRemates

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
window.geometry("1285x728")
window.configure(backgroun="#2C4D4F") #E8F6FA


#Pantalla detalles
def pantallaDetalles():
	def pantCompletaDetalles():
		windowDetalles.attributes('-fullscreen', dicc_objetos["varFullScreenDetalles"])
		dicc_objetos["varFullScreenDetalles"] = not dicc_objetos["varFullScreenDetalles"]

	windowDetalles = Tk()
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




window.mainloop()

