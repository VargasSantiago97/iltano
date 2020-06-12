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
		rows = actualizar_db(con, "catHacienda", condiciones)

		diccionarioObjetos["entryAlias"].delete(0, tk.END)
		diccionarioObjetos["entryAlias"].insert(0, rows[0][1])

		verificar()

	dicc_buscar = {"seleccionar" : "categoria de hacienda",
	"columnas" : {"0":{"id" : "alias", "cabeza" : "Alias", "ancho" : 50, "row" : 1}, "1":{"id" : "nombre", "cabeza" : "Nombre", "ancho" : 150, "row" : 2}, "2":{"id" : "descripcion", "cabeza" : "Descripcion", "ancho" : 180, "row" : 3}},
	"db" : direccionBaseDeDatos,
	"tabla" : "catHacienda",
	"condiciones" : ' WHERE (alias LIKE  "%' + str(diccionarioObjetos["entryAlias"].get()) + '%" OR nombre LIKE "%' + str(diccionarioObjetos["entryAlias"].get()) + '%") AND estado = "activo"',
	"dimensionesVentana" : "420x400"}
	tablaElegir.tabla_elegir(dicc_buscar, funcsalirr)

def verificar():
	alias = diccionarioObjetos["entryAlias"].get()

	con = sql_connection()
	condiciones = " WHERE alias = '" + str(alias) + "' AND estado='activo'"
	rows = actualizar_db(con, "catHacienda", condiciones)

	if len(rows) == 1:
		activarCampos()
		borrarCampos()
		diccionarioObjetos["entryAlias"].delete(0, tk.END)
		cargarDatosCatHacienda(rows[0])
		botonesEditar()
		diccionarioObjetos["entryRazon"].focus()
	else:
		activarCampos()
		borrarCampos()
		botonesNuevo()
		diccionarioObjetos["entryRazon"].focus()


def activarCampos():
	diccionarioObjetos["entryRazon"].config(state="normal")
	diccionarioObjetos["entryDescripcion"].config(state="normal")

def desactivarCarga():
	diccionarioObjetos["entryRazon"].config(state="disabled")
	diccionarioObjetos["entryDescripcion"].config(state="disabled")

	diccionarioObjetos["entryAlias"].delete(0, tk.END)
	diccionarioObjetos["entryAlias"].focus()
def borrarCampos():
	diccionarioObjetos["entryRazon"].delete(0, tk.END)
	diccionarioObjetos["entryDescripcion"].delete(0, tk.END)
def cargarDatosCatHacienda(row):
	idd = str(row[0])
	nombre = str(row[1])
	razon = str(row[2])
	descripcion = str(row[3])
	estado = str(row[4])

	diccionarioObjetos["textID"].set(idd)
	diccionarioObjetos["textTitulo"].set(nombre + " - " + razon)

	diccionarioObjetos["entryAlias"].insert(0, nombre)
	diccionarioObjetos["entryRazon"].insert(0, razon)
	diccionarioObjetos["entryDescripcion"].insert(0, descripcion)

def guardar():
	try:
		x_idd = diccionarioObjetos["textID"].get()
		x_nombre = diccionarioObjetos["entryAlias"].get()
		x_razon = diccionarioObjetos["entryRazon"].get()
		x_descripcion = diccionarioObjetos["entryDescripcion"].get()

		x_estado = "activo"

		entities = [str(x_nombre), str(x_razon), str(x_descripcion), str(x_estado)]

	except:
		messagebox.showerror("ERROR", "No se pudo obtener los datos")
		return 0

	try:
		MsgBox = messagebox.askquestion('ATENCION', "¿Desea guardar?", icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO catHacienda VALUES(NULL, ?, ?, ?, ?)", entities)
			con.commit()
			messagebox.showinfo("Guardado", "Guardado con Éxito")
			escape()
	except:
		messagebox.showerror("ERROR", "No se pudo Guardar")
def editar():
	try:
		x_idd = diccionarioObjetos["textID"].get()
		x_nombre = diccionarioObjetos["entryAlias"].get()
		x_razon = diccionarioObjetos["entryRazon"].get()
		x_descripcion = diccionarioObjetos["entryDescripcion"].get()
		x_estado = "activo"

		entities = [str(x_nombre), str(x_razon), str(x_descripcion), str(x_estado), str(x_idd)]
	except:
		messagebox.showerror("ERROR", "No se pudo obtener los datos")
		return 0

	try:
		MsgBox = messagebox.askquestion('ATENCION', '¿Desea editar?\nID DB: ' + str(x_idd) + '\nAlias (anterior): ' + str(x_nombre), icon = 'warning')
		if(MsgBox == 'yes'):
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute('UPDATE catHacienda SET alias = ?, nombre = ?, descripcion = ?, estado = ? where id = ?', entities)
			con.commit()
			messagebox.showinfo("Editado", "EDITADO con Éxito")
			escape()
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
			cursorObj.execute('UPDATE catHacienda SET estado = "borrado" where id = ' + str(x_id))
			con.commit()
			messagebox.showinfo("Borrado", "Borrado con Éxito")
			escape()
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
def botonesInicio():
	diccionarioObjetos["botGuardar"]["state"] = "disabled"
	diccionarioObjetos["botBorrar"]["state"] = "disabled"
	diccionarioObjetos["botEditar"]["state"] = "disabled"
	diccionarioObjetos["botBuscar"]["state"] = "normal"
def activarBuscar():
	diccionarioObjetos["botBuscar"]["state"] = "normal"
	pass
def desactivarBuscar():
	diccionarioObjetos["botBuscar"]["state"] = "disabled"
	pass

def escape():
	borrarCampos()
	desactivarCarga()
	botonesInicio()


def bodyCatHacienda(window):
	"""
	CREATE TABLE "catHacienda" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"alias"	TEXT,
	"nombre"	TEXT,
	"descripcion"	TEXT,
	"estado"	TEXT,
	"""
	tk.Label(window, text = "Alias", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 1, padx=10, pady=10)
	tk.Label(window, text = "Nombre", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)
	tk.Label(window, text = "Descripcion", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 3, padx=10, pady=10)

	entryAlias = Entry(window, font=("Helvetica Neue",14))
	entryRazon = Entry(window, font=("Helvetica Neue",14), state="disabled")
	entryDescripcion = Entry(window, font=("Helvetica Neue",14), state="disabled")

	entryAlias.grid(sticky = "w", column = 1, row = 1, padx=0, pady=10)
	entryRazon.grid(sticky = "w", column = 1, row = 2, padx=0, pady=10)
	entryDescripcion.grid(sticky = "w", column = 1, row = 3, padx=0, pady=10)

	diccionarioObjetos["entryAlias"] = entryAlias
	diccionarioObjetos["entryRazon"] = entryRazon
	diccionarioObjetos["entryDescripcion"] = entryDescripcion

	diccionarioObjetos["botBuscar"]["state"] = "normal"

	entryAlias.focus()
	entryAlias.bind('<Return>', (lambda event: verificar()))
	entryAlias.bind('<Button-1>', (lambda event: activarBuscar()))
	entryAlias.bind('<F5>', (lambda event: buscar()))

	entryRazon.bind('<Button-1>', (lambda event: desactivarBuscar()))
	entryDescripcion.bind('<Button-1>', (lambda event: desactivarBuscar()))

	entryRazon.bind('<Return>', (lambda event: entryDescripcion.focus()))


def ventana1(idProductor):

	def cerrarVentana():
		window.destroy()

	dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}

	window = Tk()
	window.title("CATEGORIAS DE HACIENDA")
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
	lblBody.pack(side=TOP, fill=X, padx=150, pady=50)

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
	textTitulo.set("Cat. hacienda")
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

	bodyCatHacienda(lblBody)

	window.mainloop()

ventana1("NULL")