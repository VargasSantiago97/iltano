#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

#from librerias import ventanaProductor
import ventanaProductor

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

diccionario_datos_productor = {"enviar":"NULL"}

diccionario_textos = {}

def sql_connection():
	try:
		con = sqlite3.connect('C:\\Users\\Santiago\\Desktop\\PROYECTO_IL_TANO\\index\\librerias\\database\\iltanohacienda.db')
		return con
	except Error:
		messagebox.showerror("ERROR", "Error conectando a la base de datos")

def actualizar_db(con, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows

def cargarTabla(rows, tabla_productor):
	for i in tabla_productor.get_children():
		tabla_productor.delete(i)
	i=0
	for row in rows:
		tabla_productor.insert("", tk.END, text = str(row[0]), iid=i, values = (str(row[1]), 
			str(row[2]),
			str(row[3]),
			str(row[19]),
			str(row[6])))
		i = i + 1 

def cargarProductor(entrada):
	cuit = str(entrada["values"][2])
	
	con = sql_connection()
	condiciones = " WHERE ndoc = '" + cuit + "' AND estado = 'activo'"
	rows = actualizar_db(con, "productores", condiciones)

	row = rows[0]

	diccionario_textos["alias"].set(row[1])
	diccionario_textos["razon"].set(row[2])
	diccionario_textos["cuit"].set(row[3])
	diccionario_textos["codicion"].set(row[6])
	diccionario_textos["ruca"].set(row[19])
	diccionario_textos["grupo"].set(row[5])
	diccionario_textos["establecimiento"].set(row[23])
	diccionario_textos["cbu"].set(row[16])
	diccionario_textos["telefono"].set(row[17])
	diccionario_textos["correo"].set(row[18])
	diccionario_textos["direccion"].set(row[7])
	diccionario_textos["localidad"].set(row[8])
	diccionario_textos["provincia"].set(row[9])
	diccionario_textos["postal"].set(row[10])
	diccionario_textos["compra"].set(row[21])
	diccionario_textos["venta"].set(row[22])

def borrarProductor(id_product):
	con = sql_connection()
	cursorObj = con.cursor()
	try:
		print(id_product)
		print(type(id_product))
		cursorObj.execute('UPDATE productores SET estado = "borrado" WHERE id = ' + str(id_product))
		con.commit()
		messagebox.showinfo("Éxito", "Productor borrado con éxito")
	except:
		messagebox.showerror("ERROR", "Error al borrar")






def func_nuevo():
	diccionario_datos_productor["enviar"] = "nuevo"
	ventanaProductor.productor(diccionario_datos_productor)

def func_editar(texto_cuit):
	if (texto_cuit == ""):
		messagebox.showerror("ERROR", "Primero seleccione un productor con doble click en la lista")
	else:
		diccionario_datos_productor["enviar"] = texto_cuit
		ventanaProductor.productor(diccionario_datos_productor)

def func_borrar(texto_cuit, tabla_productor):
	if (texto_cuit == ""):
		messagebox.showerror("ERROR", "Primero seleccione un productor con doble click en la lista")
	else:
		rows=["NULL"]
		try:
			con = sql_connection()
			condiciones = " WHERE ndoc = '" + texto_cuit + "' AND estado='activo'"
			rows = actualizar_db(con, "productores", condiciones)
		except:
			messagebox.showerror("ERROR", "Error al buscar productor en la base de datos")
		if (rows[0] != "NULL"):
			MsgBox = messagebox.askquestion('INFO','Desea eliminar este productor?\n\nNombre:  ' + str(rows[0][2]) + '\nCuit:         ' + str(rows[0][3]),icon = 'warning')
			if MsgBox == 'yes':
				try:
					borrarProductor(rows[0][0])
					productFiltrar("", tabla_productor)
				except:
					messagebox.showerror("ERROR", "Error al borrar")


def productFiltrar(entrada, tabla_productor):
	pal_clave = str(entrada)
	con = sql_connection()
	condiciones =  ' WHERE (nombre LIKE "%' + pal_clave + '%" OR razon LIKE "%' + pal_clave + '%" OR ndoc LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%" OR con_iva LIKE "%' + pal_clave + '%" OR localidad LIKE "%' + pal_clave + '%" OR provincia LIKE "%' + pal_clave + '%" OR ruca LIKE "%' + pal_clave + '%" OR establecimiento LIKE "%' + pal_clave + '%") AND estado = "activo"'
	rows = actualizar_db(con, "productores", condiciones)
	cargarTabla(rows, tabla_productor)

def productor(window):
	padX = 5
	padY = 5

	lbl_ventana_productor_buscador = LabelFrame(window, text="Buscar productor")
	lbl_ventana_productor_informacion = LabelFrame(window, text="Informacion")
	lbl_ventana_productor_acciones = LabelFrame(window, text="Acciones")

	lbl_ventana_productor_buscador.place(x = 10, y = 10, width = 730, height = 725)
	lbl_ventana_productor_informacion.place(x = 750, y = 10, width = 565, height = 590)
	lbl_ventana_productor_acciones.place(x = 750, y = 600, width = 565, height = 135)

	#--Buscador
	lbl_ventana_productor_buscador_entry = LabelFrame(lbl_ventana_productor_buscador, text="Filtrar")
	lbl_ventana_productor_buscador_tabla = LabelFrame(lbl_ventana_productor_buscador, text="Productores")

	lbl_ventana_productor_buscador_entry.pack()
	lbl_ventana_productor_buscador_tabla.pack()

	#--
	entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="43")
	entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = padY)
	entry_filtrar_productor.focus()

	btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar", command = lambda: productFiltrar(entry_filtrar_productor.get(), tabla_productor))
	btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 5)

	sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
	sbr_productor.pack(side=RIGHT, fill="y")

	tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("alias", "razon", "cuit", "ruca", "condicion"), selectmode=tk.BROWSE, height=30)
	tabla_productor.pack(side=LEFT, fill="both", expand=True)
	sbr_productor.config(command=tabla_productor.yview)
	tabla_productor.config(yscrollcommand=sbr_productor.set)

	tabla_productor.heading("#0", text="Cód.")
	tabla_productor.heading("alias", text="Alias")
	tabla_productor.heading("razon", text="Razón Social")
	tabla_productor.heading("cuit", text="CUIT/DNI")
	tabla_productor.heading("ruca", text="N° RUCA")
	tabla_productor.heading("condicion", text="IVA")

	tabla_productor.column("#0", width=40)
	tabla_productor.column("alias", width=180)
	tabla_productor.column("razon", width=180)
	tabla_productor.column("cuit", width=90)
	tabla_productor.column("ruca", width=80)
	tabla_productor.column("condicion", width=130)


	entry_filtrar_productor.bind("<Return>", (lambda event: productFiltrar(entry_filtrar_productor.get(), tabla_productor)))	


	texto_alias = StringVar()
	texto_razon = StringVar()
	texto_cuit = StringVar()
	texto_condicion = StringVar()
	texto_ruca = StringVar()
	texto_grupo = StringVar()
	texto_establecimiento = StringVar()
	texto_cbu = StringVar()
	texto_telefono = StringVar()
	texto_correo = StringVar()
	texto_direccion = StringVar()
	texto_localidad = StringVar()
	texto_provincia = StringVar()
	texto_postal = StringVar()
	texto_compra = StringVar()
	texto_venta = StringVar()

	diccionario_textos["alias"] = texto_alias
	diccionario_textos["razon"] = texto_razon
	diccionario_textos["cuit"] = texto_cuit
	diccionario_textos["codicion"] = texto_condicion
	diccionario_textos["ruca"] = texto_ruca
	diccionario_textos["grupo"] = texto_grupo
	diccionario_textos["establecimiento"] = texto_establecimiento
	diccionario_textos["cbu"] = texto_cbu
	diccionario_textos["telefono"] = texto_telefono
	diccionario_textos["correo"] = texto_correo
	diccionario_textos["direccion"] = texto_direccion
	diccionario_textos["localidad"] = texto_localidad
	diccionario_textos["provincia"] = texto_provincia
	diccionario_textos["postal"] = texto_postal
	diccionario_textos["compra"] = texto_compra
	diccionario_textos["venta"] = texto_venta


	lbl_alias = tk.Label(lbl_ventana_productor_informacion, font=("verdana",20), anchor="w")
	lbl_alias.place(x=10, y=25, width = 550, height = 30)
	lbl_alias.config(textvariable=texto_alias)

	lbl_razon = tk.Label(lbl_ventana_productor_informacion, font=("verdana",12), anchor="w")
	lbl_razon.place(x=10, y=65, width = 550, height = 22)
	lbl_razon.config(textvariable=texto_razon)

	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="CUIT:", anchor="w").place(x=10, y=130, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Condición IVA:", anchor="w").place(x=250, y=130, width = 200, height = 20)

	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="RUCA:", anchor="w").place(x=10, y=160, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Grupo:", anchor="w").place(x=250, y=160, width = 100, height = 20)

	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Establecimiento:", anchor="w").place(x=10, y=190, width = 120, height = 20)	
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="CBU", anchor="w").place(x=10, y=220, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Teléfono:", anchor="w").place(x=10, y=250, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Correo:", anchor="w").place(x=250, y=250, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Dirección:", anchor="w").place(x=10, y=280, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Localidad:", anchor="w").place(x=10, y=305, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Provincia:", anchor="w").place(x=10, y=330, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Cód. Postal:", anchor="w").place(x=250, y=330, width = 100, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Factura Compra a:", anchor="w").place(x=10, y=355, width = 130, height = 20)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Factura Venta a:", anchor="w").place(x=290, y=355, width = 125, height = 20)

	lbl_cuit = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_cuit.place(x=60, y=128, width = 180, height = 22)
	lbl_cuit.config(textvariable=texto_cuit)

	lbl_condicion = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_ruca = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_grupo = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_establecimiento = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_cbu = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_telefono = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_correo = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",10), anchor="w")
	lbl_direccion = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_localidad = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_provincia = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_postal = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_compra = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")
	lbl_venta = tk.Label(lbl_ventana_productor_informacion, font=("verdana-bold",12), anchor="w")


	lbl_condicion.place(x=350, y=128, width = 180, height = 22)
	lbl_ruca.place(x=60, y=158, width = 180, height = 22)
	lbl_grupo.place(x=300, y=158, width = 230, height = 22)
	lbl_establecimiento.place(x=130, y=188, width = 400, height = 22)
	lbl_cbu.place(x=60, y=218, width = 400, height = 22)
	lbl_telefono.place(x=70, y=248, width = 170, height = 22)
	lbl_correo.place(x=310, y=248, width = 220, height = 22)
	lbl_direccion.place(x=100, y=278, width = 400, height = 22)
	lbl_localidad.place(x=100, y=303, width = 400, height = 22)
	lbl_provincia.place(x=100, y=328, width = 180, height = 22)
	lbl_postal.place(x=340, y=328, width = 180, height = 22)
	lbl_compra.place(x=140, y=353, width = 130, height = 22)
	lbl_venta.place(x=410, y=353, width = 130, height = 22)

	lbl_condicion.config(textvariable=texto_condicion)
	lbl_ruca.config(textvariable=texto_ruca)
	lbl_grupo.config(textvariable=texto_grupo)
	lbl_establecimiento.config(textvariable=texto_establecimiento)
	lbl_cbu.config(textvariable=texto_cbu)
	lbl_telefono.config(textvariable=texto_telefono)
	lbl_correo.config(textvariable=texto_correo)
	lbl_direccion.config(textvariable=texto_direccion)
	lbl_localidad.config(textvariable=texto_localidad)
	lbl_provincia.config(textvariable=texto_provincia)
	lbl_postal.config(textvariable=texto_postal)
	lbl_compra.config(textvariable=texto_compra)
	lbl_venta.config(textvariable=texto_venta)


	#texto_alias.set("Bienvenidosada1234564789101112aaaaaaaaaaaaa")


	#Acciones
	btn_nuevo = tk.Button(lbl_ventana_productor_acciones, text="NUEVO", font=("verdana",15), backgroun="#CBF9E1", command= lambda: func_nuevo())
	btn_nuevo.place(x = 15, y = 15, width=120, height=80)

	btn_editar = tk.Button(lbl_ventana_productor_acciones, text="EDITAR", font=("verdana",15), backgroun="#D6F4F8", command= lambda: func_editar(texto_cuit.get()))
	btn_editar.place(x = 150, y = 15, width=120, height=80)

	btn_borrar = tk.Button(lbl_ventana_productor_acciones, text="BORRAR", font=("verdana",15), backgroun="#F5A9A9", command= lambda: func_borrar(texto_cuit.get(), tabla_productor))
	btn_borrar.place(x = 285, y = 15, width=120, height=80)

	btn_imprimir = tk.Button(lbl_ventana_productor_acciones, text="IMPRIMIR", font=("verdana",15), backgroun="#D6F4F8")
	btn_imprimir.place(x = 420, y = 15, width=120, height=80)

	try:
		con = sql_connection()
		condiciones = " WHERE estado = 'activo'"
		rows = actualizar_db(con, "productores", condiciones)
		cargarTabla(rows, tabla_productor)
	except:
		messagebox.showerror("ERROR", "Error al leer base de datos")

	tabla_productor.bind("<Double-1>", (lambda event: cargarProductor(tabla_productor.item((tabla_productor.selection()[0])))))
	tabla_productor.bind("<Return>", (lambda event: cargarProductor(tabla_productor.item((tabla_productor.selection()[0])))))







window1 = Tk()
window1.title("asd")
window1.geometry("1325x768")
productor(window1)
window1.mainloop()