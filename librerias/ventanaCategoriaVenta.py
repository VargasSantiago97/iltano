#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

import tablaElegir
#from librerias import tablaElegir

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Menu
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

from PIL import Image,ImageTk

import os
import os.path

import sqlite3
from sqlite3 import Error

import shutil

diccionarioObjetos = {}
direccionBaseDeDatos = 'database/iltanohacienda.db'

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

def ayuda():
	messagebox.showinfo("Atencion", "Ayuda no disponible")
	pass
def buscar():
	def funcsalirr(ssss):

		con = sql_connection()
		condiciones = " WHERE id = " + str(ssss)
		rows = actualizar_db(con, "productores", condiciones)

		diccionarioObjetos["entryAlias"].delete(0, tk.END)
		diccionarioObjetos["entryAlias"].insert(0, rows[0][1])

		verificar()

	dicc_buscar = {"seleccionar" : "productor",
	"columnas" : {"0":{"id" : "alias", "cabeza" : "Alias", "ancho" : 180, "row" : 1}, "1":{"id" : "razon", "cabeza" : "Razon Social", "ancho" : 180, "row" : 2}, "2":{"id" : "cuit", "cabeza" : "CUIT", "ancho" : 110, "row" : 3}},
	"db" : direccionBaseDeDatos,
	"tabla" : "productores",
	"condiciones" : ' WHERE (nombre LIKE  "%' + str(diccionarioObjetos["entryAlias"].get()) + '%" OR razon LIKE "%' + str(diccionarioObjetos["entryAlias"].get()) + '%" OR ndoc LIKE "%' + str(diccionarioObjetos["entryAlias"].get()) + '%") AND estado = "activo"',
	"dimensionesVentana" : "500x400"}
	tablaElegir.tabla_elegir(dicc_buscar, funcsalirr)

def verificar():
	alias = diccionarioObjetos["entryAlias"].get()

	con = sql_connection()
	condiciones = " WHERE nombre = '" + str(alias) + "' AND estado='activo'"
	rows = actualizar_db(con, "productores", condiciones)

	if len(rows) == 1:
		activarCampos()
		borrarCampos()
		diccionarioObjetos["entryAlias"].delete(0, tk.END)
		cargarDatosProductor(rows[0])
		botonesEditar()
		diccionarioObjetos["entryRazon"].focus()
	else:
		activarCampos()
		borrarCampos()
		botonesNuevo()
		diccionarioObjetos["entryRazon"].focus()


def activarCampos():
	diccionarioObjetos["entryRazon"].config(state="normal")
	diccionarioObjetos["entryDocumento"].config(state="normal")
	diccionarioObjetos["comboTipo"].config(state="readonly")
	diccionarioObjetos["comboIva"].config(state="readonly")
	diccionarioObjetos["entryRuca"].config(state="normal")
	diccionarioObjetos["entryEstablecimiento"].config(state="normal")

	diccionarioObjetos["entryDireccion"].config(state="normal")
	diccionarioObjetos["entryLocalidad"].config(state="normal")
	diccionarioObjetos["entryProvincia"].config(state="normal")
	diccionarioObjetos["entryPostal"].config(state="normal")

	diccionarioObjetos["entryTelefono"].config(state="normal")
	diccionarioObjetos["entryCorreo"].config(state="normal")
	diccionarioObjetos["entryCbu"].config(state="normal")
	diccionarioObjetos["entryObservaciones"].config(state="normal")

	diccionarioObjetos["entryCompras"].config(state="normal")
	diccionarioObjetos["entryVentas"].config(state="normal")
def desactivarCarga():
	diccionarioObjetos["entryRazon"].config(state="disabled")
	diccionarioObjetos["entryDocumento"].config(state="disabled")
	diccionarioObjetos["comboTipo"].config(state="disabled")
	diccionarioObjetos["comboIva"].config(state="disabled")
	diccionarioObjetos["entryRuca"].config(state="disabled")
	diccionarioObjetos["entryEstablecimiento"].config(state="disabled")

	diccionarioObjetos["entryDireccion"].config(state="disabled")
	diccionarioObjetos["entryLocalidad"].config(state="disabled")
	diccionarioObjetos["entryProvincia"].config(state="disabled")
	diccionarioObjetos["entryPostal"].config(state="disabled")

	diccionarioObjetos["entryTelefono"].config(state="disabled")
	diccionarioObjetos["entryCorreo"].config(state="disabled")
	diccionarioObjetos["entryCbu"].config(state="disabled")
	diccionarioObjetos["entryObservaciones"].config(state="disabled")

	diccionarioObjetos["entryCompras"].config(state="disabled")
	diccionarioObjetos["entryVentas"].config(state="disabled")

	diccionarioObjetos["botGuardar"]["state"] = "disabled"
	diccionarioObjetos["botBorrar"]["state"] = "disabled"
	diccionarioObjetos["botEditar"]["state"] = "disabled"
	diccionarioObjetos["botBuscar"]["state"] = "normal"

	diccionarioObjetos["entryAlias"].delete(0, tk.END)
	diccionarioObjetos["entryAlias"].focus()
def borrarCampos():
	diccionarioObjetos["entryRazon"].delete(0, tk.END)
	diccionarioObjetos["entryDocumento"].delete(0, tk.END)
	diccionarioObjetos["entryRuca"].delete(0, tk.END)
	diccionarioObjetos["entryEstablecimiento"].delete(0, tk.END)

	diccionarioObjetos["entryDireccion"].delete(0, tk.END)
	diccionarioObjetos["entryLocalidad"].delete(0, tk.END)
	diccionarioObjetos["entryProvincia"].delete(0, tk.END)
	diccionarioObjetos["entryPostal"].delete(0, tk.END)

	diccionarioObjetos["entryTelefono"].delete(0, tk.END)
	diccionarioObjetos["entryCorreo"].delete(0, tk.END)
	diccionarioObjetos["entryCbu"].delete(0, tk.END)
	diccionarioObjetos["entryObservaciones"].delete(0, tk.END)

	diccionarioObjetos["entryCompras"].delete(0, tk.END)
	diccionarioObjetos["entryVentas"].delete(0, tk.END)
def cargarDatosProductor(row):
	idd = str(row[0])
	nombre = str(row[1])
	razon = str(row[2])
	ndoc = str(row[3])
	tipo = str(row[4])
	grupo = str(row[5])
	con_iva = str(row[6])
	direccion = str(row[7])
	localidad = str(row[8])
	provincia = str(row[9])
	cod_postal = str(row[10])
	comprobante_defecto = str(row[11])
	punto_defecto = str(row[12])
	observaciones = str(row[13])
	creado_el = str(row[14])
	creado_por = str(row[15])
	cbu = str(row[16])
	telefono = str(row[17])
	correo = str(row[18])
	ruca = str(row[19])
	renspa = str(row[20])
	compra = str(row[21])
	venta = str(row[22])
	establecimiento = str(row[23])
	estado = str(row[24])

	diccionarioObjetos["textID"].set(idd)
	diccionarioObjetos["textTitulo"].set(nombre)

	diccionarioObjetos["entryAlias"].insert(0, nombre)
	diccionarioObjetos["entryRazon"].insert(0, razon)
	diccionarioObjetos["entryDocumento"].insert(0, ndoc)
	diccionarioObjetos["comboTipo"].set(tipo)
	diccionarioObjetos["comboIva"].set(con_iva)
	diccionarioObjetos["entryRuca"].insert(0, ruca)
	diccionarioObjetos["entryEstablecimiento"].insert(0, establecimiento)

	diccionarioObjetos["entryDireccion"].insert(0, direccion)
	diccionarioObjetos["entryLocalidad"].insert(0, localidad)
	diccionarioObjetos["entryProvincia"].insert(0, provincia)
	diccionarioObjetos["entryPostal"].insert(0, cod_postal)

	diccionarioObjetos["entryTelefono"].insert(0, telefono)
	diccionarioObjetos["entryCorreo"].insert(0, correo)
	diccionarioObjetos["entryCbu"].insert(0, cbu)
	diccionarioObjetos["entryObservaciones"].insert(0, observaciones)

	diccionarioObjetos["entryCompras"].insert(0, compra)
	diccionarioObjetos["entryVentas"].insert(0, venta)

def guardar():
	try:
		x_idd = diccionarioObjetos["textID"].get()
		x_nombre = diccionarioObjetos["entryAlias"].get()
		x_razon = diccionarioObjetos["entryRazon"].get()
		x_ndoc = diccionarioObjetos["entryDocumento"].get()
		x_tipo = diccionarioObjetos["comboTipo"].get()
		x_grupo = ""
		x_con_iva = diccionarioObjetos["comboIva"].get()
		x_direccion = diccionarioObjetos["entryDireccion"].get()
		x_localidad = diccionarioObjetos["entryLocalidad"].get()
		x_provincia = diccionarioObjetos["entryProvincia"].get()
		x_cod_postal = diccionarioObjetos["entryPostal"].get()
		x_comprobante_defecto = ""
		x_punto_defecto = ""
		x_observaciones = diccionarioObjetos["entryObservaciones"].get()
		x_creado_el = str(time.strftime("%d-%m-%y"))
		x_creado_por = "root"
		x_cbu = diccionarioObjetos["entryCbu"].get()
		x_telefono = diccionarioObjetos["entryTelefono"].get()
		x_correo = diccionarioObjetos["entryCorreo"].get()
		x_ruca = diccionarioObjetos["entryRuca"].get()
		x_renspa = "renspa"
		x_compra = diccionarioObjetos["entryCompras"].get()
		x_venta = diccionarioObjetos["entryVentas"].get()
		x_establecimiento = diccionarioObjetos["entryEstablecimiento"].get()
		x_estado = "activo"

		entities = [x_nombre, x_razon, x_ndoc, x_tipo, x_grupo, x_con_iva, x_direccion, x_localidad, x_provincia, x_cod_postal, x_comprobante_defecto, x_punto_defecto, x_observaciones, x_creado_el, x_creado_por, x_cbu, x_telefono, x_correo, x_ruca, x_renspa, x_compra, x_venta, x_establecimiento, x_estado]

	except:
		messagebox.showerror("ERROR", "No se pudo obtener los datos")
		return 0

	try:
		MsgBox = messagebox.askquestion('ATENCION', "¿Desea guardar?", icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO productores VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
			con.commit()
			messagebox.showinfo("Guardado", "Guardado con Éxito")
			borrarCampos()
			desactivarCarga()
	except:
		messagebox.showerror("ERROR", "No se pudo Guardar")
def editar():
	try:
		x_idd = diccionarioObjetos["textID"].get()
		x_nombre = diccionarioObjetos["entryAlias"].get()
		x_razon = diccionarioObjetos["entryRazon"].get()
		x_ndoc = diccionarioObjetos["entryDocumento"].get()
		x_tipo = diccionarioObjetos["comboTipo"].get()
		x_grupo = ""
		x_con_iva = diccionarioObjetos["comboIva"].get()
		x_direccion = diccionarioObjetos["entryDireccion"].get()
		x_localidad = diccionarioObjetos["entryLocalidad"].get()
		x_provincia = diccionarioObjetos["entryProvincia"].get()
		x_cod_postal = diccionarioObjetos["entryPostal"].get()
		x_comprobante_defecto = ""
		x_punto_defecto = ""
		x_observaciones = diccionarioObjetos["entryObservaciones"].get()
		x_creado_el = str(time.strftime("%d-%m-%y"))
		x_creado_por = "root"
		x_cbu = diccionarioObjetos["entryCbu"].get()
		x_telefono = diccionarioObjetos["entryTelefono"].get()
		x_correo = diccionarioObjetos["entryCorreo"].get()
		x_ruca = diccionarioObjetos["entryRuca"].get()
		x_renspa = "renspa"
		x_compra = diccionarioObjetos["entryCompras"].get()
		x_venta = diccionarioObjetos["entryVentas"].get()
		x_establecimiento = diccionarioObjetos["entryEstablecimiento"].get()
		x_estado = "activo"

		entities = [str(x_nombre),
		str(x_razon),
		str(x_ndoc),
		str(x_tipo),
		str(x_grupo),
		str(x_con_iva),
		str(x_direccion),
		str(x_localidad),
		str(x_provincia),
		str(x_cod_postal),
		str(x_comprobante_defecto),
		str(x_punto_defecto),
		str(x_observaciones),
		str(x_creado_el),
		str(x_creado_por),
		str(x_cbu),
		str(x_telefono),
		str(x_correo),
		str(x_ruca),
		str(x_renspa),
		str(x_compra),
		str(x_venta),
		str(x_establecimiento),
		str(x_estado),
		str(x_idd)]
	except:
		messagebox.showerror("ERROR", "No se pudo obtener los datos")
		return 0

	try:
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea editar?\nID DB: ' + str(x_idd) + '\nAlias (anterior): ' + str(x_nombre), icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE productores SET nombre = ?, razon = ?, ndoc = ?, tipo = ?, grupo = ?, con_iva = ?, direccion = ?, localidad = ?, provincia = ?, cod_postal = ?, comprobante_defecto = ?, punto_defecto = ?, observaciones = ?, creado_el = ?, creado_por = ?, cbu = ?, telefono = ?, correo = ?, ruca = ?, renspa = ?, compra = ?, venta = ?, establecimiento = ?, estado = ? where id = ?', entities)
			con.commit()
			messagebox.showinfo("Editado", "EDITADO con Éxito")
			borrarCampos()
			desactivarCarga()
	except:
		messagebox.showerror("ERROR", "No se pudo editar")
def borrar():
	try:
		x_nombre = diccionarioObjetos["entryAlias"].get()
		x_id = diccionarioObjetos["textID"].get()

		MsgBox = messagebox.askquestion('ATENCION', '¿Desea BORRAR?\nID DB: ' + str(x_id) + '\nAlias (anterior): ' + str(x_nombre), icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE productores SET estado = "borrado" where id = ' + str(x_id))
			con.commit()
			messagebox.showinfo("Borrado", "Borrado con Éxito")
			borrarCampos()
			desactivarCarga()
	except:
		messagebox.showerror("ERROR", "No se pudo borrar")

def botonesEditar():
	diccionarioObjetos["botGuardar"]["state"] = "disabled"
	diccionarioObjetos["botBorrar"]["state"] = "normal"
	diccionarioObjetos["botEditar"]["state"] = "normal"
	diccionarioObjetos["botBuscar"]["state"] = "disabled"
def botonesNuevo():
	diccionarioObjetos["botGuardar"]["state"] = "normal"
	diccionarioObjetos["botBorrar"]["state"] = "disabled"
	diccionarioObjetos["botEditar"]["state"] = "disabled"
	diccionarioObjetos["botBuscar"]["state"] = "disabled"
def activarBuscar():
	diccionarioObjetos["botBuscar"]["state"] = "normal"
	pass
def desactivarBuscar():
	diccionarioObjetos["botBuscar"]["state"] = "disabled"
	pass

def escape():
	borrarCampos()
	desactivarCarga()


def bodyCatVenta(window):

		tk.Label(window, text = "Alias", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 1, padx=10, pady=10)
		tk.Label(window, text = "Razon social", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)
		tk.Label(window, text = "Documento", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 3, padx=10, pady=10)
		tk.Label(window, text = "Tipo", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 4, padx=10, pady=10)
		tk.Label(window, text = "Condicion IVA", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 5, padx=10, pady=10)
		tk.Label(window, text = "RUCA", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 6, padx=10, pady=10)
		tk.Label(window, text = "Establecimiento", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 7, padx=10, pady=10)

		entryAlias = Entry(window, font=("Helvetica Neue",14))
		entryRazon = Entry(window, font=("Helvetica Neue",14), state="disabled")
		entryDocumento = Entry(window, font=("Helvetica Neue",14), state="disabled")
		comboTipo = Combobox(window, font=("Helvetica Neue",14), state="disabled")
		comboIva = Combobox(window, font=("Helvetica Neue",14), state="disabled")
		entryRuca = Entry(window, font=("Helvetica Neue",14), state="disabled")
		entryEstablecimiento = Entry(window, font=("Helvetica Neue",14), state="disabled")

		entryAlias.grid(sticky = "w", column = 1, row = 1, padx=0, pady=10)
		entryRazon.grid(sticky = "w", column = 1, row = 2, padx=0, pady=10)
		entryDocumento.grid(sticky = "w", column = 1, row = 3, padx=0, pady=10)
		comboTipo.grid(sticky = "w", column = 1, row = 4, padx=0, pady=10)
		comboIva.grid(sticky = "w", column = 1, row = 5, padx=0, pady=10)
		entryRuca.grid(sticky = "w", column = 1, row = 6, padx=0, pady=10)
		entryEstablecimiento.grid(sticky = "w", column = 1, row = 7, padx=0, pady=10)

		diccionarioObjetos["entryAlias"] = entryAlias
		diccionarioObjetos["entryRazon"] = entryRazon
		diccionarioObjetos["entryDocumento"] = entryDocumento
		diccionarioObjetos["comboTipo"] = comboTipo
		diccionarioObjetos["comboIva"] = comboIva
		diccionarioObjetos["entryRuca"] = entryRuca
		diccionarioObjetos["entryEstablecimiento"] = entryEstablecimiento

		comboTipo["values"] = ["DNI", "CUIT", "OTRO"]
		comboIva["values"] = ["Responsable inscripto", "Monotributista", "Excento", "Consumidor final", "Otro"]
		comboTipo.current(1)
		comboIva.current(0)

		diccionarioObjetos["botBuscar"]["state"] = "normal"

		entryAlias.focus()
		entryAlias.bind('<Return>', (lambda event: verificar()))
		entryAlias.bind('<Button-1>', (lambda event: activarBuscar()))
		entryAlias.bind('<F5>', (lambda event: buscar()))

		entryRazon.bind('<Button-1>', (lambda event: desactivarBuscar()))
		entryDocumento.bind('<Button-1>', (lambda event: desactivarBuscar()))
		comboTipo.bind('<Button-1>', (lambda event: desactivarBuscar()))
		comboIva.bind('<Button-1>', (lambda event: desactivarBuscar()))
		entryRuca.bind('<Button-1>', (lambda event: desactivarBuscar()))
		entryEstablecimiento.bind('<Button-1>', (lambda event: desactivarBuscar()))

		entryRazon.bind('<Return>', (lambda event: entryDocumento.focus()))
		entryDocumento.bind('<Return>', (lambda event: comboTipo.focus()))
		comboTipo.bind('<Return>', (lambda event: comboIva.focus()))
		comboIva.bind('<Return>', (lambda event: entryRuca.focus()))
		entryRuca.bind('<Return>', (lambda event: entryEstablecimiento.focus()))

	#pestaña 2 DIRECCION
	if(True):
		tk.Label(label_direccion, text = "Direccion", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 1, padx=10, pady=10)
		tk.Label(label_direccion, text = "Localidad", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)
		tk.Label(label_direccion, text = "Provincia", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 3, padx=10, pady=10)
		tk.Label(label_direccion, text = "Cod. Postal", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 4, padx=10, pady=10)

		entryDireccion = Entry(label_direccion, font=("Helvetica Neue",14), state="disabled")
		entryLocalidad = Entry(label_direccion, font=("Helvetica Neue",14), state="disabled")
		entryProvincia = Entry(label_direccion, font=("Helvetica Neue",14), state="disabled")
		entryPostal = Entry(label_direccion, font=("Helvetica Neue",14), state="disabled")


		entryDireccion.grid(sticky = "w", column = 1, row = 1, padx=0, pady=10)
		entryLocalidad.grid(sticky = "w", column = 1, row = 2, padx=0, pady=10)
		entryProvincia.grid(sticky = "w", column = 1, row = 3, padx=0, pady=10)
		entryPostal.grid(sticky = "w", column = 1, row = 4, padx=0, pady=10)

		diccionarioObjetos["entryDireccion"] = entryDireccion
		diccionarioObjetos["entryLocalidad"] = entryLocalidad
		diccionarioObjetos["entryProvincia"] = entryProvincia
		diccionarioObjetos["entryPostal"] = entryPostal

		entryDireccion.bind('<Return>', (lambda event: entryLocalidad.focus()))
		entryLocalidad.bind('<Return>', (lambda event: entryProvincia.focus()))
		entryProvincia.bind('<Return>', (lambda event: entryPostal.focus()))

	#pestaña 3 RENSPA

	#pestaña 4 OTROS
	if(True):
		tk.Label(label_otros, text = "Telefono", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 1, padx=10, pady=10)
		tk.Label(label_otros, text = "Correo electronico", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)
		tk.Label(label_otros, text = "CBU", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 3, padx=10, pady=10)

		entryTelefono = Entry(label_otros, font=("Helvetica Neue",14), state="disabled")
		entryCorreo = Entry(label_otros, font=("Helvetica Neue",14), state="disabled")
		entryCbu = Entry(label_otros, font=("Helvetica Neue",14), state="disabled")


		entryTelefono.grid(sticky = "w", column = 1, row = 1, padx=0, pady=10)
		entryCorreo.grid(sticky = "w", column = 1, row = 2, padx=0, pady=10)
		entryCbu.grid(sticky = "w", column = 1, row = 3, padx=0, pady=10)

		diccionarioObjetos["entryTelefono"] = entryTelefono
		diccionarioObjetos["entryCorreo"] = entryCorreo
		diccionarioObjetos["entryCbu"] = entryCbu

		entryTelefono.bind('<Return>', (lambda event: entryCorreo.focus()))
		entryCorreo.bind('<Return>', (lambda event: entryCbu.focus()))

		tk.Label(label_otros, text = "Observaciones", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 4, padx=10, pady=10)
		entryObservaciones = Entry(label_otros, font=("Helvetica Neue",14), state="disabled")
		entryObservaciones.grid(sticky = "w", column = 1, row = 4, padx=0, pady=10)
		diccionarioObjetos["entryObservaciones"] = entryObservaciones
		entryCbu.bind('<Return>', (lambda event: entryObservaciones.focus()))


	#pestaña 5 FACTURACION
	if(True):
		tk.Label(label_facturacion, text = "Factura a nombre de:", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "n", column = 0, row = 1, padx=10, pady=10)

		lbl_auxiliar = tk.Label(label_facturacion, backgroun="#E6F5FF")
		lbl_auxiliar.grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)

		tk.Label(lbl_auxiliar, text = "Compras", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)
		tk.Label(lbl_auxiliar, text = "Ventas", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 3, padx=10, pady=10)

		entryCompras = Entry(lbl_auxiliar, font=("Helvetica Neue",14), state="disabled")
		entryVentas = Entry(lbl_auxiliar, font=("Helvetica Neue",14), state="disabled")

		entryCompras.grid(sticky = "w", column = 1, row = 2, padx=0, pady=10)
		entryVentas.grid(sticky = "w", column = 1, row = 3, padx=0, pady=10)

		diccionarioObjetos["entryCompras"] = entryCompras
		diccionarioObjetos["entryVentas"] = entryVentas

		entryCompras.bind('<Return>', (lambda event: entryVentas.focus()))


def ventana1(idProductor):

	def cerrarVentana():
		window.destroy()

	dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}

	window = Tk()
	window.title("CATEGORIAS DE VENTA")
	window.geometry("700x500+200+50")
	window.configure(backgroun="#E6F5FF") #E8F6FA
	window.resizable(0,0)

	iconGuardar = Image.open('iconos/guardar.png')
	iconBorrar = Image.open('iconos/borrar.png')
	iconEditar = Image.open('iconos/editar.png')
	iconBuscar = Image.open('iconos/buscar.png')
	iconAyuda = Image.open('iconos/ayuda.png')
	iconCerrar = Image.open('iconos/cerrar.png')

	iconGuardar = ImageTk.PhotoImage(iconGuardar)
	iconBorrar = ImageTk.PhotoImage(iconBorrar)
	iconEditar = ImageTk.PhotoImage(iconEditar)
	iconBuscar = ImageTk.PhotoImage(iconBuscar)
	iconAyuda = ImageTk.PhotoImage(iconAyuda)
	iconCerrar = ImageTk.PhotoImage(iconCerrar)

	barraherr = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraherr.pack(side=TOP, fill=X, pady = 2)

	barraTitulo = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraTitulo.pack(side=TOP, fill=X)

	lblBody = tk.Label(window, backgroun="#E6F5FF")
	lblBody.pack(side=TOP, fill=X, padx=10)

	botGuardar = tk.Button(barraherr, image=iconGuardar, compound="top", backgroun="#b3f2bc", command=guardar)
	botBorrar = tk.Button(barraherr, image=iconBorrar, compound="top", backgroun="#FFaba8", command = borrar)
	botEditar = tk.Button(barraherr, image=iconEditar, compound="top", backgroun="#f2f0b3", command = editar)
	botBuscar = tk.Button(barraherr, image=iconBuscar, compound="top", command = buscar, backgroun="#b1fae3")
	botAyuda = tk.Button(barraherr, image=iconAyuda, compound="top", command=ayuda, backgroun="#f2f0b3")
	botCerrar = tk.Button(barraherr, image=iconCerrar, compound="top", command=cerrarVentana, backgroun="#FF6E6E")

	padX=3
	padY=2

	botGuardar.pack(side=LEFT, padx=padX, pady=padY)
	botBorrar.pack(side=LEFT, padx=padX, pady=padY)
	botEditar.pack(side=LEFT, padx=padX, pady=padY)
	botBuscar.pack(side=LEFT, padx=padX+20, pady=padY)
	botAyuda.pack(side=LEFT, padx=padX, pady=padY)
	botCerrar.pack(side=LEFT, padx=padX, pady=padY)

	botGuardar["state"] = "disabled"
	botBorrar["state"] = "disabled"
	botEditar["state"] = "disabled"
	botBuscar["state"] = "disabled"

	textTitulo = StringVar()
	textTitulo.set("Cat. venta")
	textID = StringVar()
	textID.set("")

	lbl_titulo = tk.Label(barraTitulo, font=("Helvetica Neue",10,"bold"), anchor="n", backgroun="#BAE7FF")
	lbl_titulo.pack()
	lbl_titulo.config(textvariable=textTitulo)

	diccionarioObjetos["botGuardar"] = botGuardar
	diccionarioObjetos["botBorrar"] = botBorrar
	diccionarioObjetos["botEditar"] = botEditar
	diccionarioObjetos["botBuscar"] = botBuscar

	diccionarioObjetos["textTitulo"] = textTitulo
	diccionarioObjetos["textID"] = textID
	

	window.bind("<Escape>", (lambda event: escape()))
	window.bind("<Control-s>", (lambda event: cerrarVentana()))

	bodyCatVenta(lblBody)

	window.mainloop()

ventana1("NULL")